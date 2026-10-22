from orchestration.state import UrbanFlowState
from prediction.congestion_model import predict_congestion


def prediction_agent(state: UrbanFlowState) -> UrbanFlowState:
    """
    Predict congestion based on current traffic,
    incident severity, and weather.
    """

    print("🔮 Prediction Agent running...")

    traffic_level = state.get("traffic_level", "moderate")
    severity = state.get("severity", "low")
    weather = state.get("weather", "clear")

    congestion = predict_congestion(
        traffic_level,
        severity,
        weather
    )

    state["predicted_congestion"] = congestion

    if congestion >= 80:
        state["congestion_level"] = "severe"

    elif congestion >= 50:
        state["congestion_level"] = "moderate"

    else:
        state["congestion_level"] = "low"

    return state