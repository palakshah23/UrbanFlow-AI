from orchestration.state import UrbanFlowState


def signal_coordination_agent(
    state: UrbanFlowState
) -> UrbanFlowState:

    print("🚦 Signal Coordination Agent running...")

    route = state.get("recommended_route")
    emergency_priority = state.get("emergency_priority", "normal")

    if not route:
        return state

    locations = [x.strip() for x in route.split("→")]

    # Source and destination are not junctions
    junctions = locations[1:-1]

    signal_changes = []

    # Only prioritize signals when there is an actual emergency
    if emergency_priority == "high":

        for junction in junctions:
            signal_changes.append({
                "junction": junction,
                "action": "extend_green",
                "duration_seconds": 15,
                "priority": "emergency",
                "reason": "Emergency vehicle priority"
            })

        signal_priority = "emergency"

    else:

        signal_priority = "normal"

    state["signal_plan"] = {
        "priority": signal_priority,
        "route": route,
        "changes": signal_changes
    }

    return state