SoftHelp – AI Support Response Engine (Multimodal)

API em FastAPI que recebe texto / áudio / imagem e responde em texto + áudio usando:

OCR (Tesseract)

RAG (LangChain + Chroma)

TTS (gTTS)
Sem chaves de API externas.

Estrutura do projeto

app/
  ├── main.py              # Rotas e inicialização
  ├── ocr.py               # Funções OCR
  ├── rag.py               # Busca contextual com LangChain + Chroma
  ├── tts.py               # Conversão texto → áudio
  ├── asr.py               # (opcional) Reconhecimento de fala com Whisper
  ├── kb/                  # Base de conhecimento (PDFs, TXT, imagens)
  ├── static/              # Áudios gerados (MP3)
requirements.txt
Dockerfile
README.md


Requisitos

Python 3.11

pip atualizado

Tesseract OCR instalado

Windows: C:\Program Files\Tesseract-OCR\tesseract.exe

Linux: sudo apt-get install tesseract-ocr

macOS: brew install tesseract

No Windows, o caminho já está definido em app/ocr.py.

(Opcional) FFmpeg (se usar /support/audio com Whisper)

Instalação (local)

python -m venv .venv
# Windows
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt


Base de conhecimento obrigatória

ManualDeUsusarioSofHelp.pdf

Preguntas Frecuentes (FAQ).txt

Errores Comunes en SoftHelp.txt

(opcional) imagens de erros (error1.png, error2.png)

Instalação e execução local
Criar ambiente virtual

python -m venv .venv

Ativar o ambiente
Windows (PowerShell)

.\.venv\Scripts\Activate.ps1

Linux/macOS

source .venv/bin/activate


Instalar dependências

python -m pip install --upgrade pip
pip install -r requirements.txt


Endpoints principais

Documentação Swagger: http://127.0.0.1:8000/docs

Health check: http://127.0.0.1:8000/health


Executar

uvicorn app.main:api --host 0.0.0.0 --port 8000

Health: http://127.0.0.1:8000/health

Swagger: http://127.0.0.1:8000/docs

Testes rápidos

Texto + imagem

curl -X POST "http://127.0.0.1:8000/support" \
  -F "text=No puedo iniciar sesión" \
  -F "image=@app/kb/error1.png"

O retorno terá audio_url com o caminho do MP3 gerado.

Abra o audio_url retornado (ex.: http://127.0.0.1:8000/static/resp_...mp3).

Somente texto

curl -X POST "http://127.0.0.1:8000/support" \
  -F "text=La plataforma está muy lenta. ¿Qué puedo revisar?"


Áudio + imagem (opcional)

# gerar áudio de teste (opcional)
python -c "from gtts import gTTS; import os; os.makedirs('tests', exist_ok=True); gTTS('No puedo iniciar sesión en la plataforma', lang='es').save('tests/pergunta.mp3')"

curl -X POST "http://127.0.0.1:8000/support/audio" \
  -F "audio=@tests/pergunta.mp3" \
  -F "image=@app/kb/error1.png"

Docker

docker build -t softhelp-ai .
docker run -it -p 8000:8000 softhelp-ai

Possíveis erros e soluções - Troubleshooting

500 com imagem → verifique Tesseract instalado (Windows: caminho já setado em app/ocr.py).

Whisper lento → use WHISPER_MODEL=tiny ou teste apenas /support.

Sem MP3 → verifique conexão para gTTS e pasta app/static/.


Observações para execução no teste técnico

Todas as dependências estão listadas no requirements.txt

Testado em Windows 11 e Ubuntu 22.04

Não requer variáveis de ambiente externas

Projeto funciona tanto localmente quanto via Docker




