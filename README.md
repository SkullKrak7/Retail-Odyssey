# Retail Odyssey 🧭

**Your AI-Powered Style Journey with Real Product Recommendations**

A multi-agent AI system that guides users through their daily fashion odyssey, providing personalized outfit recommendations with **real products from Frasers Group** stores.

![Gemini 3 Pro](https://img.shields.io/badge/Gemini-3%20Pro-blue)
![Multi-Agent](https://img.shields.io/badge/Agents-5-green)
![Frasers Group](https://img.shields.io/badge/Frasers-Integrated-orange)

## 🎯 HackSheffield10 Challenges

This project addresses **5 different challenges**:

1. 🏆 **Reply AI Agents Challenge** - Multi-agent collaboration with context sharing
2. 🏆 **Frasers Group Challenge** - Real product recommendations from Frasers brands
3. 🏆 **Grafana Challenge** - Real-time monitoring dashboard
4. 🏆 **Arm Challenge** - Optimized for Raspberry Pi & Apple Silicon
5. 🏆 **Best Theme (Odyssey)** - Journey-based fashion guidance

## 🤖 The 5 AI Agents

### 1. **IntentAgent** 🎯
Classifies user intent and determines the journey path

### 2. **VisionAgent** 👁️
Analyzes uploaded wardrobe images using Gemini 3 Pro vision

### 3. **RecommendationAgent** 👔
**Searches Frasers Group websites** for real products with:
- Google Search grounding
- Real prices and product names
- Direct purchase links
- Sports Direct, House of Fraser, Flannels, USC, Jack Wills

### 4. **ConversationAgent** 💬
Maintains natural dialogue and builds on other agents' insights

### 5. **ImageGenAgent** 🎨
Generates outfit visualizations using Gemini 3 Pro Image

## 🛍️ Frasers Group Integration

**Real Product Grounding:**
- Searches only Frasers Group websites
- Returns actual products with prices
- Provides clickable purchase links
- Examples: Nike Revolution 7 (€55), Adidas Runfalcon 5

**Supported Brands:**
- Sports Direct (activewear, casual)
- House of Fraser (premium fashion)
- Flannels (luxury designer)
- USC (streetwear)
- Jack Wills (British heritage)

## 🚀 Quick Start

### Docker (Recommended)
```bash
docker-compose up -d
```

### Local Development
```bash
# Backend
cd retail_odyssey
source venv/bin/activate
python -m src.api.main

# Frontend
cd frontend
npm install
npm run dev
```

### Access
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Grafana Dashboard**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090

## 📊 Grafana Monitoring

**Access:** http://localhost:3000 (admin/admin)

Real-time metrics dashboard showing:
- Total requests processed
- Agent call distribution  
- Response time per agent
- Requests per minute
- Brand mentions tracking
- Competitor blocks count

**Metrics Endpoint:** http://localhost:8000/metrics

## 🥧 Raspberry Pi / ARM Deployment

### Quick Setup (Pi 4/5 or Apple Silicon)

```bash
# 1. Install Docker (if needed)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 2. Clone and run
git clone https://github.com/SkullKrak7/HackSheff10.git
cd HackSheff10
docker-compose -f docker-compose.arm.yml up -d
```

### Performance Notes
- **Pi 4 (4GB)**: All services run, image generation 10-15s
- **Pi 5 (8GB)**: Smooth performance, image generation 5-8s
- **Apple Silicon**: Native ARM64, full performance

### Optimization
```bash
# Monitor resources
docker stats

# View logs
docker-compose logs -f backend
```

## 💡 Key Features

✅ **Multi-Agent Collaboration** - Agents share context and build on each other's responses  
✅ **Real Product Search** - Google Search grounding for actual Frasers inventory  
✅ **Journey-Based UX** - Odyssey theme for multi-destination outfit planning  
✅ **Image Analysis** - Upload wardrobe photos for personalized advice  
✅ **Image Generation** - Visualize outfit recommendations  
✅ **Real-Time Monitoring** - Grafana dashboard for system observability  
✅ **ARM Optimized** - Runs on Raspberry Pi and Apple Silicon  

## 🛠️ Tech Stack

- **AI**: Google Gemini 3 Pro (latest model)
- **Backend**: FastAPI + Python
- **Frontend**: React + TypeScript + Vite
- **Monitoring**: Prometheus + Grafana
- **Deployment**: Docker + Docker Compose
- **Architecture**: Multi-agent orchestration

## 📝 Example Conversation

```
User: "I need outfit for funeral then party after"

IntentAgent: Classifies as multi-context recommendation
RecommendationAgent: Searches Frasers sites, finds:
  - Black midi dress from House of Fraser (£89)
  - Statement blazer from Flannels (£149)
  - Provides clickable purchase links
ConversationAgent: Asks about style preferences
ImageGenAgent: Generates outfit visualization
```

## 🎨 The Odyssey Concept

Life is a journey with multiple destinations. Retail Odyssey recognizes that your style needs evolve:
- 📚 Classes → 🍺 Pub → 🎬 Movie
- 💼 Work → 🍽️ Dinner → 🎭 Theater
- ⚽ Gym → ☕ Coffee → 📅 Date

Our AI agents guide you through every transition with appropriate outfit recommendations.

## 🏗️ Architecture

```
User → Frontend (React)
         ↓
    Backend API (FastAPI)
         ↓
    Orchestrator
    ├── IntentAgent (Gemini 3 Pro)
    ├── VisionAgent (Gemini 3 Pro)
    ├── RecommendationAgent (Gemini 2.5 Flash + Search)
    ├── ConversationAgent (Gemini 3 Pro)
    └── ImageGenAgent (Gemini 3 Pro Image)
         ↓
    Prometheus → Grafana
```

## 📦 Environment Setup

Create `.env` file:
```bash
GEMINI_API_KEY=your_key_here
OPENAI_API_KEY=your_fallback_key
```

## 🤝 Contributing

Built at HackSheffield10 (Nov 29-30, 2025)

## 📄 License

MIT License

---

**Powered by Google Gemini 3 Pro • Multi-Agent Collaboration • Frasers Group**

*"Every day is a journey. Let AI guide your style."* 🧭
