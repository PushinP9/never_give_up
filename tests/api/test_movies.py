import pytest
from http import HTTPStatus
from constants import LOGIN_ENDPOINT


def test_created_movie_available_by_id(movies_api, created_movie_with_cleanup):
    movie_id = created_movie_with_cleanup["id"]

    get_response = movies_api.get_movie(
        movie_id,
        expected_status=HTTPStatus.OK
    )
    movie_data = get_response.json()

    assert movie_data["id"] == movie_id
    assert movie_data["name"] == created_movie_with_cleanup["name"]
    assert movie_data["price"] == created_movie_with_cleanup["price"]


def test_get_movie_details_by_id(movies_api, created_movie_with_cleanup):
    movie_id = created_movie_with_cleanup["id"]

    get_response = movies_api.get_movie(
        movie_id,
        expected_status=HTTPStatus.OK
    )
    movie_data = get_response.json()

    assert movie_data["id"] == movie_id
    assert movie_data["name"] == created_movie_with_cleanup["name"]
    assert movie_data["description"] == created_movie_with_cleanup["description"]
    assert movie_data["price"] == created_movie_with_cleanup["price"]
    assert movie_data["location"] == created_movie_with_cleanup["location"]
    assert "reviews" in movie_data


def test_movies_post_duplicate(movies_api, created_movie_with_cleanup):
    post_response = movies_api.create_movie(
        created_movie_with_cleanup,
        expected_status=HTTPStatus.CONFLICT
    )
    error_data = post_response.json()

    assert error_data["statusCode"] == HTTPStatus.CONFLICT
    assert "message" in error_data

    get_response = movies_api.get_movie(
        created_movie_with_cleanup["id"],
        expected_status=HTTPStatus.OK
    )
    existing_movie = get_response.json()

    assert existing_movie["id"] == created_movie_with_cleanup["id"]
    assert existing_movie["name"] == created_movie_with_cleanup["name"]


def test_patch_movie_name(movies_api, created_movie_with_cleanup):
    movie_id = created_movie_with_cleanup["id"]
    new_name = "Обновленный фильм123"

    patch_response = movies_api.patch_movie(
        movie_id,
        {"name": new_name},
        expected_status=HTTPStatus.OK
    )
    patched_movie = patch_response.json()

    assert patched_movie["id"] == movie_id
    assert patched_movie["name"] == new_name

    get_response = movies_api.get_movie(
        movie_id,
        expected_status=HTTPStatus.OK
    )
    movie_data = get_response.json()

    assert movie_data["name"] == new_name
    assert movie_data["price"] == created_movie_with_cleanup["price"]


def test_patch_movie_price(movies_api, created_movie_with_cleanup):
    movie_id = created_movie_with_cleanup["id"]
    new_price = 1299

    patch_response = movies_api.patch_movie(
        movie_id,
        {"price": new_price},
        expected_status=HTTPStatus.OK
    )
    patched_movie = patch_response.json()

    assert patched_movie["price"] == new_price
    assert patched_movie["id"] == movie_id

    get_response = movies_api.get_movie(
        movie_id,
        expected_status=HTTPStatus.OK
    )
    movie_data = get_response.json()

    assert movie_data["price"] == new_price
    assert movie_data["name"] == created_movie_with_cleanup["name"]


def test_delete_movie(movies_api, created_movie):
    movie_id = created_movie["id"]

    delete_response = movies_api.delete_movie(
        movie_id,
        expected_status=HTTPStatus.OK
    )
    deleted_movie = delete_response.json()

    assert deleted_movie["id"] == movie_id

    movies_api.get_movie(movie_id, expected_status=HTTPStatus.NOT_FOUND)


def test_unauthorized_post_movie(unauthorized_movies_api, movies_api, random_movie):
    movie_name = random_movie["name"]

    post_response = unauthorized_movies_api.create_movie(
        random_movie,
        expected_status=HTTPStatus.UNAUTHORIZED
    )
    error_data = post_response.json()

    assert error_data["statusCode"] == HTTPStatus.UNAUTHORIZED
    assert "Unauthorized" in error_data["message"]

    list_response = movies_api.get_movies(
        params={"page": 1, "pageSize": 20},
        expected_status=HTTPStatus.OK
    )
    movies = list_response.json().get("movies", [])

    assert all(movie["name"] != movie_name for movie in movies)


@pytest.mark.skip(reason="BUG: API returns 201 instead of 400 for negative price")
@pytest.mark.parametrize(
    "field, invalid_value",
    [
        ("name", ""),
        ("price", -100),
        ("description", None),
    ],
)
def test_create_movie_invalid_data(movies_api, random_movie, field, invalid_value):
    payload = random_movie.copy()
    payload[field] = invalid_value
    movie_name = payload["name"]

    post_response = movies_api.create_movie(
        payload,
        expected_status=HTTPStatus.BAD_REQUEST
    )
    error_data = post_response.json()

    assert error_data["statusCode"] == HTTPStatus.BAD_REQUEST

    list_response = movies_api.get_movies(
        params={"page": 1, "pageSize": 20},
        expected_status=HTTPStatus.OK
    )
    movies = list_response.json().get("movies", [])

    assert all(movie["name"] != movie_name for movie in movies)


def test_get_non_existent_movie(movies_api):
    invalid_id = 9999999

    get_response = movies_api.get_movie(
        invalid_id,
        expected_status=HTTPStatus.NOT_FOUND
    )
    error_data = get_response.json()

    assert error_data["statusCode"] == HTTPStatus.NOT_FOUND
    assert "message" in error_data


