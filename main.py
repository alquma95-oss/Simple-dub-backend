import subprocess
import os
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, HttpUrl
from gtts import gTTS
from deep_translator import GoogleTranslator
from faster_whisper import WhisperModel

BASE_DIR = "/tmp/files"
os.makedirs(BASE_DIR, exist_ok=True)

app = FastAPI(
    title="Simple Dub Backend",
    description="Phase-1 backend for testing audio/video dubbing flow",
    version="2.0"
)

whisper_model = WhisperModel(
    "tiny",
    device="cpu",
    compute_type="int8"
)
# ---------- Request Model ----------

class TranslateRequest(BaseModel):
    video_url: HttpUrl
    language: str
    text: str
    mode: str  # "audio" or "video"

# ---------- Health Check ----------
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Simple Dub Backend is running"
    }

@app.post("/translate")
def translate(req: TranslateRequest):
    
    if req.mode not in ["audio", "video"]:
        raise HTTPException(
            status_code=400,
            detail="mode must be 'audio' or 'video'"
        )

    # Phase-3 Step-2: validate file type
    video_url_str = str(req.video_url)

    if not video_url_str.lower().endswith((".mp3", ".wav", ".mp4")):
        raise HTTPException(
            status_code=400,
            detail="Only mp3, wav, or mp4 URLs are supported"
        )

    # Phase-3 Step-3: download video and extract audio
    if req.mode == "video":
        file_id = str(uuid.uuid4())
        video_path = f"/tmp/{file_id}.mp4"
        audio_path = f"/tmp/{file_id}.wav"

        # Download video
        subprocess.run(
            ["curl", "-L", str(req.video_url), "-o", video_path],
            check=True
        )

        # Extract audio using ffmpeg
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i", video_path,
                "-vn",
                "-acodec", "pcm_s16le",
                "-ar", "44100",
                "-ac", "2",
                audio_path
            ],
            check=True
        )
        
    elif req.mode == "audio":
        file_id = str(uuid.uuid4())
        audio_path = f"/tmp/{file_id}.wav"

        subprocess.run(
            ["curl", "-L", str(req.video_url), "-o", audio_path],
            check=True
        )
        
    segments, info = whisper_model.transcribe(audio_path)

    transcript = ""
    for segment in segments:
        transcript += segment.text.strip() + " "
        
    transcript = transcript.strip()

    return {
        "status": "success",
        "transcript": transcript
    }
        

    
