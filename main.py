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
    try:
        # ---directories---
        base_dir = os.path.dirname(__file__)
        settings_dir = os.path.join(base_dir, "settings")
        data_dir = os.path.join(base_dir, "data")
        # ---directories---

        # ---settings---
        settings = load_settings(
            settings_file=os.path.join(settings_dir, "settings.json"),
            secrets_keys_list="OPENAI_API_KEY",
        )
        api_key = settings["OPENAI_API_KEY"]
        prompt = settings["PROMP"]
        recorder = AudioRecorder(filename="test_recording", duration=5)
        # ---settings---

        # ---functions---
        logger.info("Recording...")
        recorded_filename = recorder.record()
        logger.info(f"Saved recording to: {recorded_filename}")
        output_file = recorded_filename
        logger.debug(f"output_file = {output_file}")

        logger.info(f"Transcribing {output_file}")
        transcript = call_whisper(api_key, output_file)
        logger.debug(f"transcript = {transcript}")

        logger.info("Analyzing...")
        raw_summary = call_gpt(api_key, prompt=prompt, input_text=transcript)
        logger.debug(f"raw_summary = {raw_summary}")
        summary = raw_summary.split("\n")[0]

        fmt_summary = insert_newlines(summary)
        logger.debug(f"fmt_summary = {fmt_summary}")

        # v needs fixing of saving to .txt and opening in default text editor
        # txt_file_path = "summary.txt"
        # append_to_or_create_txt_file(summary, txt_file_path)
        # summary = open_txt_file(txt_file_path)

        print(fmt_summary)
        # ---functions---

    except Exception as e:
        exception_name = log_exception(e, log_level="critical")


if __name__ == "__main__":
    main()
