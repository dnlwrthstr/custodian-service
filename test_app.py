import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "custodian-service"}

def test_api_docs():
    """Test that the API documentation is accessible."""
    response = client.get("/docs")
    assert response.status_code == 200