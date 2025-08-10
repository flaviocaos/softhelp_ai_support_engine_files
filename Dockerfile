﻿FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends 
    ffmpeg 
    tesseract-ocr 
    tesseract-ocr-eng 
    tesseract-ocr-spa 
    tesseract-ocr-por 
    libgl1 
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY app /app/app
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD [ "uvicorn", "app.main:api", "--host", "0.0.0.0", "--port", "8000" ]
