"""
ConversationAgent: Orchestrates the multi-agent graph workflow
Handles user interaction and coordinates vision, intent, recommendation, and image generation agents
Optimized for Google Gemini
"""

import os
import sys
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging
import json

# Configure logging FIRST
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add project root to path to fix imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import your other agents (with proper error handling)
try:
    from src.agents.vision_agent import VisionAgent
except (ImportError, ModuleNotFoundError):
    logger.warning("VisionAgent not found - using placeholder")
    VisionAgent = None

try:
    from src.agents.intent_agent import IntentAgent
except (ImportError, ModuleNotFoundError):
    logger.warning("IntentAgent not found - using placeholder")
    IntentAgent = None

try:
    from src.agents.recommendation_agent import RecommendationAgent
except (ImportError, ModuleNotFoundError):
    logger.warning("RecommendationAgent not found - using placeholder")
    RecommendationAgent = None

try:
    from src.agents.imagegen_agent import ImageGenAgent
except (ImportError, ModuleNotFoundError):
    logger.warning("ImageGenAgent not found - using placeholder")
    ImageGenAgent = None


# System Prompt - This guides the AI's behavior
SYSTEM_PROMPT = """
You are an AI Wardrobe Assistant that helps users choose the perfect outfit based on their wardrobe, events, weather, mood, and style preferences.

## Your Capabilities:
1. **Vision Analysis** - You can analyze uploaded wardrobe photos to detect clothing items, colors, and styles
2. **Intent Understanding** - You interpret user requirements including events, mood, weather conditions, and preferences
3. **Smart Matching** - You combine detected wardrobe items with user requirements to create perfect outfit combinations
4. **Visual Generation** - You can generate outfit preview images to help users visualize combinations
5. **Conversational Refinement** - You engage in natural dialogue to refine and improve recommendations

## How to Interact with Users:

### Understanding User Requests:
Users may ask about:
- **Event-based needs**: "What should I wear to a job interview?", "I have a wedding this weekend"
- **Weather considerations**: "It's raining outside", "Something for 25°C weather"
- **Mood and style**: "I want to look professional but approachable", "Something trendy and confident"
- **Specific requirements**: "Show me outfits using my blue jacket", "I need layers I can remove"

### Your Response Strategy:
1. **Acknowledge the request** warmly and professionally
2. **Ask clarifying questions** if needed (but don't overwhelm - max 2-3 questions):
   - Event details (formal/casual, indoor/outdoor)
   - Weather conditions (if not specified)
   - Style preferences or mood
   - Any clothing items they want to feature or avoid
3. **Analyze the wardrobe** using the vision agent
4. **Generate recommendations** that match their needs
5. **Provide visual previews** when helpful
6. **Iterate based on feedback**

### Communication Style:
- Be friendly, conversational, and helpful
- Use natural language, avoid being overly technical
- Show enthusiasm about fashion and styling
- Be concise but informative
- Respect user preferences and constraints
- Offer 2-3 outfit options when possible, not just one

### Example Interactions:

**User:** "What should I wear to a job interview?"
**You:** "I'd love to help you make a great first impression! To give you the best recommendation, could you tell me:
- What industry/role is the interview for?
- What's the weather like today?
- Do you prefer a more traditional or modern professional look?"

**User:** "I have a first date tonight at a nice restaurant. The weather is mild, around 18°C. I want to look elegant but not overdressed."
**You:** "Perfect! A first date at a nice restaurant - let me help you create an elegant yet approachable look. Let me analyze your wardrobe...

[After vision analysis]

Based on your wardrobe, I'd suggest these combinations:
1. [Specific outfit recommendation with reasoning]
2. [Alternative option]

Would you like to see visual previews of these outfits, or would you like me to adjust any of these suggestions?"

### Handling Different Scenarios:

**Incomplete Information:**
- Politely ask for missing details
- Make reasonable assumptions when appropriate
- Offer options that cover different possibilities

**Weather Integration:**
- Always consider comfort and practicality
- Suggest layering options for variable weather
- Mention fabric breathability for hot weather
- Recommend warm, insulated pieces for cold weather

**Style Guidance:**
- Explain WHY certain combinations work (colors, proportions, occasion-appropriateness)
- Educate users about styling principles when relevant
- Respect personal style while offering gentle suggestions
- Celebrate their existing wardrobe pieces

**No Perfect Match:**
- Be honest but constructive
- Suggest the closest available options
- Explain what's missing and why
- Offer creative alternatives or styling tricks

### Multi-Agent Coordination:
You orchestrate multiple specialized agents:
- **VisionAgent**: For clothing detection and analysis
- **IntentAgent**: For parsing user requirements
- **RecommendationAgent**: For matching items to needs
- **ImageGenAgent**: For generating outfit visualizations

Coordinate these agents seamlessly without exposing technical details to the user.

### Important Guidelines:
- ALWAYS consider the user's uploaded wardrobe - don't recommend items they don't have
- Prioritize practicality alongside style
- Be inclusive and body-positive in all recommendations
- Respect cultural and personal clothing preferences
- Maintain privacy - never store or share personal wardrobe information
- If you can't help with something, explain clearly and offer alternatives

### Error Handling:
- If wardrobe photos are unclear, politely ask for better images
- If no suitable outfit exists, be honest and suggest alternatives
- If technical issues occur, acknowledge them gracefully and offer to try again

Remember: Your goal is to make users feel confident, stylish, and prepared for any occasion using their existing wardrobe!
"""


