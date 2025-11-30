import os
import google.generativeai as genai
from openai import AsyncOpenAI

_gemini_configured = False
_openai_client = None

def configure_gemini():
    global _gemini_configured
    if not _gemini_configured:
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            _gemini_configured = True
    return _gemini_configured

def get_openai_client():
    global _openai_client
    if _openai_client is None:
        key = os.getenv("OPENAI_API_KEY")
        if key:
            _openai_client = AsyncOpenAI(api_key=key)
    return _openai_client

async def generate_response(conversation_history: list, user_message: str) -> str:
    """
    Generate conversational response using Gemini (FREE) or fallback to OpenAI
    """
    # Try Gemini first (FREE tier)
    if configure_gemini():
        try:
            model = genai.GenerativeModel("gemini-2.0-flash-exp")
            
            # Build conversation context
            context = "You're a fashion assistant helping the user. Read the full conversation and respond naturally to continue helping them. Build on what's already been discussed.\n\n"
            
            for msg in conversation_history[-10:]:
                role = msg["role"]
                content = msg["content"]
                context += f"{role}: {content}\n"
            
            context += f"\nUser: {user_message}\n\nYour response:"
            
            response = model.generate_content(
                context,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "max_output_tokens": 512,
                }
            )
            return response.text
            
        except Exception as e:
            print(f"Gemini conversation error: {e}")
    
    # Fallback to OpenAI
    client = get_openai_client()
    if client:
        try:
            messages = [
                {
                    "role": "system",
                    "content": "You are a friendly fashion assistant in a multi-agent chat. Help users with outfit advice, style tips, and fashion recommendations. Be conversational, helpful, and build on what other agents say."
                }
            ]
            
            for msg in conversation_history[-10:]:
                role = "assistant" if msg["role"] != "User" else "user"
                messages.append({"role": role, "content": msg["content"]})
            
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI conversation error: {e}")
    
    return "I'm here to help with fashion advice! Ask me anything about outfits, style, or trends. (no API key configured)"
