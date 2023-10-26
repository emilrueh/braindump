from src.helper.helperfuncs import retry

import time, requests

import openai


@retry(
    (
        openai.error.RateLimitError,
        requests.exceptions.ConnectionError,
        openai.error.APIError,
        openai.error.ServiceUnavailableError,
        openai.error.APIConnectionError,
        requests.exceptions.ReadTimeout,
        openai.error.Timeout,
    ),
    "simple",
)
def call_gpt(api_key, gpt_model=3, prompt="How are you?", input_text="", timeout=30):
    if api_key:
        # Set your OpenAI API key
        openai.api_key = api_key
    else:
        return "No OpenAI API key..."

    if gpt_model == 3:
        gpt_model = "3.5-turbo"
    if isinstance(gpt_model, int):
        gpt_model = str(gpt_model)

    # Concatenate the prompt and input input_text
    full_prompt = prompt + str(input_text)

    # Send the request to the OpenAI API
    response = openai.ChatCompletion.create(
        model=f"gpt-{gpt_model}",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": full_prompt},
        ],
        request_timeout=timeout,
    )

    # Extract the generated summary from the API response
    output_text = response.choices[0].message.content

    # Remove non-ASCII characters from the output_text
    output_text = output_text.encode("ascii", "ignore").decode()

    return output_text


def call_whisper(api_key, mp3_path, action="transcribe"):
    """
    Could need some love regarding other whisper functions
    and the opening of any kind of path format or taking a
    prompt as specified in the OpenAI API docs:
    https://platform.openai.com/docs/guides/speech-to-text/longer-inputs

    """
    openai.api_key = api_key

    if action.casefold() == "transcribe":
        attempts = 0
        while attempts < 5:
            try:
                with open(rf"{mp3_path}", "rb") as audio_file:
                    api_result = openai.Audio.transcribe("whisper-1", audio_file)["text"]
                if api_result is not None:
                    return api_result
                else:
                    return "Something failed and the API result is None."
            except (openai.error.RateLimitError, requests.exceptions.ConnectionError):
                time.sleep((2**attempts))
                attempts += 1
    else:
        return "Wrongly specified action. Try again."