@dataclass
class ConversationState:
    """Tracks the state of the conversation"""
    user_message: str
    wardrobe_items: List[Dict] = None
    user_intent: Dict = None
    recommendations: List[Dict] = None
    generated_images: List[str] = None
    conversation_history: List[Dict] = None
    
    def __post_init__(self):
        if self.wardrobe_items is None:
            self.wardrobe_items = []
        if self.conversation_history is None:
            self.conversation_history = []


class ConversationAgent:
    """
    Main orchestrator for the multi-agent wardrobe assistant system.
    Coordinates vision, intent, recommendation, and image generation agents.
    Optimized for Google Gemini.
    """
    
    def __init__(self, llm_client=None, api_key: Optional[str] = None, model: str = "gemini-1.5-pro"):
        """
        Initialize the conversation agent with sub-agents
        
        Args:
            llm_client: The Gemini GenerativeModel instance
            api_key: Google API key (optional, can use env var)
            model: Gemini model to use (default: gemini-1.5-pro)
        """
        self.system_prompt = SYSTEM_PROMPT
        self.llm_client = llm_client
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.model = model
        
        # Initialize Gemini if not provided
        if not self.llm_client and self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.llm_client = genai.GenerativeModel(
                    model_name=self.model,
                    system_instruction=self.system_prompt
                )
                logger.info(f"✅ Initialized Gemini with model: {self.model}")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini: {e}")
                self.llm_client = None
        
        # Log which LLM is being used
        if self.llm_client:
            logger.info(f"✅ Using Gemini with model: {self.model}")
            logger.info(f"✅ LLM Client Type: {type(self.llm_client).__name__}")
        else:
            logger.warning("⚠️ No LLM client provided - using fallback responses")
        
        # Initialize sub-agents
        try:
            self.vision_agent = VisionAgent() if VisionAgent else None
            self.intent_agent = IntentAgent(llm_client=llm_client) if IntentAgent else None
            self.recommendation_agent = RecommendationAgent(llm_client=llm_client) if RecommendationAgent else None
            self.imagegen_agent = ImageGenAgent() if ImageGenAgent else None
            
            if not any([self.vision_agent, self.intent_agent, self.recommendation_agent, self.imagegen_agent]):
                logger.warning("⚠️ No sub-agents loaded - conversation agent will work in standalone mode")
            else:
                logger.info("✅ Sub-agents initialized successfully")
        except Exception as e:
            logger.warning(f"⚠️ Some sub-agents failed to initialize: {e}")
            # Create placeholder agents for testing
            self.vision_agent = None
            self.intent_agent = None
            self.recommendation_agent = None
            self.imagegen_agent = None
        
        # Conversation state
        self.current_state = None
        
        logger.info("✅ ConversationAgent initialized successfully")
    
    
    def process_message(
        self, 
        user_message: str, 
        wardrobe_images: Optional[List[str]] = None,
        conversation_history: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Process a user message through the multi-agent workflow
        
        Args:
            user_message: The user's text input
            wardrobe_images: List of image paths/URLs of wardrobe items
            conversation_history: Previous conversation context
            
        Returns:
            Dict containing the response and metadata
        """
        try:
            logger.info(f"Processing user message: {user_message[:50]}...")
            
            # Initialize conversation state
            self.current_state = ConversationState(
                user_message=user_message,
                conversation_history=conversation_history or []
            )
            
            # Step 1: Vision Analysis (if wardrobe images provided)
            if wardrobe_images and self.vision_agent:
                logger.info("Running vision analysis...")
                try:
                    self.current_state.wardrobe_items = self.vision_agent.analyze_wardrobe(
                        wardrobe_images
                    )
                except Exception as e:
                    logger.error(f"Vision analysis error: {e}")
                    self.current_state.wardrobe_items = []
            
            # Step 2: Intent Understanding
            if self.intent_agent:
                logger.info("Parsing user intent...")
                try:
                    self.current_state.user_intent = self.intent_agent.parse_intent(
                        user_message,
                        conversation_history=self.current_state.conversation_history
                    )
                except Exception as e:
                    logger.error(f"Intent parsing error: {e}")
                    self.current_state.user_intent = {"raw_message": user_message}
            
            # Step 3: Generate Recommendations
            if self.recommendation_agent and self.current_state.wardrobe_items:
                logger.info("Generating outfit recommendations...")
                try:
                    self.current_state.recommendations = self.recommendation_agent.recommend(
                        wardrobe_items=self.current_state.wardrobe_items,
                        user_intent=self.current_state.user_intent
                    )
                except Exception as e:
                    logger.error(f"Recommendation error: {e}")
                    self.current_state.recommendations = []
            
            # Step 4: Generate Response
            response = self._generate_response()
            
            # Step 5: (Optional) Generate outfit visualizations
            if self._should_generate_images() and self.imagegen_agent:
                logger.info("Generating outfit visualizations...")
                try:
                    self.current_state.generated_images = self.imagegen_agent.generate(
                        outfit_descriptions=self.current_state.recommendations
                    )
                    response["images"] = self.current_state.generated_images
                except Exception as e:
                    logger.error(f"Image generation error: {e}")
            
            # Update conversation history
            self._update_conversation_history(user_message, response)
            
            logger.info("✅ Message processing complete")
            return response
            
        except Exception as e:
            logger.error(f"❌ Error processing message: {str(e)}")
            return {
                "response": "I apologize, but I encountered an error processing your request. Could you please try rephrasing your question?",
                "error": str(e),
                "recommendations": [],
                "intent": {},
                "wardrobe_items_count": 0
            }
    
    
    def _generate_response(self) -> Dict[str, Any]:
        """
        Generate a natural language response based on the current state
        
        Returns:
            Dict with response text and metadata
        """
        # Build context for LLM
        context = self._build_context()
        
        # Generate response using Gemini
        if self.llm_client:
            response_text = self._call_llm_gemini()
        else:
            response_text = self._generate_fallback_response()
        
        return {
            "response": response_text,
            "recommendations": self.current_state.recommendations or [],
            "intent": self.current_state.user_intent or {},
            "wardrobe_items_count": len(self.current_state.wardrobe_items) if self.current_state.wardrobe_items else 0
        }
    
    
    def _call_llm_gemini(self) -> str:
        """
        Call Gemini API to generate a response
        Optimized for Gemini 1.5 Pro
        
        Returns:
            Generated response text
        """
        try:
            # Build conversation history for Gemini
            chat_history = []
            
            # Add conversation history (Gemini format)
            if self.current_state.conversation_history:
                for msg in self.current_state.conversation_history[-6:]:  # Last 3 exchanges
                    role = "user" if msg["role"] == "user" else "model"
                    chat_history.append({
                        "role": role,
                        "parts": [msg["content"]]
                    })
            
            # Build current context and user message
            context = self._build_context()
            user_prompt = f"""
Context:
{context}

User Request: {self.current_state.user_message}

Please provide a helpful, friendly response with outfit recommendations if applicable.
"""
            
            # Start chat session with history
            logger.info(f"Calling Gemini API with model: {self.model}")
            chat = self.llm_client.start_chat(history=chat_history)
            
            # Generate response
            response = chat.send_message(
                user_prompt,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "top_k": 40,
                    "max_output_tokens": 1000,
                }
            )
            
            response_text = response.text
            
            # Log usage (if available)
            if hasattr(response, 'usage_metadata'):
                logger.info(f"Gemini API call successful - Tokens: {response.usage_metadata}")
            else:
                logger.info("Gemini API call successful")
            
            return response_text
            
        except Exception as e:
            logger.error(f"Error calling Gemini API: {str(e)}")
            return self._generate_fallback_response()
    
    
    def _build_context(self) -> str:
        """Build context string from current state"""
        context_parts = []
        
        if self.current_state.wardrobe_items:
            context_parts.append(f"Wardrobe Analysis: {len(self.current_state.wardrobe_items)} items detected")
            context_parts.append(f"Items:\n{self._format_wardrobe_items()}")
        else:
            context_parts.append("Wardrobe: No images provided yet")
        
        if self.current_state.user_intent:
            intent_str = json.dumps(self.current_state.user_intent, indent=2)
            context_parts.append(f"User Intent:\n{intent_str}")
        
        if self.current_state.recommendations:
            context_parts.append(f"\nRecommendations Generated: {len(self.current_state.recommendations)} outfits")
            context_parts.append("Recommendations:")
            for i, rec in enumerate(self.current_state.recommendations[:3], 1):
                context_parts.append(f"  {i}. {rec.get('description', 'Outfit option')}")
        
        return "\n".join(context_parts)
    
    
    def _format_wardrobe_items(self) -> str:
        """Format wardrobe items for context"""
        if not self.current_state.wardrobe_items:
            return "No items detected"
        
        items_summary = []
        for i, item in enumerate(self.current_state.wardrobe_items[:15], 1):  # Limit to first 15
            items_summary.append(
                f"  {i}. {item.get('type', 'item')}: "
                f"{item.get('color', 'unknown color')}, "
                f"{item.get('style', 'casual')}"
            )
        
        if len(self.current_state.wardrobe_items) > 15:
            items_summary.append(f"  ... and {len(self.current_state.wardrobe_items) - 15} more items")
        
        return "\n".join(items_summary)
    
    
    def _generate_fallback_response(self) -> str:
        """Generate a fallback response when LLM is not available"""
        if not self.current_state.wardrobe_items:
            return "I'd love to help you choose an outfit! Please upload photos of your wardrobe so I can make personalized recommendations based on your request."
        
        if not self.current_state.recommendations:
            return f"I've analyzed your wardrobe ({len(self.current_state.wardrobe_items)} items detected) but need a bit more information. What's the occasion, and what's the weather like?"
        
        response = "Based on your request and wardrobe, here are some outfit suggestions:\n\n"
        for i, rec in enumerate(self.current_state.recommendations[:3], 1):
            response += f"{i}. {rec.get('description', 'Outfit option')}\n"
            if rec.get('reasoning'):
                response += f"   Why: {rec.get('reasoning')}\n"
        
        response += "\nWould you like me to adjust any of these suggestions?"
        
        return response
    
    
    def _should_generate_images(self) -> bool:
        """Determine if outfit visualizations should be generated"""
        # Generate images if we have recommendations and user seems to want visuals
        keywords = ["show", "see", "visual", "picture", "image", "look like", "preview", "display"]
        user_wants_visuals = any(kw in self.current_state.user_message.lower() for kw in keywords)
        
        has_recommendations = bool(self.current_state.recommendations)
        
        return has_recommendations and user_wants_visuals
    
    
    def _update_conversation_history(self, user_message: str, response: Dict):
        """Update conversation history with latest exchange"""
        if not self.current_state.conversation_history:
            self.current_state.conversation_history = []
            
        self.current_state.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        self.current_state.conversation_history.append({
            "role": "assistant",
            "content": response["response"]
        })
        
        # Keep only last 10 messages (5 exchanges) to avoid token limits
        if len(self.current_state.conversation_history) > 10:
            self.current_state.conversation_history = self.current_state.conversation_history[-10:]
    
    
    def reset_conversation(self):
        """Reset conversation state for a new session"""
        self.current_state = None
        logger.info("Conversation state reset")
    
    
    def get_conversation_history(self) -> List[Dict]:
        """Get the current conversation history"""
        if self.current_state and self.current_state.conversation_history:
            return self.current_state.conversation_history
        return []


# Example usage
if __name__ == "__main__":
    import google.generativeai as genai
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Initialize Gemini
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)
    
    # Initialize conversation agent
    agent = ConversationAgent(api_key=api_key, model="gemini-1.5-pro")
    
    # Example interaction
    print("Testing ConversationAgent with Gemini...\n")
    
    response = agent.process_message(
        user_message="What should I wear to a job interview tomorrow? It's going to be about 20°C and sunny.",
        wardrobe_images=None  # In real usage, provide image paths here
    )
    
    print("Assistant:", response["response"])
    print("\nIntent:", response["intent"])
    print("Wardrobe items:", response["wardrobe_items_count"])