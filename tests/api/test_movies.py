import random
from requests.auth import HTTPBasicAuth
import pytest
import requests
from constants import BASE_URL, body, body_negative, create_body, HEADERS


def test_movies_get():
    response = requests.get(f'{BASE_URL}/movies')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)



def test_movies_post_happy(super_admin_token,random_movie):
    headers = {**HEADERS, "Authorization": f"Bearer {super_admin_token}"}
    response = requests.post(f'{BASE_URL}/movies', json=random_movie, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert "createdAt" in data

    # Тест на проверку создания такого же фильма
def test_movies_post_negative(super_admin_token):
    headers = {**HEADERS, "Authorization": f"Bearer {super_admin_token}"}
    response = requests.post(f'{BASE_URL}/movies', json=body, headers=headers)
    assert response.status_code == 409
    # Отправка пустого имени фильма
    response_neg = requests.post(f'{BASE_URL}/movies', json=body_negative, headers=headers)
    assert response_neg.status_code == 400


def test_get_random_movie_details():
    # 1. Получаем список фильмов (берем первые 10 для примера)
    params = {
        "pageSize": 10,
        "published": "true"
    }
    list_response = requests.get(f"{BASE_URL}/movies", params=params)

    # Проверяем, что список успешно получен
    assert list_response.status_code == 200, f"Ошибка при получении списка: {list_response.text}"

    data = list_response.json()
    movies = data.get("movies", [])

    # Проверяем, что в базе вообще есть фильмы
    assert len(movies) > 0, "Список фильмов пуст"

    # 2. Выбираем случайный фильм из полученного списка
    random_movie = random.choice(movies)
    random_id = random_movie["id"]
    expected_name = random_movie["name"]

    # 3. Запрашиваем детальную информацию по этому рандомному ID
    detail_response = requests.get(f"{BASE_URL}/movies/{random_id}")

    assert detail_response.status_code == 200

    detail_data = detail_response.json()

    # Проверяем, что API вернуло именно тот ID, который мы запрашивали
    assert detail_data["id"] == random_id

    # Проверяем, что название совпадает с тем, что было в списке
    assert detail_data["name"] == expected_name

    # Проверяем структуру (наличие ключевых полей, которых нет в общем списке)
    assert "description" in detail_data
    assert "reviews" in detail_data
    assert isinstance(detail_data["reviews"], list)





def test_delete_movies(super_admin_token,random_movie):
        # Создаём свой фильм
        headers = {**HEADERS, "Authorization": f"Bearer {super_admin_token}"}
        create = requests.post(f'{BASE_URL}/movies', headers=headers, json=random_movie)
        movie_id = create.json()["id"]
        new_body = create.json()
        assert create.status_code == 201

        # Удаляем его
        response_delite = requests.delete(f'{BASE_URL}/movies/{movie_id}',headers=headers)
        assert response_delite.status_code == 200

        response_chek = requests.delete(f'{BASE_URL}/movies/{movie_id}', headers=headers)
        assert response_chek.status_code == 404

        #  Удаление фильма по некорректному ID
def test_delete_movies_neg_id(super_admin_token):
        headers = {**HEADERS, "Authorization": f"Bearer {super_admin_token}"}
        response = requests.delete(f'{BASE_URL}/movies/228228', headers=headers)
        assert response.status_code == 404


def test_patch_movie_name(super_admin_token,random_movie):
    # 1. Сначала создаем фильм, который будем редактировать
    headers = {**HEADERS, "Authorization": f"Bearer {super_admin_token}"}
    payload = random_movie
    create_movie = requests.post(f"{BASE_URL}/movies", json=payload, headers=headers)
    assert create_movie.status_code == 201
    response_data = create_movie.json()

    # Проверяем, что id есть в ответе
    assert "id" in response_data
    movie_id = response_data["id"]

    print(f"Created movie with ID: {movie_id}")  # Для отладки
    movie_id = create_movie.json()["id"]

    # 2. Обновляем только название, тут надо разобраться почему ошибка (
    new_data = {"name": "АБВГД"}
    patch_movie = requests.patch(f"{BASE_URL}/movies/{movie_id}", json=new_data, headers=headers)
    assert patch_movie.status_code == 200
    updated_movie = patch_movie.json()

    assert updated_movie["name"] == "АБВГД"
    assert updated_movie["id"] == movie_id

    delete_res = requests.delete(f"{BASE_URL}/movies/{movie_id}", headers=headers)
    assert delete_res.status_code == 200



def test_patch_non_existent_movie(super_admin_token):
    # Тест на попытку обновить несуществующий фильм
    headers = {**HEADERS, "Authorization": f"Bearer {super_admin_token}"}
    response = requests.patch(f"{BASE_URL}/movies/999999", json={"price": 10}, headers=headers)
    assert response.status_code == 404