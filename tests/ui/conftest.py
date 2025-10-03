from core.driver_factory import DriverFactory
import pytest





@pytest.fixture(scope="function")
def driver():
    driver = DriverFactory.create_driver(browser=None)
    yield driver
    DriverFactory.quit_driver(driver)


