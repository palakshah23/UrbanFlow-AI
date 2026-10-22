def predict_congestion(
    traffic_level: str,
    severity: str,
    weather: str
) -> float:

    traffic_score = {
        "low": 20,
        "moderate": 50,
        "severe": 80
    }.get(traffic_level, 50)

    severity_factor = {
        "low": 0,
        "medium": 10,
        "high": 20
    }.get(severity, 0)

    weather_factor = {
        "clear": 0,
        "rain": 10,
        "heavy_rain": 20
    }.get(weather, 0)

    congestion = traffic_score + severity_factor + weather_factor

    return min(congestion, 100)