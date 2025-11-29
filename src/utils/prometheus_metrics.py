from prometheus_client import Counter, Histogram, generate_latest

agent_calls = Counter('retail_odyssey_agent_calls', 'Agent call count', ['agent_name'])
total_requests = Counter('retail_odyssey_total_requests', 'Total requests')
response_time = Histogram('retail_odyssey_response_time', 'Response time in seconds', ['agent_name'])

def export_metrics():
    return generate_latest()
