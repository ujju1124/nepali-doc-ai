# Nepal Doc AI

An intelligent document analysis tool for Nepali documents. Upload a photo of any Nepali document and instantly get plain-language summaries in both English and Nepali, plus the ability to ask questions about the document content.

## Features

- **OCR Extraction**: Extract text from Nepali documents using EasyOCR
- **Bilingual Summaries**: Get summaries in both English and Nepali
- **Key Facts**: Automatically identifies the 3 most important points
- **Interactive Q&A**: Ask followup questions in English or Nepali
- **Quality Indicators**: Shows OCR confidence so you know if results are reliable

## Architecture

**Backend**: FastAPI + Python
- `/extract` - OCR text extraction
- `/analyze` - Summary generation
- `/chat` - Document Q&A

**Frontend**: React + Vite
- Modern, accessible UI
- Responsive design (mobile + desktop)

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Groq API key ([get one free](https://console.groq.com/keys))

### Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env and add your GROQ_API_KEY

# Run server
python main.py
# Or with uvicorn:
uvicorn main:app --reload --port 8000
```

Backend will run on: http://localhost:8000

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment (optional for local dev)
copy .env.example .env

# Run development server
npm run dev
```

Frontend will run on: http://localhost:3000

## Example Use Cases

- **Land Records (जग्गा दस्तावेज)**: Understand property documents
- **Citizenship Certificates (नागरिकता प्रमाणपत्र)**: Extract key information
- **Government Notices (सरकारी सूचना)**: Summarize official announcements
- **Certificates**: Birth, marriage, education certificates
- **Official Letters**: Formal government correspondence

## Known Limitations

1. **Handwritten text**: Works best with printed/typed text
2. **Image quality**: Low resolution/blurry images affect accuracy
3. **Processing time**: 10-30 seconds per document on CPU
4. **Complex layouts**: Tables may extract in unexpected order
5. **First run**: Downloads EasyOCR models (~100MB)

## Tech Stack

**Backend**:
- FastAPI (web framework)
- EasyOCR (Nepali OCR)
- Groq (LLM for summaries)
- PyTorch (deep learning)

**Frontend**:
- React 18
- Vite (build tool)
- Axios (HTTP client)
- Lucide React (icons)

## API Endpoints

### POST /extract
Upload document for OCR
```json
{
  "file": <multipart file>
}
```

Returns:
```json
{
  "raw_text": "...",
  "cleaned_text": "...",
  "confidence_score": 85.5,
  "word_count": 150,
  "success": true
}
```

### POST /analyze
Generate summaries
```json
{
  "text": "document text here"
}
```

Returns:
```json
{
  "english_summary": "...",
  "nepali_summary": "...",
  "key_facts": ["fact1", "fact2", "fact3"],
  "success": true
}
```

### POST /chat
Ask questions
```json
{
  "text": "document text",
  "question": "What is the date?",
  "history": []
}
```

Returns:
```json
{
  "answer": "...",
  "success": true
}
```

## Privacy & Security

- **No data storage**: Documents processed in memory only
- **No tracking**: No user data logged
- **API security**: Keys stored in environment variables
- **CORS enabled**: For frontend-backend communication
