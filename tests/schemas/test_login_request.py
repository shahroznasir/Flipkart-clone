import pytest
from pydantic import ValidationError
from app.schemas.login_request import LoginRequest

# Valid Case
def test_login_request_valid():
    data = LoginRequest(
        email="test@example.com",
        password="StrongPass123"
    )

    assert data.email == "test@example.com"
    assert data.password == "StrongPass123"

# Invalid Email
def test_login_request_invalid_email():
    with pytest.raises(ValidationError):
        LoginRequest(
            email="invalid-email",
            password="StrongPass123"
        )

# Missing Email
def test_login_request_missing_email():
    with pytest.raises(ValidationError):
        LoginRequest(
            password="StrongPass123"
        )

# Missing Password
def test_login_request_missing_password():
    with pytest.raises(ValidationError):
        LoginRequest(
            email="test@example.com"
        )

# Empty Password
def test_login_request_empty_password():
    data = LoginRequest(
        email="test@example.com",
        password=""
    )

    assert data.password == ""