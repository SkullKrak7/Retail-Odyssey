# Retail Odyssey 🧭

**Your AI-Powered Style Journey**

A multi-agent AI system that guides users through their daily fashion odyssey - from morning classes to evening events, helping them navigate outfit transitions across different social contexts.

## The Journey Concept

Life is a journey with multiple destinations. Retail Odyssey recognizes that your style needs evolve throughout the day:
- 📚 Classes → 🍺 Pub → 🎬 Movie → 🎉 Nightclub
- 💼 Work → 🍽️ Dinner → 🎭 Theater
- ⚽ Gym → ☕ Coffee → 📅 Date

Our 5 specialized AI agents collaborate to guide you through every transition.

## Multi-Agent Architecture

### 1. **IntentAgent** 🎯
Classifies user intent and determines which agents to activate

### 2. **VisionAgent** 👁️
Analyzes uploaded wardrobe images to understand what you already own

### 3. **RecommendationAgent** 👔
Suggests outfits based on your journey, context, and wardrobe

### 4. **ConversationAgent** 💬
Maintains natural dialogue and asks clarifying questions

### 5. **ImageGenAgent** 🎨
Visualizes outfit recommendations using AI image generation

## Key Features

✅ **Context-Aware Recommendations**: Understands multi-destination journeys  
✅ **Real-Time Collaboration**: Agents share context and build on each other's insights  
✅ **Visual Feedback**: Generate outfit visualizations  
✅ **Wardrobe Analysis**: Upload images of your clothes for personalized advice  
✅ **Grafana Monitoring**: Real-time metrics on agent performance  

## Tech Stack

- **Backend**: FastAPI + Python
- **AI**: Google Gemini 2.0 (free tier) + OpenAI (fallback)
- **Frontend**: React + TypeScript + Vite
- **Monitoring**: Prometheus + Grafana
- **Deployment**: Docker (ARM-optimized for Apple Silicon)

## Quick Start

```bash
# Start all services
docker-compose up -d

# Access
Frontend: http://localhost:5173
Backend: http://localhost:8000
Grafana: http://localhost:3000 (admin/admin)
```

## Hackathon Challenges Addressed

### 🏆 Reply AI Agents Challenge
- ✅ Multi-agent group conversation design
- ✅ Targeted intent recognition
- ✅ Context management & attribution
- ✅ Asynchronous interaction & collaboration

### 🏆 Frasers Group Challenge
- ✅ Next-gen retail engagement
- ✅ Attracts Gen-Z with AI-powered personalization
- ✅ Solves real problem: outfit transitions across contexts

### 🏆 Grafana Challenge
- ✅ Real-time monitoring of agent performance
- ✅ Metrics on response times, usage patterns

### 🏆 Arm Challenge
- ✅ Dockerized for Apple Silicon (ARM architecture)

### 🏆 Best Representation of Theme (Odyssey)
- ✅ Literal journey through daily destinations
- ✅ Style evolution as you travel through your day

## Demo Scenario

**User**: "I have classes, then a pub meetup, then a movie"

**IntentAgent**: Classifies as multi-context outfit recommendation  
**VisionAgent**: (If image uploaded) Analyzes current wardrobe  
**RecommendationAgent**: Suggests versatile outfit with transition tips  
**ConversationAgent**: Asks about preferences and clarifies details  
**ImageGenAgent**: Generates visual of the recommended outfit  

## Metrics & Monitoring

View real-time agent performance in Grafana:
- Total requests processed
- Agent call distribution
- Response time per agent
- Requests per minute

## Team

Built at HackSheffield10 (Nov 29-30, 2025)

---

*"Every day is a journey. Let AI guide your style."* 🧭
