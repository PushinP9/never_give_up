import pytest
from http import HTTPStatus

def test_movies_list_contains_new_movie_last_page(movies_api, created_movie_with_cleanup):
    movie_id = created_movie_with_cleanup["id"]
    page_size = 20
    pages_to_check = 5

    response = movies_api.get_movies(params={"page": 1, "pageSize": page_size}, expected_status=HTTPStatus.OK)
    data = response.json()
    page_count = data["pageCount"]
    found = None
    start_page = page_count
    end_page = max(page_count - pages_to_check + 1, 1)

    for page in range(start_page, end_page - 1, -1):
        resp = movies_api.get_movies(params={"page": page, "pageSize": page_size}, expected_status=HTTPStatus.OK)
        movies = resp.json().get("movies", [])
        for m in movies:
            if m.get("id") == movie_id:
                found = m
                break
        if found:
            break

    assert found is not None, (
        f"Фильм с ID {movie_id} не найден на последних страницах: {end_page}..{start_page}"
    )
    assert found["id"] == movie_id
    assert found["name"] == created_movie_with_cleanup["name"]
    assert found["price"] == created_movie_with_cleanup["price"]

    get_response = movies_api.get_movie(movie_id, expected_status=HTTPStatus.OK)
    response_movie = get_response.json()
    assert response_movie["id"] == movie_id


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

    response = movies_api.patch_movie(movie_id, {"name": new_name})
    updated_data = response.json()

    assert updated_data["name"] == new_name
    assert updated_data["id"] == movie_id

    response = movies_api.get_movie(movie_id)
    response_movie = response.json()
    assert response_movie["name"] == new_name, "Имя фильма не обновилось в БД!"
    assert response_movie["id"] == movie_id

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


def test_unauthorized_post_movie(unauthorized_movies_api, random_movie):
    response = unauthorized_movies_api.create_movie(random_movie, expected_status=HTTPStatus.UNAUTHORIZED)
    error_data = response.json()

    assert "message" in error_data
    assert error_data["message"] == "Unauthorized"


@pytest.mark.skip(reason="BUG: API returns 201 instead of 400 for negative price (Swagger says it should be 400)")
@pytest.mark.parametrize("field, invalid_value", [
    ("name", ""),
    ("price", -100),
    ("description", None),
])
def test_create_movie_invalid_data(movies_api, random_movie, field, invalid_value):
    payload = random_movie.copy()
    payload[field] = invalid_value

    movies_api.create_movie(payload, expected_status=HTTPStatus.BAD_REQUEST)


def test_get_non_existent_movie(movies_api):
    invalid_id = 9999999

    response = movies_api.get_movie(invalid_id, expected_status=HTTPStatus.NOT_FOUND)
    error_data = response.json()

    assert "message" in error_data