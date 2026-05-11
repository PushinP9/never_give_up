from faker import Faker
import pytest
import requests
import uuid
from constants.constants import BASE_URL, REGISTER_ENDPOINT,LOGIN_URL
from custom_requester.custom_requester import CustomRequester
from entities.user import User
from utils.data_generator import DataGeneration
from clients.movies_api import MoviesAPI
from clients.api_manager import ApiManager
from resources.user_creds import SuperAdminCreds
from constants.roles import Roles
from models.model_test_user import RegisterUserRequest
fake = Faker()




@pytest.fixture
def test_user() -> RegisterUserRequest:
    """
    Фикстура возвращает валидированную модель пользователя.
    """

    random_password = DataGeneration.generate_random_password()

    return RegisterUserRequest(
        email=DataGeneration.generate_random_email(),
        fullName=DataGeneration.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER]
    )


@pytest.fixture(scope="function")
def registered_user(auth_requester, test_user: RegisterUserRequest):

    payload = test_user.model_dump(mode="json", exclude_unset=True)

    response = auth_requester.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=payload,
        expected_status=201
    )

    response_data = response.json()

    return {
        **payload,
        "id": response_data["id"]
    }

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

    def _create_user(role: Roles):

        password = DataGeneration.generate_random_password()

        user_model = RegisterUserRequest(
            email=DataGeneration.generate_random_email(),
            fullName=DataGeneration.generate_random_name(),
            password=password,
            passwordRepeat=password,
            roles=[role]
        )

        payload = user_model.model_dump(mode="json")

        auth_requester.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=payload,
            expected_status=201
        )

        client = MoviesAPI(session=requests.Session())
        client.authenticate(email=user_model.email, password=password)

        return client

    return _create_user

@pytest.fixture(scope="session")
def auth_requester():
    session = requests.Session()
    return CustomRequester(session=session, base_url=LOGIN_URL)


@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session)

    super_admin.api.auth_api.authenticate(
        super_admin.creds[0],
        super_admin.creds[1]
    )
    return super_admin



@pytest.fixture(scope="function")
def creation_user_data(test_user: RegisterUserRequest):
    return test_user.model_copy(
        update={
            "verified": True,
            "banned": False
        }
    )

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data: RegisterUserRequest):

    new_session = user_session()

    payload = creation_user_data.model_dump(mode="json")

    created_user = super_admin.api.auth_api.register_user(creation_user_data)

    common_user = User(
        created_user.email,
        creation_user_data.password,
        [Roles.USER.value],
        new_session
    )

    common_user.id = created_user.id
    common_user.api.auth_api.authenticate(
        common_user.creds[0],
        common_user.creds[1]
    )

    return common_user


@pytest.fixture
def admin_user(user_session, super_admin):

    new_session = user_session()

    password = DataGeneration.generate_random_password()

    user_model = RegisterUserRequest(
        email=DataGeneration.generate_random_email(),
        fullName=DataGeneration.generate_random_name(),
        password=password,
        passwordRepeat=password,
        roles=[Roles.ADMIN],
        verified=True,
        banned=False
    )

    created_user = super_admin.api.auth_api.register_user(user_model)

    admin = User(
        created_user.email,
        password,
        [Roles.ADMIN.value],
        new_session
    )

    admin.id = created_user.id

    admin.api.auth_api.authenticate(
        admin.creds[0],
        admin.creds[1]
    )

    return admin