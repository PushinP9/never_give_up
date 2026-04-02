import pytest
from constants import MOVIES_ENDPOINT


def test_movies_list_contains_new_movie(requester, created_movie):
    """Проверка наличия созданного фильма в общем списке через простой цикл."""
    # 1. Получаем список всех фильмов
    response = requester.send_request(method="GET", endpoint=MOVIES_ENDPOINT)
    all_movies = response.json().get("movies", [])

    # 2. Ищем наш фильм по ID среди всех полученных фильмов
    target_id = created_movie["id"]
    found_movie = None

    for movie in all_movies:
        if movie["id"] == target_id:
            found_movie = movie
            break  # Если нашли, дальше искать нет смысла, выходим из цикла

    # 3. Проверяем, что фильм действительно нашелся
    assert found_movie is not None, f"Фильм с ID {target_id} не найден в общем списке"

    # 4. Сравниваем данные из списка с данными из фикстуры (как просил ментор)
    assert found_movie["name"] == created_movie["name"]
    assert found_movie["price"] == created_movie["price"]


def test_get_movie_details_by_id(requester, created_movie):
    """Сверка всех полей детальной информации с данными из фикстуры."""
    movie_id = created_movie["id"]
    # Формируем эндпоинт: /movies/{id}
    response = requester.send_request(method="GET", endpoint=f"{MOVIES_ENDPOINT}/{movie_id}")
    detail_data = response.json()

    assert detail_data["id"] == movie_id
    assert detail_data["name"] == created_movie["name"]
    assert detail_data["description"] == created_movie["description"]
    assert detail_data["price"] == created_movie["price"]
    assert detail_data["location"] == created_movie["location"]
    assert "reviews" in detail_data


def test_movies_post_duplicate(requester, super_admin_token, created_movie):
    """Негативный тест: создание дубликата (409)."""
    requester.headers.update({"Authorization": f"Bearer {super_admin_token}"})

    payload = {
        "name": created_movie["name"],
        "description": created_movie["description"],
        "price": created_movie["price"],
        "location": created_movie["location"],
        "published": True,
        "genreId": created_movie["genreId"]
    }

    requester.send_request(
        method="POST",
        endpoint=MOVIES_ENDPOINT,
        data=payload,
        expected_status=409
    )


def test_patch_movie_name(requester, super_admin_token, created_movie):
    """Частичное обновление фильма (PATCH)."""
    requester.headers.update({"Authorization": f"Bearer {super_admin_token}"})
    movie_id = created_movie["id"]
    new_name = "Обновленный фильм"

    response = requester.send_request(
        method="PATCH",
        endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
        data={"name": new_name},
        expected_status=200
    )

    updated_data = response.json()
    assert updated_data["name"] == new_name
    assert updated_data["id"] == movie_id


def test_delete_movie_flow(requester, super_admin_token, created_movie):
    """Удаление и проверка через GET (404)."""
    requester.headers.update({"Authorization": f"Bearer {super_admin_token}"})
    movie_id = created_movie["id"]

    # Удаляем
    requester.send_request(
        method="DELETE",
        endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
        expected_status=200
    )

    # Проверяем отсутствие
    requester.send_request(
        method="GET",
        endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
        expected_status=404
    )


def test_unauthorized_post(requester, random_movie):
    """Попытка создания без авторизации (401)."""
    # Удаляем токен из заголовков, если он там был
    requester.headers.pop("Authorization", None)

    requester.send_request(
        method="POST",
        endpoint=MOVIES_ENDPOINT,
        data=random_movie,
        expected_status=401
    )