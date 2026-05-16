from models.rate_models import (get_all_currency, get_latest_rates, get_nbu_latest, get_average_rates)
from lib.helpers import parse_list_param
from configs.general_constants import SUPPORTED_CURRENCIES, SUPPORTED_BANKS

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

    if banks:
        valid_banks = [b for b in banks if b in SUPPORTED_BANKS]
        if not valid_banks:
            banks = []
        else:    
            banks = valid_banks
        

    if currencies:
        valid_currencies = [c for c in currencies if c in SUPPORTED_CURRENCIES]
        if not valid_currencies:
            currencies = []
        else:    
            currencies = valid_currencies

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