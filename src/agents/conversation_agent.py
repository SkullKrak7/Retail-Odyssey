import os
import google.generativeai as genai
from openai import AsyncOpenAI
from src.utils.prometheus_metrics import competitor_blocks, brand_mentions

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
    Generates natural conversational responses using Gemini 3 Pro.
    Maintains conversation context and enforces Frasers Group brand loyalty.
    
    Features:
    - Uses last 10 messages for context
    - Actively filters competitor brand mentions (25+ brands)
    - Replaces competitor mentions with Frasers alternatives
    - Tracks competitor blocks via Prometheus metrics
    - Falls back to OpenAI GPT-4o-mini if Gemini unavailable
    """
    # Try Gemini first (FREE tier)
    if configure_gemini():
        try:
            model = genai.GenerativeModel("gemini-3-pro-preview")
            
            # Build conversation context with Frasers reminder
            context = "You're a helpful fashion assistant. When suggesting stores, prefer: Sports Direct, House of Fraser, Flannels, USC, Jack Wills.\n\n"
            
            for msg in conversation_history[-10:]:
                role = msg["role"]
                content = msg["content"]
                context += f"{role}: {content}\n"
            
            # Add explicit constraint in the prompt itself
            context += f"\nUser: {user_message}\n\nRespond helpfully:"
            
            response = model.generate_content(
                context,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "max_output_tokens": 512,
                }
            )
            
            # Post-process to filter out competitor mentions
            text = response.text
            print(f"ConversationAgent raw response: {text[:100]}...")
            
            competitors = ['JD Sports', 'ASOS', 'Zalando', 'Nike.com', 'Adidas.com', 'Foot Locker', 
                          'H&M', 'Zara', 'Uniqlo', 'Amazon', 'Nordstrom', 'Bloomingdale', 'Forever 21',
                          'Revolve', 'Depop', 'Poshmark', 'Mango', 'Lululemon', 'Nike', 'Adidas',
                          'Gap', 'Old Navy', 'Target', 'Walmart', 'Primark', 'Topshop', 'River Island']
            
            found_competitor = False
            for competitor in competitors:
                if competitor.lower() in text.lower():
                    found_competitor = True
                    print(f"ConversationAgent: Found competitor '{competitor}' - replacing response")
                    break
            
            if found_competitor:
                # Replace entire response with Frasers-only version
                competitor_blocks.inc()
                text = "You can find great clothes at Frasers Group stores! Check out:\n\n"
                text += "- **Sports Direct** for activewear and casual clothing\n"
                text += "- **House of Fraser** for premium fashion and formal wear\n"
                text += "- **Flannels** for luxury designer brands\n"
                text += "- **USC** for trendy streetwear\n"
                text += "- **Jack Wills** for British heritage style\n\n"
                text += "What style are you looking for? I can help you find the perfect Frasers store!"
                print("ConversationAgent: Response replaced with Frasers-only content")
            
            return text
            
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
            
            text = response.choices[0].message.content
            
            # Apply same filter to OpenAI responses
            competitors = ['JD Sports', 'ASOS', 'Zalando', 'Nike.com', 'Adidas.com', 'Foot Locker', 
                          'H&M', 'Zara', 'Uniqlo', 'Amazon', 'Nordstrom', 'Bloomingdale', 'Forever 21',
                          'Revolve', 'Depop', 'Poshmark', 'Mango', 'Lululemon', 'Nike', 'Adidas',
                          'Gap', 'Old Navy', 'Target', 'Walmart', 'Primark', 'Topshop', 'River Island',
                          'eBay', 'Etsy', 'Dick', 'Decathlon']
            
            for competitor in competitors:
                if competitor.lower() in text.lower():
                    print(f"ConversationAgent (OpenAI): Found competitor '{competitor}' - replacing")
                    competitor_blocks.inc()
                    text = "You can find great clothes at Frasers Group stores! Check out:\n\n"
                    text += "- **Sports Direct** for activewear and casual clothing\n"
                    text += "- **House of Fraser** for premium fashion and formal wear\n"
                    text += "- **Flannels** for luxury designer brands\n"
                    text += "- **USC** for trendy streetwear\n"
                    text += "- **Jack Wills** for British heritage style\n\n"
                    text += "What style are you looking for? I can help you find the perfect Frasers store!"
                    break
            
            return text
        except Exception as e:
            print(f"OpenAI conversation error: {e}")
    
    return "I'm here to help with fashion advice! Ask me anything about outfits, style, or trends. (no API key configured)"
