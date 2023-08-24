# Braindump

## Overview
Braindump is an innovative project designed to transcribe speech into text files. Users can speak directly into their laptops, and the spoken content is transcribed and analyzed using OpenAI artificial intelligence models, specifically WISPA and GPT models, along with the E3.5 Turbo API. The transcribed content is then saved to a text file that can be easily viewed by the user.

### Features
- **Speech Transcription**: Transcribes user's speech into text.
- **Content Analysis**: Utilizes OpenAI's WISPA and GPT models for analysis.
- **Text File Generation**: Outputs the transcribed content into a text file.
- **Easy Viewing**: Opens the text file in the default text editor for easy viewing.

### Code Structure
Here's a snippet from `main.py` highlighting the main functionality:

```python
logger.info(f"Transcribing {output_audio_file}")
transcript = call_whisper(api_key, output_audio_file)
logger.debug(f"transcript = {transcript}")  # DEBUG
write_to_txt_file(
    transcript,
    file_name=transcript_file_name,
    output_directory=text_dir,
    mode="write",
)
```

## Getting Started
1. **Clone the repository**: Use your preferred method to clone the project.
2. **Install necessary dependencies**: Follow instructions in the project's documentation.
3. **Run main.py**: Execute `main.py` to initiate the transcription and analysis.

## Author
[Emil Rühmland](https://github.com/emilrueh)

---

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
