import requests


NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"


def geocode_location(place: str):
    """
    Convert a place name into latitude and longitude.
    """

    params = {
        "q": f"{place}, Indore, Madhya Pradesh, India",
        "format": "json",
        "limit": 1,
    }

    headers = {
        "User-Agent": "UrbanFlowAI/1.0"
    }

    response = requests.get(
        NOMINATIM_URL,
        params=params,
        headers=headers,
        timeout=15,
    )

    response.raise_for_status()

    results = response.json()

    if not results:
        raise ValueError(
            f"Location not found: {place}"
        )

    return {
        "name": results[0]["display_name"],
        "latitude": float(results[0]["lat"]),
        "longitude": float(results[0]["lon"]),
    }