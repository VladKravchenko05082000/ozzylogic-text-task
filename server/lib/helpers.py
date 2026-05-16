import logging
from pathlib import Path

from configs.regex import EMAIL_RE
from configs.general_constants import SECOND_MULTIPLIER_CONFIG

from configs.types import TimeUnit
from logging import Logger 

LOGS_DIR = Path(__file__).parent.parent / "logs"

_loggers: dict[str, Logger] = {}


def get_file_logger(filename: str) -> Logger:
    if filename in _loggers:
        return _loggers[filename]

    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(filename)
    logger.setLevel(logging.ERROR)
    logger.propagate = False

    handler = logging.FileHandler(LOGS_DIR / filename, encoding="utf-8")
    handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    )

    logger.addHandler(handler)
    _loggers[filename] = logger

    return logger



def validate_type(value, expected_type, param_name: str, logger: Logger):
    if not isinstance(value, expected_type):
        logger.error(
            "Argument %s must be %s, got %s (value: %r)",
            param_name,
            expected_type.__name__,
            type(value).__name__,
            value,
        )
        return False
    return True

def format_seconds_to_define_unit(interval: float, unit: TimeUnit = "minute"):
    multiplier = SECOND_MULTIPLIER_CONFIG.get(unit)
    return interval * multiplier


def parse_list_param(value):
    if not value:
        return None
    return [v.strip() for v in value.split(",") if v.strip()]

def validate_email(email: str) -> str:
    email = (email or "").strip().lower()
    if not EMAIL_RE.match(email):
        raise ValueError("invalid email")
    return email