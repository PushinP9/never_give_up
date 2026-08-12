import allure
import pytest


@allure.epic("Cinescope UI")
@allure.feature("Авторизация")
class TestLogin:

    @allure.title("Успешный вход ранее зарегистрированным пользователем")
    @pytest.mark.ui
    def test_login(self, login_page, common_user):

        with allure.step("Вводим email и пароль зарегистрированного пользователя"):
            login_page.login(
                email=common_user.email,
                password=common_user.password,
            )

        with allure.step("Проверяем редирект на главную страницу"):
            login_page.expect_redirect_to_main_page()

        with allure.step("Проверяем появление уведомления об успешном входе"):
            login_page.expect_success_notification()