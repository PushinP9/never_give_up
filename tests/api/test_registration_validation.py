import pytest
from pydantic import ValidationError
from models.model_test_user import RegisterUserRequest


def test_valid_user():
    valid_data = {
        "email": "test@example.com",
        "fullName": "Test User",
        "password": "Password123",
        "passwordRepeat": "Password123",
        "roles": ["USER"]
    }

    user = RegisterUserRequest(**valid_data)

    assert user.email == "test@example.com"
    assert user.password == "Password123"


def test_invalid_email():
    invalid_data = {
        "email": "invalid_email",
        "fullName": "Test User",
        "password": "Password123",
        "passwordRepeat": "Password123",
        "roles": ["USER"]
    }

    with pytest.raises(ValidationError):
        RegisterUserRequest(**invalid_data)


def test_short_password():
    invalid_data = {
        "email": "test@example.com",
        "fullName": "Test User",
        "password": "123",
        "passwordRepeat": "123",
        "roles": ["USER"]
    }

    with pytest.raises(ValidationError):
        RegisterUserRequest(**invalid_data)


def test_password_mismatch():
    invalid_data = {
        "email": "test@example.com",
        "fullName": "Test User",
        "password": "Password123",
        "passwordRepeat": "WrongPassword",
        "roles": ["USER"]
    }

    with pytest.raises(ValidationError):
        RegisterUserRequest(**invalid_data)