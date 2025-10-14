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


