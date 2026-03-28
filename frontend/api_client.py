import os
import requests
from typing import List, Dict
import streamlit as st

API_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


def fetch_topics() -> List[Dict]:
    try:
        res = requests.get(f"{API_URL}/topics/")
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"⚠️ Error fetching data: {e}")
        return []

def create_topic(payload: Dict):
    try:
        res = requests.post(f"{API_URL}/topics/", json=payload)
        res.raise_for_status()
    except Exception as e:
        st.error(f"⚠️ Failed to save: {e}")

def update_topic(topic_id: int, payload: Dict):
    try:
        res = requests.patch(f"{API_URL}/topics/{topic_id}", json=payload)
        res.raise_for_status()
    except Exception as e:
        st.error(f"⚠️ Failed to update: {e}")

def delete_topic(topic_id: int):
    try:
        res = requests.delete(f"{API_URL}/topics/{topic_id}")
        res.raise_for_status()
    except Exception as e:
        st.error(f"⚠️ Failed to delete: {e}")

def generate_study_hack(topic_id: int):
    try:
        res = requests.post(f"{API_URL}/topics/{topic_id}/hack")
        res.raise_for_status()
    except Exception as e:
        st.error(f"⚠️ AI Generation Error: {e}")
