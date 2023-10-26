# Braindump

>This is a highly WIP version and not distributed yet elsewhere than via this repo.

## Overview
Braindump is an innovative project designed to transcribe speech into text files. Users can speak directly into their laptops, and the spoken content is transcribed and analyzed using OpenAI artificial intelligence models. The transcribed and analyzed content is then being output as voice and saved to a text file that can be easily viewed by the user.

### Features
- **Speech Transcription**: Transcribes user's speech into text using OpenAI's Whisper model.
- **Content Analysis**: Utilizes OpenAI's GPT-3.5 Turbo model for analysis and guidance.
- **Text File Generation**: Outputs the transcribed content into a text file.
- **Speech-To-Text**: Using gTTS lib to output analysis as simple voice.
- **Easy Viewing**: Opens the text file in the default text editor for easy viewing.

## Getting Started
1. **Clone the repository**: Use your preferred method to clone the project.
2. **Install necessary dependencies**: Execute `pip install -r requirements.txt`
3. **Customize settings**: Specify your name in `settings.json` and customize `prompt.txt` (optionally)
4. **Run main.py**: Execute `python main.py` to initiate the transcription and analysis.

## Author
[Emil Rühmland](https://github.com/emilrueh)

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
