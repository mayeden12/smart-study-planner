import os

import requests
from typing import List, Dict

API_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


def fetch_topics() -> List[Dict]:
    try:
        res = requests.get(f"{API_URL}/topics/")
        res.raise_for_status()
        return res.json()
    except:
        return []

def create_topic(payload: Dict):
    try:
        requests.post(f"{API_URL}/topics/", json=payload)
    except:
        pass

def update_topic(topic_id: int, payload: Dict):
    try:
        requests.patch(f"{API_URL}/topics/{topic_id}", json=payload)
    except:
        pass

def delete_topic(topic_id: int):
    try:
        requests.delete(f"{API_URL}/topics/{topic_id}")
    except:
        pass

def generate_study_hack(topic_id: int):
    try:
        requests.patch(f"{API_URL}/topics/{topic_id}/generate-hack")
    except:
        pass
