from routing.geocoder import geocode_location


def test_geocoder():
    result = geocode_location("Sapna Sangeeta Road")

    print("\nPlace:", result["name"])
    print("Latitude:", result["latitude"])
    print("Longitude:", result["longitude"])

    assert result["latitude"] != 0
    assert result["longitude"] != 0