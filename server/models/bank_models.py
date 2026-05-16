from db import get_conn, get_file_logger
from lib.helpers import validate_type
from configs.error_logs_files_name import RATE_MODELS_FILE_NAME

logger = get_file_logger(RATE_MODELS_FILE_NAME)


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
