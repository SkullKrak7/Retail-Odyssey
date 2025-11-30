from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
from dotenv import load_dotenv
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from .routers import router as metrics_router

load_dotenv()

app = FastAPI(title="RetailOdyssey", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(metrics_router, prefix="/api", tags=["metrics"])

from ..agents.group_chat_orchestrator import GroupChatOrchestrator

orchestrator = GroupChatOrchestrator()

class ChatRequest(BaseModel):
    message: str
    image_url: Optional[str] = None

@app.post("/api/chat")
async def chat(request: ChatRequest):
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
    orchestrator.clear_history()
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
