import allure
import pytest

from utils.data_generator import DataGeneration


@allure.epic("Cinescope UI")
@allure.feature("Регистрация")
class TestRegistration:

    @allure.title("Успешная регистрация нового пользователя")
    @pytest.mark.ui
    def test_registration(self, register_page):
        password = DataGeneration.generate_random_password()

        with allure.step("Заполняем форму регистрации"):
            register_page.register(
                full_name=DataGeneration.generate_random_name(),
                email=DataGeneration.generate_random_email(),
                password=password,
            )