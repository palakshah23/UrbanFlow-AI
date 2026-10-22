from orchestration.state import UrbanFlowState


def citizen_advisory_agent(
    state: UrbanFlowState
) -> UrbanFlowState:

    print("📢 Citizen Advisory Agent running...")

    route = state.get("recommended_route")
    eta = state.get("estimated_time")
    congestion = state.get("congestion_level")
    emergency_priority = state.get("emergency_priority")

    if emergency_priority == "high":
        message = (
            f"🚨 Emergency traffic alert: Heavy congestion detected. "
            f"Please keep the emergency corridor clear. "
            f"Recommended route: {route}. "
            f"Estimated travel time: {eta} minutes."
        )

    else:
        message = (
            f"🚦 Traffic alert: {congestion} congestion detected. "
            f"Recommended route: {route}. "
            f"Estimated travel time: {eta} minutes."
        )

    state["citizen_message"] = message

    return state