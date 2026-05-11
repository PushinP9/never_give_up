from http import HTTPStatus
from custom_requester.custom_requester import CustomRequester
from constants.constants import LOGIN_URL, LOGIN_ENDPOINT, REGISTER_ENDPOINT
from models.model_test_user import (
    RegisterUserRequest,
    RegisterUserResponse
)


class AuthAPI(CustomRequester):

    def __init__(self, session, headers=None):
        super().__init__(session=session, base_url=LOGIN_URL, headers=headers)

    def register_user(
        self,
        user_data: RegisterUserRequest,
        expected_status=HTTPStatus.CREATED
    ) -> RegisterUserResponse:

        response = self.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,  # /register
            data=user_data.model_dump(mode="json", exclude_unset=True),
            expected_status=expected_status
        )

        return RegisterUserResponse(**response.json())

    def login_user(
        self,
        email: str,
        password: str,
        expected_status=HTTPStatus.OK
    ) -> dict:

        response = self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,  # /login
            data={
                "email": email,
                "password": password
            },
            expected_status=expected_status
        )

        return response.json()

    def authenticate(
        self,
        email: str,
        password: str,
        expected_status=HTTPStatus.OK
    ) -> dict:

        login_response = self.login_user(
            email=email,
            password=password,
            expected_status=expected_status
        )

        token = login_response.get("accessToken")
        if not token:
            raise KeyError("accessToken is missing in login response")

        self.session.headers.update({
            "Authorization": f"Bearer {token}"
        })

        return login_response