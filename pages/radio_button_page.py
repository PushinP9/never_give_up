from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class RadioButtonPage(BasePage):
    URL = 'https://demoqa.com/radio-button'

    def __init__(self, page: Page):
        super().__init__(page)
        self.yes_radio = page.locator('#yesRadio')
        self.impressive_radio = page.locator('#impressiveRadio')
        self.no_radio = page.locator('#noRadio')

    def expect_yes_enabled(self):
        expect(self.yes_radio).to_be_enabled()

    def expect_impressive_enabled(self):
        expect(self.impressive_radio).to_be_enabled()

    def expect_no_disabled(self):
        expect(self.no_radio).to_be_disabled()
