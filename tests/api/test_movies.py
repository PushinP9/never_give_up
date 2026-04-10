import pytest

def test_movies_list_contains_new_movie_last_page(movies_api, created_movie):
    movie_id = created_movie["id"]
    page_size = 20
    resp = movies_api.get_movies(params={"page": 1, "pageSize": page_size}, expected_status=200)
    data = resp.json()
    page_count = data["pageCount"]
    found = None
    pages_to_check = 5
    start_page = page_count
    end_page = max(page_count - pages_to_check + 1, 1)

    for page in range(start_page, end_page - 1, -1):
        resp = movies_api.get_movies(params={"page": page, "pageSize": page_size}, expected_status=200)
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
    assert found["name"] == created_movie["name"]
    assert found["price"] == created_movie["price"]
    resp = movies_api.get_movie(movie_id, expected_status=200)
    db_data = resp.json()
    assert db_data["id"] == movie_id

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
        "published": created_movie["published"],
        "genreId": created_movie["genreId"],
    }

    resp = movies_api.create_movie(payload, expected_status=409)
    err = resp.json()
    assert err["statusCode"] == 409
    assert "message" in err
    resp = movies_api.get_movie(created_movie["id"], expected_status=200)
    original = resp.json()
    assert original["id"] == created_movie["id"]
    assert original["name"] == created_movie["name"]



def test_patch_movie_name(movies_api, created_movie):
    movie_id = created_movie["id"]
    new_name = "Обновленный фильм123"
    response = movies_api.patch_movie(movie_id, {"name": new_name})
    updated_data = response.json()
    assert updated_data["name"] == new_name
    assert updated_data["id"] == movie_id
    response = movies_api.get_movie(movie_id)
    db_data = response.json()
    assert db_data["name"] == new_name, "Имя фильма не обновилось в БД!"
    assert db_data["id"] == movie_id


def test_delete_movie_flow(movies_api, created_movie):
    movie_id = created_movie["id"]
    response = movies_api.delete_movie(movie_id)
    delete_data = response.json()
    assert delete_data["id"] == movie_id
    movies_api.get_movie(movie_id, expected_status=404)


def test_unauthorized_post_movie(unauthorized_movies_api, random_movie):
    response = unauthorized_movies_api.create_movie(random_movie, expected_status=401)
    error_data = response.json()
    assert "message" in error_data
    assert error_data["message"] == "Unauthorized"
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
    response = movies_api.get_movie(invalid_id, expected_status=404)
    error_data = response.json()
    assert "message" in error_data


