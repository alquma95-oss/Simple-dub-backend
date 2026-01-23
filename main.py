from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl

app = FastAPI(
    title="Simple Dub Backend",
    description="Phase-1 backend for testing audio/video dubbing flow",
    version="2.0"
)

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
    supported_languages = ["en", "hi", "ur"]
    if req.language not in supported_languages:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language: {req.language}"
        )

    # Step 2: Validate file type (basic safety)
    if not req.video_url.lower().endswith((".mp3", ".wav", ".mp4")):
        raise HTTPException(
            status_code=400,
            detail="Only mp3, wav, or mp4 URLs are supported in v2"
        )

    # Step 3: MOCK dubbing response (intentional)
    return {
        "status": "success",
        "audio_url": str(req.video_url),
        "language": req.language,
        "note": "This is a mock response. Real dubbing will be added in v3."
    }
    
