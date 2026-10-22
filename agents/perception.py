from orchestration.state import UrbanFlowState


def perception_agent(state: UrbanFlowState) -> UrbanFlowState:
    """
    Analyze incoming traffic incident information
    and determine emergency priority.
    """

    print("👁️ Perception Agent running...")

    severity = state.get("severity", "low")
    emergency_vehicle = state.get("emergency_vehicle")

    # Determine emergency priority
    if severity == "high" and emergency_vehicle:
        state["emergency_priority"] = "high"

    elif severity == "high":
        state["emergency_priority"] = "medium"

    else:
        state["emergency_priority"] = "normal"

    return state

    