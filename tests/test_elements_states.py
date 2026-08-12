from playwright.sync_api import Page

from pages.radio_button_page import RadioButtonPage
from pages.checkbox_page import CheckBoxPage
from pages.dynamic_properties_page import DynamicPropertiesPage


def test_radio_button_states(page: Page):
    radio_button_page = RadioButtonPage(page)
    radio_button_page.open()

    radio_button_page.expect_yes_enabled()
    radio_button_page.expect_impressive_enabled()
    radio_button_page.expect_no_disabled()


def test_checkbox_visibility(page: Page):
    checkbox_page = CheckBoxPage(page)
    checkbox_page.open()

    checkbox_page.expect_home_visible()
    checkbox_page.expect_desktop_hidden()

    checkbox_page.expand_tree()

    checkbox_page.expect_desktop_visible()


def test_dynamic_properties_appearance(page: Page):
    dynamic_properties_page = DynamicPropertiesPage(page)
    dynamic_properties_page.open()

    dynamic_properties_page.expect_visible_after_absent()

    dynamic_properties_page.wait_for_visible_after()

    dynamic_properties_page.expect_visible_after_visible()
