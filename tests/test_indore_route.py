from routing.geocoder import geocode_location
from routing.real_router import get_route


def test_indore_route():

    origin = geocode_location(
        "Sapna Sangeeta Road"
    )

    destination = geocode_location(
    "Brilliant Convention Centre"
)
    

    print("\nORIGIN")
    print(origin)

    print("\nDESTINATION")
    print(destination)

    result = get_route(
        start_lat=origin["latitude"],
        start_lon=origin["longitude"],
        end_lat=destination["latitude"],
        end_lon=destination["longitude"],
    )

    print("\nROUTE RESULT")
    print("Distance:", result["distance_km"], "km")
    print("ETA:", result["estimated_time"], "minutes")
    print(
        "Route points:",
        len(result["geometry"]["coordinates"])
    )

    assert result["distance_km"] > 0
    assert result["estimated_time"] > 0
    assert len(result["geometry"]["coordinates"]) > 0