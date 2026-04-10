from faker import Faker
import pytest
import requests
import uuid
from constants import BASE_URL, REGISTER_ENDPOINT
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGeneration
import random
from clients.movies_api import MoviesAPI
fake = Faker()

@pytest.fixture(scope="session")
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGeneration.generate_random_email()
    random_name = DataGeneration.generate_random_name()
    random_password = DataGeneration.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }

@pytest.fixture(scope="session")
def registered_user(requester, test_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = requester.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user,
        expected_status=201
    )
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user

@pytest.fixture(scope="session")
def requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)


@pytest.fixture(scope="session")
def movies_api(requester):
    client = MoviesAPI(session=requester.session)
    client.authenticate(email="api1@gmail.com", password="asdqwe123Q")
    return client


@pytest.fixture
def random_movie(faker):
    unique_suffix = uuid.uuid4().hex[:10]
    return {
        "name": f"{faker.sentence(nb_words=2).rstrip('.')} {unique_suffix}",
        "description": faker.text(max_nb_chars=80),
        "price": 499,
        "location": "SPB",
        "published": True,
        "genreId": 1,
    }

@pytest.fixture
def created_movie(movies_api, random_movie):
    """
    Фикстура создает фильм, используя методы клиента MoviesAPI.
    """
    response = movies_api.create_movie(random_movie)
    movie = response.json()
    yield movie
    # После каждого теста удаляем фильм из БД
    movies_api.delete_movie(movie["id"], expected_status=(200,404))

@pytest.fixture
def unauthorized_movies_api():
    """
    Фикстура создает клиент MoviesAPI без токена авторизации.
    Используется для тестов на проверку прав доступа (401 Unauthorized).
    """
    session = requests.Session()
    return MoviesAPI(session=session)