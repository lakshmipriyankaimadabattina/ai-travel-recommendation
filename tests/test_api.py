from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    res = client.get("/")
    assert res.status_code == 200


def test_nlp_query():
    res = client.post("/api/smart-search", json={"text": "find me a warm beach"})
    assert res.status_code == 200
    data = res.json()
    assert "parsed" in data


def test_weather():
    res = client.get("/api/weather/Tokyo")
    assert res.status_code == 200
