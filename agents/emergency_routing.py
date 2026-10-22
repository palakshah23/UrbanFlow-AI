from orchestration.state import UrbanFlowState
from routing.route_optimizer import find_best_route
from routing.geocoder import geocode_location
from routing.real_router import get_route


def emergency_routing_agent(
    state: UrbanFlowState
) -> UrbanFlowState:

    print("🚑 Emergency Routing Agent running...")

    start = state.get("location")

    destination = state.get(
        "destination",
        "Choithram Hospital, Indore"
    )

    congestion = state.get(
        "predicted_congestion",
        0
    )

    blocked_roads = [
        tuple(road)
        for road in state.get(
            "blocked_roads",
            []
        )
    ]

    if not start:
        print("⚠️ Emergency location missing.")
        return state

    try:
        print("🗺️ Attempting real Indore road routing...")

        origin = geocode_location(start)

        destination_location = geocode_location(
            destination
        )

        real_route = get_route(
            start_lat=origin["latitude"],
            start_lon=origin["longitude"],
            end_lat=destination_location["latitude"],
            end_lon=destination_location["longitude"],
            blocked_roads=blocked_roads,
        )

        state["recommended_route"] = (
            f"{origin['name']} → "
            f"{destination_location['name']}"
        )

        state["estimated_time"] = (
            real_route["estimated_time"]
        )

        state["route_geometry"] = (
            real_route["geometry"]
        )

        state["route_origin"] = origin

        state["route_destination"] = (
            destination_location
        )

        state["route_alternatives"] = (
            real_route.get("alternatives", [])
        )

        print("✅ Real road route calculated.")

        print(
            "📏 Distance:",
            real_route["distance_km"],
            "km"
        )

        print(
            "⏱️ ETA:",
            real_route["estimated_time"],
            "minutes"
        )

        return state

    except Exception as error:

        print(
            "⚠️ Real routing unavailable."
        )

        print(
            "↩️ Using UrbanFlow simulated road network."
        )

        print(
            "Reason:",
            error
        )

        route, travel_time = find_best_route(
            start=start,
            destination="Hospital",
            congestion=congestion,
            blocked_roads=blocked_roads,
        )

        state["recommended_route"] = (
            " → ".join(route)
        )

        state["estimated_time"] = round(
            float(travel_time),
            2
        )

        return state