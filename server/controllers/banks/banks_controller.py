from geopy.distance import geodesic

from models.bank_models import get_all_banks, get_bank_info, get_all_branches_with_coords
from lib.helpers import get_file_logger
from configs.error_logs_files_name import BANKS_CONTROLLER_FILE_NAME

logger = get_file_logger(BANKS_CONTROLLER_FILE_NAME)

def _nearest_branches(
    user_lat: float,
    user_lon: float,
    branches: list[dict],
    limit: int = 10,
    max_km: float | None = None,
) -> list[dict]:
    user = (user_lat, user_lon)
    enriched = []
    for b in branches:
        lat, lon = b.get("latitude"), b.get("longitude")
        if lat is None or lon is None:
            continue
        dist = geodesic(user, (lat, lon)).km
        if max_km is not None and dist > max_km:
            continue
        enriched.append({**b, "distance_km": round(dist, 3)})

    enriched.sort(key=lambda x: x["distance_km"])
    return enriched[:limit]



def get_banks_list(*, query, **_):
    banks = get_all_banks()

    return {
        "status": 200,
        "response": {
            "total": len(banks),
            "banks": banks
        }
    }

def get_full_bank_info(*, query, **_):
    slug = query.get("slug")
    if not slug:
        return {
            "status": 400,
            "response": {"error": "slug is required"}
        }
    
    info = get_bank_info(slug)
    if info is None:
        return {
            "status": 404,
            "response": {"error": "bank not found"}
        }

    return {
        "status": 200,
        "response": info
    }

def get_nearest_branches_with_coords(*, query, **_):
    latitude = query.get("latitude")
    longitude = query.get("longitude")
    distance_limit = query.get("distance_limit", 10)
    limit = query.get("limit", 10)

    if not latitude or not longitude:
        return {
            "status": 400,
            "response": {"error": "latitude and longitude are required"}
        }

    try:
        latitude = float(latitude)
        longitude = float(longitude)
        distance_limit = float(distance_limit)
    except (ValueError, TypeError):
        return {
            "status": 400,
            "response": {"error": "latitude or longitude or distance_limit must be valid numbers"}
        }

    try:
        limit = int(limit)
    except (ValueError, TypeError):
        return {
            "status": 400,
            "response": {"error": "limit must be a valid integer"}
        }

    if distance_limit <= 0:
        return {
            "status": 400,
            "response": {"error": "distance_limit must be a positive number"}
        }

    if not (1 <= limit <= 100):
        return {
            "status": 400,
            "response": {"error": "limit must be between 1 and 100"}
        }

    all_branches = get_all_branches_with_coords()
    result = _nearest_branches(latitude, longitude, all_branches, limit=limit, max_km=distance_limit)

    return {
        "status": 200,
        "response": {"total": len(result), "branches": result}
    }