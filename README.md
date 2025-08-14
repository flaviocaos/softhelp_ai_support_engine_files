## Ambiente recomendado

- Sistema operacional: Windows 11 ou Ubuntu 22.04
- Python 3.11 (obrigatório)
- Pip 24+
- Espaço em disco: mínimo 500MB livres
- RAM recomendada: 4GB


# SoftHelp – AI Support Response Engine (Multimodal)

Sistema de suporte automatizado baseado em IA que recebe **texto, áudio e imagens** como entrada, processa-os utilizando **OCR**, **RAG** e **TTS**, e responde em **texto** e **áudio**, sem depender de chaves de API externas.

## 🚀 Tecnologias e Bibliotecas Utilizadas

- **FastAPI** – Framework para API em Python
- **Tesseract OCR** – Extração de texto de imagens
- **LangChain + Chroma** – Recuperação de informações via RAG (Retrieval-Augmented Generation)
- **gTTS** – Conversão texto → fala (MP3)
- **(Opcional) OpenAI Whisper** – Reconhecimento de fala para entrada de áudio
- **Pillow** – Manipulação de imagens
- **Docker** – Containerização
- **cURL** – Testes de requisições
- **Python 3.11** – Linguagem base

---

## 📂 Estrutura do Projeto

```
app/
  ├── main.py              # Rotas e inicialização da API
  ├── ocr.py               # Funções de OCR com Tesseract
  ├── rag.py               # Busca contextual com LangChain + Chroma
  ├── tts.py               # Conversão de texto para áudio (gTTS)
  ├── asr.py               # (Opcional) Reconhecimento de fala com Whisper
  ├── kb/                  # Base de conhecimento (arquivos PDF, TXT e imagens)
  ├── static/              # Áudios gerados (MP3)
requirements.txt           # Lista de dependências do Python
Dockerfile                 # Configuração para execução via Docker
README.md                  # Este arquivo
```

---

## 📦 Requisitos

- **Python** 3.11
- **pip** atualizado
- **Tesseract OCR** instalado:
  - Windows: `C:\Program Files\Tesseract-OCR\tesseract.exe`
  - Linux: `sudo apt-get install tesseract-ocr`
  - macOS: `brew install tesseract`
- **(Opcional)** FFmpeg (necessário se utilizar o endpoint `/support/audio` com Whisper)

> 💡 No Windows, o caminho para o executável do Tesseract já está definido em `app/ocr.py`.

---

## 📚 Base de Conhecimento Obrigatória

Colocar os seguintes arquivos na pasta `app/kb/`:

- `ManualDeUsusarioSofHelp.pdf`
- `Preguntas Frecuentes (FAQ).txt`
- `Errores Comunes en SoftHelp.txt`
- *(Opcional)* imagens de erros:
  - `error1.png`
  - `error2.png`

---

## ⚙️ Instalação e Execução Local

1. **Criar ambiente virtual**
   ```bash
   python -m venv .venv
   ```

2. **Ativar o ambiente**
   - **Windows (PowerShell)**:
     ```bash
     .\.venv\Scripts\Activate.ps1
     ```
   - **Linux/macOS**:
     ```bash
     source .venv/bin/activate
     ```

3. **Instalar dependências**
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Executar servidor**
   ```bash
   uvicorn app.main:api --host 0.0.0.0 --port 8000
   ```

---

## 🌐 Endpoints Principais

- **Health check**:  
  `GET http://127.0.0.1:8000/health`
- **Documentação Swagger**:  
  `GET http://127.0.0.1:8000/docs`
- **Processar suporte multimodal**:  
  `POST /support` (texto e imagem)  
  `POST /support/audio` (áudio e imagem)

---

## 🧪 Exemplos de Teste

### Texto + Imagem
```bash
curl -X POST "http://127.0.0.1:8000/support"   -F "text=No puedo iniciar sesión"   -F "image=@app/kb/error1.png"
```
A resposta incluirá `audio_url` apontando para o MP3 gerado.

---

### Somente Texto
```bash
curl -X POST "http://127.0.0.1:8000/support"   -F "text=La plataforma está muy lenta. ¿Qué puedo revisar?"
```

---

### Áudio + Imagem
Gerar áudio de teste:
```bash
python -c "from gtts import gTTS; import os; os.makedirs('tests', exist_ok=True); gTTS('No puedo iniciar sesión en la plataforma', lang='es').save('tests/pergunta.mp3')"
```
Enviar áudio e imagem:
```bash
curl -X POST "http://127.0.0.1:8000/support/audio"   -F "audio=@tests/pergunta.mp3"   -F "image=@app/kb/error1.png"
```

---

## 🐳 Execução via Docker

1. **Build da imagem**
   ```bash
   docker build -t softhelp-ai .
   ```

2. **Executar container**
   ```bash
   docker run -it -p 8000:8000 softhelp-ai
   ```

---

## 🛠 Troubleshooting

| Problema | Possível Solução |
|----------|-----------------|
| Erro 500 ao enviar imagem | Verifique se o Tesseract está instalado e configurado corretamente |
| Whisper muito lento | Use `WHISPER_MODEL=tiny` ou teste apenas o endpoint `/support` |
| Sem geração de MP3 | Verifique conexão com a internet e permissões na pasta `app/static/` |

---

## 📌 Observações para Avaliação

- Todas as dependências estão listadas em `requirements.txt`
- Testado em **Windows 11** e **Ubuntu 22.04**
- Não requer variáveis de ambiente externas
- Funciona tanto **localmente** quanto via **Docker**
- Repositório GitHub incluso no envio `.zip`  
- Inclui **áudios de teste** e **vídeo opcional** de demonstração
