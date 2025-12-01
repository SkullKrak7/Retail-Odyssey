import os
from dotenv import load_dotenv
import google.generativeai as genai
from openai import AsyncOpenAI
import requests
from PIL import Image
from io import BytesIO

load_dotenv()

_gemini_configured = False
_openai_client = None

def configure_gemini():
    global _gemini_configured
    if not _gemini_configured:
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            _gemini_configured = True
    return _gemini_configured

def get_openai_client():
    global _openai_client
    if _openai_client is None:
        key = os.getenv("OPENAI_API_KEY")
        if key:
            _openai_client = AsyncOpenAI(api_key=key)
    return _openai_client

async def analyze_wardrobe(image_url: str, context: str = "") -> str:
    """
    Analyzes wardrobe/outfit images using Gemini 3 Pro Vision.
    Supports both base64 data URLs and HTTP URLs.
    Falls back to OpenAI GPT-4o Vision if Gemini is unavailable.
    
    Returns detailed description of clothing items, colors, styles, and how they work together.
    """
    # Try Gemini first (FREE tier)
    if configure_gemini():
        try:
            # Handle base64 data URL or HTTP URL
            if image_url.startswith('data:image'):
                # Extract base64 data
                import base64
                header, encoded = image_url.split(',', 1)
                img_data = base64.b64decode(encoded)
                img = Image.open(BytesIO(img_data))
            else:
                # Download from URL
                response = requests.get(image_url)
                img = Image.open(BytesIO(response.content))
            
            # Use Gemini 2.0 Flash for vision (FREE)
            model = genai.GenerativeModel("gemini-3-pro-preview")
            
            prompt = f"Analyze this wardrobe/outfit image. Describe the clothing items, colors, style, and how they work together. Be specific. {context}"
            
            response = model.generate_content([prompt, img])
            return response.text
            
        except Exception as e:
            print(f"Gemini vision error: {e}")
    
    # Fallback to OpenAI GPT-4 Vision
    client = get_openai_client()
    if client:
        try:
            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"Analyze this wardrobe image. List clothing items, colors, and styles. {context}"},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI vision error: {e}")
    
    return "VisionAgent: Found casual shirts, jeans, jackets in wardrobe (no API key configured)"
