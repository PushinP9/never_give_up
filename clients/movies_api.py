from http import HTTPStatus
try:
    from http import HTTPMethod
except ImportError:
    class HTTPMethod:
        GET = 'GET'
        POST = 'POST'
        PATCH = 'PATCH'
        DELETE = 'DELETE'

from constants import MOVIES_ENDPOINT, BASE_URL
from custom_requester.custom_requester import CustomRequester

class MoviesAPI(CustomRequester):
    def __init__(self, session, token=None):
        super().__init__(session, BASE_URL)
        if token:
            self.headers.update({"Authorization": f"Bearer {token}"})

    def create_movie(self, movie_data, expected_status=HTTPStatus.CREATED):
        return self.send_request(
            method=HTTPMethod.POST,
            endpoint=MOVIES_ENDPOINT,
            data=movie_data,
            expected_status=expected_status
        )

    def get_movies(self, params=None, expected_status=HTTPStatus.OK):
        return self.send_request(
            method=HTTPMethod.GET,
            endpoint=MOVIES_ENDPOINT,
            params=params,
            expected_status=expected_status
        )

    def get_movie(self, movie_id, params=None, expected_status=HTTPStatus.OK):
        return self.send_request(
            method=HTTPMethod.GET,
            endpoint=f'{MOVIES_ENDPOINT}/{movie_id}',
            params=params,
            expected_status=expected_status
        )

    def delete_movie(self, movie_id, expected_status=HTTPStatus.OK):
        return self.send_request(
            method=HTTPMethod.DELETE,
            endpoint=f'{MOVIES_ENDPOINT}/{movie_id}',
            expected_status=expected_status
        )

    def patch_movie(self, movie_id, movie_data, expected_status=HTTPStatus.OK):
        return self.send_request(
            method=HTTPMethod.PATCH,
            endpoint=f'{MOVIES_ENDPOINT}/{movie_id}',
            data=movie_data,
            expected_status=expected_status
        )


