import pytest
from pydantic import ValidationError
from app.schemas.user_response import UserResponse

# Valid Case
def test_user_response_valid():
    user = UserResponse(
        id=1,
        email="user@example.com",
        role="user"
    )
    assert user.id == 1
    assert user.email == "user@example.com"
    assert user.role == "user"

# Missing Fields
def test_user_response_missing_id():
    with pytest.raises(ValidationError):
        UserResponse(
            email="user@example.com",
            role="user"
        )

def test_user_response_missing_email():
    with pytest.raises(ValidationError):
        UserResponse(
            id=1,
            role="user"
        )

def test_user_response_missing_role():
    with pytest.raises(ValidationError):
        UserResponse(
            id=1,
            email="user@example.com"
        )

# Wrong Data Types
def test_user_response_invalid_id_type():
    with pytest.raises(ValidationError):
        UserResponse(
            id="not-an-int",
            email="user@example.com",
            role="user"
        )

def test_user_response_invalid_email_type():
    with pytest.raises(ValidationError):
        UserResponse(
            id=1,
            email=123,
            role="user"
        )

# from_attributes Support
class DummyUser:
    def __init__(self, id, email, role):
        self.id = id
        self.email = email
        self.role = role

def test_user_response_from_attributes():
    dummy = DummyUser(5, "dummy@example.com", "admin")
    user = UserResponse.model_validate(dummy)
    assert user.id == 5
    assert user.email == "dummy@example.com"
    assert user.role == "admin"