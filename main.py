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
    write_to_txt_file,
    load_text_from_file,
    open_txt_file,
)

from datetime import datetime
import argparse


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
        # ---flags---
        parser = argparse.ArgumentParser(
            description=f"The flag -test allows for loading of previously recorded and transcribed files."
        )
        parser.add_argument(
            "-test",
            action="store_true",
            help=f"This flag will set the project on runtime into a testing environment.",
        )
        args = parser.parse_args()
        # ---flags---

        # ---settings---
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # directories
        base_dir = os.path.dirname(__file__)
        settings_dir = os.path.join(base_dir, "settings")
        data_dir = os.path.join(base_dir, "data")
        audio_dir = os.path.join(data_dir, "audio")
        text_dir = os.path.join(data_dir, "text")
        backup_dir = os.path.join(data_dir, "backup")

        settings = load_settings(
            settings_file=os.path.join(settings_dir, "settings.json"),
            secrets_keys_list=["OPENAI_API_KEY"],
        )

        api_key = settings["OPENAI_API_KEY"]
        prompt = settings["PROMPT"]

        # file names
        audio_file_name = f"{settings['AUDIO_FILE_NAME']}_{timestamp}"
        transcript_file_name = f"{settings['TRANSCRIPT_FILE_NAME']}_{timestamp}"
        summary_file_name = f"{settings['SUMMARY_FILE_NAME']}_{timestamp}"

        test_transcript_file_name = os.path.join(
            text_dir,
            "backup",
            f"{settings['TEST_TRANSCRIPT_FILE_NAME']}.txt",
        )

        # audio recorder class initialization
        recorder = AudioRecorder(
            filename=audio_file_name,
            output_directory=audio_dir,
            duration=settings["RECORDING_LENGTH"],
        )
        # ---settings---

        if args.test:
            transcript = load_text_from_file(test_transcript_file_name)
            logger.info(f"Loading transcript from: {test_transcript_file_name}")
        else:
            # ---functions---
            # recording (audio)
            logger.info("Recording...")
            output_audio_file = recorder.record()
            logger.info(f"Saved recording to: {output_audio_file}")

            # transcribing (whisper)
            logger.info(f"Transcribing {output_audio_file}")
            transcript = call_whisper(api_key, output_audio_file)
            logger.debug(f"transcript = {transcript}")  # DEBUG
            write_to_txt_file(
                transcript,
                file_name=transcript_file_name,
                output_directory=text_dir,
                mode="write",
            )

        if transcript:
            # analyzing (gpt)
            logger.info("Analyzing...")
            raw_summary = call_gpt(api_key, prompt=prompt, input_text=transcript)
            logger.debug(f"raw_summary = {raw_summary}")  # DEBUG
            write_to_txt_file(
                raw_summary,
                file_name=summary_file_name,
                output_directory=text_dir,
                mode="write",
            )

            # presenting of output text via default .txt editor
            open_txt_file(os.path.join(text_dir, f"{summary_file_name}.txt"))
            # ---functions---

    except Exception as e:
        exception_name = log_exception(e, log_level="critical")


if __name__ == "__main__":
    main()
