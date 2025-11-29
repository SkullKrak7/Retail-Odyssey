import asyncio
import time
from typing import List, Dict
from datetime import datetime
from .vision_agent import analyze_wardrobe
from .recommendation_agent import recommend_outfit
from .intent_agent import parse_intent
from .conversation_agent import generate_response
from .imagegen_agent import generate_outfit_image
from ..utils.prometheus_metrics import agent_calls, total_requests, response_time

class Message:
    def __init__(self, sender: str, content: str, timestamp: datetime = None):
        self.sender = sender
        self.content = content
        self.timestamp = timestamp or datetime.now()

class GroupChatOrchestrator:
    def __init__(self):
        self.messages: List[Message] = []
        self.wardrobe_context = ""
    
    async def process_message(self, user_message: str, image_url: str = None) -> List[Message]:
        total_requests.inc()
        self.messages.append(Message("User", user_message))
        
        relevant_agents = self._identify_relevant_agents(user_message, image_url)
        
        # Auto-add ImageGenAgent if RecommendationAgent is triggered
        if "RecommendationAgent" in relevant_agents and "ImageGenAgent" not in relevant_agents:
            relevant_agents.append("ImageGenAgent")
        
        responses = []
        for agent_name in relevant_agents:
            response = await self._get_agent_response(agent_name, user_message, image_url)
            msg = Message(agent_name, response)
            self.messages.append(msg)
            responses.append(msg)
        
        return responses
    
    def _identify_relevant_agents(self, message: str, has_image: bool) -> List[str]:
        agents = []
        msg_lower = message.lower()
        
        if has_image or any(word in msg_lower for word in ["wardrobe", "clothes", "picture", "image", "wearing", "outfit"]):
            agents.append("VisionAgent")
        if "recommend" in msg_lower or "suggest" in msg_lower or "wear" in msg_lower:
            agents.append("RecommendationAgent")
        if any(word in msg_lower for word in ["generate", "create", "show", "visualize", "visual"]):
            agents.append("ImageGenAgent")
        if not agents:
            agents.append("ConversationAgent")
        
        return agents
    
    async def _get_agent_response(self, agent_name: str, message: str, image_url: str = None) -> str:
        start_time = time.time()
        agent_calls.labels(agent_name=agent_name).inc()
        
        history = [{"role": m.sender, "content": m.content} for m in self.messages[-5:]]
        
        result = ""
        if agent_name == "VisionAgent" and image_url:
            response = await analyze_wardrobe(image_url, message)
            self.wardrobe_context = response
            result = response
        elif agent_name == "RecommendationAgent":
            response = await recommend_outfit(message, self.wardrobe_context)
            result = response
        elif agent_name == "ImageGenAgent":
            outfit_desc = self.wardrobe_context or message
            image_data = await generate_outfit_image(outfit_desc)
            result = f"IMAGE_URL:{image_data}"
        elif agent_name == "ConversationAgent":
            result = await generate_response(history, message)
        else:
            result = f"{agent_name}: Processing your request..."
        
        response_time.labels(agent_name=agent_name).observe(time.time() - start_time)
        return result
    
    def get_conversation_history(self) -> List[Dict]:
        return [{"sender": m.sender, "content": m.content, "time": m.timestamp.isoformat()} 
                for m in self.messages]
