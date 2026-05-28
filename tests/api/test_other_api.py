import pytest
from http import HTTPStatus
from utils.data_generator import DataGeneration
from db_models.db_transaction import AccountTransactionTemplate
from sqlalchemy.orm import Session
import allure
from constants.constants import LOGIN_ENDPOINT


class TestLoginSuccess:

    def test_status_code(self, login_response):
        assert login_response.status_code == HTTPStatus.OK

    def test_has_access_token(self, login_response):
        data = login_response.json()

        assert "accessToken" in data
        assert len(data["accessToken"]) > 0

    def test_has_user_with_email(self, login_response, test_user):
        data = login_response.json()

        assert "user" in data
        assert data["user"]["email"] == test_user.email


class TestLoginNegative:

    @pytest.mark.parametrize(
        "email, password, expected_status",
        [
            ("wrong@email.com", "Password123", HTTPStatus.UNAUTHORIZED),
            ("", "Password123", HTTPStatus.UNAUTHORIZED),
            ("valid@email.com", "", HTTPStatus.UNAUTHORIZED),
        ]
    )
    def test_login_negative_cases(
        self,
        auth_requester,
        test_user,
        email,
        password,
        expected_status
    ):
        login_data = {
            "email": email if email != "valid@email.com" else test_user.email,
            "password": password if password != "Password123" else test_user.password
        }

        response = auth_requester.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )

        assert response.status_code == expected_status

@allure.epic("Тестирование транзакций")
@allure.feature("Тестирование транзакций между счетами")
class TestAccountTransactionTemplate:

    @allure.story("Недостаточно средств при переводе между двумя счетами")
    @allure.description("""
    Этот тест проверяет, что при недостатке средств перевод не выполняется,
    а балансы в базе данных остаются без изменений.
    Шаги:
    1. Создание двух счетов: Stan и Bob.
    2. Попытка перевода 200 единиц от Stan к Bob при балансе Stan = 100.
    3. Проверка ошибки о недостатке средств.
    4. Проверка неизменности балансов в БД.
    5. Очистка тестовых данных.
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Ivan Petrovich")
    @allure.title("Тест: перевод отклоняется при недостатке средств")
    def test_accounts_transaction_template(self, db_session: Session):
        with allure.step("Создание тестовых данных в базе данных: счета Stan и Bob"):
            stan = AccountTransactionTemplate(
                user=f"Stan_{DataGeneration.generate_random_int(10)}",
                balance=100
            )
            bob = AccountTransactionTemplate(
                user=f"Bob_{DataGeneration.generate_random_int(10)}",
                balance=500
            )
            db_session.add_all([stan, bob])
            db_session.commit()

        @allure.step("Функция перевода денег: transfer_money")
        def transfer_money(session, from_account, to_account, amount):
            from_account = session.query(AccountTransactionTemplate).filter_by(user=from_account).one()
            to_account = session.query(AccountTransactionTemplate).filter_by(user=to_account).one()

            if from_account.balance < amount:
                raise ValueError("Недостаточно средств на счете")

            from_account.balance -= amount
            to_account.balance += amount
            session.commit()

        try:
            with allure.step("Проверяем начальные балансы"):
                assert stan.balance == 100
                assert bob.balance == 500

            with allure.step("Пытаемся выполнить перевод 200 единиц от Stan к Bob"):
                with pytest.raises(ValueError, match="Недостаточно средств на счете"):
                    transfer_money(db_session, from_account=stan.user, to_account=bob.user, amount=200)

            with allure.step("Проверяем, что балансы в базе данных не изменились"):
                db_stan = db_session.query(AccountTransactionTemplate).filter_by(user=stan.user).one()
                db_bob = db_session.query(AccountTransactionTemplate).filter_by(user=bob.user).one()

                assert db_stan.balance == 100
                assert db_bob.balance == 500
                assert stan.balance == 100
                assert bob.balance == 500

        finally:
            with allure.step("Удаляем данные для тестирования из базы"):
                db_session.delete(stan)
                db_session.delete(bob)
                db_session.commit()