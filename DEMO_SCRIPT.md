# RetailOdyssey Demo Script

## 30-Second Pitch
"RetailOdyssey is a multi-agent AI fashion assistant where specialized agents collaborate in real-time to provide personalized outfit recommendations. Watch as VisionAgent, RecommendationAgent, and ConversationAgent work together like a team of fashion experts."

## Live Demo (2 minutes)

### 1. Show Multi-Agent Collaboration (Reply Challenge)
**Action**: Type "What should I wear to a wedding?"

**Point out**:
- Multiple agents respond in the same conversation
- Agents reference each other's insights
- Real-time collaboration visible in chat

### 2. Show Wardrobe Analysis (Frasers Challenge)
**Action**: Upload wardrobe image or use sample URL

**Point out**:
- VisionAgent analyzes clothing items, colors, styles
- RecommendationAgent builds on VisionAgent's analysis
- Next-gen retail engagement through AI

### 3. Show Metrics Dashboard (Grafana Challenge)
**Action**: Open http://localhost:8000/api/metrics

**Point out**:
- Real-time agent performance tracking
- Request counts and response times
- Grafana dashboard configuration ready

### 4. Highlight Theme (Odyssey)
**Point out**:
- Fashion journey metaphor
- Multi-agent collaboration = exploration
- RetailOdyssey brand identity

## Key Technical Points

- 5 specialized AI agents working together
- OpenAI GPT-4o-mini for real-time responses
- FastAPI + Streamlit architecture
- Prometheus metrics + Grafana ready
- Full test coverage (pytest passing)

## Challenge Coverage

✅ Reply: Multi-agent group conversation with cross-referencing  
✅ Frasers: AI-powered fashion recommendations with image analysis  
✅ Grafana: Metrics collection and dashboard configuration  
✅ Theme: Fashion odyssey journey concept

## Backup Talking Points

- Agents use sliding window context (last 5 messages) for efficiency
- Demo mode works without API key for reliability
- Extensible architecture - easy to add more agents
- Production-ready with error handling and fallbacks
