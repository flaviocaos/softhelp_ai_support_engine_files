from gtts import gTTS
import os
from datetime import datetime
def synthesize(text: str, out_dir: str) -> str:
    os.makedirs(out_dir, exist_ok=True)
    fname = f"resp_{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}.mp3"
    out_path = os.path.join(out_dir, fname)
    tts = gTTS(text=text, lang='es')
    tts.save(out_path)
    return out_path
