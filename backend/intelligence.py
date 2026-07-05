"""
Intelligence module for document summarization and Q&A using Groq.
Handles English/Nepali summaries and context-aware question answering.
"""

from groq import Groq
import os
from typing import Dict, List, Tuple
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_groq_client():
    """Initialize and return Groq client."""
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")
    return Groq(api_key=api_key)


def generate_summary(extracted_text: str) -> Dict:
    """
    Generate English summary, Nepali summary, and key facts from document text.
    
    Args:
        extracted_text: Text extracted from the document
        
    Returns:
        Dictionary containing:
            - english_summary: 3-4 sentence summary in English
            - nepali_summary: 3-4 sentence summary in Nepali
            - key_facts: List of 3 key facts extracted
            - success: Boolean indicating if generation succeeded
            - error: Error message if failed
    """
    try:
        client = get_groq_client()
        
        system_prompt = """You are a helpful assistant that explains Nepali government documents in simple language. 
Your task is to analyze the provided document text and create:
1. A clear 3-4 sentence summary in English
2. A clear 3-4 sentence summary in Nepali (using Devanagari script)
3. Three key facts or important points from the document

Always base your analysis strictly on the provided document text. If the text is unclear or incomplete, mention that in your summary."""

        user_prompt = f"""Analyze this Nepali document text and provide:

1. English Summary (3-4 sentences in plain English)
2. Nepali Summary (3-4 sentences in Nepali/Devanagari script)
3. Three Key Facts (as a numbered list)

Document Text:
{extracted_text}

Format your response exactly like this:

ENGLISH SUMMARY:
[Your 3-4 sentence English summary here]

NEPALI SUMMARY:
[Your 3-4 sentence Nepali summary here]

KEY FACTS:
1. [First key fact]
2. [Second key fact]
3. [Third key fact]"""

        # Call Groq API
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        content = response.choices[0].message.content.strip()
        
        # Parse the response
        english_summary = ""
        nepali_summary = ""
        key_facts = []
        
        sections = content.split('\n\n')
        current_section = None
        
        for section in sections:
            section = section.strip()
            
            if 'ENGLISH SUMMARY:' in section:
                current_section = 'english'
                english_summary = section.replace('ENGLISH SUMMARY:', '').strip()
            elif 'NEPALI SUMMARY:' in section:
                current_section = 'nepali'
                nepali_summary = section.replace('NEPALI SUMMARY:', '').strip()
            elif 'KEY FACTS:' in section:
                current_section = 'facts'
                facts_text = section.replace('KEY FACTS:', '').strip()
                # Extract numbered items
                lines = facts_text.split('\n')
                for line in lines:
                    line = line.strip()
                    if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                        # Remove numbering/bullets
                        fact = line.lstrip('0123456789.-•) ').strip()
                        if fact:
                            key_facts.append(fact)
            elif current_section == 'english' and section:
                english_summary += ' ' + section
            elif current_section == 'nepali' and section:
                nepali_summary += ' ' + section
        
        # Ensure we have at least some content
        if not english_summary:
            english_summary = "Unable to generate summary from the provided text."
        if not nepali_summary:
            nepali_summary = "प्रदान गरिएको पाठबाट सारांश उत्पन्न गर्न असमर्थ।"
        if not key_facts:
            key_facts = ["No key facts could be extracted from the document."]
        
        # Limit to 3 facts
        key_facts = key_facts[:3]
        
        logger.info("Successfully generated document summary")
        
        return {
            'english_summary': english_summary.strip(),
            'nepali_summary': nepali_summary.strip(),
            'key_facts': key_facts,
            'success': True,
            'error': None
        }
        
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        return {
            'english_summary': '',
            'nepali_summary': '',
            'key_facts': [],
            'success': False,
            'error': f'Summary generation failed: {str(e)}'
        }


def answer_question(extracted_text: str, question: str, chat_history: List[Tuple[str, str]] = None) -> Dict:
    """
    Answer a question about the document using extracted text as context.
    
    Args:
        extracted_text: Text extracted from the document
        question: User's question (can be in English or Nepali)
        chat_history: List of (question, answer) tuples from previous conversation
        
    Returns:
        Dictionary containing:
            - answer: AI-generated answer
            - success: Boolean indicating if answer generation succeeded
            - error: Error message if failed
    """
    try:
        client = get_groq_client()
        
        system_prompt = """You are a helpful assistant that explains Nepali government documents in simple language. 

IMPORTANT RULES:
- Always base your answers strictly on the provided document text
- If something is not mentioned in the document, clearly state: "This information is not found in the document."
- Answer in the same language as the question (English for English questions, Nepali for Nepali questions)
- Be concise but thorough
- If the document text is unclear, mention that the OCR quality may affect accuracy"""

        # Build conversation context
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add document context
        context_message = f"""Here is the document text you should use to answer questions:

DOCUMENT TEXT:
{extracted_text}

Please answer questions based strictly on this document."""
        
        messages.append({"role": "user", "content": context_message})
        messages.append({"role": "assistant", "content": "I understand. I will answer questions based strictly on the provided document text. If information is not in the document, I will say so clearly."})
        
        # Add chat history if provided
        if chat_history:
            for q, a in chat_history[-3:]:  # Include last 3 exchanges for context
                messages.append({"role": "user", "content": q})
                messages.append({"role": "assistant", "content": a})
        
        # Add current question
        messages.append({"role": "user", "content": question})
        
        # Call Groq API
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.3,
            max_tokens=500
        )
        
        answer = response.choices[0].message.content.strip()
        
        logger.info(f"Successfully answered question: {question[:50]}...")
        
        return {
            'answer': answer,
            'success': True,
            'error': None
        }
        
    except Exception as e:
        logger.error(f"Error answering question: {str(e)}")
        return {
            'answer': '',
            'success': False,
            'error': f'Question answering failed: {str(e)}'
        }
