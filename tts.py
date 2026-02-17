import os
from elevenlabs import ElevenLabs

api_key = os.getenv("ELEVEN_API_KEY")

if not api_key:
    raise ValueError("ELEVEN_API_KEY not set in environment variables")

client = ElevenLabs(api_key=api_key)


def generate_audio(text, language="en"):
    response = client.text_to_speech.convert(
        voice_id="Rachel",  # You can change later
        model_id="eleven_multilingual_v2",
        text=text
    )

    file_path = f"/tmp/files/{language}_output.mp3"

    with open(file_path, "wb") as f:
        f.write(response)

    return file_path
