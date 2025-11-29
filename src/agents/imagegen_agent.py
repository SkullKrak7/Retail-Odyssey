import os
from openai import AsyncOpenAI

_client = None

def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            _client = AsyncOpenAI(api_key=api_key)
    return _client

async def generate_outfit_image(description: str) -> str:
    client = get_client()
    
    if not client:
        return "demo_mode:Image generation requires OpenAI API key"
    
    try:
        prompt = f"Professional fashion photography: {description}. Studio lighting, neutral background, high quality, detailed."
        
        response = await client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        
        return response.data[0].url
    except Exception as e:
        return f"demo_mode:Error generating image: {str(e)}"
