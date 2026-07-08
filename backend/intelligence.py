"""
Intelligence module for document summarization and Q&A with multiple free LLM providers.
Supports automatic fallback: Groq -> Google Gemini -> Hugging Face
"""

from groq import Groq
import os
from typing import Dict, List, Tuple, Optional
import logging
import requests

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMProvider:
    """Base class for LLM providers with fallback support."""
    
    @staticmethod
    def get_groq_client() -> Optional[Groq]:
        """Initialize Groq client (primary provider)."""
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            logger.warning("GROQ_API_KEY not found")
            return None
        try:
            return Groq(api_key=api_key)
        except Exception as e:
            logger.error(f"Failed to initialize Groq: {e}")
            return None
    
    @staticmethod
    def call_google_gemini(messages: List[Dict], max_tokens: int = 1000) -> Optional[str]:
        """Call Google Gemini API (fallback provider #1 - Free tier: 15 requests/min)."""
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            logger.warning("GOOGLE_API_KEY not found")
            return None
        
        try:
            # Use v1 API with simpler format
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
            headers = {"Content-Type": "application/json"}
            
            # Combine all messages into a single prompt
            prompt = ""
            for msg in messages:
                role = msg['role']
                content = msg['content']
                if role == 'system':
                    prompt += f"{content}\n\n"
                elif role == 'user':
                    prompt += f"User: {content}\n\n"
                elif role == 'assistant':
                    prompt += f"Assistant: {content}\n\n"
            
            data = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "maxOutputTokens": max_tokens,
                    "temperature": 0.3
                }
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            # Log more details on error
            if response.status_code != 200:
                logger.error(f"Google Gemini error: {response.status_code} - {response.text[:200]}")
            
            response.raise_for_status()
            result = response.json()
            
            if 'candidates' in result and len(result['candidates']) > 0:
                text = result['candidates'][0]['content']['parts'][0]['text']
                return text.strip()
            return None
            
        except Exception as e:
            logger.error(f"Google Gemini API failed: {e}")
            return None
    
    @staticmethod
    def call_huggingface_api(messages: List[Dict], max_tokens: int = 1000) -> Optional[str]:
        """Call Hugging Face Inference API (fallback provider #2 - Free tier available)."""
        api_key = os.getenv('HUGGINGFACE_API_KEY')
        if not api_key:
            logger.warning("HUGGINGFACE_API_KEY not found")
            return None
        
        try:
            url = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            # Convert messages to prompt format
            prompt = ""
            for msg in messages:
                role = msg['role']
                content = msg['content']
                if role == 'system':
                    prompt += f"[INST] <<SYS>>\n{content}\n<</SYS>>\n\n"
                elif role == 'user':
                    prompt += f"{content} [/INST] "
                elif role == 'assistant':
                    prompt += f"{content} [INST] "
            
            data = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": max_tokens,
                    "temperature": 0.3,
                    "return_full_text": False
                }
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', '').strip()
            return None
            
        except Exception as e:
            logger.error(f"Hugging Face API failed: {e}")
            return None
    
    @staticmethod
    def generate_completion(messages: List[Dict], max_tokens: int = 1000) -> Tuple[Optional[str], str]:
        """
        Try multiple providers in order: Groq -> Google Gemini -> Hugging Face.
        Returns (response_text, provider_used).
        """
        # Try Groq first
        client = LLMProvider.get_groq_client()
        if client:
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=messages,
                    temperature=0.3,
                    max_tokens=max_tokens
                )
                content = response.choices[0].message.content.strip()
                logger.info("✅ Used Groq API")
                return content, "Groq"
            except Exception as e:
                logger.warning(f"Groq failed: {e}, trying fallback...")
        
        # Try Google Gemini
        response = LLMProvider.call_google_gemini(messages, max_tokens)
        if response:
            logger.info("✅ Used Google Gemini (fallback)")
            return response, "Google Gemini"
        
        # Try Hugging Face
        response = LLMProvider.call_huggingface_api(messages, max_tokens)
        if response:
            logger.info("✅ Used Hugging Face (fallback)")
            return response, "Hugging Face"
        
        # All providers failed
        logger.error("❌ All LLM providers failed")
        return None, "None"


def generate_summary(extracted_text: str) -> Dict:
    """
    Generate English summary, Nepali summary, and key facts from document text.
    Uses multiple LLM providers with automatic fallback.
    
    Args:
        extracted_text: Text extracted from the document
        
    Returns:
        Dictionary containing:
            - english_summary: 3-4 sentence summary in English
            - nepali_summary: 3-4 sentence summary in Nepali
            - key_facts: List of 3 key facts extracted
            - provider: Which LLM provider was used
            - success: Boolean indicating if generation succeeded
            - error: Error message if failed
    """
    try:
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

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        # Try all providers with fallback
        content, provider = LLMProvider.generate_completion(messages, max_tokens=1000)
        
        if not content:
            raise Exception("All LLM providers failed. Please add at least one API key: GROQ_API_KEY, GOOGLE_API_KEY, or HUGGINGFACE_API_KEY")
        
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
        
        logger.info(f"Successfully generated document summary using {provider}")
        
        return {
            'english_summary': english_summary.strip(),
            'nepali_summary': nepali_summary.strip(),
            'key_facts': key_facts,
            'provider': provider,
            'success': True,
            'error': None
        }
        
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        return {
            'english_summary': '',
            'nepali_summary': '',
            'key_facts': [],
            'provider': 'None',
            'success': False,
            'error': f'Summary generation failed: {str(e)}'
        }


def answer_question(extracted_text: str, question: str, chat_history: List[Tuple[str, str]] = None) -> Dict:
    """
    Answer a question about the document using extracted text as context.
    Uses multiple LLM providers with automatic fallback.
    
    Args:
        extracted_text: Text extracted from the document
        question: User's question (can be in English or Nepali)
        chat_history: List of (question, answer) tuples from previous conversation
        
    Returns:
        Dictionary containing:
            - answer: AI-generated answer
            - provider: Which LLM provider was used
            - success: Boolean indicating if answer generation succeeded
            - error: Error message if failed
    """
    try:
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
        
        # Try all providers with fallback
        answer, provider = LLMProvider.generate_completion(messages, max_tokens=500)
        
        if not answer:
            raise Exception("All LLM providers failed. Please add at least one API key: GROQ_API_KEY, GOOGLE_API_KEY, or HUGGINGFACE_API_KEY")
        
        logger.info(f"Successfully answered question using {provider}: {question[:50]}...")
        
        return {
            'answer': answer,
            'provider': provider,
            'success': True,
            'error': None
        }
        
    except Exception as e:
        logger.error(f"Error answering question: {str(e)}")
        return {
            'answer': '',
            'provider': 'None',
            'success': False,
            'error': f'Question answering failed: {str(e)}'
        }
