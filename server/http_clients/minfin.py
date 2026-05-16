import requests

from configs.general_constants import DEFAULT_REQUEST_TIMEOUT

MINFIN_URL = "https://minfin.com.ua/api"

def min_fin_fetch_currency_list() -> list[dict]:
    params = {"type": "money", "locale": "uk"}

    response = requests.get(
        f"{MINFIN_URL}/currency/list",
        params=params,
        timeout=DEFAULT_REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def min_fin_fetch_bank_rates(currency_code: str, date, page=1, cpp = 20) -> list[dict]:
    params = {
        "date":date,
        "page": page,
        "cpp": cpp 
    }

    response = requests.get(
        f"{MINFIN_URL}/currency/rates/banks/{currency_code.lower()}",
        params=params,
        timeout=DEFAULT_REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()