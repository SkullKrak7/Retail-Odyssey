# Retail Odyssey

**AI-Powered Multi-Agent Fashion Assistant with Real-Time Product Recommendations**

**Winner: Best use of AI Agents on Arm** - HackSheffield10 (November 2025)

A sophisticated multi-agent AI system that provides personalized fashion recommendations through collaborative agent intelligence, featuring real product search from Frasers Group stores, real-time monitoring, and ARM-optimized deployment.

![Gemini 3 Pro](https://img.shields.io/badge/Gemini-3%20Pro-blue)
![Multi-Agent](https://img.shields.io/badge/Agents-5-green)
![Frasers Group](https://img.shields.io/badge/Frasers-Integrated-orange)
![ARM64](https://img.shields.io/badge/ARM64-Optimized-red)

---

## Built With

This project was developed using:
- **[Kiro CLI](https://aws.amazon.com/q/developer/)** - AWS AI-powered development assistant
- **[Perplexity](https://www.perplexity.ai/)** - Research and information gathering
- **[Claude Sonnet 4.5](https://www.anthropic.com/claude)** - Code generation and architecture design
- **[Google Gemini 3 Pro](https://deepmind.google/technologies/gemini/)** - Core AI agent intelligence
- **[Google AI Studio](https://aistudio.google.com/)** - API configuration and testing
- **[OpenAI API](https://openai.com/api/)** - Fallback language model support

---

## HackSheffield10 Achievement

**Award Category:** Best use of AI Agents on Arm (by HackathonsUK)  
**Prize:** Raspberry Pi Zero 2 W Kit  
**Event:** HackSheffield10, November 29-30, 2024

### Challenge Requirements Met

**Frasers Group - Next-Gen Retail Engagement:**
- Digital experience targeting next-generation customers
- Real product search from Frasers Group websites
- Shopping cart with direct purchase links
- Competitor brand filtering (25+ brands blocked)
- Brand loyalty tracking through Prometheus metrics

**Arm - AI Agents on ARM:**
- Native ARM64 support for Raspberry Pi 4/5
- Apple Silicon (M1/M2/M3) compatibility
- Multi-platform Docker images
- Optimized performance on ARM architecture

**Additional Features:**
- Multi-agent collaboration with context sharing for Reply Challenge
- Real-time monitoring via Grafana dashboards for Grafana Challenge
- Journey-based UX aligned with "Odyssey" theme for HackSheffield10 Challenge

---

## The 5 AI Agents

Our multi-agent system employs specialized AI agents that collaborate to provide comprehensive fashion assistance. Each agent has a distinct role and communicates through a centralized orchestrator.

### 1. **IntentAgent** - Request Classifier
**Model:** Google Gemini 3 Pro  
**Purpose:** Analyzes user messages to determine intent and required actions

**Capabilities:**
- Classifies primary intent (wardrobe analysis, outfit recommendation, style advice, image generation, general chat)
- Extracts contextual information (occasion, style preference, urgency)
- Determines which agents should be activated for the request
- Provides structured intent analysis to guide the conversation flow

**Implementation:** Uses Gemini 3 Pro with temperature 0.3 for consistent classification. Falls back to OpenAI GPT-4o-mini if Gemini is unavailable, with keyword-based classification as final fallback.

### 2. **VisionAgent** 👁️ - Image Analyzer
**Model:** Google Gemini 3 Pro (Vision)  
**Purpose:** Analyzes uploaded wardrobe and outfit images

**Capabilities:**
- Identifies clothing items, colors, and styles from images
- Evaluates how garments work together
- Provides detailed descriptions for recommendation context
- Supports both base64 data URLs and HTTP image URLs

**Implementation:** Processes images through Gemini 3 Pro's vision capabilities. Handles image preprocessing and format conversion. Falls back to OpenAI GPT-4o Vision when needed.

### 3. **RecommendationAgent** 👔 - Product Search Specialist
**Model:** Google Gemini 2.5 Flash with Google Search Grounding  
**Purpose:** Finds real products from Frasers Group stores

**Capabilities:**
- Searches exclusively on Frasers Group domains (sportsdirect.com, houseoffraser.co.uk, flannels.com, usc.co.uk, jackwills.com)
- Returns actual product names, prices, and purchase links
- Filters out competitor brands automatically
- Tracks brand mentions and product recommendations via Prometheus metrics
- Provides clickable citations to product pages

**Implementation:** Leverages Gemini's Google Search grounding feature to retrieve real-time product information. Extracts grounding metadata to create inline citations. Tracks Frasers brand mentions and blocks 25+ competitor brands.

### 4. **ConversationAgent** 💬 - Dialogue Manager
**Model:** Google Gemini 3 Pro  
**Purpose:** Maintains natural, contextual conversation flow

**Capabilities:**
- Builds on insights from other agents
- Maintains conversation history (last 10 messages)
- Enforces Frasers-only brand mentions
- Provides follow-up questions and clarifications
- Creates cohesive multi-turn dialogues

**Implementation:** Uses conversation history to maintain context. Actively filters competitor mentions post-generation and replaces with Frasers alternatives. Tracks competitor blocks via Prometheus.

### 5. **ImageGenAgent** 🎨 - Outfit Visualizer
**Model:** Google Gemini 3 Pro Image  
**Purpose:** Generates visual representations of outfit recommendations

**Capabilities:**
- Creates realistic fashion photography shots
- Visualizes outfit combinations on mannequins
- Professional studio lighting and neutral backgrounds
- High-resolution image generation

**Implementation:** Generates images using Gemini 3 Pro Image model. Returns base64-encoded images for immediate display in the frontend.

---

## Agent Collaboration Flow

The agents work together through a centralized orchestrator that manages their interactions:

```
User Message
    ↓
IntentAgent (classifies intent)
    ↓
┌─────────────────────────────────────┐
│  Orchestrator determines actions    │
└─────────────────────────────────────┘
    ↓
┌─────────────┬──────────────────┬─────────────────┐
│ VisionAgent │ RecommendationAgent │ ConversationAgent │
│ (if image)  │ (if recommendation) │ (always)          │
└─────────────┴──────────────────┴─────────────────┘
    ↓
ImageGenAgent (if visualization requested)
    ↓
Combined Response to User
```

**Context Sharing:** All agents have access to the last 20 messages, enabling them to build on previous interactions and maintain conversation coherence.

**Asynchronous Execution:** Agents are called sequentially with results from earlier agents informing later ones (e.g., VisionAgent results feed into RecommendationAgent).

---

## Key Features

### Real Product Integration
- **Live Product Search:** Google Search grounding retrieves actual products from Frasers inventory
- **Price Information:** Real-time pricing from Frasers websites
- **Purchase Links:** Direct clickable links to product pages
- **Brand Filtering:** Automatically blocks 25+ competitor brands

### Multi-Agent Intelligence
- **Collaborative Processing:** 5 specialized agents work together on each request
- **Context Awareness:** Agents share conversation history (20 messages)
- **Sequential Reasoning:** Later agents build on earlier agents' outputs
- **Fallback Support:** OpenAI API fallback ensures reliability

### User Experience
- **Journey Timeline:** Visualizes multi-destination outfit planning
- **Shopping Cart:** Add products to cart with total price calculation
- **Image Upload:** Analyze wardrobe photos for personalized advice
- **Image Generation:** Visualize outfit recommendations
- **Responsive Design:** Works on desktop and mobile devices

### Monitoring & Observability
- **Prometheus Metrics:** Tracks agent calls, response times, brand mentions, competitor blocks
- **Grafana Dashboard:** Real-time visualization of system and business metrics
- **Performance Tracking:** Monitor agent-specific response times
- **Business Intelligence:** Track product recommendations and user sessions

### ARM Optimization
- **Native ARM64:** Runs efficiently on Raspberry Pi 4/5
- **Apple Silicon:** Full support for M1/M2/M3 Macs
- **Multi-Platform Docker:** Single image works across architectures
- **Performance Tuned:** Optimized for ARM processors

---

## Tech Stack

**Backend:**
- FastAPI (Python) - High-performance async API framework
- Google Gemini 3 Pro - Primary AI model for agents
- Google Gemini 2.5 Flash - Search-grounded recommendations
- OpenAI GPT-4o - Fallback language model
- Prometheus Client - Metrics collection

**Frontend:**
- React 19 - UI framework
- TypeScript - Type-safe development
- Vite - Fast build tool
- React Markdown - Formatted message rendering

**Infrastructure:**
- Docker & Docker Compose - Containerization
- Prometheus - Metrics storage and querying
- Grafana - Monitoring dashboards
- ARM64 & x86_64 support - Multi-architecture deployment

**APIs:**
- Google Gemini API - AI agent intelligence
- Google Search Grounding - Real product retrieval
- OpenAI API - Fallback support

---

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Google Gemini API key ([Get one here](https://aistudio.google.com/))
- (Optional) OpenAI API key for fallback

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/Retail-Odyssey.git
cd Retail-Odyssey
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your API keys:
# GEMINI_API_KEY=your_gemini_key_here
# GOOGLE_API_KEY=your_gemini_key_here
# OPENAI_API_KEY=your_openai_key_here (optional)
```

### 3. Launch with Docker (Recommended)
```bash
docker-compose up -d
```

### 4. Access the Application
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Grafana Dashboard:** http://localhost:3000 (admin/admin)
- **Prometheus:** http://localhost:9090

---

## 🖥️ Local Development

### Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run backend
python -m src.api.main
```

Backend will be available at http://localhost:8000

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will be available at http://localhost:5173

---

## Raspberry Pi / ARM Deployment

### Supported Devices
- Raspberry Pi 4 (4GB+ recommended)
- Raspberry Pi 5 (8GB recommended)
- Apple Silicon Macs (M1/M2/M3)
- Any ARM64 Linux device

### Quick Setup
```bash
# 1. Install Docker (if not already installed)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 2. Clone and configure
git clone https://github.com/yourusername/Retail-Odyssey.git
cd Retail-Odyssey
cp .env.example .env
# Edit .env with your API keys

# 3. Launch
docker-compose up -d
```

### Performance Notes
- **Raspberry Pi 4 (4GB):** All services run smoothly, image generation takes 10-15 seconds
- **Raspberry Pi 5 (8GB):** Excellent performance, image generation 5-8 seconds
- **Apple Silicon:** Native ARM64 performance, sub-second agent responses

### Monitoring Resources
```bash
# Check container resource usage
docker stats

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

---

## Monitoring & Metrics

### Grafana Dashboard
Access at http://localhost:3000 (default credentials: admin/admin)

**System Metrics:**
- Total requests processed
- User sessions count
- Messages per session distribution
- Agent call distribution
- Response time per agent (histogram)

**Business Metrics:**
- Product recommendations count
- Brand mentions by Frasers brand
- Competitor blocks count
- Average outfit price (when available)

### Prometheus Metrics
Raw metrics available at http://localhost:8000/metrics

**Available Metrics:**
- `retail_odyssey_total_requests` - Counter of all API requests
- `retail_odyssey_agent_calls{agent_name}` - Counter per agent
- `retail_odyssey_response_time{agent_name}` - Histogram of response times
- `retail_odyssey_brand_mentions{brand_name}` - Counter per Frasers brand
- `retail_odyssey_competitor_blocks` - Counter of blocked competitor mentions
- `retail_odyssey_product_recommendations` - Counter of products recommended
- `retail_odyssey_user_sessions` - Counter of user sessions
- `retail_odyssey_messages_per_session` - Histogram of session lengths

---

## API Endpoints

### POST /api/chat
Send a message to the multi-agent system

**Request:**
```json
{
  "message": "I need an outfit for a business meeting",
  "image_url": "https://example.com/wardrobe.jpg"  // optional
}
```

**Response:**
```json
{
  "responses": [
    {
      "agent": "IntentAgent",
      "message": "**Intent Classification**\n- Primary Intent: Outfit Recommendation\n- Occasion: Business\n- Urgency: Normal",
      "timestamp": "2024-11-30T10:00:00",
      "image_base64": null
    },
    {
      "agent": "RecommendationAgent",
      "message": "For a business meeting, I recommend:\n\n1. Navy blazer from House of Fraser (£149) [🔗](https://...)\n2. White dress shirt from Sports Direct (£29.99) [🔗](https://...)",
      "timestamp": "2024-11-30T10:00:02",
      "image_base64": null
    }
  ],
  "conversation": [...]
}
```

### GET /api/history
Retrieve conversation history

**Response:**
```json
{
  "conversation": [
    {
      "sender": "User",
      "content": "I need an outfit for a business meeting",
      "time": "2024-11-30T10:00:00"
    }
  ]
}
```

### POST /api/clear
Clear conversation history and start new session

**Response:**
```json
{
  "status": "cleared"
}
```

### GET /api/health
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "agents": ["IntentAgent", "VisionAgent", "RecommendationAgent", "ConversationAgent", "ImageGenAgent"]
}
```

### GET /metrics
Prometheus metrics endpoint (for Grafana)

---

## Frasers Group Integration

### Supported Stores
- **Sports Direct** - Activewear, casual clothing, footwear
- **House of Fraser** - Premium fashion, formal wear, accessories
- **Flannels** - Luxury designer brands, high-end fashion
- **USC** - Trendy streetwear, urban fashion
- **Jack Wills** - British heritage style, preppy clothing

### Product Search Features
- **Real-Time Search:** Uses Google Search grounding to find current products
- **Price Information:** Displays actual prices in GBP/EUR
- **Direct Links:** Clickable citations to product pages
- **Brand Filtering:** Automatically excludes 25+ competitor brands
- **Availability:** Only shows products currently listed on Frasers websites

### Competitor Filtering
The system actively blocks mentions of competitor brands including:
JD Sports, ASOS, Zalando, Nike.com, Adidas.com, Foot Locker, H&M, Zara, Uniqlo, Amazon Fashion, Nordstrom, Bloomingdale's, Forever 21, Revolve, Depop, Poshmark, Mango, Lululemon, Gap, Old Navy, Target, Walmart, Primark, Topshop, River Island, and others.

When a competitor is mentioned, the response is automatically replaced with Frasers alternatives.

---

## Project Structure

```
Retail-Odyssey/
├── src/
│   ├── agents/
│   │   ├── intent_agent.py           # Intent classification
│   │   ├── vision_agent.py           # Image analysis
│   │   ├── recommendation_agent.py   # Product search
│   │   ├── conversation_agent.py     # Dialogue management
│   │   ├── imagegen_agent.py         # Outfit visualization
│   │   └── group_chat_orchestrator.py # Agent coordination
│   ├── api/
│   │   └── main.py                   # FastAPI application
│   ├── utils/
│   │   └── prometheus_metrics.py     # Metrics definitions
│   └── __init__.py
├── frontend/
│   ├── components/
│   │   └── MultiAgentChat.tsx        # Main UI component
│   ├── App.tsx                       # React app entry
│   ├── types.ts                      # TypeScript definitions
│   ├── index.tsx                     # React DOM entry
│   ├── index.html                    # HTML template
│   ├── package.json                  # Node dependencies
│   ├── tsconfig.json                 # TypeScript config
│   ├── vite.config.ts                # Vite configuration
│   └── Dockerfile                    # Frontend container
├── grafana/
│   ├── dashboards/
│   │   ├── agents.json               # Dashboard definition
│   │   └── dashboard.yml             # Dashboard provisioning
│   └── datasources/
│       └── prometheus.yml            # Prometheus datasource
├── docker-compose.yml                # Multi-service orchestration
├── Dockerfile                        # Backend container
├── requirements.txt                  # Python dependencies
├── prometheus.yml                    # Prometheus configuration
├── .env.example                      # Environment template
├── .gitignore                        # Git ignore rules
├── .dockerignore                     # Docker ignore rules
├── LICENSE                           # MIT License
└── README.md                         # This file
```

---

## Contributing

This project was built for HackSheffield10. Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **HackSheffield10** - For hosting an amazing hackathon
- **HackathonsUK** - For the "Best use of AI Agents on Arm" award
- **Reply** - For the multi-agent multi-user challenge
- **Grafana** - For the doashboard integration challenge
- **Frasers Group** - For the retail integration challenge
- **Google** - For Gemini API and AI Studio
- **Anthropic** - For Claude assistance during development
- **AWS** - For Kiro CLI development tools
- **Perplexity** - For research support

---

## Contact

Built at HackSheffield10 (November 29-30, 2024)

**Team:** Retail Odyssey  
**GitHub:** https://github.com/SkullKrak7/

---

*"Every day is a journey. Let AI guide your style."* 
