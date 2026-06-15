import pytest
from models.model_test_user import RegisterUserRequest

class TestUser:

    def test_create_user(self, super_admin, creation_user_data: RegisterUserRequest):
        response = super_admin.api.auth_api.register_user(
            creation_user_data
        )

        assert response.email == creation_user_data.email
        assert response.fullName == creation_user_data.fullName
        assert response.roles == creation_user_data.roles
        assert response.verified is True
        assert response.banned is False

    def test_get_user_by_locator(self, super_admin, creation_user_data: RegisterUserRequest):
        created_user = super_admin.api.auth_api.register_user(
            creation_user_data
        )

        response_by_id = super_admin.api.user_api.get_user(created_user.id)
        response_by_email = super_admin.api.user_api.get_user(created_user.email)

        assert response_by_id == response_by_email
        assert response_by_id.id != ""
        assert response_by_id.email == creation_user_data.email
        assert response_by_id.fullName == creation_user_data.fullName
        assert response_by_id.roles == creation_user_data.roles
        assert response_by_id.verified is True

    @pytest.mark.slow
    def test_get_user_by_id_common_user(self, common_user):
        response = common_user.api.user_api.get_user(
            common_user.id,
            expected_status=403
        )

        error = response.json()
        assert error["statusCode"] == 403
        assert "Forbidden" in error["message"]



