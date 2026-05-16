from typing import Optional

from db import (get_conn, get_file_logger)
from lib.helpers import validate_type
from configs.error_logs_files_name import RATE_MODELS_FILE_NAME
from configs.general_constants import SUPPORTED_CURRENCIES

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

def get_all_currency() -> list[str]:
    return SUPPORTED_CURRENCIES

def get_latest_rates(
    banks: Optional[list[str]] = None,
    currencies: Optional[list[str]] = None,
) -> list[dict]:
    if banks is not None and not validate_type(banks, list, "banks", logger):
        return []
    if currencies is not None and not validate_type(currencies, list, "currencies", logger):
        return []

    with get_conn() as conn:
        cursor = conn.cursor()

        sql = """
            SELECT b.slug AS bank_slug, br.currency, br.buy, br.sell, br.updated_at
            FROM bank_rates br
            JOIN banks b ON b.id = br.bank_id
        """
        conditions: list[str] = []
        params: list = []

        if banks:
            conditions.append(f"b.slug IN ({','.join('?' * len(banks))})")
            params.extend(banks)

        if currencies:
            conditions.append(f"br.currency IN ({','.join('?' * len(currencies))})")
            params.extend([c.upper() for c in currencies])

        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        sql += " ORDER BY b.slug, br.currency"

        cursor.execute(sql, params)
        rates = cursor.fetchall()

    return [dict(r) for r in rates]

def get_nbu_latest() -> list[dict]:
    with get_conn() as conn:
        cursor = conn.cursor()
        placeholders = ",".join(["?"] * len(SUPPORTED_CURRENCIES))
        
        cursor.execute(
            f"""
            SELECT currency, rate, updated_at 
            FROM nbu_rates r1
            WHERE currency IN ({placeholders})
              AND updated_at = (
                SELECT MAX(updated_at) 
                FROM nbu_rates r2 
                WHERE r2.currency = r1.currency
              )
            ORDER BY currency
            """,
            SUPPORTED_CURRENCIES
        )

        rows = cursor.fetchall()

        return [dict(r) for r in rows]

def get_average_rates() -> list[dict]:
    with get_conn() as conn:
        cursor = conn.cursor()
        placeholders = ",".join(["?"] * len(SUPPORTED_CURRENCIES))

        cursor.execute(
            f"""
            SELECT currency,
                   AVG(buy)  AS avg_buy,
                   AVG(sell) AS avg_sell
            FROM bank_rates r1
            WHERE currency IN ({placeholders})
              AND updated_at = (
                SELECT MAX(updated_at)
                FROM bank_rates r2
                WHERE r2.bank_id  = r1.bank_id
                  AND r2.currency = r1.currency
              )
            GROUP BY currency
            ORDER BY currency
            """,
            SUPPORTED_CURRENCIES
        )

        rows = cursor.fetchall()

        return [dict(r) for r in rows]