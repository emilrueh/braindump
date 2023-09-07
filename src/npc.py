import logging
from helpinghands.utility.logger import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

from urllib.parse import urlparse

from helpinghands.utility.data import write_to_txt_file, split_path
from helpinghands.ai import call_gpt, call_whisper

from helpinghands.utility.web import get_website

from gtts import gTTS
import os


def listening(audio_recorder):
    audio_file = audio_recorder.record()
    return audio_file


def transcribing(audio_file, whisper_api_key, output_file_path):
    directory, filename, _ = split_path(output_file_path)

    transcript = call_whisper(whisper_api_key, audio_file)
    write_to_txt_file(transcript, filename, directory, mode="write")
    return transcript


def analyzing(input_text, what_to_do, gpt_api_key, output_file_path):
    directory, filename, _ = split_path(output_file_path)

    analysis = call_gpt(gpt_api_key, prompt=what_to_do, input_text=input_text, timeout=120)
    write_to_txt_file(analysis, filename, directory, mode="write")
    return analysis


def speaking(text, output_file_path, lang="en"):
    tts = gTTS(text=text, lang=lang)
    tts.save(output_file_path)
    os.system(f"start {output_file_path}")
    return output_file_path


def deciding():
    pass


def responding(understood, trigger, name):
    if "http" in understood or "www" in understood or ".com" in understood:
        url = understood
        get_website(url)

        parsed_url = urlparse(url)
        website_name = ".".join(parsed_url.netloc.split(".")[1:])
        answer = f"Opening {website_name}."

    elif "what is" in understood:
        query = understood.split("what")[1]
        answer = f"Looking up {query}?"

    elif name in understood:
        answer = "Yes?"

    else:
        answer = "Sorry, say again please?"

    return answer
