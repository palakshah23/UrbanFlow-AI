from orchestration.graph import build_urbanflow_graph


app = build_urbanflow_graph()


initial_state = {
    "incident_type": "accident",
    "location": "Vijay Nagar",
    "severity": "high",
    "traffic_level": "severe",
    "weather": "heavy_rain",
    "emergency_vehicle": "ambulance"
}


result = app.invoke(initial_state)


print("\n==============================")
print("🚨 URBANFLOW AI RESULT")
print("==============================")

print("\nEmergency Priority:")
print(result["emergency_priority"])

print("\nPredicted Congestion:")
print(result["predicted_congestion"])

print("\nCongestion Level:")
print(result["congestion_level"])

print("\nRecommended Route:")
print(result["recommended_route"])

print("\nEstimated Time:")
print(result["estimated_time"], "minutes")

print("\nSignal Plan:")
print(result["signal_plan"])

print("\nConfidence:")
print(result["confidence"], "%")

print("\nRisk Level:")
print(result["risk_level"])

print("\nValidation Status:")
print(result["validation_status"])

print("\nEvidence:")
for item in result["evidence"]:
    print("•", item)