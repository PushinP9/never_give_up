import pytest
from models.model_test_user import RegisterUserRequest


def get_valid_user_data():
    return {
        "email": "test@example.com",
        "fullName": "Test User",
        "password": "Password123",
        "passwordRepeat": "Password123",
        "roles": ["USER"]
    }


def test_valid_user():
    user = RegisterUserRequest(**get_valid_user_data())

    assert user.email == "test@example.com"
    assert user.password == "Password123"
    assert user.roles == ["USER"]


@pytest.mark.parametrize(
    "field, invalid_value",
    [
        ("email", "invalid_email"),
        ("password", "123"),
        ("passwordRepeat", "WrongPassword"),
    ]
)
def test_invalid_user(field, invalid_value):

    data = get_valid_user_data()
    data[field] = invalid_value


    if field == "passwordRepeat":
        data["password"] = "Password123"


