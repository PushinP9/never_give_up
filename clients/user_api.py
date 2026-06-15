from http import HTTPStatus
from custom_requester.custom_requester import CustomRequester
from constants.constants import LOGIN_URL
from models.model_test_user import RegisterUserResponse


class UserAPI(CustomRequester):

    def __init__(self, session, headers=None):
        super().__init__(session=session, base_url=LOGIN_URL, headers=headers)

    def get_user(
            self,
            locator: str,
            expected_status=HTTPStatus.OK
    ):
        response = self.send_request(
            method="GET",
            endpoint=f"/user/{locator}",
            expected_status=expected_status
        )

        if expected_status == HTTPStatus.OK:
            return RegisterUserResponse(**response.json())

        return response
