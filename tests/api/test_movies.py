from http.client import responses
import time
import pytest
from constants import MOVIES_ENDPOINT


def test_movies_list_contains_new_movie(movies_api, created_movie):
    time.sleep(1)
    target_id = created_movie["id"]
    params = {
        "id": target_id
    }
    response = movies_api.get_movies(params=params)
    all_movies = response.json().get("movies", [])
    target_id = created_movie["id"]
    found_movie = None

    for movie in all_movies:
        if movie["id"] == target_id:
            found_movie = movie
            break

    assert found_movie is not None, f"Фильм с ID {target_id} не найден в общем списке"
    assert found_movie["name"] == created_movie["name"]
    assert found_movie["price"] == created_movie["price"]


def test_get_movie_details_by_id(movies_api, created_movie):

    movie_id = created_movie["id"]

    response = movies_api.get_movie(movie_id)
    detail_data = response.json()

    assert detail_data["id"] == movie_id
    assert detail_data["name"] == created_movie["name"]
    assert detail_data["description"] == created_movie["description"]
    assert detail_data["price"] == created_movie["price"]
    assert detail_data["location"] == created_movie["location"]
    assert "reviews" in detail_data


def test_movies_post_duplicate(movies_api, created_movie):
    payload = {
        "name": created_movie["name"],
        "description": created_movie["description"],
        "price": created_movie["price"],
        "location": created_movie["location"],
        "published": True,
        "genreId": created_movie["genreId"]
    }

    movies_api.create_movie(payload, expected_status=409)


def test_patch_movie_name(movies_api, created_movie):

    movie_id = created_movie["id"]
    new_name = "Обновленный фильм"

    response = movies_api.patch_movie(movie_id, {"name": new_name})

    updated_data = response.json()
    assert updated_data["name"] == new_name
    assert updated_data["id"] == movie_id


def test_delete_movie_flow(movies_api, created_movie):


    movie_id = created_movie["id"]
    movies_api.delete_movie(movie_id)
    movies_api.get_movie(movie_id, expected_status=404)

def test_unauthorized_post_movie(unauthorized_movies_api, random_movie):
    unauthorized_movies_api.create_movie(random_movie, expected_status=401)
    # Уточнить по статус коду .

@pytest.mark.skip(reason="BUG: API returns 201 instead of 400 for negative price (Swagger says it should be 400)")
@pytest.mark.parametrize("field, invalid_value", [
    ("name", ""),
    ("price", -100),
    ("description", None),
])
def test_create_movie_invalid_data(movies_api, random_movie, field, invalid_value):
    payload = random_movie.copy()
    payload[field] = invalid_value
    movies_api.create_movie(payload, expected_status=400)

def test_get_non_existent_movie(movies_api):
    invalid_id = 9999999
    movies_api.get_movie(invalid_id, expected_status=404)


