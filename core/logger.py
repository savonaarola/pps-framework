import logging
from pathlib import Path
from datetime import datetime
from config.settings import settings
import os
import uuid

LOG_DIR = Path(settings.LOG_PATH)

def configure_logging():
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    log_level_str = settings.LOG_LEVEL.upper()
    log_level = getattr(logging,log_level_str,logging.INFO)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    if root_logger.handlers:
        return
    
    console_fmt = logging.Formatter(settings.LOG_FORMAT_CONSOLE)
    file_fmt = logging.Formatter(settings.LOG_FORMAT_FILE)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_fmt)
    console_handler.setLevel(log_level)

    log_file = LOG_DIR / f"run_{settings.env}_{datetime.now():%Y%m%d_%H%M%S}_{os.getpid()}_{uuid.uuid4().hex[:6]}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(file_fmt)
    file_handler.setLevel(logging.DEBUG)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    root_logger.info(f"Logging configured | Level: {log_level_str} | File: {log_file.name}")

configure_logging()

    