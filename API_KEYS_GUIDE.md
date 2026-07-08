# 🔑 Free LLM API Keys Guide

Your app now supports 3 free LLM providers with automatic fallback. You only need **ONE** of these keys, but having multiple provides better reliability.

---

## Priority Order (Automatic Fallback)

1. **Groq** (Primary - fastest)
2. **Together AI** (Fallback #1 - free tier)
3. **Hugging Face** (Fallback #2 - free tier)

If Groq fails → tries Together AI → tries Hugging Face → shows error

---

## Option 1: Groq (Recommended - Fastest)

### Free Tier
- **Cost**: FREE
- **Limits**: 14,400 requests/day, 30 requests/minute
- **Speed**: Very fast
- **Models**: Llama 3.1 8B Instant

### How to Get Key

1. **Sign Up**: Go to https://console.groq.com
2. **Verify Email**: Check your inbox and verify
3. **Create API Key**:
   - Click your profile (top right)
   - Go to "API Keys"
   - Click "Create API Key"
   - Give it a name like "Nepal Doc AI"
   - Copy the key (starts with `gsk_...`)

### If Restricted
- Check if your organization was restricted
- Contact support: https://console.groq.com/support
- Or create a new account with different email

---

## Option 2: Together AI (Fallback #1)

### Free Tier
- **Cost**: FREE (with $25 credit on signup)
- **Limits**: After credit runs out, need payment
- **Speed**: Fast
- **Models**: Llama 3 8B Chat

### How to Get Key

1. **Sign Up**: Go to https://api.together.xyz
2. **Verify Email**: Check inbox
3. **Get Free Credits**:
   - You get $25 free credits automatically
   - No credit card required initially
4. **Create API Key**:
   - Go to "Settings" → "API Keys"
   - Click "Create new API key"
   - Give it a name
   - Copy the key (starts with a long string)

### Free Credits Last
- Depends on usage
- For your app: ~500-1000 documents (rough estimate)
- After that, need to add payment method

---

## Option 3: Hugging Face (Fallback #2)

### Free Tier
- **Cost**: FREE (truly free, no credit card)
- **Limits**: Rate-limited (slower than others)
- **Speed**: Slower (can take 5-10 seconds)
- **Models**: Llama 2 7B Chat

### How to Get Key

1. **Sign Up**: Go to https://huggingface.co/join
2. **Verify Email**: Check inbox
3. **Create Access Token**:
   - Go to https://huggingface.co/settings/tokens
   - Click "New token"
   - Name: "Nepal Doc AI"
   - Type: **Read** (default is fine)
   - Click "Generate token"
   - Copy the token (starts with `hf_...`)

### Notes
- Completely free, no payment ever needed
- Slower than Groq/Together
- May have rate limits during peak times
- Can take 5-10 seconds per request

---

## How to Add Keys to Your App

### For Local Development

Edit `backend/.env`:
```env
# Add at least one (all three for best reliability)
GROQ_API_KEY=gsk_your_key_here
TOGETHER_API_KEY=your_together_key_here
HUGGINGFACE_API_KEY=hf_your_key_here
```

### For Hugging Face Spaces (Production)

1. Go to: https://huggingface.co/spaces/Ujju33/nepali-doc-ai-backend/settings
2. Scroll to **Repository secrets**
3. Add each key as a separate secret:

| Secret Name | Value |
|-------------|-------|
| `GROQ_API_KEY` | `gsk_...` |
| `TOGETHER_API_KEY` | Your Together AI key |
| `HUGGINGFACE_API_KEY` | `hf_...` |

4. Click "Save" after each
5. Space will restart automatically

---

## Recommended Setup

### Best Reliability (All 3)
```env
GROQ_API_KEY=gsk_...           # Primary (fastest)
TOGETHER_API_KEY=...           # Fallback 1
HUGGINGFACE_API_KEY=hf_...     # Fallback 2
```

### Minimum (Pick 1)

**If you want speed**: Just Groq
```env
GROQ_API_KEY=gsk_...
```

**If Groq is restricted**: Together AI
```env
TOGETHER_API_KEY=...
```

**If you want completely free forever**: Hugging Face
```env
HUGGINGFACE_API_KEY=hf_...
```

---

## Testing Your Setup

### Check What's Configured

Visit your backend:
```
https://ujju33-nepali-doc-ai-backend.hf.space/health
```

Will show which providers are available:
```json
{
  "status": "healthy",
  "groq_configured": true,
  "together_configured": true,
  "huggingface_configured": false,
  "ocr_ready": true
}
```

### Test Document Upload

1. Go to: https://nepali-doc-ai.vercel.app/
2. Upload a test image
3. Check logs to see which provider was used

Logs will show:
- `✅ Used Groq API` (if Groq worked)
- `✅ Used Together AI (fallback)` (if Groq failed, Together worked)
- `✅ Used Hugging Face (fallback)` (if both failed, HF worked)
- `❌ All LLM providers failed` (if all failed - need to add keys!)

---

## Cost Comparison

| Provider | Cost | Speed | Reliability | Free Forever? |
|----------|------|-------|-------------|---------------|
| **Groq** | FREE | ⚡⚡⚡ | ⭐⭐⭐ | Yes (with limits) |
| **Together AI** | $25 credit | ⚡⚡ | ⭐⭐⭐ | No (credit runs out) |
| **Hugging Face** | FREE | ⚡ | ⭐⭐ | Yes (unlimited) |

---

## Quick Start (Right Now)

### 1. Create Hugging Face Token (5 minutes - completely free)
- Go to: https://huggingface.co/settings/tokens
- Click "New token"
- Copy token (starts with `hf_...`)
- Add to HF Space secrets as `HUGGINGFACE_API_KEY`

This will get your app working immediately!

### 2. Later: Add Groq for Speed (5 minutes)
- Go to: https://console.groq.com
- Create account
- Get API key
- Add to HF Space as `GROQ_API_KEY`

Now you have fast primary + free fallback! 🎉

---

## Troubleshooting

### "All LLM providers failed"
- Check you added at least one key
- Verify key starts with correct prefix (`gsk_`, `hf_`, etc.)
- Check key is valid (try in provider's playground)

### "Groq organization restricted"
- Your Groq account was suspended
- Use Together AI or Hugging Face instead
- Or contact Groq support

### "Rate limit exceeded"
- You hit the free tier limit
- Wait a few minutes
- Or add another provider as fallback

### Slow responses
- Hugging Face is slower (5-10 sec)
- Add Groq or Together AI for faster responses
- Check your internet connection

---

## Summary

**Easiest setup (5 min)**: Just Hugging Face token
**Best setup (10 min)**: All three keys
**Fastest**: Groq (if not restricted)
**Completely free forever**: Hugging Face

Pick what works for you! The fallback system ensures your app keeps working even if one provider fails. 🚀

