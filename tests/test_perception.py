from agents.perception import perception_agent


state = {
    "incident_type": "accident",
    "location": "Vijay Nagar",
    "severity": "high",
    "traffic_level": "severe",
    "weather": "heavy_rain",
    "emergency_vehicle": "ambulance"
}

result = perception_agent(state)

print(result)