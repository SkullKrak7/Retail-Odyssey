import os
from dotenv import load_dotenv
import google.generativeai as genai
from openai import AsyncOpenAI

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

async def recommend_outfit(user_request: str, wardrobe_context: str = "") -> str:
    """
    Recommend outfit using Gemini (FREE) or fallback to OpenAI
    """
    # Try Gemini first (FREE tier)
    if configure_gemini():
        try:
            model = genai.GenerativeModel("gemini-2.0-flash-exp")
            
            prompt = f"""You're a fashion stylist. Based on the context, suggest a specific outfit.

{user_request}

Wardrobe available: {wardrobe_context if wardrobe_context else "No wardrobe info provided"}

Give a concise outfit suggestion (200 words max) with main pieces and why it works."""
            
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "max_output_tokens": 1024,
                }
            )
            return response.text
            
        except Exception as e:
            print(f"Gemini recommendation error: {e}")
    
    # Fallback to OpenAI
    client = get_openai_client()
    if client:
        try:
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "system",
                    "content": "You are a fashion stylist. Suggest outfits based on occasion, weather, and available wardrobe."
                }, {
                    "role": "user",
                    "content": f"Request: {user_request}\nWardrobe: {wardrobe_context}\nSuggest an outfit."
                }]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI recommendation error: {e}")
    
    return "RecommendationAgent: Try pairing a blazer with dark jeans and boots (no API key configured)"
