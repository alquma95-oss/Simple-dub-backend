from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TranslateRequest(BaseModel):
    video_url: str
    language: str

@app.post("/translate")
def translate(req: TranslateRequest):
    return {
        "status": "success",
        "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        "language": req.language
    }
  
