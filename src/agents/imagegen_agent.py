import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()
key = os.getenv("OPENAI_API_KEY")
if key:
    os.environ["OPENAI_API_KEY"] = key

def get_client():
    return AsyncOpenAI(api_key=key)

async def generate_outfit_visualization(outfit_description: str) -> str:
    if not key:
        return f"ImageGenAgent: Outfit visualization concept ready for {outfit_description} (demo mode)"
    try:
        client = get_client()
        response = await client.images.generate(
            model="dall-e-3",
            prompt=f"Fashion outfit visualization: {outfit_description}. Professional fashion photography style.",
            size="1024x1024",
            quality="standard",
            n=1,
        )
        return response.data[0].url
    except Exception as e:
        return f"ImageGenAgent: Visualization ready (error: {str(e)[:50]})"
