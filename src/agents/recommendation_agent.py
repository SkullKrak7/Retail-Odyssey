import os
from dotenv import load_dotenv
import google.generativeai as genai
from openai import AsyncOpenAI

load_dotenv()

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

async def recommend_outfit(user_request: str, wardrobe_context: str = "") -> str:
    """
    Recommend outfit using Gemini with real Frasers product grounding
    """
    if configure_gemini():
        try:
            model = genai.GenerativeModel(
                "gemini-3-pro-preview",
                tools=[{"google_search": {}}]  # Enable search grounding
            )
            
            prompt = f"""You're a fashion stylist. Search for REAL products available on Frasers Group websites and recommend them.

**Search these sites for actual products:**
- sportsdirect.com (activewear, casual)
- houseoffraser.co.uk (premium fashion)
- flannels.com (designer brands)
- usc.co.uk (streetwear)
- jackwills.com (British style)

**User Request:** {user_request}
**Available Wardrobe:** {wardrobe_context if wardrobe_context else "None"}

**Your Response Must:**
1. Search for 2-3 REAL products with prices
2. Provide specific product names and brands
3. Mention which Frasers site to buy from
4. Keep under 150 words

Format example:
"Nike Air Max 90 (£89.99) from Sports Direct
Ted Baker Blazer (£199) from House of Fraser"

Search now and recommend real products."""
            
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "max_output_tokens": 512,
                }
            )
            
            result = response.text
            
            # Extract grounding metadata if available
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata:
                    if hasattr(candidate.grounding_metadata, 'grounding_chunks'):
                        result += "\n\n**🔗 Product Links:**"
                        for chunk in candidate.grounding_metadata.grounding_chunks[:5]:
                            if hasattr(chunk, 'web') and chunk.web:
                                title = chunk.web.title if hasattr(chunk.web, 'title') else 'Product'
                                uri = chunk.web.uri if hasattr(chunk.web, 'uri') else ''
                                if uri:
                                    result += f"\n- [{title}]({uri})"
            
            return result
            
        except Exception as e:
            print(f"Gemini recommendation error: {e}")
    
    # Fallback to OpenAI
    client = get_openai_client()
    if client:
        try:
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "system",
                    "content": "You are a fashion stylist. Suggest outfits based on occasion, weather, and available wardrobe."
                }, {
                    "role": "user",
                    "content": f"Request: {user_request}\nWardrobe: {wardrobe_context}\nSuggest an outfit."
                }]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI recommendation error: {e}")
    
    return "RecommendationAgent: Try pairing a blazer with dark jeans and boots (no API key configured)"
