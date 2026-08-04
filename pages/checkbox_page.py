from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class CheckBoxPage(BasePage):
    URL = 'https://demoqa.com/checkbox'

    def __init__(self, page: Page):
        super().__init__(page)
        self.home_label = page.get_by_text('Home', exact=True)
        self.desktop_label = page.get_by_text('Desktop', exact=True)
        self.toggle_button = page.locator('.rc-tree-switcher_close').first

    def expect_home_visible(self):
        expect(self.home_label).to_be_visible()

    def expect_desktop_hidden(self):
        expect(self.desktop_label).to_be_hidden()

    def expand_tree(self):
        self.toggle_button.click()

    def expect_desktop_visible(self):
        expect(self.desktop_label).to_be_visible()
