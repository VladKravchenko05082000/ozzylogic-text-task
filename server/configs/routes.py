import re

from controllers.banks_controller import (get_banks_list, get_full_bank_info, get_nearest_branches_with_coords) 
from controllers.currency_controller import (get_supported_currency_list, get_latest_currency_list, get_summary_nbu_rates, get_rates_history)
from controllers.session.auth.auth_controller import (user_register, user_login)
from controllers.session.tokens.tokens_controller import (refresh, logout_from_session)
from controllers.user_controller import (get_me, update_user_profile, change_password)


ROUTES = [
    ("GET", re.compile(r"^/api/health?$"), lambda **_: ({"status":200, "response":{"status": "ok"}})),

    ("GET", re.compile(r"^/api/banks/banks-list?$"),  get_banks_list),
    ("GET", re.compile(r"^/api/banks?$"), get_full_bank_info),
    ("GET", re.compile(r"^/api/banks/nearest-branches?$"), get_nearest_branches_with_coords),

    ("GET", re.compile(r"^/api/currency/currency-list?$"), get_supported_currency_list),
    ("GET", re.compile(r"^/api/currency/latest-currency_list?$"), get_latest_currency_list),
    ("GET", re.compile(r"^/api/currency/summary-nbu_rates?$"), get_summary_nbu_rates),
    ("GET", re.compile(r"^/api/currency/rates/history?$"), get_rates_history),

    ("GET", re.compile(r"^/api/user/me?$"), get_me),
    ("PATCH", re.compile(r"^/api/user/update-profile?$"),  update_user_profile),
    ("POST",  re.compile(r"^/api/user/change-password?$"), change_password),

    ("POST", re.compile(r"^/api/auth/register?$"), user_register),
    ("POST", re.compile(r"^/api/auth/login?$"), user_login),
    ("POST", re.compile(r"^/api/auth/refresh?$"), refresh),
    ("POST", re.compile(r"^/api/auth/logout?$"),  logout_from_session),
]