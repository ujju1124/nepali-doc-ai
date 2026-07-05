# 🚀 Quick Start Guide - Nepal Doc AI

## ✅ Installation Complete!

All dependencies have been installed successfully.

## 🔑 Next Steps

### 1. Add Your Groq API Key

Edit the `.env` file and add your Groq API key:

```bash
notepad .env
```

Replace `your_groq_key_here` with your actual key from: https://console.groq.com/keys

Example:
```
GROQ_API_KEY=gsk_1234567890abcdefghijklmnopqrstuvwxyz
```

### 2. Run the App

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

## 📸 How to Use

1. **Upload** a document (JPG, PNG, or PDF)
2. **Click** "Extract & Analyze Document"
3. **Wait** 10-30 seconds for OCR processing
4. **Review** the summaries in English and Nepali
5. **Ask** questions about the document

## 💡 Tips

- Use **clear, well-lit photos** for best OCR results
- Check the **confidence score** - if below 50%, try a clearer image
- The app works best with **printed/typed text** (not handwritten)
- **First run** downloads EasyOCR models (~100MB) - be patient!

## 🐛 Troubleshooting

### "GROQ_API_KEY not found"
→ Make sure you edited `.env` and added your API key

### OCR is slow
→ First run downloads models. Subsequent runs are faster (~10-30s per image)

### Low OCR confidence
→ Try taking a better quality photo with good lighting

### PDF not working
→ Make sure you have Poppler installed (required for pdf2image)
   Windows: Download from https://github.com/oschwartz10612/poppler-windows/releases

## 📝 Example Documents to Try

- Citizenship certificates (नागरिकता प्रमाणपत्र)
- Land records (जग्गा दस्तावेज)
- Government notices (सरकारी सूचना)
- Official letters
- Birth/marriage certificates

## 🎯 What Gets Analyzed

For each document, you get:
- ✅ English summary (3-4 sentences)
- ✅ Nepali summary (3-4 sentences)
- ✅ 3 key facts
- ✅ Q&A capability (ask anything about the document)

---

**Enjoy using Nepal Doc AI! 🇳🇵**
