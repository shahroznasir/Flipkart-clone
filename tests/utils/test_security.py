import pytest
from app.utils.security import hash_password, verify_password


# Test hashing creates a different value
def test_hash_password_creates_hash():
    password = "mysecret123"
    hashed = hash_password(password)
    assert hashed is not None
    assert hashed != password
    assert isinstance(hashed, str)

# Test correct password verification
def test_verify_password_success():
    password = "mysecret123"
    hashed = hash_password(password)
    result = verify_password(password, hashed)
    assert result is True

# Test wrong password verification
def test_verify_password_failure():
    password = "mysecret123"
    wrong_password = "wrong123"
    hashed = hash_password(password)
    result = verify_password(wrong_password, hashed)
    assert result is False

# Test hash uniqueness (bcrypt salt)
def test_hash_password_is_unique():
    password = "mysecret123"
    hash1 = hash_password(password)
    hash2 = hash_password(password)
    assert hash1 != hash2

# Test empty password
def test_empty_password():
    password = ""
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True