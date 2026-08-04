import time

from playwright.sync_api import Page

from pages.registration_page import RegistrationPage
from utils.data_generator import random_first_name, random_last_name, random_email, random_phone_number


def test_registration(page: Page):
    registration_page = RegistrationPage(page)
    registration_page.open()

    registration_page.fill_first_name(random_first_name())
    registration_page.fill_last_name(random_last_name())
    registration_page.fill_email(random_email())
    registration_page.type_phone_number(random_phone_number())

    registration_page.select_gender_male()
    registration_page.select_hobbies_sports_and_music()

    default_value = registration_page.get_default_dob_value()
    today_str = registration_page.today_formatted()
    assert default_value == today_str, (
        f"Дефолтная дата рождения ({default_value}) не равна сегодняшней ({today_str})"
    )

    registration_page.set_date_of_birth(month_label='March', year_value='1998', day='002')

    registration_page.fill_subject('Maths')

    registration_page.upload_picture(r'C:\Users\Admin\Desktop\KARTINKA.jpg')

    registration_page.fill_current_address('г. Москва, ул. Примерная, д. 1')

    registration_page.select_state('NCR')
    registration_page.select_city('Delhi')

    footer_text = registration_page.get_footer_text()

    assert "TOOLSQA.COM" in footer_text.upper(), f"Неожиданный текст футера: {footer_text}"

    registration_page.submit()

    time.sleep(2)
