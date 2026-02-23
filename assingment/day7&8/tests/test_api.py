from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

def test_generation_endpoint():
    response = client.get(
        "/generate",
        params={"prompt": "Hello, world!", "model": "gemini"}
    )
    assert response.status_code == 200
    assert "response" in response.json()

def test_generation_invalid_model():
    response = client.get("/generate", params={"prompt": "Hello, world!", "model": "unknown"})
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


