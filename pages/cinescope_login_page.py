from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from constants.constants import UI_BASE_URL, UI_LOGIN_PATH


class CinescopeLoginPage(BasePage):
    URL = UI_BASE_URL + UI_LOGIN_PATH

    def __init__(self, page: Page):
        super().__init__(page)
        self.email_input = page.locator('[data-qa-id="login_email_input"]')
        self.password_input = page.locator('[data-qa-id="login_password_input"]')
        self.submit_button = page.locator('[data-qa-id="login_submit_button"]')

    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()

    def expect_redirect_to_main_page(self):
        expect(self.page).to_have_url(UI_BASE_URL + '/', timeout=10000)

    def expect_success_notification(self):
        notification = self.page.locator('[data-qa-id="notification"]')
        expect(notification).to_be_visible()