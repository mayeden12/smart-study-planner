import pytest
from fastapi.testclient import TestClient

from app.main import app
client = TestClient(app)

def test_create_summary_success():
    # כאן אנחנו נותנים למערכת לפנות ל-AI האמיתי ולסכם את הטקסט
    payload = {"text": "This is a meeting about a test. We need to finish the tests by tomorrow."}
    response = client.post("/summarize/", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    
    # בגלל שה-AI מנסח תשובה שונה בכל פעם, פשוט נוודא שחזר אלינו סיכום ושהוא לא ריק
    assert "summary" in data
    assert len(data["summary"]) > 0


def test_create_summary_validation_error():
    # בדיקה שהמערכת דוחה טקסט קצר מדי (min_length=10)
    payload = {"text": "short"}
    response = client.post("/summarize/", json=payload)
    
    assert response.status_code == 422