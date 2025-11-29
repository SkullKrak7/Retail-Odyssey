import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()
key = os.getenv("OPENAI_API_KEY")
if key:
    os.environ["OPENAI_API_KEY"] = key

def get_client():
    return AsyncOpenAI(api_key=key)

async def analyze_wardrobe(image_url: str, context: str = "") -> str:
    if not key:
        return "VisionAgent: Found casual shirts, jeans, jackets in wardrobe (demo mode)"
    try:
        client = get_client()
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": f"Analyze this wardrobe image. List clothing items, colors, and styles. {context}"},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }],
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"VisionAgent: Found casual shirts, jeans, jackets (error: {str(e)[:50]})"
