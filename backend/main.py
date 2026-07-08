"""
Nepal Doc AI - FastAPI Backend
Handles OCR extraction, document analysis, and Q&A
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Tuple, Optional
import logging
from dotenv import load_dotenv
import os

# Import our existing modules
from ocr import extract_text_from_document
from intelligence import generate_summary, answer_question

# Load environment variables
load_dotenv()

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Nepal Doc AI API",
    description="OCR and AI-powered analysis for Nepali documents",
    version="1.0.0"
)

# Configure CORS - allow all origins for Vercel → HF Spaces communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


# Request/Response Models
class AnalyzeRequest(BaseModel):
    text: str


class ChatRequest(BaseModel):
    text: str
    question: str
    history: Optional[List[Tuple[str, str]]] = []


class OCRResponse(BaseModel):
    raw_text: str
    cleaned_text: str
    confidence_score: float
    word_count: int
    success: bool
    error: Optional[str] = None


class AnalyzeResponse(BaseModel):
    english_summary: str
    nepali_summary: str
    key_facts: List[str]
    success: bool
    error: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    success: bool
    error: Optional[str] = None


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "Nepal Doc AI API",
        "version": "1.0.0",
        "endpoints": {
            "extract": "POST /extract - Upload document for OCR",
            "analyze": "POST /analyze - Generate summaries from text",
            "chat": "POST /chat - Ask questions about document"
        }
    }


@app.post("/extract", response_model=OCRResponse)
async def extract_document(file: UploadFile = File(...)):
    """
    Extract text from uploaded document using OCR.
    
    Accepts: JPG, PNG, PDF files
    Returns: Extracted text with confidence scores
    """
    try:
        logger.info(f"Processing file: {file.filename}")
        
        # Validate file type
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'application/pdf']
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed: JPG, PNG, PDF. Got: {file.content_type}"
            )
        
        # Read file bytes
        file_bytes = await file.read()
        
        if len(file_bytes) == 0:
            raise HTTPException(status_code=400, detail="Empty file uploaded")
        
        # Extract text using our OCR module
        result = extract_text_from_document(file_bytes, file.filename)
        
        logger.info(f"OCR completed for {file.filename}: {result['word_count']} words, {result['confidence_score']:.1f}% confidence")
        
        return OCRResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_document(request: AnalyzeRequest):
    """
    Generate bilingual summaries and key facts from document text.
    
    Accepts: Document text string
    Returns: English summary, Nepali summary, and key facts
    """
    try:
        if not request.text or len(request.text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        logger.info(f"Analyzing document text ({len(request.text)} characters)")
        
        # Generate summary using our intelligence module
        result = generate_summary(request.text)
        
        if not result['success']:
            raise HTTPException(status_code=500, detail=result['error'])
        
        logger.info("Summary generation completed successfully")
        
        return AnalyzeResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/chat", response_model=ChatResponse)
async def chat_about_document(request: ChatRequest):
    """
    Answer questions about the document using extracted text as context.
    
    Accepts: Document text, user question, and chat history
    Returns: AI-generated answer
    """
    try:
        if not request.text or len(request.text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Document text cannot be empty")
        
        if not request.question or len(request.question.strip()) == 0:
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        logger.info(f"Processing chat question: {request.question[:50]}...")
        
        # Convert history from list of tuples if needed
        history = request.history if request.history else []
        
        # Answer question using our intelligence module
        result = answer_question(request.text, request.question, history)
        
        if not result['success']:
            raise HTTPException(status_code=500, detail=result['error'])
        
        logger.info("Question answered successfully")
        
        return ChatResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error answering question: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")


@app.get("/health")
async def health_check():
    """
    Health check endpoint for deployment monitoring.
    Shows which LLM providers are configured.
    """
    try:
        # Check all LLM provider API keys
        groq_key = os.getenv('GROQ_API_KEY')
        together_key = os.getenv('TOGETHER_API_KEY')
        hf_key = os.getenv('HUGGINGFACE_API_KEY')
        
        groq_configured = groq_key is not None and groq_key != 'your_groq_key_here' and groq_key != ''
        together_configured = together_key is not None and together_key != '' 
        hf_configured = hf_key is not None and hf_key != ''
        
        # Check if at least one provider is configured
        any_provider = groq_configured or together_configured or hf_configured
        
        return {
            "status": "healthy" if any_provider else "degraded",
            "groq_configured": groq_configured,
            "together_configured": together_configured,
            "huggingface_configured": hf_configured,
            "ocr_ready": True,
            "api_version": "1.0.0",
            "note": "At least one LLM provider required for summaries" if not any_provider else None
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
