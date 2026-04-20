import pytest
from constants import LOGIN_ENDPOINT
from http import HTTPStatus


def test_created_movie_available_by_id(movies_api, created_movie_with_cleanup):
    movie_id = created_movie_with_cleanup["id"]

    response = movies_api.get_movie(
        movie_id,
        expected_status=HTTPStatus.OK
    )

    data = response.json()

    assert data["id"] == movie_id
    assert data["name"] == created_movie_with_cleanup["name"]
    assert data["price"] == created_movie_with_cleanup["price"]


def test_get_movie_details_by_id(movies_api, created_movie_with_cleanup):
    movie_id = created_movie_with_cleanup["id"]

    response = movies_api.get_movie(movie_id)
    detail_data = response.json()

    assert detail_data["id"] == movie_id
    assert detail_data["name"] == created_movie_with_cleanup["name"]
    assert detail_data["description"] == created_movie_with_cleanup["description"]
    assert detail_data["price"] == created_movie_with_cleanup["price"]
    assert detail_data["location"] == created_movie_with_cleanup["location"]
    assert "reviews" in detail_data


def test_movies_post_duplicate(movies_api, created_movie_with_cleanup):
    duplicate_response = movies_api.create_movie(created_movie_with_cleanup, expected_status=HTTPStatus.CONFLICT)
    err = duplicate_response.json()

    assert err["statusCode"] == HTTPStatus.CONFLICT
    assert "message" in err

    get_response = movies_api.get_movie(created_movie_with_cleanup["id"], expected_status=HTTPStatus.OK)
    existing_movie = get_response.json()
    assert existing_movie["id"] == created_movie_with_cleanup["id"]
    assert existing_movie["name"] == created_movie_with_cleanup["name"]


def test_patch_movie_name(movies_api, created_movie_with_cleanup):
    movie_id = created_movie_with_cleanup["id"]
    new_name = "Обновленный фильм123"

    patch_response = movies_api.patch_movie(movie_id, {"name": new_name})
    updated_data = patch_response.json()

    assert updated_data["name"] == new_name
    assert updated_data["id"] == movie_id

    get_response = movies_api.get_movie(movie_id)
    movie_data = get_response.json()
    assert movie_data["name"] == new_name, "Имя фильма не обновилось в БД!"
    assert movie_data["id"] == movie_id


def test_patch_movie_price(movies_api, created_movie_with_cleanup):
    movie_id = created_movie_with_cleanup["id"]
    new_price = 1299

    response = movies_api.patch_movie(movie_id, {"price": new_price})
    updated_data = response.json()

    assert updated_data["price"] == new_price
    assert updated_data["id"] == movie_id

    response = movies_api.get_movie(movie_id)
    data = response.json()
    assert data["price"] == new_price


def test_delete_movie(movies_api, created_movie):
    movie_id = created_movie["id"]

    response = movies_api.delete_movie(movie_id)
    delete_data = response.json()

    assert delete_data["id"] == movie_id
    movies_api.get_movie(movie_id, expected_status=HTTPStatus.NOT_FOUND)


def test_unauthorized_post_movie(unauthorized_movies_api, movies_api, random_movie):
    movie_name = random_movie["name"]

    response = unauthorized_movies_api.create_movie(
        random_movie,
        expected_status=HTTPStatus.UNAUTHORIZED
    )

    error_data = response.json()

    assert error_data["statusCode"] == HTTPStatus.UNAUTHORIZED
    assert "Unauthorized" in error_data["message"]


    list_response = movies_api.get_movies(
        params={"page": 1, "pageSize": 20},
        expected_status=HTTPStatus.OK
    )

    movies = list_response.json().get("movies", [])

    assert all(movie["name"] != movie_name for movie in movies), \
        "Фильм не должен был создаться при 401"


@pytest.mark.skip(reason="BUG: API returns 201 instead of 400 for negative price (Swagger says it should be 400)")
@pytest.mark.parametrize("field, invalid_value", [
    ("name", ""),
    ("price", -100),
    ("description", None),
])
def test_create_movie_invalid_data(movies_api, random_movie, field, invalid_value):
    payload = random_movie.copy()
    payload[field] = invalid_value
    movie_name = payload["name"]

    response = movies_api.create_movie(
        payload,
        expected_status=HTTPStatus.BAD_REQUEST
    )

    error_data = response.json()

    assert error_data["statusCode"] == HTTPStatus.BAD_REQUEST

    list_response = movies_api.get_movies(
        params={"page": 1, "pageSize": 50},
        expected_status=HTTPStatus.OK
    )

    movies = list_response.json().get("movies", [])

    assert all(movie["name"] != movie_name for movie in movies), \
        "Фильм не должен был создаться при 400"


def test_get_non_existent_movie(movies_api):
    invalid_id = 9999999

    response = movies_api.get_movie(invalid_id, expected_status=HTTPStatus.NOT_FOUND)
    error_data = response.json()

    assert "message" in error_data


