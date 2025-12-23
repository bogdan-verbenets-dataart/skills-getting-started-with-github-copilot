import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Soccer Team" in data

def test_signup_and_unregister():
    # Use a unique email for test
    activity = "Soccer Team"
    email = "testuser@mergington.edu"
    # Signup
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    # Check participant added
    response = client.get("/activities")
    assert email in response.json()[activity]["participants"]
    # Unregister
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    # Check participant removed
    response = client.get("/activities")
    assert email not in response.json()[activity]["participants"]

def test_signup_duplicate():
    activity = "Soccer Team"
    email = "duplicate@mergington.edu"
    # Signup first time
    client.post(f"/activities/{activity}/signup?email={email}")
    # Signup again (should fail)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    # Cleanup
    client.delete(f"/activities/{activity}/unregister?email={email}")

def test_unregister_not_found():
    activity = "Soccer Team"
    email = "notfound@mergington.edu"
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
