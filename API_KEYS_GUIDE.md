# 🔑 Free LLM API Keys Guide

Your app supports 3 free LLM providers with automatic fallback. You only need **ONE** key, but having multiple provides better reliability.

---

## Priority Order (Automatic Fallback)

1. **Groq** (Primary - fastest, if working)
2. **Google Gemini** (Fallback #1 - completely free) ⭐
3. **Hugging Face** (Fallback #2 - completely free)

If Groq fails → tries Google Gemini → tries Hugging Face → shows error

---

## ⭐ Option 1: Google Gemini (RECOMMENDED - Free & Fast)

### Free Tier
- **Cost**: COMPLETELY FREE FOREVER
- **Limits**: 15 requests/minute, 1500 requests/day
- **Speed**: Fast (2-4 seconds)
- **Models**: Gemini 1.5 Flash
- **No credit card required!**

### How to Get Key (2 minutes)

1. **Go to**: https://aistudio.google.com/apikey
2. **Sign in**: With your Google account
3. **Create API Key**:
   - Click **"Create API Key"** button
   - Select **"Create API key in new project"**
   - Copy the key (it's a long string of letters/numbers)
4. **Done!** No verification, no credit card, instant key

### Why Recommended
✅ Completely free forever  
✅ No credit card needed  
✅ Fast responses (2-4 sec)  
✅ 1500 requests/day (more than enough)  
✅ Instant setup (2 minutes)  

**Perfect for your app!**

---

## Option 2: Hugging Face (Free Forever)

### Free Tier
- **Cost**: FREE (no credit card ever)
- **Limits**: Rate-limited during peak hours
- **Speed**: Slower (5-10 seconds)
- **Models**: Llama 2 7B Chat

### How to Get Key

1. **Sign Up**: https://huggingface.co/join
2. **Verify Email**: Check inbox and click link
3. **Create Token**:
   - Go to: https://huggingface.co/settings/tokens
   - Click **"New token"**
   - Name: "Nepal Doc AI"
   - Type: **Read** (default)
   - Click **"Generate token"**
   - Copy token (starts with `hf_...`)

### Notes
- Completely free forever
- Slower than Google Gemini
- Good as backup/fallback
- No limits, but rate-limited

---

## Option 3: Groq (Fastest, if not restricted)

### Free Tier
- **Cost**: FREE
- **Limits**: 14,400 requests/day, 30 requests/minute
- **Speed**: Very fast (1-2 seconds)
- **Models**: Llama 3.1 8B Instant

### How to Get Key

1. **Sign Up**: https://console.groq.com
2. **Verify Email**: Check inbox
3. **Create API Key**:
   - Click profile (top right) → "API Keys"
   - Click **"Create API Key"**
   - Name: "Nepal Doc AI"
   - Copy key (starts with `gsk_...`)

### If Restricted
Your account was suspended. Use Google Gemini instead!

---

## How to Add Keys to Your App

### For HF Spaces (Production)

1. Go to: https://huggingface.co/spaces/Ujju33/nepali-doc-ai-backend/settings
2. Scroll to **Repository secrets**
3. Add keys (one or more):

| Secret Name | Get From | Example |
|-------------|----------|---------|
| `GOOGLE_API_KEY` | https://aistudio.google.com/apikey | Long alphanumeric string |
| `HUGGINGFACE_API_KEY` | https://huggingface.co/settings/tokens | `hf_...` |
| `GROQ_API_KEY` | https://console.groq.com | `gsk_...` |

4. Click **"Add"** for each
5. Space restarts automatically

### For Local Development

Edit `backend/.env`:
```env
# Add at least one (Google Gemini recommended)
GOOGLE_API_KEY=your_google_key_here
HUGGINGFACE_API_KEY=hf_your_key_here
GROQ_API_KEY=gsk_your_key_here
```

---

## Recommended Setup

### Minimum (Pick ONE)

**Best option**: Just Google Gemini
```env
GOOGLE_API_KEY=your_key
```
- ✅ Free forever
- ✅ Fast (2-4 sec)
- ✅ 1500 requests/day
- ✅ No credit card

**If Google doesn't work**: Hugging Face
```env
HUGGINGFACE_API_KEY=hf_...
```
- ✅ Free forever
- ⚠️ Slower (5-10 sec)
- ✅ No limits

### Best Reliability (All 3)
```env
GROQ_API_KEY=gsk_...           # Primary (if not restricted)
GOOGLE_API_KEY=...             # Fallback 1 (fast & free)
HUGGINGFACE_API_KEY=hf_...     # Fallback 2 (always works)
```

---

## Testing Your Setup

### Check Configuration
Visit:
```
https://ujju33-nepali-doc-ai-backend.hf.space/health
```

Will show:
```json
{
  "status": "healthy",
  "groq_configured": false,
  "google_configured": true,
  "huggingface_configured": true,
  "ocr_ready": true
}
```

### Test Upload
1. Go to: https://nepali-doc-ai.vercel.app/
2. Upload test image
3. Check which provider was used in logs

---

## Cost Comparison

| Provider | Cost | Speed | Daily Limit | Setup | Forever Free? |
|----------|------|-------|-------------|-------|---------------|
| **Google Gemini** | FREE | ⚡⚡ | 1500 | 2 min | ✅ YES |
| **Hugging Face** | FREE | ⚡ | Unlimited* | 5 min | ✅ YES |
| **Groq** | FREE | ⚡⚡⚡ | 14,400 | 5 min | ✅ YES (if not restricted) |

*Rate-limited during peak hours

---

## Quick Start (RIGHT NOW - 2 minutes)

### Get Google Gemini API Key

1. **Open**: https://aistudio.google.com/apikey
2. **Sign in**: Google account
3. **Click**: "Create API Key" → "Create API key in new project"
4. **Copy**: The key

### Add to HF Space

1. **Open**: https://huggingface.co/spaces/Ujju33/nepali-doc-ai-backend/settings
2. **Scroll**: Repository secrets
3. **Add**:
   - Name: `GOOGLE_API_KEY`
   - Value: [paste your key]
4. **Save**

### Test

Visit: https://nepali-doc-ai.vercel.app/

Upload a document - it will work! 🎉

---

## Troubleshooting

### "All LLM providers failed"
- Add at least one API key
- Check key is correct (no spaces, complete)

### Groq "organization restricted"
- Your account was suspended
- Use Google Gemini instead

### Google Gemini slow/failing
- You hit the 15 req/min limit
- Add Hugging Face as backup
- Wait 1 minute and try again

### Hugging Face very slow
- It's the slowest option (5-10 sec)
- Add Google Gemini for faster responses

---

## Summary

**Easiest & Best**: Google Gemini (2 min setup, fast, free forever)  
**Backup**: Hugging Face (slower but always free)  
**Optional**: Groq (fastest, if account works)

**Recommendation**: Start with Google Gemini now! 🚀

