from selenium import webdriver

from config.settings import settings
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from core.logger import logging

logger = logging.getLogger(__name__)



class DriverFactory:
    

    @staticmethod
    def create_driver(browser: str):
        browser_name = (browser or settings.BROWSER).lower()
        logger.info(f"Creating {browser_name} driver")
        if browser_name == "chrome":
            driver = DriverFactory._create_chrome_driver()
        elif browser_name == "firefox":
            driver = DriverFactory._create_firefox_driver()
        else:
            logger.error(f"Unsupported browser: {browser_name}")
            raise ValueError(f"Unsupported browser: {browser_name}")
        
        driver.implicitly_wait(settings.IMPLICIT_WAIT)
        driver.set_page_load_timeout(settings.PAGE_LOAD_TIMEOUT)
        driver.maximize_window()
        logger.info(f"{browser_name.capitalize()} driver created successfully")
        return driver
    
    @staticmethod
    def _create_chrome_driver():
        chrome_options = ChromeOptions()

        chrome_options.add_argument(f"--window-size={settings.WINDOW_WIDTH},{settings.WINDOW_HEIGHT}")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        
        if settings.HEADLESS:
            chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(options=chrome_options)
        return driver
    
    @staticmethod
    def _create_firefox_driver():
        firefox_options = FirefoxOptions()

        firefox_options.add_argument(f"--width={settings.WINDOW_WIDTH}")
        firefox_options.add_argument(f"--height={settings.WINDOW_HEIGHT}")

        if settings.HEADLESS:
            firefox_options.add_argument("--headless")

        driver = webdriver.Firefox(options=firefox_options)
        return driver

    @staticmethod
    def quit_driver(driver):
        try:
            if driver:
                driver.quit()
        except Exception as e:
            raise e