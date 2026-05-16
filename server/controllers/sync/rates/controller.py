from datetime import date, timedelta

from http_clients.minfin import min_fin_fetch_bank_rates
from http_clients.nbu import fetch_nbu_rates
from models.rate_models import (insert_min_fin_rate, insert_nbu_rate)

from lib.helpers import (get_file_logger, validate_type)

from configs.general_constants import SUPPORTED_CURRENCIES, SUPPORTED_BANKS
from configs.error_logs_files_name import SYNC_ERROR_FILE_NAME

logger = get_file_logger(SYNC_ERROR_FILE_NAME)

_SUPPORTED_BANKS = set(SUPPORTED_BANKS)
_MAX_DATE_RETRIES = 7

def _fetch_min_fin_rates_with_fallback(currency: str) -> list:
    for days_ago in range(_MAX_DATE_RETRIES):
        query_date = (date.today() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        try:
            rates = min_fin_fetch_bank_rates(currency, date=query_date)
        except Exception as e:
            logger.error("MinFin fetch failed for %s date=%s: %s", currency, query_date, e)
            return []

        if not validate_type(rates, dict, "rates", logger):
            return []

        rates_list = rates.get("data", [])

        if not validate_type(rates_list, list, "rates.data", logger):
            return []

        if rates_list:
            return rates_list

    return []


def _parse_rate_entry(entry: dict, currency: str) -> dict | None:
    slug = entry.get("slug")
    cash = entry.get("cash") or {}
    try:
        buy = float(cash.get("ask", 0) or 0)
        sell = float(cash.get("bid", 0) or 0)
    except (TypeError, ValueError) as e:
        logger.error("Bad rate for %s/%s: %s", slug, currency, e)
        return None

    if not buy or not sell:
        return None

    return {"slug": slug, "currency": currency, "buy": buy, "sell": sell}


def sync_min_fin_bank_rates():
    for currency in SUPPORTED_CURRENCIES:
        rates_list = _fetch_min_fin_rates_with_fallback(currency)

        for entry in rates_list:
            if entry.get("slug") not in _SUPPORTED_BANKS:
                continue

            parsed = _parse_rate_entry(entry, currency)
            if parsed:
                current_slug = parsed.get("slug", "")
                current_currency = parsed.get("currency", "")
                current_buy_rate = parsed.get("buy", 0)
                current_sell_rate = parsed.get("sell", 0)

                insert_min_fin_rate(bank_slug=current_slug, currency=current_currency, buy=current_buy_rate, sell=current_sell_rate)

def sync_nbu_rates():
    try:
        rates = fetch_nbu_rates()
    except Exception as e:
        logger.error("Nbu fetch failed: %s", e)
        return

    for rate in rates:
        cc = rate.get("cc", "")
        current_rate = rate.get("rate", 0.0)

        if cc in SUPPORTED_CURRENCIES:
            insert_nbu_rate(currency=cc, rate=current_rate)