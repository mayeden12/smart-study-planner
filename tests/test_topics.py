import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# Setup a separate in-memory database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    # Create tables before each test and drop them after
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_topic():
    response = client.post(
        "/topics/",
        json={"title": "Learn Python", "description": "Study FastAPI", "status": "todo"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Learn Python"
    assert "id" in data

def test_list_topics():
    client.post("/topics/", json={"title": "Math Exam", "status": "todo"})
    response = client.get("/topics/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_topic():
    create_resp = client.post("/topics/", json={"title": "Physics", "status": "todo"})
    topic_id = create_resp.json()["id"]
    
    update_resp = client.patch(f"/topics/{topic_id}", json={"status": "done", "is_favorite": True})
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "done"

def test_delete_topic():
    create_resp = client.post("/topics/", json={"title": "History", "status": "todo"})
    topic_id = create_resp.json()["id"]
    
    delete_resp = client.delete(f"/topics/{topic_id}")
    assert delete_resp.status_code == 200