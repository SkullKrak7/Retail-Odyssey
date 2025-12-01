"""
Prometheus Metrics for Retail Odyssey

Tracks system performance and business metrics:
- Agent call counts and response times
- Total requests and user sessions
- Brand mentions and competitor blocks
- Product recommendations and pricing
"""

from prometheus_client import Counter, Histogram, Gauge, generate_latest

# System Performance Metrics
agent_calls = Counter('retail_odyssey_agent_calls', 'Agent call count', ['agent_name'])
total_requests = Counter('retail_odyssey_total_requests', 'Total requests')
response_time = Histogram('retail_odyssey_response_time', 'Response time in seconds', ['agent_name'])

# Business metrics
brand_mentions = Counter('retail_odyssey_brand_mentions', 'Brand mention count', ['brand_name'])
competitor_blocks = Counter('retail_odyssey_competitor_blocks', 'Competitor mentions blocked')
product_recommendations = Counter('retail_odyssey_product_recommendations', 'Products recommended')
average_outfit_price = Gauge('retail_odyssey_avg_outfit_price', 'Average outfit price in GBP')
user_sessions = Counter('retail_odyssey_user_sessions', 'Total user sessions')
messages_per_session = Histogram('retail_odyssey_messages_per_session', 'Messages per session')

def export_metrics():
    return generate_latest()
