from random import randint, choice


FIRST_NAMES = ['Валерий', 'Иван', 'Дмитрий', 'Ольга', 'Мария', 'Сергей']
LAST_NAMES = ['Жмышенко', 'Смирнов', 'Кузнецов', 'Иванова', 'Петрова']
DEPARTMENTS = ['QA', 'Development', 'Support', 'Management']


def random_first_name() -> str:
    return choice(FIRST_NAMES)


def random_last_name() -> str:
    return choice(LAST_NAMES)


def random_full_name() -> str:
    return f'{random_first_name()} {random_last_name()}'


def random_email() -> str:
    return f'test_{randint(1, 9999)}@email.qa'


def random_phone_number() -> str:
    return str(randint(7000000000, 7999999999))


def random_age(min_age: int = 18, max_age: int = 60) -> int:
    return randint(min_age, max_age)


def random_salary(min_salary: int = 10000, max_salary: int = 90000) -> int:
    return randint(min_salary, max_salary)


def random_department() -> str:
    return choice(DEPARTMENTS)
