from orchestration.state import UrbanFlowState


state: UrbanFlowState = {
    "incident_type": "accident",
    "location": "Vijay Nagar",
    "severity": "high",
    "traffic_level": "severe",
    "weather": "heavy_rain",
    "emergency_vehicle": "ambulance",
    "emergency_priority": "high"
}

print(state)