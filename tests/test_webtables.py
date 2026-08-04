from playwright.sync_api import Page

from pages.web_tables_page import WebTablesPage
from utils.data_generator import (
    random_first_name, random_last_name, random_email,
    random_age, random_salary, random_department
)


def test_add_new_record(page: Page):
    web_tables_page = WebTablesPage(page)

    web_tables_page.open()
    web_tables_page.open_add_form()
    web_tables_page.expect_form_opened()

    web_tables_page.fill_form(
        first_name=random_first_name(),
        last_name=random_last_name(),
        email=random_email(),
        age=random_age(),
        salary=random_salary(),
        department=random_department(),
    )

    web_tables_page.submit()
    web_tables_page.expect_form_closed()
