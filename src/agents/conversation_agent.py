import os
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_response(conversation_history: list, user_message: str) -> str:
    try:
        messages = [{"role": "system", "content": "You are a fashion assistant in a group chat with other AI agents."}]
        messages.extend(conversation_history[-5:])
        messages.append({"role": "user", "content": user_message})
        
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        return "ConversationAgent: How can I help with your outfit today?"
