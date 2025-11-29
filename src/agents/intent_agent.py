import os
from openai import AsyncOpenAI

def get_client():
    return AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY", "dummy-key"))

async def parse_intent(user_message: str) -> dict:
    if not os.getenv("OPENAI_API_KEY"):
        return {"intent": "casual_outfit", "occasion": "general", "raw": user_message}
    try:
        client = get_client()
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "system",
                "content": "Extract occasion, weather, style preference, formality from user request. Return JSON."
            }, {
                "role": "user",
                "content": user_message
            }],
            max_tokens=150
        )
        return {"intent": response.choices[0].message.content, "raw": user_message}
    except Exception as e:
        return {"intent": "casual_outfit", "occasion": "general", "raw": user_message}
