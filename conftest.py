import uuid
import pytest
import requests
from faker import Faker
from sqlalchemy.orm import Session

from constants.constants import BASE_URL, REGISTER_ENDPOINT, LOGIN_URL, LOGIN_ENDPOINT
from custom_requester.custom_requester import CustomRequester
from entities.user import User
from utils.data_generator import DataGeneration
from clients.movies_api import MoviesAPI
from clients.api_manager import ApiManager
from resources.user_creds import SuperAdminCreds
from constants.roles import Roles
from models.model_test_user import RegisterUserRequest, RegisterUserResponse
from db_requester.db_client import get_db_session
from db_requester.db_helpers import DBHelper

fake = Faker()


@pytest.fixture
def test_user() -> RegisterUserRequest:
    random_password = DataGeneration.generate_random_password()
    return RegisterUserRequest(
        email=DataGeneration.generate_random_email(),
        fullName=DataGeneration.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER],
    )


@pytest.fixture(scope="function")
def registered_user(auth_requester, test_user: RegisterUserRequest):
    payload = test_user.model_dump(mode="json", exclude_unset=True)

    created_user = auth_requester.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=payload,
        expected_status=201,
        success_model=RegisterUserResponse,
    )

    return {
        **payload,
        "id": created_user.id,
    }


@pytest.fixture(scope="session")
def requester():
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)


@pytest.fixture(scope="session")
def movies_api(requester):
    client = MoviesAPI(session=requester.session)
    client.authenticate(email="api1@gmail.com", password="asdqwe123Q")
    return client


@pytest.fixture
def random_movie():
    unique_suffix = uuid.uuid4().hex[:10]
    return {
        "name": f"{fake.sentence(nb_words=2).rstrip('.')} {unique_suffix}",
        "description": fake.text(max_nb_chars=80),
        "price": 499,
        "location": "SPB",
        "published": True,
        "genreId": 1,
    }


@pytest.fixture
def created_movie(movies_api, random_movie):
    return movies_api.create_movie(
        random_movie,
        expected_status=201,
    )


@pytest.fixture
def created_movie_with_cleanup(movies_api, created_movie):
    movie = created_movie
    yield movie
    movies_api.delete_movie(
        movie.id,
        expected_status=200,
    )


@pytest.fixture
def unauthorized_movies_api():
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
            roles=[role],
        )

        auth_requester.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=user_model.model_dump(mode="json"),
            expected_status=201,
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
        manager = ApiManager(session)
        user_pool.append(manager)
        return manager

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session,
    )

    admin.api.auth_api.authenticate(admin.creds[0], admin.creds[1])
    return admin


@pytest.fixture(scope="function")
def creation_user_data(test_user: RegisterUserRequest):
    return test_user.model_copy(
        update={
            "verified": True,
            "banned": False,
        }
    )


@pytest.fixture
def common_user(user_session, super_admin, creation_user_data: RegisterUserRequest):
    new_session = user_session()

    created_user = super_admin.api.auth_api.register_user(creation_user_data)

    user = User(
        created_user.email,
        creation_user_data.password,
        [Roles.USER.value],
        new_session,
    )

    user.id = created_user.id
    user.api.auth_api.authenticate(user.creds[0], user.creds[1])
    return user


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
        banned=False,
    )

    created_user = super_admin.api.auth_api.register_user(user_model)

    admin = User(
        created_user.email,
        password,
        [Roles.ADMIN.value],
        new_session,
    )

    admin.id = created_user.id
    admin.api.auth_api.authenticate(admin.creds[0], admin.creds[1])
    return admin


@pytest.fixture
def login_response(auth_requester, registered_user):
    return auth_requester.send_request(
        method="POST",
        endpoint=LOGIN_ENDPOINT,
        data={
            "email": registered_user["email"],
            "password": registered_user["password"],
        },
        expected_status=200,
    )


@pytest.fixture(scope="module")
def db_session() -> Session:
    session = get_db_session()
    yield session
    session.close()


@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    return DBHelper(db_session)


@pytest.fixture(scope="function")
def created_test_user(db_helper):
    user = db_helper.create_test_user(DataGeneration.generate_user_data())
    yield user
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)