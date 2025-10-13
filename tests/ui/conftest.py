from core.driver_factory import DriverFactory
import pytest
import allure
import os
from pathlib import Path
import selenium
import sys
import json
from core.logger import logging
from config.settings import settings

logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def driver(request):
    logger.info(f"Starting test: {request.node.name}")
    driver = DriverFactory.create_driver(browser=None)
    yield driver
    logger.info(f"Finished test: {request.node.name}")
    DriverFactory.quit_driver(driver)


@pytest.fixture(scope="session", autouse=True)
def attach_logs_to_allure():
    yield
    log_files = Path(settings.LOG_PATH).glob("*.log")
    for log_file in sorted(log_files, key=lambda x: x.stat().st_mtime, reverse=True):
        with open(log_file, 'r', encoding='utf-8') as f:
            allure.attach(
                f.read(),
                name=f"Log: {log_file.name}",
                attachment_type=allure.attachment_type.TEXT
            )
        break

@pytest.fixture(scope="session", autouse=True)
def environment_info():
    
    allure_results = settings.ALLURE_RESULTS_PATH
    allure_results.mkdir(exist_ok=True)
    
    env_properties = allure_results / "environment.properties"
    with open(env_properties, 'w') as f:
        f.write(f"Browser={settings.BROWSER}\n")
        f.write(f"Environment={settings.env}\n")
        f.write(f"Headless={settings.HEADLESS}\n")
        f.write(f"Python.Version={sys.version.split()[0]}\n")
        f.write(f"Selenium.Version={selenium.__version__}\n")

@pytest.fixture(scope="session", autouse=True)
def setup_allure_categories():
    allure_results = settings.ALLURE_RESULTS_PATH
    allure_results.mkdir(exist_ok=True)
    
    categories = [
        {
            "name": "Product defects",
            "matchedStatuses": ["failed"],
            "messageRegex": ".*AssertionError.*"
        },
        {
            "name": "Test defects",
            "matchedStatuses": ["broken"],
            "messageRegex": ".*"
        },
        {
            "name": "Timeout errors",
            "matchedStatuses": ["broken"],
            "messageRegex": ".*TimeoutException.*"
        },
        {
            "name": "Element not found",
            "matchedStatuses": ["broken"],
            "messageRegex": ".*NoSuchElementException.*"
        }
    ]
    
    categories_file = allure_results / "categories.json"
    with open(categories_file, 'w') as f:
        json.dump(categories, f, indent=2)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == 'call' and rep.failed:
        logger.error(f"Test FAILED: {item.name}")
        driver = item.funcargs.get('driver')
        if driver:
            logger.debug(f"Capturing screenshot and page source")
            allure.attach(
                driver.get_screenshot_as_png(),
                name='screenshot_on_failure',
                attachment_type=allure.attachment_type.PNG
            )
            
            allure.attach(
                driver.page_source,
                name='page_source',
                attachment_type=allure.attachment_type.HTML
            )
            
            allure.attach(
                driver.current_url,
                name='current_url',
                attachment_type=allure.attachment_type.TEXT
            )