import os
from dotenv import load_dotenv
import sys
from pathlib import Path

load_dotenv()

class Settings:
    def __init__(self, env: str = None):
        self.env = env or os.getenv("ENV", "dev")

        self.BROWSER = os.getenv("BROWSER", "chrome")
        self.HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
        self.IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "10"))
        self.PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))
        self.WINDOW_HEIGHT = int(os.getenv("WINDOW_HEIGHT", "1080"))
        self.WINDOW_WIDTH = int(os.getenv("WINDOW_WIDTH", "1920"))
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_PATH = os.getenv("LOG_PATH", "reports/logs")
        self.LOG_FORMAT_CONSOLE = '%(asctime)s | %(levelname)s | %(message)s'
        self.LOG_FORMAT_FILE = '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
        self.ALLURE_RESULTS_PATH = Path(os.getenv("ALLURE_RESULTS_PATH", "reports/allure-results"))
        self.BASE_URL = os.getenv("BASE_URL", "https://example.com")

settings = Settings()
