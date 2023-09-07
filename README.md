# Braindump

## Overview
Braindump is an innovative project designed to transcribe speech into text files. Users can speak directly into their laptops, and the spoken content is transcribed and analyzed using OpenAI artificial intelligence models. The transcribed and analyzed content is then being output as voice and saved to a text file that can be easily viewed by the user.

### Features
- **Speech Transcription**: Transcribes user's speech into text using OpenAI's Whisper model.
- **Content Analysis**: Utilizes OpenAI's GPT-3.5 Turbo model for analysis and guidance.
- **Text File Generation**: Outputs the transcribed content into a text file.
- **Speech-To-Text**: Using gTTS lib to output analysis as simple voice.
- **Easy Viewing**: Opens the text file in the default text editor for easy viewing.

### Code Structure
Here's a snippet from `npc.py` highlighting the main functionality:

```python
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
```

## Getting Started
1. **Clone the repository**: Use your preferred method to clone the project.
2. **Install necessary dependencies**: Follow instructions in the project's documentation.
3. **Run main.py**: Execute `main.py` to initiate the transcription and analysis.

## Author
[Emil Rühmland](https://github.com/emilrueh)

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
