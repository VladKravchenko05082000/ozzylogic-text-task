import os
from dotenv import load_dotenv

load_dotenv()

SUPPORTED_CURRENCIES = ["USD", "EUR", "GBP", "CHF", "PLN"];

SUPPORTED_BANKS = [
  "privatbank",
  "monobank",
  "oschadbank",
  "raiffeisen-bank-aval",
  "ukrsibbank",
];

SECOND_MULTIPLIER_CONFIG = {
    "second": 1,
    "minute": 60,
    "hour": 3600
}

DEFAULT_REQUEST_TIMEOUT = 15

RATES_INTERVAL_MINUTES_TIME = 30
BANKS_UPDATE_INTERVAL_HOURS = 12

JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_TTL_MIN = 15
REFRESH_TOKEN_TTL_DAYS = 30

BCRYPT_ROUNDS = 12

user_login_RATE_LIMIT = (5, 300)
