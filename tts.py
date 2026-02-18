import os
from elevenlabs.client import ElevenLabs

api_key = os.getenv("ELEVEN_API_KEY")

if not api_key:
    raise ValueError("ELEVEN_API_KEY not set in environment variables")

client = ElevenLabs(api_key=api_key)


def generate_audio(text, language="en"):
    voice_id = "21m00Tcm4TlvDq8ikWAM"  # Rachel voice ID

    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        text=text,
        model_id="eleven_multilingual_v2"
    )

    file_path = f"/tmp/files/{language}_output.mp3"

    with open(file_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    return file_path
