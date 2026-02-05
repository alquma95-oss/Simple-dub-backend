from datetime import datetime
import uuid

def create_transaction(
    mode: str,
    source_url: str,
    language: str,
    status: str,
    transcript: str | None = None,
    error: str | None = None
):
    return {
        "transaction_id": str(uuid.uuid4()),
        "mode": mode,
        "source_url": source_url,
        "language": language,
        "status": status,
        "transcript_length": len(transcript) if transcript else 0,
        "error": error,
        "created_at": datetime.utcnow().isoformat()
    }
