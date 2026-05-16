import requests

from configs.general_constants import DEFAULT_REQUEST_TIMEOUT

FINANCE_URL = "https://finance.ua"


def finance_ua_fetch_banks_list() -> list[dict]:
    params = {"locale": "uk"}

    response = requests.get(
        f"{FINANCE_URL}/banks/api/organizationsList",
        params=params,
        timeout=DEFAULT_REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def finance_ua_fetch_branches(bank_slug: str) -> list[dict]:
    params = {"slug": bank_slug, "locale": "uk"}
    
    response = requests.get(
        f"{FINANCE_URL}/api/organization/v1/branches",
        params=params,
        timeout=DEFAULT_REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()

