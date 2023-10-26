from dotenv import load_dotenv
import os, sys, json

import sounddevice as sd
import numpy as np
import threading, wavio

import platform, subprocess


def load_settings(
    settings_file,
    secrets_keys_list=None,
    dotenv_path=None,
    remote_env="REMOTE_ENV",
    default_settings_file="data/settings.json",
):
    settings_path = settings_file if settings_file else default_settings_file

    # Initialize an empty dictionary for secrets
    secrets_dict = {}

    in_docker = os.getenv(remote_env) is not None

    try:
        if not in_docker:
            # Get directory of the main script
            main_script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
            if dotenv_path:
                load_dotenv(dotenv_path)
            else:
                # Load .env file relative to the main script directory
                dotenv_path = os.path.join(main_script_dir, ".env")
                load_dotenv(dotenv_path)

        # Load .env variables if keys are provided
        if secrets_keys_list:
            for secret_key in secrets_keys_list:
                value = os.getenv(secret_key)
                if value:
                    secrets_dict[secret_key] = value
                else:
                    print(f"Missing environment variable: {secret_key}")

        # Check if the settings file exists
        if not os.path.exists(settings_path):
            raise FileNotFoundError(f"Settings file not found: {settings_path}")

        # Load the settings dictionary from the .json file
        with open(settings_path, "r") as fp:
            settings_dict = json.load(fp)

        # Merge the API keys and other settings
        settings_dict.update(secrets_dict)

        return settings_dict

    except json.JSONDecodeError:
        raise
    except Exception as e:
        raise


class AudioRecorder:
    def __init__(
        self,
        sample_rate=44100,
        channels=2,
        audio_dir=".",
        audio_file_name="output",
        stop_button="q",
        max_rec_time=None,
    ):
        self.sample_rate = sample_rate
        self.channels = channels
        self.audio_dir = audio_dir
        self.audio_file_name = audio_file_name
        self.audio_file_path = os.path.join(self.audio_dir, f"{self.audio_file_name}.wav")
        self.stop_button = stop_button
        self.max_rec_time = max_rec_time
        self.stop_event = threading.Event()

    def record(self):
        audio_data = []

        with sd.InputStream(samplerate=self.sample_rate, channels=self.channels) as stream:
            stop_thread = threading.Thread(target=self.listen_for_stop)
            timer_thread = threading.Thread(target=self.time_limit) if self.max_rec_time else None

            stop_thread.start()
            if timer_thread:
                timer_thread.start()

            while not self.stop_event.is_set():
                data, _ = stream.read(1000)
                audio_data.append(data)

            stop_thread.join()
            if timer_thread:
                timer_thread.join()

        audio_data = np.vstack(audio_data)
        audio_data = (audio_data * 32767).astype(np.int16)

        wavio.write(self.audio_file_path, audio_data, self.sample_rate, sampwidth=2)

        return self.audio_file_path

    def listen_for_stop(self):
        while not self.stop_event.is_set():
            inp = input()
            if inp == self.stop_button:
                self.stop_event.set()
                break

    def time_limit(self):
        self.stop_event.wait(timeout=self.max_rec_time)
        self.stop_event.set()


def load_text_from_file(txt_file_path):
    try:
        with open(txt_file_path, "r") as f:
            return f.read()
    except:
        return print(f"Failed to open .txt file at path: {txt_file_path}")


def open_txt_file(file_path):
    try:
        if platform.system() == "Windows":
            os.startfile(file_path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", file_path], check=True)
        elif platform.system() == "Linux":
            subprocess.run(["xdg-open", file_path], check=True)
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def write_to_txt_file(input_text, file_name, output_directory, mode="append", encoding="utf-8"):
    """
    Specify any mode except for 'append' for write and replace.
    """
    output_file_path = os.path.join(output_directory, f"{file_name}.txt")
    with open(output_file_path, "a" if mode == "append" else "w", encoding=encoding) as f:
        f.write(("\n" if mode == "append" and f.tell() > 0 else "") + input_text)


def split_path(file_path):
    directory = os.path.dirname(file_path)
    split_name = os.path.splitext(os.path.basename(file_path))
    filename_without_extension = split_name[0]
    extension = split_name[1]
    return directory, filename_without_extension, extension


import functools, time


def retry(exceptions, time_mode: str = "medium"):
    """
    A retry decorator that applies a backoff strategy for retries and controls the
    number of retry attempts based on the selected time_mode. It will retry the decorated
    function upon raising specified exceptions.

    The decorator supports four modes represented by a string determining: total tries, initial wait, backoff factor.

        'simple': 2 total tries, 1 second initial wait, backoff factor of 2.
        'medium': 3 total tries, 2 seconds initial wait, backoff factor of 3.
        'advanced': 4 total tries, 4 seconds initial wait, backoff factor of 4.
        'verbose': 6 total tries, 6 seconds initial wait, backoff factor of 3.

        (If no time_mode or an unrecognized time_mode is specified, it defaults to 'medium'.)

    Returns:
        A decorator which can be used to decorate a function with the retry logic.

    Raises:
        The exceptions specified in the 'exceptions' parameter if all retry attempts fail.
    """

    if time_mode == "simple":
        total_tries = 2
        initial_wait = 1
        backoff_factor = 2
    elif time_mode == "medium":
        total_tries = 3
        initial_wait = 2
        backoff_factor = 3
    elif time_mode == "advanced":
        total_tries = 4
        initial_wait = 4
        backoff_factor = 4
    elif time_mode == "verbose":
        total_tries = 6
        initial_wait = 6
        backoff_factor = 3
    else:
        total_tries = 3
        initial_wait = 2
        backoff_factor = 3

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wait_time = initial_wait
            for attempt in range(total_tries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt >= total_tries - 1:
                        raise
                    else:
                        time.sleep(wait_time)
                        wait_time *= backoff_factor

        return wrapper

    return decorator
