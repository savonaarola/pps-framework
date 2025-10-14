import pytest
from config.settings import settings
import allure
from pathlib import Path
import json
from core.logger import logging

logger = logging.getLogger(__name__)


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
            "messageRegex": ".*TimeoutException.*|.*ReadTimeout.*|.*ConnectTimeout.*"
        },
        {
            "name": "Element not found (UI)",
            "matchedStatuses": ["broken"],
            "messageRegex": ".*NoSuchElementException.*"
        },
        {
            "name": "API errors",
            "matchedStatuses": ["failed", "broken"],
            "messageRegex": ".*HTTPStatusError.*|.*HTTPError.*|.*ConnectError.*"
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
        
        # UI ТЕСТЫ
        driver = item.funcargs.get('driver')
        if driver:
            logger.debug(f"UI test failure - capturing screenshot and page source")
            
            try:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name='Screenshot on Failure',
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                logger.warning(f"Failed to capture screenshot: {e}")
            
            try:
                allure.attach(
                    driver.page_source,
                    name='Page Source',
                    attachment_type=allure.attachment_type.HTML
                )
            except Exception as e:
                logger.warning(f"Failed to capture page source: {e}")
            
            try:
                allure.attach(
                    driver.current_url,
                    name='Current URL',
                    attachment_type=allure.attachment_type.TEXT
                )
            except Exception as e:
                logger.warning(f"Failed to capture current URL: {e}")
        
        # API ТЕСТЫ
        http_client = item.funcargs.get('http_client')
        last_response = item.funcargs.get('last_response')
        
        if http_client or last_response:
            logger.debug(f"API test failure - attempting to capture request/response")
            
            if last_response:
                try:
                    request_info = (
                        f"Method: {last_response.request.method}\n"
                        f"URL: {last_response.request.url}\n"
                        f"Headers: {dict(last_response.request.headers)}\n"
                    )
                    if last_response.request.content:
                        request_info += f"\nBody:\n{last_response.request.content.decode('utf-8')}"
                    
                    allure.attach(
                        request_info,
                        name='Request',
                        attachment_type=allure.attachment_type.TEXT
                    )
                except Exception as e:
                    logger.warning(f"Failed to capture request: {e}")
                
                try:
                    response_info = (
                        f"Status Code: {last_response.status_code}\n"
                        f"Headers: {dict(last_response.headers)}\n"
                        f"\nBody:\n{last_response.text}"
                    )
                    
                    allure.attach(
                        response_info,
                        name='Response',
                        attachment_type=allure.attachment_type.TEXT
                    )
                except Exception as e:
                    logger.warning(f"Failed to capture response: {e}")