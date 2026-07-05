---
title: Nepal Doc AI Backend
emoji: 📄
colorFrom: blue
colorTo: red
sdk: docker
app_port: 7860
pinned: false
---

# Nepal Doc AI Backend

FastAPI backend for Nepal Doc AI - Nepali document intelligence service.

## Features

- **OCR**: EasyOCR with Nepali + English support
- **AI Analysis**: Groq (llama-3.1-8b-instant) for summaries and Q&A
- **Endpoints**: `/extract`, `/analyze`, `/chat`

## API Endpoints

### POST /extract
Upload document for OCR extraction
- Accepts: JPG, PNG, PDF (multipart/form-data)
- Returns: Extracted text with confidence scores

### POST /analyze
Generate bilingual summaries
- Accepts: JSON with document text
- Returns: English summary, Nepali summary, key facts

### POST /chat
Ask questions about document
- Accepts: JSON with text, question, history
- Returns: AI-generated answer

## Environment Variables

- `GROQ_API_KEY`: Required for AI analysis (set in HF Space secrets)

## Tech Stack

- FastAPI
- EasyOCR (Nepali OCR)
- Groq API (LLM)
- PyTorch (CPU)
- Uvicorn

## Deployment

Deployed on Hugging Face Spaces using Docker.

Port: 7860
