import requests

from configs.general_constants import DEFAULT_REQUEST_TIMEOUT

NBU_URL = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"

def fetch_nbu_rates() -> list[dict]:
    params = {"json": ""}

    response = requests.get(NBU_URL, params=params, timeout=DEFAULT_REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json()