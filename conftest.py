from faker import Faker
import pytest
import requests
import uuid
from constants import BASE_URL, REGISTER_ENDPOINT,LOGIN_URL
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGeneration
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
def registered_user(auth_requester, test_user):
    response = auth_requester.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user,
        expected_status=201
    )

    response_data = response.json()
    user = test_user.copy()
    user["id"] = response_data["id"]

    return user


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
    response = movies_api.create_movie(
        random_movie,
        expected_status=201
    )
    return response.json()


@pytest.fixture
def created_movie_with_cleanup(movies_api, created_movie):
    movie = created_movie

    yield movie

    movies_api.delete_movie(
        movie["id"],
        expected_status=200
    )


@pytest.fixture
def unauthorized_movies_api():
    """
    Фикстура создает клиент MoviesAPI без токена авторизации.
    Используется для тестов на проверку прав доступа (401 Unauthorized).
    """
    session = requests.Session()
    return MoviesAPI(session=session)

@pytest.fixture
def user_with_role(auth_requester):
    """
    Создает пользователя с указанной ролью
    и возвращает авторизованный MoviesAPI клиент
    """

    def _create_user(role: str):
        email = DataGeneration.generate_random_email()
        password = DataGeneration.generate_random_password()

        user_data = {
            "email": email,
            "fullName": DataGeneration.generate_random_name(),
            "password": password,
            "passwordRepeat": password,
            "roles": [role],
        }

        auth_requester.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=user_data,
            expected_status=201
        )

        client = MoviesAPI(session=requests.Session())
        client.authenticate(email=email, password=password)

        return client

    return _create_user


@pytest.fixture(scope="session")
def auth_requester():
    session = requests.Session()
    return CustomRequester(session=session, base_url=LOGIN_URL)