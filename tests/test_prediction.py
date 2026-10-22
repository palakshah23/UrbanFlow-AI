from agents.prediction import prediction_agent


state = {
    "incident_type": "accident",
    "location": "Vijay Nagar",
    "severity": "high",
    "traffic_level": "severe",
    "weather": "heavy_rain",
    "emergency_vehicle": "ambulance",
    "emergency_priority": "high"
}

result = prediction_agent(state)

print("\nPrediction Result:")
print(result)