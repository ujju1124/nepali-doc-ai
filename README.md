# 📄 Nepal Doc AI (React + FastAPI)

Nepal Doc AI is an intelligent document analysis tool that makes Nepali government documents easy to understand. Upload a photo of any Nepali document and instantly get plain-language summaries in both English and Nepali, plus the ability to ask questions about the document content.

## 🎯 What It Does

- **OCR Extraction**: Extract text from Nepali documents using EasyOCR
- **Bilingual Summaries**: Get 3-4 sentence summaries in both English and Nepali
- **Key Facts**: Automatically identifies the 3 most important points
- **Interactive Q&A**: Ask followup questions in English or Nepali
- **Quality Indicators**: Shows OCR confidence so you know if results are reliable

## 🏗️ Architecture

**Backend**: FastAPI + Python
- `/extract` - OCR text extraction
- `/analyze` - Summary generation
- `/chat` - Document Q&A

**Frontend**: React + Vite
- Modern, accessible UI
- No framework dependencies (plain CSS)
- Responsive design (mobile + desktop)

## 🚀 Quick Start

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

## 📝 Example Use Cases

- **Land Records (जग्गा दस्तावेज)**: Understand property documents
- **Citizenship Certificates (नागरिकता प्रमाणपत्र)**: Extract key information
- **Government Notices (सरकारी सूचना)**: Summarize official announcements
- **Certificates**: Birth, marriage, education certificates
- **Official Letters**: Formal government correspondence

## 🎨 Design

**Visual Direction**: Civic tech tool for everyday Nepali citizens

**Color Palette**:
- Deep Navy (#1B2B4B) - Primary
- Warm White (#F8F6F1) - Background
- Crimson (#C41E3A) - Accent (Nepal flag red)
- Slate Gray (#64748B) - Secondary text

**Typography**:
- Inter - UI elements and English text
- Tiro Devanagari - Nepali text rendering

## 🐳 Deployment

### Backend (Hugging Face Spaces)

1. Create a new Space on Hugging Face
2. Choose "Docker" as SDK
3. Upload backend files including Dockerfile
4. Add GROQ_API_KEY as a secret
5. Deploy!

### Frontend (Vercel/Netlify)

```bash
cd frontend
npm run build

# Deploy dist/ folder to Vercel or Netlify
# Set VITE_API_URL environment variable to your HF Space URL
```

## ⚠️ Known Limitations

1. **Handwritten text**: Works best with printed/typed text
2. **Image quality**: Low resolution/blurry images affect accuracy
3. **Processing time**: 10-30 seconds per document on CPU
4. **Complex layouts**: Tables may extract in unexpected order
5. **First run**: Downloads EasyOCR models (~100MB)

## 🛠️ Tech Stack

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
- Plain CSS (no frameworks)

## 📊 API Endpoints

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

## 🔒 Privacy & Security

- **No data storage**: Documents processed in memory only
- **No tracking**: No user data logged
- **API security**: Keys stored in environment variables
- **CORS enabled**: For frontend-backend communication

## 📄 License

Open source - available for educational and personal use

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report issues
- Submit pull requests
- Suggest features
- Improve documentation

---

**Built with ❤️ for making Nepali documents accessible to everyone**
