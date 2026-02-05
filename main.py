import subprocess
import os
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from typing import Optional
from pydantic import BaseModel, HttpUrl
from gtts import gTTS
from deep_translator import GoogleTranslator
from faster_whisper import WhisperModel
from transactions import create_transaction

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
    mode: str
    video_url: HttpUrl
    language: Optional[str] = None
    text: Optional[str] = None

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
        try:
           file_id = str(uuid.uuid4())
           audio_path = f"/tmp/{file_id}.wav"
           cut_audio_path = f"/tmp/{file_id}_cut.wav"
        
           subprocess.run(
               ["curl", "-L", str(req.video_url), "-o", audio_path],
               check=True
           )
     # HARD LIMIT: first 20 seconds only (Render-safe)
           subprocess.run(
               [
                   "ffmpeg",
                   "-y",
                   "-i", audio_path,
                   "-t", "20",
                   cut_audio_path
               ],
               check=True
           ) 
    
           segments, info = whisper_model.transcribe(
               cut_audio_path,
               language=req.language or "en",
               vad_filter=False
           )

           transcript = ""
           for segment in segments:
               transcript += segment.text.strip() + " "
        
           transcript = transcript.strip()

           
           target_lang = req.language or "en"

           translated_text = GoogleTranslator(
               source="auto",
               target=target_lang
           ).translate(transcript)
            
           transaction = create_transaction(
               mode=req.mode,
               source_url=str(req.video_url),
               language=target_lang,
               status="success",
               transcript=translated_text
           )
            
           return {
               "status": "success",
               "transaction": transaction,
               "transcript": transcript,
               "translated_text": translated_text,
               "language": target_lang
           } 
              
        except Exception as e:
           print("ERROR:", str(e))
           raise HTTPException(
               status_code=500,
               detail=str(e)
           )



