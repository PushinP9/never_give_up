from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from constants.constants import UI_BASE_URL, UI_REGISTER_PATH


class CinescopeRegisterPage(BasePage):
    URL = UI_BASE_URL + UI_REGISTER_PATH

    def __init__(self, page: Page):
        super().__init__(page)
        self.full_name_input = page.locator('[data-qa-id="register_full_name_input"]')
        self.email_input = page.locator('[data-qa-id="register_email_input"]')
        self.password_input = page.locator('[data-qa-id="register_password_input"]')
        self.password_repeat_input = page.locator('[data-qa-id="register_password_repeat_input"]')
        self.submit_button = page.locator('[data-qa-id="register_submit_button"]')

    def register(self, full_name: str, email: str, password: str):
        self.full_name_input.fill(full_name)
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.password_repeat_input.fill(password)
        self.submit_button.click()