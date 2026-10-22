
import requests

OSRM_URL = "https://router.project-osrm.org/route/v1/driving"


def get_route(
    start_lat,
    start_lon,
    end_lat,
    end_lon,
    blocked_roads=None,
):
    """
    Get a driving route using the public OSRM routing service.
    No Google API key is required.

    OSRM provides route geometry, distance and estimated duration.
    It does not provide live traffic conditions.
    Road-closure simulations are handled separately by osm_closure.py.
    """

    coordinates = (
        f"{float(start_lon)},{float(start_lat)};"
        f"{float(end_lon)},{float(end_lat)}"
    )

    params = {
        "overview": "full",
        "geometries": "geojson",
        "steps": "false",
        "alternatives": "true",
    }

    try:
        response = requests.get(
            f"{OSRM_URL}/{coordinates}",
            params=params,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

    except requests.RequestException as error:
        raise RuntimeError(
            f"OSRM routing request failed: {error}"
        ) from error

    if data.get("code") != "Ok" or not data.get("routes"):
        raise RuntimeError(
            f"OSRM could not calculate a route: "
            f"{data.get('message', data.get('code', 'Unknown error'))}"
        )

    formatted_routes = []

    for route in data["routes"]:
        geometry = route.get("geometry")

        if not geometry or not geometry.get("coordinates"):
            continue

        distance_km = float(route["distance"]) / 1000
        duration_minutes = float(route["duration"]) / 60

        formatted_routes.append({
            "distance_km": round(distance_km, 2),
            "estimated_time": round(duration_minutes, 2),
            "static_time": round(duration_minutes, 2),
            "traffic_delay_minutes": None,
            "traffic_level": "unavailable",
            "geometry": geometry,
            "traffic_aware": False,
        })

    if not formatted_routes:
        raise RuntimeError(
            "OSRM returned no usable route geometry."
        )

    best_route = min(
        formatted_routes,
        key=lambda route: route["estimated_time"],
    )

        # Copy routes to avoid a circular reference.
    alternatives = [route.copy() for route in formatted_routes]

    best_route["alternatives"] = alternatives
    best_route["blocked_roads"] = blocked_roads or []
    best_route["closure_applied"] = False
    best_route["routing_provider"] = "OSRM"

    print("Route calculated using OSRM.")
    print("Distance:", best_route["distance_km"], "km")
    print("Estimated duration:", best_route["estimated_time"], "minutes")
    print("Live traffic data: unavailable")

    return best_route