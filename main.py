from helpinghands.utility.logger import config_logger
import os

in_docker = os.getenv("DOCKER_ENV") is not None

logger = config_logger(
    name="main_logger",
    lvl_console="debug" if not in_docker else "info",
    lvl_file="debug" if not in_docker else None,
    lvl_root="debug",
    fmt_console="\n%(asctime)s - %(name)s - %(levelname)s - %(module)s @line %(lineno)3d\n%(message)s"
    if not in_docker
    else "\n%(name)s - %(levelname)s - %(module)s @line %(lineno)3d\n%(message)s",
    fmt_file="%(asctime)s - %(name)s - %(levelname)s - %(module)s @line %(lineno)3d ---> %(message)s",
    fmt_date="%d.%m.%Y %H:%M:%S",
    file_name="runtime",
    file_timestamp="%d%m%Y-%H%M%S",
    prints=True,
    encoding="utf-8",
)
from helpinghands.utility import load_settings, log_exception

from helpinghands.audio import AudioRecorder
from helpinghands.openai import call_whisper, call_gpt

from helpinghands.utility.data import (
    insert_newlines,
    append_to_or_create_txt_file,
    open_txt_file,
)


def main():
    """
    TO-DO:
        1. check whisper's transcribing
            - where is it saved?
            - it should be saved as .txt
            - is it accurate?

        2. check GPT's analysis
            - where is it saved?
            - it should be saved as .txt
            - is it accurate?

        3. write .txt savers for the full summary
        4. write file opener in default .txt software
        5. distribute everything into single src/ files

        6. re-evaluate GPT's prompt
        7. package into .exe
        8. send to Deniz for testing
    """

    try:
        # ---directories---

        base_dir = os.path.dirname(__file__)
        settings_dir = os.path.join(base_dir, "settings")
        data_dir = os.path.join(base_dir, "data")
        audio_dir = os.path.join(data_dir, "audio")
        text_dir = os.path.join(data_dir, "text")
        backup_dir = os.path.join(data_dir, "backup")

        # ---directories---
        #
        # ---settings---

        settings = load_settings(
            settings_file=os.path.join(settings_dir, "settings.json"),
            secrets_keys_list=["OPENAI_API_KEY"],
        )

        api_key = settings["OPENAI_API_KEY"]
        prompt = settings["PROMPT"]
        audio_file_name = settings["AUDIO_FILE_NAME"]

        recorder = AudioRecorder(
            filename=audio_file_name, output_directory=audio_dir, duration=5
        )

        # ---settings---
        #
        # ---functions---

        # recording (audio)
        logger.info("Recording...")
        recorded_file = recorder.record()
        logger.info(f"Saved recording to: {recorded_file}")
        output_file = recorded_file
        logger.debug(f"output_file = {output_file}")  # DEBUG

        # transcribing (whisper)
        logger.info(f"Transcribing {output_file}")
        transcript = call_whisper(api_key, output_file)
        logger.debug(f"transcript = {transcript}")  # DEBUG

        # analyzing (gpt)
        logger.info("Analyzing...")
        raw_summary = call_gpt(api_key, prompt=prompt, input_text=transcript)
        logger.debug(f"raw_summary = {raw_summary}")  # DEBUG

        # printing (text)
        fmt_summary = insert_newlines(raw_summary)
        logger.debug(f"fmt_summary = {fmt_summary}")  # DEBUG

        # v needs fixing of saving to .txt and opening in default text editor
        # txt_file_path = "summary.txt"
        # append_to_or_create_txt_file(summary, txt_file_path)
        # summary = open_txt_file(txt_file_path)

        summary = fmt_summary
        print(summary)

        # ---functions---

    except Exception as e:
        exception_name = log_exception(e, log_level="critical")


if __name__ == "__main__":
    main()
