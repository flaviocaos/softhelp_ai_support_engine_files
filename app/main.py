import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional
from .stt import transcribe
from .tts import synthesize
from .ocr import ocr_image, classify_from_ocr
from .rag import search
from .llm import generate_answer
api = FastAPI(title='SoftHelp AI Support Engine', version='1.0')
static_dir = os.path.join(os.path.dirname(__file__), 'static')
api.mount('/static', StaticFiles(directory=static_dir), name='static')
def detect_language(s: str) -> str:
    s = (s or '').lower()
    if any(k in s for k in ['¿', 'usuario', 'contraseña', 'iniciar sesión']): return 'es'
    if any(k in s for k in ['senha', 'iniciar sessão', 'não', 'erro']): return 'pt'
    return 'en'
def pipeline(question_text: str, image_file: Optional[UploadFile]) -> JSONResponse:
    ocr_txt, tags = '', {}
    if image_file is not None:
        tmp_path = os.path.join(static_dir, f'_upload_{image_file.filename}')
        with open(tmp_path, 'wb') as f:
            f.write(image_file.file.read())
        ocr_txt = ocr_image(tmp_path)
        tags = classify_from_ocr(ocr_txt)
    q = question_text
    if ocr_txt:
        q = f"{q}\n\nTexto detectado en imagen:\n{ocr_txt[:300]}"
    context, sources = search(q, k=4)
    lang = detect_language(question_text + ' ' + ocr_txt)
    if tags.get('issue') == 'login_incorrect_credentials':
        c2, s2 = search('No puedo iniciar sesión contraseña incorrecta', k=4)
        context, sources = c2 + '\n' + context, list(set(sources + s2))
    elif tags.get('issue') == 'critical_error':
        c2, s2 = search('Error crítico plataforma solución revisar log', k=4)
        context, sources = c2 + '\n' + context, list(set(sources + s2))
    answer = generate_answer(question_text, context, language=lang)
    mp3_path = synthesize(answer, static_dir)
    audio_url = f"/static/{os.path.basename(mp3_path)}"
    return JSONResponse({
        'transcription': None,
        'answer': answer,
        'audio_url': audio_url,
        'source_documents': sources
    })
@api.post('/support')
async def support(text: str = Form(...), image: Optional[UploadFile] = File(None)):
    return pipeline(text, image)
@api.post('/support/audio')
async def support_audio(audio: UploadFile = File(...), image: Optional[UploadFile] = File(None)):
    tmp_path = os.path.join(static_dir, f'_upload_{audio.filename}')
    with open(tmp_path, 'wb') as f:
        f.write(await audio.read())
    text = transcribe(tmp_path)
    resp = pipeline(text, image)
    return JSONResponse({**resp.json(), 'transcription': text})
@api.get('/health')
async def health():
    return {'status': 'ok'}
