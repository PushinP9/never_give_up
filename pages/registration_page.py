from datetime import date

from playwright.sync_api import Page

from pages.base_page import BasePage


class RegistrationPage(BasePage):
    URL = 'https://demoqa.com/automation-practice-form'

    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name_input = page.locator('#firstName')
        self.last_name_input = page.locator('#lastName')
        self.email_input = page.locator('#userEmail')
        self.phone_input = page.locator('#userNumber')

        self.gender_male_label = page.locator("label[for='gender-radio-1']")

        self.hobby_sports_label = page.locator("label[for='hobbies-checkbox-1']")
        self.hobby_music_label = page.locator("label[for='hobbies-checkbox-3']")

        self.dob_input = page.locator('#dateOfBirthInput')
        self.month_select = page.locator('.react-datepicker__month-select')
        self.year_select = page.locator('.react-datepicker__year-select')

        self.subjects_input = page.locator('#subjectsInput')

        self.upload_picture_input = page.locator('#uploadPicture')

        self.current_address_input = page.locator('#currentAddress')

        self.state_dropdown = page.locator('#state')
        self.city_dropdown = page.locator('#city')

        self.footer = page.locator('footer')

        self.submit_button = page.locator('#submit')

    def fill_first_name(self, value: str):
        self.first_name_input.fill(value)

    def fill_last_name(self, value: str):
        self.last_name_input.fill(value)

    def fill_email(self, value: str):
        self.email_input.fill(value)

    def type_phone_number(self, value: str):
        self.phone_input.type(value)

    def select_gender_male(self):
        self.gender_male_label.click()

    def select_hobbies_sports_and_music(self):
        self.hobby_sports_label.click()
        self.hobby_music_label.click()

    def get_default_dob_value(self) -> str:
        return self.dob_input.get_attribute('value')

    @staticmethod
    def today_formatted() -> str:
        return date.today().strftime('%d %b %Y')

    def set_date_of_birth(self, month_label: str, year_value: str, day: str):
        self.dob_input.click()
        self.month_select.select_option(label=month_label)
        self.year_select.select_option(value=year_value)
        self.page.click(
            f".react-datepicker__day--{day}:not(.react-datepicker__day--outside-month)"
        )

    def fill_subject(self, subject: str):
        self.subjects_input.type(subject)
        self.page.keyboard.press('Enter')

    def upload_picture(self, file_path: str):
        self.upload_picture_input.set_input_files(file_path)

    def fill_current_address(self, value: str):
        self.current_address_input.fill(value)

    def select_state(self, state_name: str):
        self.state_dropdown.click()
        self.page.get_by_text(state_name, exact=True).click()

    def select_city(self, city_name: str):
        self.city_dropdown.click()
        self.page.get_by_text(city_name, exact=True).click()

    def get_footer_text(self) -> str:
        return self.footer.inner_text().strip()

    def submit(self):
        self.submit_button.scroll_into_view_if_needed()
        self.submit_button.click(force=True)
