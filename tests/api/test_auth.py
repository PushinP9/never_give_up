from constants.constants import REGISTER_ENDPOINT, LOGIN_ENDPOINT
import pytest

class TestAuthAPI:
    @pytest.mark.slow
    def test_register_user(self, auth_requester, test_user):
        response = auth_requester.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=test_user.model_dump(mode="json", exclude_unset=True),
            expected_status=201
        )

        response_data = response.json()

        assert response_data["email"] == test_user.email
        assert "id" in response_data
        assert "roles" in response_data
        assert "USER" in response_data["roles"]

    def test_register_and_login_user(self, auth_requester, registered_user):
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }

        response = auth_requester.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=200
        )

        response_data = response.json()

        assert "accessToken" in response_data
        assert response_data["user"]["email"] == registered_user["email"]