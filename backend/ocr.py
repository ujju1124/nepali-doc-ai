"""
OCR extraction logic for Nepali documents using EasyOCR.
Handles images and PDFs with Nepali + English text extraction.
"""

import easyocr
import numpy as np
from PIL import Image
import io
import re
from typing import Dict, Optional
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# IMPORTANT: Initialize EasyOCR reader ONCE at module level (singleton pattern)
# This prevents 10-20 second initialization on every upload
_reader_cache = None


def get_reader():
    """Get or create the cached EasyOCR reader instance."""
    global _reader_cache
    if _reader_cache is None:
        logger.info("Initializing EasyOCR reader (this may take 10-20 seconds)...")
        _reader_cache = easyocr.Reader(['ne', 'en'], gpu=False)
        logger.info("EasyOCR reader initialized successfully")
    return _reader_cache


def clean_extracted_text(raw_text: str) -> str:
    """
    Clean OCR output by removing excessive whitespace and joining broken lines intelligently.
    
    Args:
        raw_text: Raw OCR output text
        
    Returns:
        Cleaned text with proper spacing
    """
    if not raw_text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', raw_text)
    
    # Remove spaces before punctuation
    text = re.sub(r'\s+([।,.!?;:])', r'\1', text)
    
    # Add space after Nepali full stop (Devanagari danda) if missing
    text = re.sub(r'।(\S)', r'। \1', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def extract_text_from_image(image_bytes: bytes, filename: str) -> Dict:
    """
    Extract text from image using EasyOCR.
    
    Args:
        image_bytes: Image file bytes
        filename: Original filename (for logging/debugging)
        
    Returns:
        Dictionary containing:
            - raw_text: Extracted text with original spacing
            - cleaned_text: Cleaned and formatted text
            - confidence_score: Average confidence (0-100)
            - word_count: Number of words extracted
            - success: Boolean indicating if extraction succeeded
            - error: Error message if failed
    """
    try:
        # Load image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary (EasyOCR expects RGB)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert PIL Image to numpy array
        img_array = np.array(image)
        
        # Get EasyOCR reader
        reader = get_reader()
        
        # Perform OCR
        results = reader.readtext(img_array)
        
        if not results:
            return {
                'raw_text': '',
                'cleaned_text': '',
                'confidence_score': 0.0,
                'word_count': 0,
                'success': False,
                'error': 'No text detected in the image'
            }
        
        # Extract text and confidence scores
        text_parts = []
        confidence_scores = []
        
        for (bbox, text, confidence) in results:
            text_parts.append(text)
            confidence_scores.append(confidence)
        
        # Join text parts with spaces
        raw_text = ' '.join(text_parts)
        
        # Clean the text
        cleaned_text = clean_extracted_text(raw_text)
        
        # Calculate average confidence (convert to percentage)
        avg_confidence = (sum(confidence_scores) / len(confidence_scores)) * 100
        
        # Count words (approximate)
        word_count = len(cleaned_text.split())
        
        logger.info(f"Extracted {word_count} words with {avg_confidence:.1f}% confidence from {filename}")
        
        return {
            'raw_text': raw_text,
            'cleaned_text': cleaned_text,
            'confidence_score': round(avg_confidence, 2),
            'word_count': word_count,
            'success': True,
            'error': None
        }
        
    except Exception as e:
        logger.error(f"Error extracting text from {filename}: {str(e)}")
        return {
            'raw_text': '',
            'cleaned_text': '',
            'confidence_score': 0.0,
            'word_count': 0,
            'success': False,
            'error': f'OCR failed: {str(e)}'
        }


def pdf_to_image(pdf_bytes: bytes) -> Optional[bytes]:
    """
    Convert first page of PDF to image bytes.
    
    Args:
        pdf_bytes: PDF file bytes
        
    Returns:
        Image bytes (JPEG format) or None if conversion failed
    """
    try:
        from pdf2image import convert_from_bytes
        
        # Convert first page only
        images = convert_from_bytes(pdf_bytes, first_page=1, last_page=1)
        
        if not images:
            return None
        
        # Convert PIL Image to bytes
        img_byte_arr = io.BytesIO()
        images[0].save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        
        return img_byte_arr.read()
        
    except Exception as e:
        logger.error(f"Error converting PDF to image: {str(e)}")
        return None


def extract_text_from_document(file_bytes: bytes, filename: str) -> Dict:
    """
    Extract text from document (image or PDF).
    
    Args:
        file_bytes: Document file bytes
        filename: Original filename
        
    Returns:
        Dictionary with extraction results (same format as extract_text_from_image)
    """
    file_extension = filename.lower().split('.')[-1]
    
    # Handle PDF files
    if file_extension == 'pdf':
        logger.info(f"Converting PDF to image: {filename}")
        image_bytes = pdf_to_image(file_bytes)
        
        if image_bytes is None:
            return {
                'raw_text': '',
                'cleaned_text': '',
                'confidence_score': 0.0,
                'word_count': 0,
                'success': False,
                'error': 'Failed to convert PDF to image'
            }
        
        return extract_text_from_image(image_bytes, filename)
    
    # Handle image files directly
    else:
        return extract_text_from_image(file_bytes, filename)
