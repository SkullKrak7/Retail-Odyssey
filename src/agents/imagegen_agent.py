import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

_client = None

def get_client():
    global _client
    if _client is None:
        key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if key:
            _client = genai.Client(api_key=key)
    return _client

async def generate_outfit_image(description: str) -> str:
    """
    Generates outfit visualization images using Gemini 3 Pro Image.
    Creates realistic fashion photography with professional studio lighting.
    
    Returns base64-encoded image data for immediate display, or None if generation fails.
    """
    client = get_client()
    if not client:
        print("ImageGenAgent: No client configured")
        return None
    
    try:
        prompt = f"A realistic fashion photography shot of a mannequin wearing: {description}. Neutral studio background, professional lighting, high resolution."
        print(f"ImageGenAgent: Generating image...")
        
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents={"parts": [{"text": prompt}]}
        )
        
        # Extract image from response
        if response.candidates:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    import base64
                    img_data = base64.b64encode(part.inline_data.data).decode('utf-8')
                    print(f"ImageGenAgent: Generated {len(img_data)} chars")
                    return img_data
        
        print("ImageGenAgent: No image in response")
        return None
        
    except Exception as e:
        print(f"ImageGenAgent error: {e}")
        return None
