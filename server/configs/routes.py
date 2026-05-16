import re

from controllers.banks.banks_controller import (get_banks_list, get_full_bank_info, get_nearest_branches_with_coords) 
from controllers.currency.currency_controller import (get_supported_currency_list, get_latest_currency_list, get_summary_nbu_rates)


ROUTES = [
    ("GET", re.compile(r"^/api/health?$"), lambda **_: ({"status":200, "response":{"status": "ok"}})),

    ("GET", re.compile(r"^/api/banks/banks_list?$"),  get_banks_list),
    ("GET", re.compile(r"^/api/banks?$"), get_full_bank_info),
    ("GET", re.compile(r"^/api/banks/nearest_branches?$"), get_nearest_branches_with_coords),

    ("GET", re.compile(r"^/api/currency/currency_list?$"), get_supported_currency_list),
    ("GET", re.compile(r"^/api/currency/latest_currency_list?$"), get_latest_currency_list),
    ("GET", re.compile(r"^/api/currency/summary_nbu_rates?$"), get_summary_nbu_rates)
]