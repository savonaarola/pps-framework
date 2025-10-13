from config.settings import settings
import allure
from selenium import webdriver
from typing import Union

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException



class BasePage:
    def __init__(self, driver: Union[webdriver.Chrome, webdriver.Firefox, webdriver.Remote]):
        self.driver = driver
        self.timeout = settings.IMPLICIT_WAIT
        self.wait = WebDriverWait(self.driver, self.timeout)
    
    def find_element(self, locator, timeout=None):
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            raise 
    def find_elements(self, locator, timeout=None):
        wait_time = timeout or self.timeout
        try:
            elements = WebDriverWait(self.driver,wait_time).until(
                EC.presence_of_all_elements_located(locator)
            )
            return elements
        except TimeoutException:
            raise

    @allure.step("Clicking on element {locator}")
    def click(self, locator, timeout=None):
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable(locator)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
        except TimeoutException:
            raise

    @allure.step("Clicking on element {locator} using JavaScript")
    def click_js(self, locator, timeout=None):
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable(locator)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            self.driver.execute_script("arguments[0].click();", element)
        except TimeoutException:
            raise
    def to_be_clickable(self, locator, timeout=None):
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException:
            raise
    
    @allure.step("Getting text from element {locator}")
    def get_text(self,locator,timeout=None):
        element = self.find_element(locator, timeout)
        text = element.text
        return text
    
    def verify_url_contains(self, url_fragment, timeout=None):
        wait_time = timeout or self.timeout
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.url_contains(url_fragment)
            )
        except TimeoutException:
            current_url = self.driver.current_url
            raise AssertionError(
                f"Expected URL to contain '{url_fragment}', but current URL is '{current_url}'"
            )