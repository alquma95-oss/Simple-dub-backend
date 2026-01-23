from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import requests
import uuid
import os

app = FastAPI()

AUDIO_DIR = "audio_files"
os.makedirs(AUDIO_DIR, exist_ok=True)

class TranslateRequest(BaseModel):
    video_url: str
    language: str

@app.post("/translate")
def translate(req: TranslateRequest):
    try:
        r = requests.get(req.video_url, timeout=30)
        if r.status_code != 200:
            raise HTTPException(status_code=400, detail="Audio download failed")

        file_id = f"{uuid.uuid4()}.mp3"
        file_path = os.path.join(AUDIO_DIR, file_id)

        with open(file_path, "wb") as f:
            f.write(r.content)

        return {
            "status": "success",
            "audio_url": f"/audio/{file_id}",
            "language": req.language
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/audio/{filename}")
def get_audio(filename: str):
    file_path = os.path.join(AUDIO_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio not found")

    return FileResponse(file_path, media_type="audio/mpeg")
    
