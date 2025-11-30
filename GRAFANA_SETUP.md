# Grafana Monitoring Setup

## Quick Start

1. **Start all services:**
```bash
docker-compose up -d
```

2. **Access Grafana:**
- URL: http://localhost:3000
- Username: `admin`
- Password: `admin`

3. **View Dashboard:**
- Navigate to Dashboards → "Retail Odyssey - AI Agents"

## Metrics Available

- **Total Requests**: Overall API usage
- **Agent Calls by Agent**: Which agents are being used most
- **Agent Response Time**: Performance of each agent
- **Requests Per Minute**: Real-time traffic

## Architecture

```
User → Frontend (5173) → Backend (8000) → AI Agents
                              ↓
                         Prometheus (9090) → Grafana (3000)
```

## Metrics Endpoint

Direct access: http://localhost:8000/metrics

## Demo Tips

1. Generate some traffic by chatting with agents
2. Show real-time metrics updating in Grafana
3. Highlight which agents are most active
4. Show response time differences between agents
