import pytest
from http import HTTPStatus
from constants.constants import LOGIN_ENDPOINT


@pytest.mark.smoke
def test_created_movie_available_by_id(movies_api, created_movie_with_cleanup):
    movie_id = created_movie_with_cleanup.id

    movie = movies_api.get_movie(movie_id, expected_status=HTTPStatus.OK)

    assert movie.id == movie_id
    assert movie.name == created_movie_with_cleanup.name
    assert movie.price == created_movie_with_cleanup.price


def test_get_movie_details_by_id(movies_api, created_movie_with_cleanup):
    movie_id = created_movie_with_cleanup.id

    movie = movies_api.get_movie(movie_id, expected_status=HTTPStatus.OK)

    assert movie.id == movie_id
    assert movie.name == created_movie_with_cleanup.name
    assert movie.description == created_movie_with_cleanup.description
    assert movie.price == created_movie_with_cleanup.price
    assert movie.location == created_movie_with_cleanup.location


def test_movies_post_duplicate(movies_api, created_movie_with_cleanup):
    error = movies_api.create_movie(
        {
            "name": created_movie_with_cleanup.name,
            "description": created_movie_with_cleanup.description,
            "price": created_movie_with_cleanup.price,
            "location": created_movie_with_cleanup.location,
            "published": created_movie_with_cleanup.published,
            "genreId": created_movie_with_cleanup.genreId,
        },
        expected_status=HTTPStatus.CONFLICT,
    )

    assert error.statusCode == HTTPStatus.CONFLICT

    existing_movie = movies_api.get_movie(
        created_movie_with_cleanup.id,
        expected_status=HTTPStatus.OK,
    )

    assert existing_movie.id == created_movie_with_cleanup.id
    assert existing_movie.name == created_movie_with_cleanup.name


@pytest.mark.regression
def test_patch_movie_name(movies_api, created_movie_with_cleanup):
    movie_id = created_movie_with_cleanup.id
    new_name = "Обновленный фильм123"

    patched_movie = movies_api.patch_movie(
        movie_id,
        {"name": new_name},
        expected_status=HTTPStatus.OK,
    )

    assert patched_movie.id == movie_id
    assert patched_movie.name == new_name

    movie = movies_api.get_movie(
        movie_id,
        expected_status=HTTPStatus.OK,
    )

    assert movie.name == new_name
    assert movie.price == created_movie_with_cleanup.price


@pytest.mark.regression
def test_patch_movie_price(movies_api, created_movie_with_cleanup):
    movie_id = created_movie_with_cleanup.id
    new_price = 1299

    patched_movie = movies_api.patch_movie(
        movie_id,
        {"price": new_price},
        expected_status=HTTPStatus.OK,
    )

    assert patched_movie.price == new_price
    assert patched_movie.id == movie_id

    movie = movies_api.get_movie(
        movie_id,
        expected_status=HTTPStatus.OK,
    )

    assert movie.price == new_price
    assert movie.name == created_movie_with_cleanup.name


@pytest.mark.smoke
def test_delete_movie(movies_api, created_movie):
    movie_id = created_movie.id

    deleted_movie = movies_api.delete_movie(
        movie_id,
        expected_status=HTTPStatus.OK,
    )

    assert deleted_movie.id == movie_id

    error = movies_api.get_movie(movie_id, expected_status=HTTPStatus.NOT_FOUND)
    assert error.statusCode == HTTPStatus.NOT_FOUND


def test_get_non_existent_movie(movies_api):
    invalid_id = 9999999

    error = movies_api.get_movie(
        invalid_id,
        expected_status=HTTPStatus.NOT_FOUND,
    )

    assert error.statusCode == HTTPStatus.NOT_FOUND


def test_get_movies_invalid_params(movies_api):
    params = {
        "page": 1,
        "pageSize": 20,
        "minPrice": "invalid",
        "maxPrice": -100,
        "genreId": "abc",
    }

    error = movies_api.get_movies(
        params=params,
        expected_status=HTTPStatus.BAD_REQUEST,
    )

    assert error.statusCode == HTTPStatus.BAD_REQUEST


def test_delete_movie_with_invalid_id(movies_api):
    invalid_id = -999

    error = movies_api.delete_movie(
        invalid_id,
        expected_status=HTTPStatus.NOT_FOUND,
    )

    assert error.statusCode == HTTPStatus.NOT_FOUND


def test_patch_movie_with_invalid_id(movies_api):
    invalid_id = -999

    error = movies_api.patch_movie(
        invalid_id,
        {"name": "Новое имя"},
        expected_status=HTTPStatus.NOT_FOUND,
    )

    assert error.statusCode == HTTPStatus.NOT_FOUND


@pytest.mark.regression
def test_patch_movie_unauthorized(movies_api, unauthorized_movies_api, created_movie_with_cleanup):
    movie_id = created_movie_with_cleanup.id
    original_name = created_movie_with_cleanup.name

    error = unauthorized_movies_api.patch_movie(
        movie_id,
        {"name": "Hacked"},
        expected_status=HTTPStatus.UNAUTHORIZED,
    )

    assert error.statusCode == HTTPStatus.UNAUTHORIZED

    movie = movies_api.get_movie(
        movie_id,
        expected_status=HTTPStatus.OK,
    )

    assert movie.name == original_name


def test_patch_movie_with_empty_body(movies_api, created_movie_with_cleanup):
    movie_id = created_movie_with_cleanup.id

    patched_movie = movies_api.patch_movie(
        movie_id,
        {},
        expected_status=HTTPStatus.OK,
    )

    assert patched_movie.id == movie_id

    movie = movies_api.get_movie(
        movie_id,
        expected_status=HTTPStatus.OK,
    )

    assert movie.name == created_movie_with_cleanup.name
    assert movie.price == created_movie_with_cleanup.price


def test_delete_movie_twice(movies_api, created_movie):
    movie_id = created_movie.id

    movies_api.delete_movie(movie_id, expected_status=HTTPStatus.OK)

    error = movies_api.delete_movie(
        movie_id,
        expected_status=HTTPStatus.NOT_FOUND,
    )

    assert error.statusCode == HTTPStatus.NOT_FOUND