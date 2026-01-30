import subprocess
import os
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, HttpUrl
from gtts import gTTS
from deep_translator import GoogleTranslator

BASE_DIR = "/tmp/files"
os.makedirs(BASE_DIR, exist_ok=True)

app = FastAPI(
    title="Simple Dub Backend",
    description="Phase-1 backend for testing audio/video dubbing flow",
    version="2.0"
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
    # Phase-3 Step-1: mode validation
    if req.mode not in ["audio", "video"]:
        raise HTTPException(
            status_code=400,
            detail="mode must be 'audio' or 'video'"
        )   

    # Phase-3 Step-4: Translate text to English (AUDIO only)
    translated_text = req.text
    if req.mode == "audio" and req.language != "en":
        try:
           from googletrans import Translator
           translator = Translator()
           translated_text = translator.translate(req.text, dest="en").text
       except Exception as e:
           raise HTTPException(
               status_code=500,
               detail=f"Translation failed: {str(e)}"
           )

    # Phase-3 Step-3: download video and extract audio
    if req.mode == "video":
        file_id = str(uuid.uuid4())
        video_path = f"/tmp/{file_id}.mp4"
        audio_path = f"/tmp/{file_id}.wav"

        subprocess.run(
            ["curl", "-L", req.video_url, "-o", video_path],
            check=True
        )

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
        audio_path = req.video_url  # placeholder for audio input

    return {
        "status": "success",
        "audio_path": audio_path
    }
        
    # Step 4: Translate non-English text to English (REAL)
    if req.language != "en":
        translated_text = GoogleTranslator(
            source="auto",
            target="en"
        ).translate(req.text)
        final_language = "en"
    else:
        translated_text = req.text
        final_language = "en"
        
    # Step 3: Generate real audio using Google gTTS (FREE)
    file_id = str(uuid.uuid4())
    output_filename = f"{file_id}.mp3"
    output_path = os.path.join(BASE_DIR, output_filename)

    text_to_speak = translated_text

    tts = gTTS(
        text=text_to_speak,
        lang=final_language,
        slow=False
    )

    tts.save(output_path)

    return FileResponse(
        path=output_path,
        media_type="audio/mpeg",
        filename=output_filename
    )
