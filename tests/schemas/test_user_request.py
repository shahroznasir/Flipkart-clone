import pytest
from pydantic import ValidationError
from app.schemas.user_request import UserRequest

# Valid Case
def test_user_request_valid():
    user = UserRequest(
        email="user@example.com",
        password="StrongPass1",
        role="user"
    )
    assert user.email == "user@example.com"
    assert user.password == "StrongPass1"
    assert user.role == "user"

# Default Role
def test_user_request_default_role():
    user = UserRequest(
        email="user@example.com",
        password="StrongPass1"
    )
    assert user.role == "user"

# Invalid Email
def test_user_request_invalid_email():
    with pytest.raises(ValidationError):
        UserRequest(
            email="invalid-email",
            password="StrongPass1"
        )

# Password Too Short
def test_user_request_password_too_short():
    with pytest.raises(ValidationError):
        UserRequest(
            email="user@example.com",
            password="Short1"
        )

# Password Too Long
def test_user_request_password_too_long():
    with pytest.raises(ValidationError):
        UserRequest(
            email="user@example.com",
            password="A1" * 30  # 60 characters
        )

# Password Without Uppercase
def test_user_request_password_no_uppercase():
    with pytest.raises(ValidationError):
        UserRequest(
            email="user@example.com",
            password="strongpass1"
        )

# Password Without Number
def test_user_request_password_no_number():
    with pytest.raises(ValidationError):
        UserRequest(
            email="user@example.com",
            password="StrongPassword"
        )

# Invalid Role
def test_user_request_invalid_role():
    with pytest.raises(ValidationError):
        UserRequest(
            email="user@example.com",
            password="StrongPass1",
            role="manager"
        )