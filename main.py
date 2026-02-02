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
@app.post("/translate")
def translate(req: TranslateRequest):
    return {
        "status": "ok",
        "message": "translate endpoint reset"
    }