def test_get_movies_invalid_params(movies_api):
    params = {
        "page": 1,
        "pageSize": 20,
        "minPrice": "invalid",
        "maxPrice": -100,
        "genreId": "abc"
    }

    response = movies_api.get_movies(params=params, expected_status=HTTPStatus.BAD_REQUEST)
    error_data = response.json()

    assert "message" in error_data


def test_delete_movie_with_invalid_id(movies_api):
    invalid_id = -999

    response = movies_api.delete_movie(invalid_id, expected_status=HTTPStatus.NOT_FOUND)
    error_data = response.json()

    assert "message" in error_data


def test_patch_movie_with_invalid_id(movies_api):
    invalid_id = -999
    payload = {"name": "Новое имя"}

    response = movies_api.patch_movie(invalid_id, payload, expected_status=HTTPStatus.NOT_FOUND)
    error_data = response.json()

    assert "message" in error_data

def test_patch_movie_unauthorized(unauthorized_movies_api, created_movie_with_cleanup):
    movie_id = created_movie_with_cleanup["id"]

    response = unauthorized_movies_api.patch_movie(
        movie_id,
        {"name": "Hacked"},
        expected_status=HTTPStatus.UNAUTHORIZED
    )

    error_data = response.json()
    assert "message" in error_data
    assert error_data["message"] == "Unauthorized"


def test_patch_movie_with_empty_body(movies_api, created_movie_with_cleanup):
    movie_id = created_movie_with_cleanup["id"]

    original_name = created_movie_with_cleanup["name"]
    original_price = created_movie_with_cleanup["price"]

    response = movies_api.patch_movie(
        movie_id,
        {},
        expected_status=HTTPStatus.OK
    )

    updated_data = response.json()

    assert updated_data["name"] == original_name
    assert updated_data["price"] == original_price


@pytest.mark.parametrize(
    "role, expected_status",
    [
        ("SUPER_ADMIN", HTTPStatus.OK),
        ("ADMIN", HTTPStatus.FORBIDDEN),
        ("USER", HTTPStatus.FORBIDDEN),
    ],
    ids=["super_admin", "admin", "user"]
)


def test_delete_movie_role_based(movies_api, user_with_role, random_movie, role, expected_status):
    create_response = movies_api.create_movie(
        random_movie,
        expected_status=HTTPStatus.CREATED
    )

    created_data = create_response.json()
    movie_id = created_data["id"]

    if role == "SUPER_ADMIN":
        client = movies_api
    else:
        client = user_with_role(role)

    delete_response = client.delete_movie(movie_id, expected_status=expected_status)

    if expected_status == HTTPStatus.OK:
        data = delete_response.json()
        assert data["id"] == movie_id

        movies_api.get_movie(movie_id, expected_status=HTTPStatus.NOT_FOUND)
    else:
        assert delete_response.status_code == expected_status

        movies_api.delete_movie(movie_id, expected_status=HTTPStatus.OK)


def test_login_with_invalid_password(auth_requester, registered_user):
    payload = {
        "email": registered_user["email"],
        "password": "WrongPassword123"
    }

    response = auth_requester.send_request(
        method="POST",
        endpoint=LOGIN_ENDPOINT,
        data=payload,
        expected_status=HTTPStatus.UNAUTHORIZED
    )

    error_data = response.json()

    assert error_data["statusCode"] == HTTPStatus.UNAUTHORIZED
    assert "Неверный логин или пароль" in error_data["message"]


def test_login_with_nonexistent_email(auth_requester):
    payload = {
        "email": "fakeuser@test.com",
        "password": "SomePassword123"
    }

    response = auth_requester.send_request(
        method="POST",
        endpoint=LOGIN_ENDPOINT,
        data=payload,
        expected_status=HTTPStatus.UNAUTHORIZED
    )

    error_data = response.json()

    assert error_data["statusCode"] == HTTPStatus.UNAUTHORIZED
    assert "Неверный логин или пароль" in error_data["message"]

def test_login_with_empty_data(auth_requester):
    payload = {
        "email": "",
        "password": ""
    }

    response = auth_requester.send_request(
        method="POST",
        endpoint=LOGIN_ENDPOINT,
        data=payload,
        expected_status=HTTPStatus.UNAUTHORIZED
    )

    error_data = response.json()
    assert error_data["statusCode"] == HTTPStatus.UNAUTHORIZED
    assert "Неверный логин или пароль" in error_data["message"]


def test_delete_movie_twice(movies_api, created_movie):
    movie_id = created_movie["id"]

    movies_api.delete_movie(movie_id, expected_status=HTTPStatus.OK)

    response = movies_api.delete_movie(
        movie_id,
        expected_status=HTTPStatus.NOT_FOUND
    )

    error_data = response.json()
    assert "message" in error_data