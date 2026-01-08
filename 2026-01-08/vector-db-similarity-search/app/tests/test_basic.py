import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app  

# Create test client
client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_create_vector():
    response = client.post("/vectors", json={
        "id": "test_1",
        "text": "This is a test document"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Document added successfully"

def test_query_vectors():
    client.post("/vectors", json={
        "id": "test_query",
        "text": "Safety training is mandatory for all employees"
    })
    
    response = client.post("/vectors/query", json={
        "query": "safety training"
    })
    assert response.status_code == 200
    assert "results" in response.json()

def test_get_all_vectors():
    response = client.get("/vectors")
    assert response.status_code == 200
    assert "ids" in response.json()

def test_delete_vector():
    # First add
    client.post("/vectors", json={
        "id": "test_delete",
        "text": "Document to delete"
    })
    

    response = client.delete("/vectors/test_delete")
    assert response.status_code == 200
    assert response.json()["message"] == "Document deleted"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])