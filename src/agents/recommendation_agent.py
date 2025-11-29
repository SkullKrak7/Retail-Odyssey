import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()
key = os.getenv("OPENAI_API_KEY")
if key:
    os.environ["OPENAI_API_KEY"] = key

def get_client():
    return AsyncOpenAI(api_key=key)

async def recommend_outfit(user_request: str, wardrobe_context: str = "") -> str:
    if not key:
        return "RecommendationAgent: Try pairing a blazer with dark jeans and boots (demo mode)"
    try:
        client = get_client()
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "system",
                "content": "You are a fashion stylist. Suggest outfits based on occasion, weather, and available wardrobe."
            }, {
                "role": "user",
                "content": f"Request: {user_request}\nWardrobe: {wardrobe_context}\nSuggest an outfit."
            }],
            max_tokens=200
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"RecommendationAgent: Try pairing a blazer with dark jeans (error: {str(e)[:50]})"
