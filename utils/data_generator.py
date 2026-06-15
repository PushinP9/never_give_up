import random
import string
import datetime
from faker import Faker

faker = Faker()


class DataGeneration:

    @staticmethod
    def generate_random_email():
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"kek{random_string}@gmail.com"

    @staticmethod
    def generate_random_name():
        return f"{faker.first_name()} {faker.last_name()}"

    @staticmethod
    def generate_random_int(length: int = 10) -> int:
        if length < 1:
            raise ValueError("length must be >= 1")
        lower_bound = 10 ** (length - 1)
        upper_bound = (10 ** length) - 1
        return random.randint(lower_bound, upper_bound)

    @staticmethod
    def generate_random_int(length: int = 10) -> int:
        if length < 1:
            raise ValueError("length must be >= 1")
        lower_bound = 10 ** (length - 1)
        upper_bound = (10 ** length) - 1
        return random.randint(lower_bound, upper_bound)

    @staticmethod
    def generate_random_password():
        """
        Генерация пароля, соответствующего требованиям:
        - Минимум 1 буква.
        - Минимум 1 цифра.
        - Допустимые символы.
        - Длина от 8 до 20 символов.
        """
        letter = random.choice(string.ascii_letters)
        digit = random.choice(string.digits)

        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18)
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

        password = list(letter + digit + remaining_chars)
        random.shuffle(password)

        return ''.join(password)

    @staticmethod
    def generate_user_data() -> dict:
        """Генерирует данные для тестового пользователя"""
        from uuid import uuid4

        return {
            'id': f'{uuid4()}',  # генерируем UUID как строку
            'email': DataGeneration.generate_random_email(),
            'full_name': DataGeneration.generate_random_name(),
            'password': DataGeneration.generate_random_password(),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
            'verified': False,
            'banned': False,
            'roles': '{USER}'
        }


