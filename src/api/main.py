"""
Retail Odyssey - FastAPI Backend

Multi-agent AI fashion assistant with real-time product recommendations.
Provides REST API for frontend communication and Prometheus metrics endpoint.

Endpoints:
- POST /api/chat: Send message to multi-agent system
- GET /api/history: Retrieve conversation history
- POST /api/clear: Clear conversation and start new session
- GET /api/health: Health check
- GET /metrics: Prometheus metrics for Grafana
"""

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
from dotenv import load_dotenv
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from ..utils.prometheus_metrics import user_sessions, messages_per_session

load_dotenv()

app = FastAPI(title="RetailOdyssey", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from ..agents.group_chat_orchestrator import GroupChatOrchestrator

orchestrator = GroupChatOrchestrator()
session_message_count = 0

class ChatRequest(BaseModel):
    message: str
    image_url: Optional[str] = None

@app.post("/api/chat")
async def chat(request: ChatRequest):
    global session_message_count
    session_message_count += 1
    
    agent_conversation = await orchestrator.process_message(request.message, request.image_url)
    
    return {
        "responses": agent_conversation,
        "conversation": orchestrator.get_conversation_history()
    }

@app.get("/api/history")
async def get_history():
    return {"conversation": orchestrator.get_conversation_history()}

@app.post("/api/clear")
async def clear_history():
    global session_message_count
    
    # Track session metrics
    if session_message_count > 0:
        messages_per_session.observe(session_message_count)
        user_sessions.inc()
    
    orchestrator.clear_history()
    session_message_count = 0
    return {"status": "cleared"}

@app.get("/api/health")
async def health():
    return {"status": "healthy", "agents": ["IntentAgent", "VisionAgent", "RecommendationAgent", "ConversationAgent", "ImageGenAgent"]}

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint for Grafana"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
