import os
from dotenv import load_dotenv

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

        self.BASE_URL = os.getenv("BASE_URL", "https://example.com")

settings = Settings()
