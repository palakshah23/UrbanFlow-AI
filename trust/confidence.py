def calculate_confidence(state) -> float:
    """
    Calculate decision confidence based on
    availability of important decision factors.
    """

    score = 0

    if state.get("incident_type"):
        score += 20

    if state.get("severity"):
        score += 20

    if state.get("traffic_level"):
        score += 20

    if state.get("weather"):
        score += 15

    if state.get("recommended_route"):
        score += 15

    if state.get("signal_plan"):
        score += 10

    return float(score)