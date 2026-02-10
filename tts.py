from gtts import gTTS
import uuid
import os

AUDIO_DIR = "files/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

def generate_audio(text: str, language: str = "en") -> str:
    file_id = str(uuid.uuid4())
    file_path = f"{AUDIO_DIR}/{file_id}.mp3"

    tts = gTTS(text=text, lang=language)
    tts.save(file_path)

    return file_path
