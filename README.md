# SoftHelp AI Support Engine

Sistema de suporte técnico com OCR, RAG e síntese de voz.

## 📦 Instalação local
```bash
git clone https://github.com/SEU-USUARIO/softhelp_ai_support_engine.git
cd softhelp_ai_support_engine
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:api --reload --port 8000

Requisitos
Python 3.10+

Tesseract OCR instalado
Download UB Mannheim

Modelo HuggingFace: sentence-transformers/all-MiniLM-L6-v2

Docker

docker build -t softhelp-ai .
docker run -it -p 8000:8000 softhelp-ai

Teste rápido

curl.exe -X POST "http://127.0.0.1:8000/support" -F "text=No puedo iniciar sesión" -F "image=@app/kb/error2.png"




