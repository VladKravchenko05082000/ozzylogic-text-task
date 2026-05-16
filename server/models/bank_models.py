from db import (get_conn, get_file_logger)

from lib.helpers import validate_type

from configs.error_logs_files_name import BANKS_ERROR_FILE_NAME

logger = get_file_logger(BANKS_ERROR_FILE_NAME)

def insert_bank(slug: str, name: str, description: str | None, logo: str | None,
                site: str | None, phone: str | None, email: str | None,
                legal_address: str | None, rating: float | None):
    if not validate_type(slug, str, "slug", logger):
        return None
    if not validate_type(name, str, "name", logger):
        return None

    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO banks (slug, name, description, logo, site, phone, email, legal_address, rating)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(slug) DO UPDATE SET
                name          = excluded.name,
                description   = excluded.description,
                logo          = excluded.logo,
                site          = excluded.site,
                phone         = excluded.phone,
                email         = excluded.email,
                legal_address = excluded.legal_address,
                rating        = excluded.rating,
                updated_at    = datetime('now')
            """,
            (slug, name, description, logo, site, phone, email, legal_address, rating),
        )


def insert_branch(bank_slug: str, name: str, address: str | None,
                  latitude: float | None, longitude: float | None, phone: str | None):
    if not validate_type(bank_slug, str, "bank_slug", logger):
        return None
    if not validate_type(name, str, "name", logger):
        return None

    with get_conn() as conn:
        row = conn.execute(
            "SELECT id FROM banks WHERE slug = ?", (bank_slug,)
        ).fetchone()
        if row is None:
            logger.error("insert_branch: bank with slug '%s' not found", bank_slug)
            return None
        bank_id = row["id"]
        conn.execute(
            """
            INSERT INTO bank_branches (bank_id, name, address, latitude, longitude, phone)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (bank_id, name, address, latitude, longitude, phone),
        )

def get_all_banks() -> list[dict]:
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name, logo, rating, phone, email FROM banks ORDER BY name"
        )

        rows = cursor.fetchall()

        return [dict(r) for r in rows] 
    
def get_all_branches_with_coords() -> list[dict]:
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT bb.id, bb.name, bb.address, bb.latitude, bb.longitude, bb.phone,
                   bk.slug AS bank_slug, bk.name AS bank_name, bk.logo
            FROM bank_branches bb
            JOIN banks bk ON bk.id = bb.bank_id
            WHERE bb.latitude IS NOT NULL AND bb.longitude IS NOT NULL
            """
        )
        rows = cursor.fetchall()

    return [dict(r) for r in rows]


def get_bank_info(slug: str) -> dict | None:
    if not validate_type(slug, str, "slug", logger):
        return None

    with get_conn() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM banks WHERE slug = ?", (slug,))
        bank = cursor.fetchone()
        if bank is None:
            return None

        bank = dict(bank)
        bank_id = bank.get("id")

        cursor.execute(
            "SELECT currency, buy, sell FROM bank_rates WHERE bank_id = ?", (bank_id,)
        )
        rates = cursor.fetchall()

        cursor.execute(
            "SELECT name, address, latitude, longitude, phone FROM bank_branches WHERE bank_id = ?",
            (bank_id,)
        )
        branches = cursor.fetchall()

    return {
        "bank": dict(bank),
        "rates": [dict(r) for r in rates],
        "branches": [dict(b) for b in branches],
    }
