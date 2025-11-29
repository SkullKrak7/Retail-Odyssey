# RetailOdyssey

Multi-agent fashion recommendation system for HackSheffield10.

## Features

- Multi-agent AI collaboration
- Fashion outfit recommendations
- Wardrobe image analysis
- Group chat interface

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Add your OPENAI_API_KEY to .env
```

## Run

Terminal 1:
```bash
python -m src.api.main
```

Terminal 2:
```bash
streamlit run frontend/streamlit_ui/app.py
```

## Architecture

- VisionAgent: Analyzes wardrobe images
- RecommendationAgent: Suggests outfits
- IntentAgent: Parses user requests
- ConversationAgent: Manages dialogue
- GroupChatOrchestrator: Coordinates agents

## Challenges

- Reply: Multi-agent group conversation
- Frasers: Next-gen retail engagement
- Grafana: Monitoring integration
- Theme: Fashion odyssey journey

## Tech Stack

- FastAPI
- Streamlit
- OpenAI GPT-4
- Python 3.11+

## License

MIT
