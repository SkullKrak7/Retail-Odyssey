import os
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY", "dummy-key"))

async def recommend_outfit(user_request: str, wardrobe_context: str = "") -> str:
    if not os.getenv("OPENAI_API_KEY"):
        return "RecommendationAgent: Try pairing a blazer with dark jeans and boots (demo mode)"
    try:
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
        return "RecommendationAgent: Try pairing a blazer with dark jeans and boots (demo mode)"
