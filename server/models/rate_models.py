from db import (get_conn, get_file_logger)
from lib.helpers import validate_type
from configs.error_logs_files_name import RATE_MODELS_FILE_NAME

logger = get_file_logger(RATE_MODELS_FILE_NAME)

def insert_min_fin_rate(bank_slug: str, currency: str, buy: float, sell: float):
    if not validate_type(bank_slug, str, "bank_slug", logger):
        return None
    
    if not validate_type(currency, str, "currency", logger):
        return None
    
    if not validate_type(buy, (int, float), "buy", logger):
        return None
    
    if not validate_type(sell, (int, float), "sell", logger):
        return None
    
    with get_conn() as conn:
        row = conn.execute(
            "SELECT id FROM banks WHERE slug = ?", (bank_slug,)
        ).fetchone()
        if row is None:
            logger.error("insert_min_fin_rate: bank with slug '%s' not found", bank_slug)
            return None
        bank_id = row["id"]
        conn.execute(
            """
            INSERT INTO bank_rates (bank_id, currency, buy, sell)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(bank_id, currency) DO UPDATE SET
                buy        = excluded.buy,
                sell       = excluded.sell,
                updated_at = datetime('now')
            """,
            (bank_id, currency.upper(), buy, sell),
        )

def insert_nbu_rate(currency: str, rate: float):
    if not validate_type(currency, str, "currency", logger):
        return None
    
    if not validate_type(rate, (int, float), "rate", logger):
        return None

    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO nbu_rates (currency, rate) VALUES (?, ?)
            ON CONFLICT(currency) DO UPDATE SET
                rate       = excluded.rate,
                updated_at = datetime('now')
            """,
            (currency.upper(), float(rate)),
        )