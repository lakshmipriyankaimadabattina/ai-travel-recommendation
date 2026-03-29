from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    res = client.get("/")
    assert res.status_code == 200
    assert "running" in res.json()["message"]

def test_nlp_query():
    res = client.post("/api/query", json={"text": "find me a warm beach"})
    assert res.status_code == 200
    data = res.json()
    assert data["intent"] == "destination_search"
    assert data["category"] == "beach"
