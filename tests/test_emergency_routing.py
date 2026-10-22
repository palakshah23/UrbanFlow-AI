from agents.emergency_routing import emergency_routing_agent


state = {
    "incident_type": "accident",
    "location": "Vijay Nagar",
    "severity": "high",
    "traffic_level": "severe",
    "weather": "heavy_rain",
    "emergency_vehicle": "ambulance",
    "emergency_priority": "high",
    "predicted_congestion": 100,
    "congestion_level": "severe"
}

result = emergency_routing_agent(state)

print("\nEmergency Routing Result:")
print(result)

print("\n🚑 Recommended Emergency Route:")
print(result["recommended_route"])

print(f"⏱️ Estimated Time: {result['estimated_time']} minutes")