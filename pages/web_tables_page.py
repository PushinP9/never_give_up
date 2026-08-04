from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class WebTablesPage(BasePage):
    URL = 'https://demoqa.com/webtables'

    def __init__(self, page: Page):
        super().__init__(page)
        self.add_button = page.locator('#addNewRecordButton')
        self.registration_form = page.locator('.modal-content')
        self.form_title = self.registration_form.locator('.modal-title')

        self.first_name_input = page.locator('#firstName')
        self.last_name_input = page.locator('#lastName')
        self.email_input = page.locator('#userEmail')
        self.age_input = page.locator('#age')
        self.salary_input = page.locator('#salary')
        self.department_input = page.locator('#department')
        self.submit_button = page.locator('#submit')

    def open_add_form(self):
        self.add_button.click()

    def expect_form_opened(self):
        expect(self.registration_form).to_be_visible()
        expect(self.form_title).to_have_text('Registration Form')

    def fill_form(self, first_name: str, last_name: str, email: str,
                  age: int, salary: int, department: str):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.email_input.fill(email)
        self.age_input.fill(str(age))
        self.salary_input.fill(str(salary))
        self.department_input.fill(department)

    def submit(self):
        self.submit_button.click()

    def expect_form_closed(self):
        expect(self.registration_form).to_be_hidden()
