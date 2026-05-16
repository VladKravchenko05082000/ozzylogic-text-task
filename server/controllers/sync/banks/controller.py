from http_clients.finance_ua import finance_ua_fetch_banks_list, finance_ua_fetch_branches
from models.bank_models import (insert_bank, insert_branch)

from lib.helpers import (get_file_logger, validate_type)

from configs.general_constants import SUPPORTED_BANKS
from configs.error_logs_files_name import SYNC_ERROR_FILE_NAME

logger = get_file_logger(SYNC_ERROR_FILE_NAME)


def _parse_bank_entry(raw: dict) -> dict | None:
    slug = raw.get("slug", None)
    if not slug:
        return None
    
    rating = raw.get("ratingBank", None)

    logo = raw.get("logo", [])
    if isinstance(logo, list):
        logo = logo[0] if logo else None

    return {
        "slug": slug,
        "name": raw.get("title", ""),
        "description": raw.get("description", ""),
        "logo": logo,
        "site": raw.get("site", ""),
        "phone": raw.get("phone", ""),
        "email": raw.get("email", ""),
        "legal_address": raw.get("legalAddress", ""),
        "rating": rating,
    }


def _parse_branch_entry(raw: dict, bank_slug: str) -> dict | None:
    name = raw.get("branch_name", "")
    if not name:
        return None

    try:
        latitude = raw.get("lat", 0)
        longitude = raw.get("lng", 0)
    except (TypeError, ValueError) as e:
        logger.error("Bad coordinates for branch in %s: %s", bank_slug, e)
        return None

    return {
        "bank_slug": bank_slug,
        "name": name,
        "address": raw.get("address", ""),
        "latitude": latitude,
        "longitude": longitude,
        "phone": raw.get("phone", ""),
    }


def sync_banks():
    try:
        all_banks = finance_ua_fetch_banks_list()
    except Exception as e:
        logger.error("Failed to fetch banks list: %s", e)
        return

    if not validate_type(all_banks, dict, "banks", logger):
        return

    all_banks = all_banks.get("responseData", [])

    by_slug = {
        b["slug"]: b for b in all_banks
        if isinstance(b, dict) and "slug" in b
    }

    for slug in SUPPORTED_BANKS:
        raw = by_slug.get(slug)
        if not raw:
            logger.error("Bank %s not found in finance.ua list", slug)
            continue

        parsed = _parse_bank_entry(raw)
        if parsed:
            current_slug = parsed.get("slug", "")
            current_name = parsed.get("name", "")
            current_description = parsed.get("description", "")
            current_logo = parsed.get("logo", "")
            current_site = parsed.get("site", "")
            current_phone = parsed.get("phone", "")
            current_email = parsed.get("email", "")
            current_legal_address = parsed.get("legal_address", "")
            current_rating = parsed.get("rating")
            insert_bank(
                current_slug, current_name, current_description,
                current_logo, current_site, current_phone,
                current_email, current_legal_address, current_rating,
            )


def sync_branches():
    for slug in SUPPORTED_BANKS:
        try:
            raw_list = finance_ua_fetch_branches(slug)
        except Exception as e:
            logger.error("Failed to fetch branches for %s: %s", slug, e)
            continue

        if not validate_type(raw_list, dict, f"branches[{slug}]", logger):
            continue

        for city_group in raw_list.get("data", []):
            for raw in city_group.get("data", []):
                parsed = _parse_branch_entry(raw, slug)
                if parsed:
                    current_bank_slug = parsed.get("bank_slug", "")
                    current_name = parsed.get("name", "")
                    current_address = parsed.get("address")
                    current_latitude = parsed.get("latitude")
                    current_longitude = parsed.get("longitude")
                    current_phone = parsed.get("phone")
                    insert_branch(
                        current_bank_slug, current_name, current_address,
                        current_latitude, current_longitude, current_phone,
                    )
