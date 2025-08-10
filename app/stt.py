import os
import whisper
_model = None
def load_model():
    global _model
    if _model is None:
        _model = whisper.load_model(os.getenv("WHISPER_MODEL","base"))
    return _model
def transcribe(audio_path: str) -> str:
    model = load_model()
    result = model.transcribe(audio_path)
    return result.get("text","").strip()
