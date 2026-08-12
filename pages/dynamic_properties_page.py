from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class DynamicPropertiesPage(BasePage):
    URL = 'https://demoqa.com/dynamic-properties'
    VISIBLE_AFTER_SELECTOR = '#visibleAfter'

    def __init__(self, page: Page):
        super().__init__(page)
        self.visible_after_button = page.locator(self.VISIBLE_AFTER_SELECTOR)

    def expect_visible_after_absent(self):
        expect(self.visible_after_button).to_have_count(0)

    def wait_for_visible_after(self, timeout: int = 6000):
        self.page.wait_for_selector(self.VISIBLE_AFTER_SELECTOR, timeout=timeout)

    def expect_visible_after_visible(self):
        expect(self.visible_after_button).to_be_visible()
