import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_list_summary():
    # Create
    payload = {"text": "Alice will do the design by tomorrow. Bob handles the DB."}
    response = client.post("/meetings/summarize", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "summary_text" in data
    assert len(data["summary_text"]) > 0
    
    meeting_id = data["id"]
    
    # List
    list_res = client.get("/meetings/")
    assert list_res.status_code == 200
    assert len(list_res.json()) > 0
    
    # Delete
    del_res = client.delete(f"/meetings/{meeting_id}")
    assert del_res.status_code == 200