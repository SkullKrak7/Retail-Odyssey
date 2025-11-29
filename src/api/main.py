from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
from dotenv import load_dotenv
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
    responses = await orchestrator.process_message(request.message, request.image_url)
    formatted_responses = []
    
    for r in responses:
        response_data = {
            "agent": r.sender,
            "message": r.content,
            "time": r.timestamp.isoformat()
        }
        
        if r.content.startswith("IMAGE_URL:"):
            image_url = r.content.replace("IMAGE_URL:", "")
            response_data["image_url"] = image_url
            response_data["message"] = "Generated outfit visualization"
        
        formatted_responses.append(response_data)
    
    return {
        "responses": formatted_responses,
        "conversation": orchestrator.get_conversation_history()
    }

@app.get("/api/history")
async def get_history():
    return {"conversation": orchestrator.get_conversation_history()}

@app.get("/api/health")
async def health():
    return {"status": "healthy", "agents": ["VisionAgent", "RecommendationAgent", "ConversationAgent", "ImageGenAgent"]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
