import asyncio
import time
from typing import List, Dict
from datetime import datetime

try:
    from .vision_agent import analyze_wardrobe
    from .recommendation_agent import recommend_outfit
    from .conversation_agent import generate_response
    from .imagegen_agent import generate_outfit_image
    from .intent_agent import parse_intent
    from ..utils.prometheus_metrics import agent_calls, total_requests, response_time
except ImportError:
    from vision_agent import analyze_wardrobe
    from recommendation_agent import recommend_outfit
    from conversation_agent import generate_response
    from imagegen_agent import generate_outfit_image
    from intent_agent import parse_intent
    try:
        from utils.prometheus_metrics import agent_calls, total_requests, response_time
    except:
        # Mock metrics if not available
        class MockMetric:
            def inc(self): pass
            def labels(self, **kwargs): return self
            def observe(self, val): pass
        agent_calls = total_requests = response_time = MockMetric()

class Message:
    def __init__(self, sender: str, content: str, timestamp: datetime = None, image_base64: str = None):
        self.sender = sender
        self.content = content
        self.timestamp = timestamp or datetime.now()
        self.image_base64 = image_base64

class GroupChatOrchestrator:
    """
    Coordinates multi-agent collaboration for fashion recommendations.
    
    Manages conversation flow between 5 specialized agents:
    - IntentAgent: Classifies user requests
    - VisionAgent: Analyzes wardrobe images
    - RecommendationAgent: Searches Frasers products
    - ConversationAgent: Maintains dialogue
    - ImageGenAgent: Generates outfit visualizations
    
    Maintains conversation history (last 20 messages) and tracks metrics via Prometheus.
    """
    def __init__(self):
        self.messages: List[Message] = []
        self.wardrobe_context = ""
        self.outfit_recommendation = ""
        self.user_preferences = {}
        self.conversation_state = "initial"
    
    async def process_message(self, user_message: str, image_url: str = None) -> List[Dict]:
        total_requests.inc()
        self.messages.append(Message("User", user_message))
        
        agent_conversation = []
        
        # Build full conversation context
        full_history = [{"role": m.sender, "content": m.content} for m in self.messages[-20:]]
        
        # Step 0: Parse intent using IntentAgent
        intent = await parse_intent(user_message, full_history)
        
        # IntentAgent announces its analysis
        intent_parts = []
        intent_parts.append(f"**Intent Classification**")
        intent_parts.append(f"- Primary Intent: {intent['primary_intent'].replace('_', ' ').title()}")
        intent_parts.append(f"- Occasion: {intent['occasion'].title()}")
        if intent.get('style_preference') != 'unknown':
            intent_parts.append(f"- Style: {intent['style_preference'].title()}")
        intent_parts.append(f"- Urgency: {intent['urgency'].title()}")
        
        actions = []
        if intent.get('needs_vision'): actions.append("Image Analysis")
        if intent.get('needs_recommendation'): actions.append("Outfit Recommendation")
        if intent.get('needs_image_gen'): actions.append("Visualization")
        if actions:
            intent_parts.append(f"- Actions: {', '.join(actions)}")
        
        intent_msg = "\n".join(intent_parts)
        intent_response = await self._agent_speak("IntentAgent", intent_msg)
        agent_conversation.append(intent_response)
        
        # Step 1: If image provided or vision needed, VisionAgent analyzes
        if image_url or intent.get("needs_vision"):
            if image_url:
                vision_response = await self._agent_speak("VisionAgent", 
                    f"Analyzing wardrobe for {intent['occasion']} occasion: {user_message}", image_url)
                agent_conversation.append(vision_response)
                self.wardrobe_context = vision_response["message"]
        
        # Step 2: If recommendation needed
        if intent.get("needs_recommendation"):
            # Include full conversation context
            context_summary = "\n".join([f"{m['role']}: {m['content'][:100]}" for m in full_history[-10:]])
            rec_context = f"CONVERSATION HISTORY:\n{context_summary}\n\nCURRENT REQUEST: {user_message}\nOccasion: {intent['occasion']}\nStyle: {intent['style_preference']}"
            if self.wardrobe_context:
                rec_context += f"\nWardrobe: {self.wardrobe_context}"
            
            rec_response = await self._agent_speak("RecommendationAgent", rec_context)
            agent_conversation.append(rec_response)
            self.outfit_recommendation = rec_response["message"]
            
            # ConversationAgent with full context
            conv_context = f"CONVERSATION:\n{context_summary}\n\nLATEST: User said '{user_message}'. Outfit suggested: {self.outfit_recommendation[:200]}. Continue the conversation naturally."
            conv_review = await self._agent_speak("ConversationAgent", conv_context)
            agent_conversation.append(conv_review)
        
        # Step 3: If visualization needed
        if intent.get("needs_image_gen"):
            description = self.outfit_recommendation if self.outfit_recommendation else user_message
            
            # ImageGenAgent generates
            img_response = await self._agent_speak("ImageGenAgent", description)
            agent_conversation.append(img_response)
        
        # Step 4: If no specific task, just conversation
        if len(agent_conversation) <= 1:  # Only IntentAgent spoke
            conv_response = await self._agent_speak("ConversationAgent", user_message)
            agent_conversation.append(conv_response)
        
        # Update conversation state
        self.conversation_state = intent['primary_intent']
        if intent.get('occasion') != 'unknown':
            self.user_preferences['last_occasion'] = intent['occasion']
        if intent.get('style_preference') != 'unknown':
            self.user_preferences['style'] = intent['style_preference']
        
        return agent_conversation
    
    async def _agent_speak(self, agent_name: str, message: str, image_url: str = None) -> Dict:
        start_time = time.time()
        agent_calls.labels(agent_name=agent_name).inc()
        
        history = [{"role": m.sender, "content": m.content} for m in self.messages[-10:]]
        
        result = ""
        image_base64 = None
        
        if agent_name == "IntentAgent":
            result = message
        elif agent_name == "VisionAgent" and image_url:
            result = await analyze_wardrobe(image_url, message)
        elif agent_name == "RecommendationAgent":
            # Pass full context including what other agents said
            context = f"{message}\n\nPrevious agent insights:\n"
            for msg in self.messages[-5:]:
                if msg.sender in ["VisionAgent", "IntentAgent"]:
                    context += f"{msg.sender}: {msg.content[:200]}\n"
            result = await recommend_outfit(context, self.wardrobe_context)
        elif agent_name == "ImageGenAgent":
            image_base64 = await generate_outfit_image(message)
            result = "I've generated a visual representation of the outfit."
        elif agent_name == "ConversationAgent":
            # Pass what other agents said in the prompt - include full agent messages
            full_history = []
            for msg in self.messages[-10:]:
                full_history.append({"role": msg.sender, "content": msg.content})
            result = await generate_response(full_history, message)
        
        msg = Message(agent_name, result, image_base64=image_base64)
        self.messages.append(msg)
        
        response_time.labels(agent_name=agent_name).observe(time.time() - start_time)
        
        return {
            "agent": agent_name,
            "message": result,
            "timestamp": msg.timestamp.isoformat(),
            "image_base64": image_base64
        }
    
    def get_conversation_history(self) -> List[Dict]:
        return [{"sender": m.sender, "content": m.content, "time": m.timestamp.isoformat()} 
                for m in self.messages]
    
    def clear_history(self):
        self.messages = []
        self.wardrobe_context = ""
        self.outfit_recommendation = ""
