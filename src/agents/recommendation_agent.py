import os
from dotenv import load_dotenv
import google.generativeai as genai
from openai import AsyncOpenAI
from src.utils.prometheus_metrics import brand_mentions, product_recommendations

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
    Recommends outfits using Gemini 2.5 Flash with Google Search grounding.
    Searches exclusively on Frasers Group websites for real products.
    
    Features:
    - Restricts search to Frasers domains (sportsdirect.com, houseoffraser.co.uk, etc.)
    - Returns actual product names, prices, and clickable links
    - Tracks brand mentions and product recommendations via Prometheus
    - Adds inline citations to product pages when available
    - Falls back to OpenAI GPT-4o-mini if Gemini unavailable
    """
    if configure_gemini():
        try:
            from google import genai
            from google.genai import types
            
            client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"))
            
            grounding_tool = types.Tool(
                google_search=types.GoogleSearch()
            )
            
            config = types.GenerateContentConfig(
                tools=[grounding_tool],
                temperature=0.7,
                top_p=0.95,
                max_output_tokens=512,
            )
            
            prompt = f"""You are a fashion stylist for Frasers Group. ONLY recommend products available on these Frasers websites:

SEARCH ONLY THESE SITES:
- site:sportsdirect.com
- site:houseoffraser.co.uk
- site:flannels.com
- site:usc.co.uk
- site:jackwills.com

User request: {user_request}
Wardrobe: {wardrobe_context if wardrobe_context else "None"}

IMPORTANT RULES:
1. Search ONLY the Frasers sites listed above
2. If a product doesn't exist on Frasers sites, suggest the closest alternative that DOES exist
3. Recommend 2-3 real products with prices
4. If you can't find exact items, say "Frasers Group offers similar items like..." and suggest alternatives

Keep response under 150 words."""
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=config,
            )
            
            text = response.text
            
            # Track Frasers brand mentions
            frasers_brands = ['Sports Direct', 'House of Fraser', 'Flannels', 'USC', 'Jack Wills']
            for brand in frasers_brands:
                if brand.lower() in text.lower():
                    brand_mentions.labels(brand_name=brand).inc()
            
            # Track product recommendations (rough estimate by counting price mentions)
            import re
            price_count = len(re.findall(r'[£€$]\d+', text))
            if price_count > 0:
                product_recommendations.inc(price_count)
            
            # Check if grounding found Frasers products
            has_frasers_links = False
            if response.candidates and response.candidates[0].grounding_metadata:
                metadata = response.candidates[0].grounding_metadata
                
                if hasattr(metadata, 'grounding_chunks') and metadata.grounding_chunks:
                    # Check if any links are from Frasers domains
                    frasers_domains = ['sportsdirect.com', 'houseoffraser.co.uk', 'flannels.com', 'usc.co.uk', 'jackwills.com']
                    for chunk in metadata.grounding_chunks:
                        if hasattr(chunk, 'web') and chunk.web and hasattr(chunk.web, 'uri'):
                            if any(domain in chunk.web.uri for domain in frasers_domains):
                                has_frasers_links = True
                                break
                
                if has_frasers_links and hasattr(metadata, 'grounding_supports') and metadata.grounding_supports:
                    chunks = metadata.grounding_chunks
                    
                    # Sort by end_index descending to avoid shifting
                    sorted_supports = sorted(
                        metadata.grounding_supports,
                        key=lambda s: s.segment.end_index,
                        reverse=True
                    )
                    
                    for support in sorted_supports:
                        end_index = support.segment.end_index
                        if support.grounding_chunk_indices:
                            citation_links = []
                            for i in support.grounding_chunk_indices:
                                if i < len(chunks) and hasattr(chunks[i], 'web'):
                                    uri = chunks[i].web.uri
                                    # Only add Frasers links
                                    if any(domain in uri for domain in frasers_domains):
                                        citation_links.append(f"[Link]({uri})")
                            
                            if citation_links:
                                citation_string = " " + " ".join(citation_links)
                                text = text[:end_index] + citation_string + text[end_index:]
            
            # If no Frasers products found, add disclaimer
            if not has_frasers_links:
                text += "\n\n*Note: Visit Frasers Group stores (Sports Direct, House of Fraser, Flannels, USC, Jack Wills) to find similar items.*"
            
            return text
            
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
