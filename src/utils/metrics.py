from datetime import datetime
from collections import defaultdict

class MetricsCollector:
    def __init__(self):
        self.agent_calls = defaultdict(int)
        self.response_times = []
        self.total_requests = 0
        
    def log_agent_call(self, agent_name: str, response_time: float):
        self.agent_calls[agent_name] += 1
        self.response_times.append(response_time)
        self.total_requests += 1
        
    def get_metrics(self) -> dict:
        avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0
        return {
            "total_requests": self.total_requests,
            "agent_calls": dict(self.agent_calls),
            "avg_response_time": avg_response_time,
            "timestamp": datetime.now().isoformat()
        }

metrics = MetricsCollector()
