from routing.real_router import get_route


# Approximate test coordinates.
# We will replace these with verified geocoded coordinates
# once the routing layer itself is confirmed.
START_LAT = 22.7196
START_LON = 75.8577

END_LAT = 22.754
END_LON = 75.893


def test_real_route():
    result = get_route(
        START_LAT,
        START_LON,
        END_LAT,
        END_LON,
    )

    print("\nDistance:", result["distance_km"], "km")
    print("ETA:", result["estimated_time"], "minutes")

    assert result["distance_km"] > 0
    assert result["estimated_time"] > 0
    assert len(result["geometry"]["coordinates"]) > 0