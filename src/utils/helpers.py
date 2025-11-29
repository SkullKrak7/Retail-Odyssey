import re
from typing import List

def extract_keywords(text: str) -> List[str]:
    words = re.findall(r'\b\w+\b', text.lower())
    fashion_keywords = ['outfit', 'wear', 'style', 'fashion', 'clothes', 'wardrobe', 
                        'dress', 'shirt', 'pants', 'jacket', 'shoes', 'casual', 'formal']
    return [w for w in words if w in fashion_keywords]

def format_agent_name(agent_class_name: str) -> str:
    return agent_class_name.replace("Agent", "")
