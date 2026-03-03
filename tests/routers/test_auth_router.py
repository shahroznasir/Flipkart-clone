import pytest
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from app.schemas.user_request import UserRequest
from app.schemas.login_request import LoginRequest
from app.dependency import get_auth_service

# Mock Service
class MockAuthService:
    def register_user(self, user: UserRequest):
        if user.email == "existing@gmail.com":
            from fastapi import HTTPException
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )
        return {
            "id": 1,
            "email": user.email,
            "role": user.role
        }

    def login_user(self, data: LoginRequest):
        from fastapi import HTTPException
        if data.email != "test@gmail.com":
            raise HTTPException(
                status_code=400,
                detail="Invalid email"
            )

        if data.password != "Password1":
            raise HTTPException(
                status_code=400,
                detail="Invalid password"
            )
        return {
            "access_token": "fake_token",
            "token_type": "bearer",
            "user": {
                "id": 1,
                "email": data.email,
                "role": "user"
            }
        }

# Dependency Override
def override_auth_service():
    return MockAuthService()

app.dependency_overrides[get_auth_service] = override_auth_service
client = TestClient(app)

# Register Success
def test_register_success():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@gmail.com",
            "password": "Password1",
            "role": "user"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED

# Register Duplicate
def test_register_duplicate():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "existing@gmail.com",
            "password": "Password1",
            "role": "user"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# Login Success
def test_login_success():
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@gmail.com",
            "password": "Password1"
        }
    )
    assert response.status_code == status.HTTP_200_OK

# Wrong Password
def test_login_wrong_password():
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@gmail.com",
            "password": "WrongPassword1"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# User Not Found
def test_login_user_not_found():
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "unknown@gmail.com",
            "password": "Password1"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST