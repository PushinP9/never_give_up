from http.client import responses

import pytest
import requests
from Tools.scripts.fixdiv import report

from constants import BASE_URL, HEADERS, LOGIN_ENDPOINT


"""@pytest.fixture
def login_response(test_user,auth_session):
    login_url = f'{BASE_URL}{LOGIN_ENDPOINT}'
    login_data = {
        "email": test_user["email"],
        "password": test_user["password"]
    }
    response = requests.post(login_url, json=login_data, headers=HEADERS)
    return response
"""

class TestLoginSuccess:

    def test_status_code(self, login_response):
        assert login_response.status_code == 200

    def test_has_access_token(self,login_response):
        data = login_response.json()
        assert "accessToken" in data, "Нет поля accessToken"
        assert len(data["accessToken"]) > 0, "accessToken пустой"

    def test_has_user_with_email(self,login_response, test_user):
        data = login_response.json()
        assert  "user" in data, "Нет поля user"
        assert data["user"]["email"] == test_user["email"], "Email не совпадает"



class TestLoginNegative:

    def test_login_wrong_password(self, test_user):
        login_url = f'{BASE_URL}{LOGIN_ENDPOINT}'
        login_data = {
            "email": test_user["email"],
            "password": "password123qwe"
        }

        response = requests.post(login_url, json=login_data, headers=HEADERS)
        assert response.status_code in [401, 403]

    def test_login_wrong_email(self,test_user):
        login_url = f'{BASE_URL}{LOGIN_ENDPOINT}'
        login_data = {
            "email": "123qwe@gmail.com",
            "password": test_user["password"]
        }
        response = requests.post(login_url, json=login_data, headers=HEADERS)
        assert response.status_code in [401,403,404]

    def test_login_empty_email(self):
        login_url = f'{BASE_URL}{LOGIN_ENDPOINT}'
        login_data = {
            "email": "",
            "password": "password"
        }

        response = requests.post(login_url,json=login_data, headers=HEADERS)
        assert response.status_code in [400, 401,]

    def test_login_empty_password(self,test_user):
        login_url = f'{BASE_URL}{LOGIN_ENDPOINT}'
        login_data = {
            "email": test_user["email"],
            "password": ""
        }

        response = requests.post(login_url,json=login_data, headers=HEADERS)
        assert response.status_code in [400, 401,]