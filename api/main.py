
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from orchestration.graph import build_urbanflow_graph
from routing.geocoder import geocode_location
from routing.real_router import get_route
from routing.osm_closure import compare_routes


app = FastAPI(
    title="UrbanFlow AI",
    description=(
        "Trustworthy Multi-Agent Decision "
        "Support for Emergency Urban Mobility"
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = build_urbanflow_graph()


def convert_to_geojson(geometry):
    """Convert route coordinates to GeoJSON LineString."""

    if not geometry:
        return None

    if (
        isinstance(geometry, dict)
        and geometry.get("type") == "LineString"
    ):
        return geometry

    if isinstance(geometry, list):
        coordinates = []

        for point in geometry:
            if not isinstance(point, (list, tuple)) or len(point) < 2:
                continue

            # OSM closure simulation uses [latitude, longitude].
            coordinates.append([
                float(point[1]),
                float(point[0]),
            ])

        if len(coordinates) < 2:
            return None

        return {
            "type": "LineString",
            "coordinates": coordinates,
        }

    return None


@app.get("/")
def root():
    return {
        "message": "UrbanFlow AI is running",
        "status": "online",
        "routing": {
            "provider": "OSRM",
            "traffic_aware": False,
            "traffic_available": False,
        },
        "what_if": {
            "provider": "OSMnx road-network simulation",
            "live_traffic_available": False,
        },
    }


@app.post("/route")
def route(data: dict):
    try:
        origin = data.get("origin")
        destination = data.get("destination")

        if not origin or not destination:
            return {
                "status": "error",
                "message": "Origin and destination are required.",
            }

        origin_location = geocode_location(origin)
        destination_location = geocode_location(destination)

        real_route = get_route(
            start_lat=origin_location["latitude"],
            start_lon=origin_location["longitude"],
            end_lat=destination_location["latitude"],
            end_lon=destination_location["longitude"],
        )

        return {
            "status": "success",
            "origin": origin_location,
            "destination": destination_location,
            "recommended_route": (
                f"{origin_location['name']} → "
                f"{destination_location['name']}"
            ),
            "distance_km": real_route["distance_km"],
            "estimated_time": real_route["estimated_time"],
            "static_time": real_route["static_time"],
            "traffic_delay_minutes": real_route.get(
                "traffic_delay_minutes"
            ),
            "traffic_level": real_route.get(
                "traffic_level", "unavailable"
            ),
            "traffic_aware": False,
            "eta_type": "static_estimate",
            "route_geometry": real_route.get("geometry"),
            "geometry": real_route.get("geometry"),
            "route_alternatives": real_route.get(
                "alternatives", []
            ),
            "traffic_available": False,
            "blocked_roads": [],
        }

    except Exception as error:
        print("Route error:", repr(error))
        return {
            "status": "error",
            "message": str(error),
        }


@app.post("/analyze")
def analyze(data: dict):
    try:
        state = {
            "incident_type": data.get("incident_type", "accident"),
            "location": data.get("location"),
            "destination": data.get(
                "destination", "Choithram Hospital, Indore"
            ),
            "severity": data.get("severity", "high"),
            "traffic_level": data.get("traffic_level", "severe"),
            "weather": data.get("weather", "clear"),
            "emergency_vehicle": data.get("emergency_vehicle"),
            "blocked_roads": data.get("blocked_roads", []),
        }

        result = graph.invoke(state)

        return {
            "status": "success",
            **result,
        }

    except Exception as error:
        print("Analyze error:", repr(error))
        return {
            "status": "error",
            "message": str(error),
        }


@app.post("/what-if")
def what_if(data: dict):
    try:
        origin = data.get("origin")
        destination = data.get("destination")
        closure_road = data.get("closure_road")

        if not origin or not destination or not closure_road:
            return {
                "status": "error",
                "message": (
                    "Origin, destination, and closure_road "
                    "are required."
                ),
            }

        closure_radius = float(data.get("closure_radius", 150))

        if closure_radius <= 0:
            return {
                "status": "error",
                "message": "closure_radius must be greater than zero.",
            }

        print("\n========== WHAT-IF ROAD CLOSURE ==========")
        print("Origin:", origin)
        print("Destination:", destination)
        print("Closure:", closure_road)
        print("Closure radius (m):", closure_radius)

        origin_location = geocode_location(origin)
        destination_location = geocode_location(destination)
        closure_location = geocode_location(closure_road)

        result = compare_routes(
            start_lat=origin_location["latitude"],
            start_lon=origin_location["longitude"],
            end_lat=destination_location["latitude"],
            end_lon=destination_location["longitude"],
            closure_lat=closure_location["latitude"],
            closure_lon=closure_location["longitude"],
            closure_radius=closure_radius,
        )

        required_fields = [
            "normal_distance_km",
            "alternative_distance_km",
            "distance_change_km",
            "normal_geometry",
            "alternative_geometry",
            "closure_intersects_route",
            "closure_nodes_removed",
            "route_changed",
            "simulation_status",
        ]

        missing_fields = [
            field for field in required_fields
            if field not in result
        ]

        if missing_fields:
            print("Missing simulation fields:", missing_fields)
            print("Fields returned by compare_routes:", list(result.keys()))

            return {
                "status": "error",
                "message": (
                    "compare_routes did not return all required "
                    "road-closure diagnostics. Check "
                    "routing/osm_closure.py."
                ),
                "missing_fields": missing_fields,
                "result_fields_received": list(result.keys()),
            }

        normal_geometry = convert_to_geojson(
            result["normal_geometry"]
        )
        alternative_geometry = convert_to_geojson(
            result["alternative_geometry"]
        )

        return {
            "status": "success",
            "origin": origin_location,
            "destination": destination_location,
            "closure_road": closure_location,
            "normal_distance_km": result["normal_distance_km"],
            "alternative_distance_km": result["alternative_distance_km"],
            "distance_change_km": result["distance_change_km"],
            "normal_geometry": normal_geometry,
            "alternative_geometry": alternative_geometry,
            "eta_type": "road_network_simulation",
            "live_traffic_available": False,
            "closure_simulation": True,
            "closure_intersects_route": result["closure_intersects_route"],
            "closure_nodes_removed": result["closure_nodes_removed"],
            "route_changed": result["route_changed"],
            "simulation_status": result["simulation_status"],
        }

    except Exception as error:
        print("What-if error:", repr(error))
        return {
            "status": "error",
            "message": str(error),
        }