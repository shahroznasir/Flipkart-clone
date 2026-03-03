import os
os.environ["PYTEST_RUNNING"] = "1"

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, db_instance


# 🔹 Create tables once for entire test session
Base.metadata.create_all(bind=db_instance.engine)


@pytest.fixture(scope="session")
def client():
    """
    Global TestClient for all tests.
    """
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def auth_headers(client):
    """
    Creates a fresh user and logs in.
    Returns Authorization header for protected routes.
    """

    test_email = "testuser@example.com"
    test_password = "StrongPass123"

    # Try to register user (ignore if already exists)
    client.post(
        "/api/v1/auth/register",
        json={
            "name": "TestUser",
            "email": test_email,
            "password": test_password
        }
    )

    # Login
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": test_email,
            "password": test_password
        }
    )

    data = login_response.json()

    token = (
        data.get("access_token")
        or data.get("token")
        or data.get("data", {}).get("access_token")
        or data.get("data", {}).get("token")
    )

    if not token:
        raise Exception(f"Login failed. Got: {data}")

    return {"Authorization": f"Bearer {token}"}