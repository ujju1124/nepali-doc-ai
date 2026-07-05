"""
Test script to verify Nepal Doc AI setup
"""

import sys

print("🔍 Testing Nepal Doc AI Setup...\n")

# Test 1: Check Python version
print(f"✓ Python version: {sys.version.split()[0]}")

# Test 2: Import core packages
try:
    import easyocr
    print("✓ EasyOCR installed")
except ImportError as e:
    print(f"✗ EasyOCR missing: {e}")
    sys.exit(1)

try:
    import streamlit
    print("✓ Streamlit installed")
except ImportError as e:
    print(f"✗ Streamlit missing: {e}")
    sys.exit(1)

try:
    import groq
    print("✓ Groq installed")
except ImportError as e:
    print(f"✗ Groq missing: {e}")
    sys.exit(1)

try:
    import pdf2image
    print("✓ pdf2image installed")
except ImportError as e:
    print(f"✗ pdf2image missing: {e}")
    sys.exit(1)

try:
    from PIL import Image
    print("✓ Pillow installed")
except ImportError as e:
    print(f"✗ Pillow missing: {e}")
    sys.exit(1)

try:
    import cv2
    print("✓ OpenCV installed")
except ImportError as e:
    print(f"✗ OpenCV missing: {e}")
    sys.exit(1)

try:
    import torch
    print(f"✓ PyTorch {torch.__version__} installed")
except ImportError as e:
    print(f"✗ PyTorch missing: {e}")
    sys.exit(1)

# Test 3: Check environment variables
print("\n📁 Checking configuration files...")

import os
from pathlib import Path

if Path('.env').exists():
    print("✓ .env file exists")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    if os.getenv('GROQ_API_KEY'):
        key = os.getenv('GROQ_API_KEY')
        if key != 'your_groq_key_here' and len(key) > 10:
            print(f"✓ GROQ_API_KEY configured (starts with: {key[:10]}...)")
        else:
            print("⚠ GROQ_API_KEY needs to be updated in .env file")
    else:
        print("⚠ GROQ_API_KEY not found in .env file")
else:
    print("⚠ .env file not found - copy .env.example to .env")

# Test 4: Test module imports
print("\n📦 Testing module imports...")

try:
    from ocr import get_reader
    print("✓ ocr.py module working")
except Exception as e:
    print(f"✗ ocr.py module error: {e}")

try:
    from intelligence import generate_summary, answer_question
    print("✓ intelligence.py module working")
except Exception as e:
    print(f"✗ intelligence.py module error: {e}")

print("\n" + "="*50)
print("🎉 Setup verification complete!")
print("="*50)
print("\n📝 Next steps:")
print("1. Make sure GROQ_API_KEY is set in .env file")
print("2. Run: streamlit run app.py")
print("3. Upload a Nepali document and test!\n")
