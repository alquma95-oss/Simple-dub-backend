import uuid
import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, HttpUrl
from gtts import gTTS

BASE_DIR = "/tmp/files"
os.makedirs(BASE_DIR, exist_ok=True)

app = FastAPI(
    title="Simple Dub Backend",
    description="Phase-1 backend for testing audio/video dubbing flow",
    version="2.0"
)
app.mount("/files", StaticFiles(directory="/tmp/files"), name="files")

# ---------- Request Model ----------
class TranslateRequest(BaseModel):
    video_url: HttpUrl
    language: str


# ---------- Health Check ----------
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Simple Dub Backend is running"
    }


# ---------- Translate API ----------
@app.post("/translate")
def translate(req: TranslateRequest):
    # Step 1: Validate language
    supported_languages = ["en", "hi"]
    if req.language not in supported_languages:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language: {req.language}"
        )

    # Step 2: Validate file type
    video_url_str = str(req.video_url)
    if not video_url_str.lower().endswith((".mp3", ".wav", ".mp4")):
        raise HTTPException(
            status_code=400,
            detail="Only mp3, wav, or mp4 URLs are supported"
        )

    # Step 3: Generate real audio using Google gTTS (FREE)
    file_id = str(uuid.uuid4())
    output_filename = f"{file_id}.mp3"
    output_path = os.path.join(BASE_DIR, output_filename)

    text_to_speak = "Hello, this is a test voice generated using Google TTS."

    tts = gTTS(
        text=text_to_speak,
        lang=req.language,
        slow=False
    )

    tts.save(output_path)

    public_audio_url = f"/files/{output_filename}"

    return {
        "status": "success",
        "audio_url": public_audio_url,
        "language": req.language,
        "note": "Dummy audio generated (Phase-1, no OpenAI)"
    }
