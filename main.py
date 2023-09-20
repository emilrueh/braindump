from src.helper.helpinghands import load_settings
from src.helper.helpinghands import AudioRecorder
from src.helper.helpinghands import (
    load_text_from_file,
    open_txt_file,
)

from datetime import datetime
import os

from src.npc import listening, transcribing, analyzing, speaking


def main():
    try:
        # SETTINGS
        timestamp = datetime.now().strftime("%y-%b-%d_%H-%M-%S")

        # directories
        base_dir = os.path.dirname(__file__)
        settings_dir = os.path.join(base_dir, "settings")
        data_dir = os.path.join(base_dir, "data")
        audio_dir = os.path.join(data_dir, "audio")
        text_dir = os.path.join(data_dir, "text")
        backup_dir = os.path.join(data_dir, "backup")

        # load
        settings = load_settings(
            settings_file=os.path.join(settings_dir, "settings.json"),
            secrets_keys_list=["OPENAI_API_KEY"],
        )

        # vars
        name = str(settings["NAME"]).title()

        openai_api_key = settings["OPENAI_API_KEY"]
        # prompt = settings["PROMPT_ANALYSIS"].format(name.title() if name else "you")
        prompt = load_text_from_file(os.path.join(settings_dir, "prompt.txt"))
        prompt = prompt.format(name.title() if name else "you") if "{}" in prompt else prompt

        # file names
        audio_file_name = f"{settings['AUDIO_FILE_NAME']}_{timestamp}"
        test_audio_file = os.path.join(backup_dir, settings["TEST_AUDIO_FILE"])

        transcript_file_name = f"{settings['TRANSCRIPT_FILE_NAME']}_{timestamp}"
        transcript_file = os.path.join(text_dir, f"{transcript_file_name}.txt")
        test_transcript = os.path.join(backup_dir, settings["TEST_TRANSCRIPT_FILE"])

        analysis_file_name = f"{settings['ANALYSIS_FILE_NAME']}_{timestamp}"
        analysis_file = os.path.join(text_dir, f"{analysis_file_name}.txt")
        test_analysis = os.path.join(backup_dir, settings["TEST_ANALYSIS_FILE"])

        voice_file_name = f"{settings['VOICE_FILE_NAME']}_{timestamp}"
        voice_file = os.path.join(audio_dir, f"{voice_file_name}.mp3")

        # audio recorder class initialization
        audio_recorder = AudioRecorder(
            sample_rate=44100,
            channels=2,
            stop_button="q",
            audio_dir=audio_dir,
            audio_file_name=audio_file_name,
            max_rec_time=settings["RECORDING_LENGTH"],
        )
        # SETTINGS

        # -----------------
        # |   S T A R T   |
        # -----------------

        # 1. RECORDING AUDIO
        print("\nListening...")
        audio_file = listening(audio_recorder=audio_recorder)
        print("Audio file saved to: ", audio_file)

        # 2. TRANSCRIBING AUDIO
        print("\nTranscribing...")
        transcript = transcribing(
            audio_file=audio_file,
            whisper_api_key=openai_api_key,
            output_file_path=transcript_file,
        )
        print(f"\nTranscript:\n-----------\n{transcript}\n\nSaved to: {transcript_file}")

        # 3. ANALYZING TRANSCRIPT
        print("\nAnalyzing...")
        analysis = analyzing(
            input_text=transcript,
            what_to_do=prompt,
            gpt_api_key=openai_api_key,
            output_file_path=analysis_file,
        )
        print(f"\Analysis:\n-----------\n{analysis}\n\nSaved to: {analysis_file}")

        # 4. TEXT TO SPEECH
        speaking(analysis, output_file_dir=voice_file)

        # 5. OPENING ANALYSIS IN TEXT EDITOR
        open_txt_file(analysis_file)

        # -----------------
        # |     E N D     |
        # -----------------

    except Exception as e:
        print(f"{type(e).__name__}\n{e}\nShutting down...")


if __name__ == "__main__":
    main()
