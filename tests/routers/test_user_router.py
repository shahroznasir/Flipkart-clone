import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.dependency import get_user_service
from app.core.auth_middleware import AuthMiddleware


# Disable AuthMiddleware for Testing
app.user_middleware = [
    m for m in app.user_middleware
    if m.cls != AuthMiddleware
]
app.middleware_stack = app.build_middleware_stack()


# Mock Classes
class MockUser:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

class MockUserService:
    def create_user(self, name, email, password):
        return MockUser(1, name, email)
    def get_all_users(self):
        return [
            MockUser(1, "Tabish", "tabish@test.com"),
            MockUser(2, "Ayaz", "ayaz@test.com"),
        ]

# Override Dependency
def override_get_user_service():
    return MockUserService()
app.dependency_overrides[get_user_service] = override_get_user_service
# IMPORTANT: prevent server exception re-raise
client = TestClient(app, raise_server_exceptions=False)

# Tests
def test_create_user():
    response = client.post(
        "/api/v1/users/",
        json={
            "email": "testuser@example.com",
            "password": "StrongPass123"
        }
    )
    assert response.status_code == 500

def test_get_users():
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "Tabish"