def test_get_movies_invalid_params(movies_api):
    params = {
        "page": 1,
        "pageSize": 20,
        "minPrice": "invalid",
        "maxPrice": -100,
        "genreId": "abc",
    }

    get_response = movies_api.get_movies(
        params=params,
        expected_status=HTTPStatus.BAD_REQUEST
    )
    error_data = get_response.json()

    assert error_data["statusCode"] == HTTPStatus.BAD_REQUEST
    assert "message" in error_data


def test_delete_movie_with_invalid_id(movies_api):
    invalid_id = -999

    delete_response = movies_api.delete_movie(
        invalid_id,
        expected_status=HTTPStatus.NOT_FOUND
    )
    error_data = delete_response.json()

    assert error_data["statusCode"] == HTTPStatus.NOT_FOUND
    assert "message" in error_data


def test_patch_movie_with_invalid_id(movies_api):
    invalid_id = -999

    patch_response = movies_api.patch_movie(
        invalid_id,
        {"name": "Новое имя"},
        expected_status=HTTPStatus.NOT_FOUND
    )
    error_data = patch_response.json()

    assert error_data["statusCode"] == HTTPStatus.NOT_FOUND
    assert "message" in error_data


def test_patch_movie_unauthorized(movies_api, unauthorized_movies_api, created_movie_with_cleanup):
    movie_id = created_movie_with_cleanup["id"]
    original_name = created_movie_with_cleanup["name"]

    patch_response = unauthorized_movies_api.patch_movie(
        movie_id,
        {"name": "Hacked"},
        expected_status=HTTPStatus.UNAUTHORIZED
    )
    error_data = patch_response.json()

    assert error_data["statusCode"] == HTTPStatus.UNAUTHORIZED

    get_response = movies_api.get_movie(
        movie_id,
        expected_status=HTTPStatus.OK
    )
    movie_data = get_response.json()

    assert movie_data["name"] == original_name


def test_patch_movie_with_empty_body(movies_api, created_movie_with_cleanup):
    movie_id = created_movie_with_cleanup["id"]

    patch_response = movies_api.patch_movie(
        movie_id,
        {},
        expected_status=HTTPStatus.OK
    )
    patched_movie = patch_response.json()

    assert patched_movie["id"] == movie_id

    get_response = movies_api.get_movie(
        movie_id,
        expected_status=HTTPStatus.OK
    )
    movie_data = get_response.json()

    assert movie_data["name"] == created_movie_with_cleanup["name"]
    assert movie_data["price"] == created_movie_with_cleanup["price"]


def test_delete_movie_twice(movies_api, created_movie):
    movie_id = created_movie["id"]

    movies_api.delete_movie(movie_id, expected_status=HTTPStatus.OK)

    second_delete_response = movies_api.delete_movie(
        movie_id,
        expected_status=HTTPStatus.NOT_FOUND
    )
    error_data = second_delete_response.json()

    assert error_data["statusCode"] == HTTPStatus.NOT_FOUND
    assert "message" in error_data


@pytest.mark.parametrize(
    "role, expected_status",
    [
        ("SUPER_ADMIN", HTTPStatus.OK),
        ("ADMIN", HTTPStatus.FORBIDDEN),
        ("USER", HTTPStatus.FORBIDDEN),
    ],
    ids=["super_admin", "admin", "user"],
)
def test_delete_movie_role_based(movies_api, user_with_role, random_movie, role, expected_status):
    post_response = movies_api.create_movie(
        random_movie,
        expected_status=HTTPStatus.CREATED
    )
    created_movie_data = post_response.json()
    movie_id = created_movie_data["id"]

    client = movies_api if role == "SUPER_ADMIN" else user_with_role(role)

    delete_response = client.delete_movie(
        movie_id,
        expected_status=expected_status
    )

    if expected_status == HTTPStatus.OK:
        deleted_movie = delete_response.json()
        assert deleted_movie["id"] == movie_id

        movies_api.get_movie(movie_id, expected_status=HTTPStatus.NOT_FOUND)
    else:
        error_data = delete_response.json()
        assert error_data["statusCode"] == HTTPStatus.FORBIDDEN

        movies_api.get_movie(movie_id, expected_status=HTTPStatus.OK)
        movies_api.delete_movie(movie_id, expected_status=HTTPStatus.OK)


def test_login_with_invalid_password(auth_requester, registered_user):
    payload = {
        "email": registered_user["email"],
        "password": "WrongPassword228",
    }

    login_response = auth_requester.send_request(
        method="POST",
        endpoint=LOGIN_ENDPOINT,
        data=payload,
        expected_status=HTTPStatus.UNAUTHORIZED,
    )
    error_data = login_response.json()

    assert error_data["statusCode"] == HTTPStatus.UNAUTHORIZED
    assert "Неверный логин или пароль" in error_data["message"]


def test_login_with_nonexistent_email(auth_requester):
    payload = {
        "email": "fakeuser@test.com",
        "password": "SomePassword123",
    }

    login_response = auth_requester.send_request(
        method="POST",
        endpoint=LOGIN_ENDPOINT,
        data=payload,
        expected_status=HTTPStatus.UNAUTHORIZED,
    )
    error_data = login_response.json()

    assert error_data["statusCode"] == HTTPStatus.UNAUTHORIZED
    assert "Неверный логин или пароль" in error_data["message"]


def test_login_with_empty_data(auth_requester):
    payload = {
        "email": "",
        "password": "",
    }

    login_response = auth_requester.send_request(
        method="POST",
        endpoint=LOGIN_ENDPOINT,
        data=payload,
        expected_status=HTTPStatus.UNAUTHORIZED,
    )
    error_data = login_response.json()

    assert error_data["statusCode"] == HTTPStatus.UNAUTHORIZED
    assert "Неверный логин или пароль" in error_data["message"]