from typing import TypedDict, Optional


class UrbanFlowState(TypedDict, total=False):

    # Incident information
    incident_type: str
    location: str
    destination: str
    severity: str

    # Current conditions
    traffic_level: str
    weather: str

    # Emergency information
    emergency_vehicle: Optional[str]
    blocked_roads: Optional[list[tuple[str, str]]]
    emergency_priority: Optional[str]

    # Prediction
    predicted_congestion: Optional[float]
    congestion_level: Optional[str]

    # Routing
    recommended_route: Optional[str]
    estimated_time: Optional[float]
    route_alternatives: Optional[list[dict]]

    # REAL ROAD ROUTING
    route_geometry: Optional[dict]
    route_origin: Optional[dict]
    route_destination: Optional[dict]

    # Traffic signal decision
    signal_plan: Optional[dict]

    # Trust and validation
    confidence: Optional[float]
    risk_level: Optional[str]
    evidence: Optional[list[str]]
    validation_status: Optional[str]

    # Final communication
    citizen_message: Optional[str]