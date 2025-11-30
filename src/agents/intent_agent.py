import os
import json
import google.generativeai as genai
from openai import AsyncOpenAI
from typing import Dict, List

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

async def parse_intent(user_message: str, conversation_history: List[Dict] = None) -> Dict:
    """
    Parse user intent using Gemini (FREE) or fallback to OpenAI
    Returns: {
        "primary_intent": str,
        "needs_vision": bool,
        "needs_recommendation": bool,
        "needs_image_gen": bool,
        "occasion": str,
        "style_preference": str,
        "urgency": str
    }
    """
    # Try Gemini first (FREE tier)
    if configure_gemini():
        try:
            model = genai.GenerativeModel("gemini-2.0-flash-exp")
            
            context = ""
            if conversation_history:
                recent = conversation_history[-3:]
                context = "\n".join([f"{m['role']}: {m['content']}" for m in recent])
            
            prompt = f"""You are an intent classifier for a fashion AI system. Analyze the user's message and return ONLY a JSON object with this exact structure:

{{
    "primary_intent": "wardrobe_analysis" or "outfit_recommendation" or "style_advice" or "image_generation" or "general_chat",
    "needs_vision": true or false,
    "needs_recommendation": true or false,
    "needs_image_gen": true or false,
    "occasion": "casual" or "formal" or "business" or "party" or "date" or "workout" or "unknown",
    "style_preference": "classic" or "trendy" or "minimalist" or "bold" or "unknown",
    "urgency": "immediate" or "normal" or "planning"
}}

Rules:
- If user says "show", "visualize", "picture", "image", "see", "generate" → set needs_image_gen=true and primary_intent="image_generation"
- If user uploads image or asks "how does this look" → set needs_vision=true and primary_intent="wardrobe_analysis"
- If user asks for outfit advice → set needs_recommendation=true and primary_intent="outfit_recommendation"

Recent conversation:
{context}

New message: {user_message}

Return ONLY the JSON, no other text:"""
            
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.3,
                    "top_p": 0.95,
                    "max_output_tokens": 256,
                }
            )
            
            # Extract JSON from response
            text = response.text.strip()
            # Remove markdown code blocks if present
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            
            return json.loads(text)
            
        except Exception as e:
            print(f"Gemini intent parsing error: {e}")
    
    # Fallback to OpenAI
    client = get_openai_client()
    if client:
        try:
            context = ""
            if conversation_history:
                recent = conversation_history[-3:]
                context = "\n".join([f"{m['role']}: {m['content']}" for m in recent])
            
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "system",
                    "content": """You are an intent classifier for a fashion AI system. Analyze the user's message and return a JSON object with:
                    {
                        "primary_intent": "wardrobe_analysis" | "outfit_recommendation" | "style_advice" | "image_generation" | "general_chat",
                        "needs_vision": true/false,
                        "needs_recommendation": true/false,
                        "needs_image_gen": true/false,
                        "occasion": "casual" | "formal" | "business" | "party" | "date" | "workout" | "unknown",
                        "style_preference": "classic" | "trendy" | "minimalist" | "bold" | "unknown",
                        "urgency": "immediate" | "normal" | "planning"
                    }"""
                }, {
                    "role": "user",
                    "content": f"Recent conversation:\n{context}\n\nNew message: {user_message}\n\nClassify this intent:"
                }],
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"OpenAI intent parsing error: {e}")
    
    # Fallback to keyword-based intent
    return {
        "primary_intent": "general_chat",
        "needs_vision": "image" in user_message.lower() or "wardrobe" in user_message.lower(),
        "needs_recommendation": any(w in user_message.lower() for w in ["recommend", "suggest", "outfit", "wear"]),
        "needs_image_gen": any(w in user_message.lower() for w in ["show", "visualize", "generate", "create"]),
        "occasion": "casual",
        "style_preference": "unknown",
        "urgency": "normal"
    }
