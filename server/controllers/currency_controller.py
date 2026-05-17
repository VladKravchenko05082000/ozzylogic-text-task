from models.rate_models import (get_all_currency, get_latest_rates, get_nbu_latest, get_average_rates, get_rates_history_model)

from lib.helpers import parse_list_param

from configs.general_constants import (SUPPORTED_CURRENCIES, SUPPORTED_BANKS)
from configs.regex import DATE_ONLY_RE

def _filter_supported(items: list | None, supported: list) -> list | None:
    if not items:
        return items
    return [x for x in items if x in supported]

def get_supported_currency_list(*, query, **_):
    currency_list = get_all_currency()
    return {
        "status": 200,
        "response": {
            "currency_list": currency_list
        }
    }

def get_latest_currency_list(*, query, **_):
    banks = parse_list_param(query.get("banks"))
    currencies = parse_list_param(query.get("currencies"))

    banks = _filter_supported(banks, SUPPORTED_BANKS)
    currencies = _filter_supported(currencies, SUPPORTED_CURRENCIES)

    latest_rates =  get_latest_rates(banks=banks, currencies=currencies)   

    return {
        "status": 200,
        "response": {
            "total": len(latest_rates),
            "latest_rates": latest_rates
        }
    }

def get_summary_nbu_rates(*, query, **_):
    nbu_latest_rates = get_nbu_latest()
    average_banks_rates = get_average_rates()

    return {
        "status": 200,
        "response": {
            "nbu_latest_rates": nbu_latest_rates,
            "average_banks_rates": average_banks_rates
        }
    }

def get_rates_history(*, query, **_):
    currencies_param = parse_list_param(query.get("currencies"))
    if not currencies_param:
        raise ValueError("currency is required")
    valid_currencies = _filter_supported(currencies_param, SUPPORTED_CURRENCIES)
    if not valid_currencies:
        raise ValueError("unsupported currency")
    currency = valid_currencies[0]

    date_from = query.get("from")
    date_to = query.get("to")
    if not (date_from and date_to):
        raise ValueError("from and to are required")
    if DATE_ONLY_RE.match(date_from):
        date_from += " 00:00:00"
    if DATE_ONLY_RE.match(date_to):
        date_to += " 23:59:59"

    rates_history = get_rates_history_model(
                currency, query.get("bank"), date_from, date_to
            )   

    return {
        "status":200,
        "response":{
            "total": len(rates_history),
            "history": rates_history
        }
    }
