import os
from elevenlabs import generate, save, set_api_key

# Set your API key from environment variable
api_key = os.getenv("ELEVEN_API_KEY")
if not api_key:
    raise ValueError("ELEVEN_API_KEY not set in environment variables")

set_api_key(api_key)

def generate_audio(text, language="en"):
    
    # Default voice (you can change later)
    voice_id = "Rachel"

    audio = generate(
        text=text,
        voice=voice_id,
        model="eleven_multilingual_v2"
    )

    file_path = f"/tmp/files/{language}_output.mp3"
    save(audio, file_path)

    return file_path
