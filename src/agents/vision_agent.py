import os
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY", "dummy-key"))

async def analyze_wardrobe(image_url: str, context: str = "") -> str:
    if not os.getenv("OPENAI_API_KEY"):
        return "VisionAgent: Found casual shirts, jeans, jackets in wardrobe (demo mode)"
    try:
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
        return "VisionAgent: Found casual shirts, jeans, jackets in wardrobe (demo mode)"
