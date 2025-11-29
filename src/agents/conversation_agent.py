import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()
key = os.getenv("OPENAI_API_KEY")
if key:
    os.environ["OPENAI_API_KEY"] = key

def get_client():
    return AsyncOpenAI(api_key=key)

async def generate_response(conversation_history: list, user_message: str) -> str:
    if not key:
        return "ConversationAgent: How can I help with your outfit today? (demo mode)"
    try:
        client = get_client()
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
        return f"ConversationAgent: How can I help? (error: {str(e)[:50]})"
