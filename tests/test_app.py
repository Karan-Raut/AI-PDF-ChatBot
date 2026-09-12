from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_ask_empty_question():
    response = client.post("/ask", json={"question": ""})
    # Pydantic validation kicks in and returns 422 Unprocessable Entity
    assert response.status_code == 422

def test_upload_invalid_file_type():
    # Attempt to upload a text file instead of PDF
    files = {'file': ('test.txt', b"This is a text file", 'text/plain')}
    response = client.post("/upload", files=files)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid file type. Only PDF files are allowed."
