from pages.login_page import LoginPage
import pytest
import allure


@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Login without credentials shows error")
@pytest.mark.ui
def test_login_with_no_credentials(driver):
    driver.get("https://www.saucedemo.com/")

    login_page = LoginPage(driver)
    login_page.click_login_button()
    error_text = login_page.get_error_message()

    assert error_text == "Epic sadface: Username is required"