import os
import base64
import io
from google import genai

_client = None

def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            _client = genai.Client(api_key=api_key)
    return _client

async def generate_outfit_image(description: str) -> str:
    client = get_client()
    
    if not client:
        return ""
    
    try:
        prompt = f"Professional fashion photography of a mannequin wearing: {description}. Studio lighting, neutral background, fashion retail display style."
        
        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=[prompt]
        )
        
        for part in response.parts:
            if part.inline_data is not None:
                image = part.as_image()
                buffered = io.BytesIO()
                image.save(buffered, format="JPEG")
                return base64.b64encode(buffered.getvalue()).decode()
        
        return ""
    except Exception as e:
        print(f"Image generation error: {e}")
        return ""
