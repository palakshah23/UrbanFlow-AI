from orchestration.state import UrbanFlowState
from trust.confidence import calculate_confidence


def validation_agent(state: UrbanFlowState) -> UrbanFlowState:
    """
    Validate the final traffic decision and
    provide confidence, evidence and risk.
    """

    print("🛡️ Trust & Validation Agent running...")

    confidence = calculate_confidence(state)

    evidence = [
        f"Incident severity: {state.get('severity')}",
        f"Traffic level: {state.get('traffic_level')}",
        f"Weather condition: {state.get('weather')}",
        f"Predicted congestion: {state.get('predicted_congestion')}%",
        f"Emergency priority: {state.get('emergency_priority')}",
        f"Recommended route: {state.get('recommended_route')}"
    ]

    if confidence >= 80:
        risk_level = "low"
        validation_status = "validated"

    elif confidence >= 60:
        risk_level = "medium"
        validation_status = "validated_with_caution"

    else:
        risk_level = "high"
        validation_status = "requires_human_review"

    state["confidence"] = confidence
    state["risk_level"] = risk_level
    state["evidence"] = evidence
    state["validation_status"] = validation_status

    return state