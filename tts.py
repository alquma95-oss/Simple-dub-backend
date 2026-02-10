from gtts import gTTS
import uuid
import os

BASE_DIR = "/tmp/files"
os.makedirs(BASE_DIR, exist_ok=True)

def generate_audio(text: str, language: str = "en") -> str:
    file_id = str(uuid.uuid4())
    filename = f"{file_id}.mp3"
    file_path = os.path.join(BASE_DIR, filename)

    tts = gTTS(text=text, lang=language)
    tts.save(file_path)

    return filename
