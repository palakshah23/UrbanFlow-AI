from agents.signal_coordination import signal_coordination_agent


state = {
    "incident_type": "accident",
    "location": "Vijay Nagar",
    "severity": "high",
    "traffic_level": "severe",
    "weather": "heavy_rain",
    "emergency_vehicle": "ambulance",
    "emergency_priority": "high",
    "predicted_congestion": 100,
    "congestion_level": "severe",
    "recommended_route": "Vijay Nagar → Bhawarkua → Hospital",
    "estimated_time": 24.0
}

result = signal_coordination_agent(state)

print("\n🚦 Signal Coordination Result:")
print(result["signal_plan"])

print("\nSignal Changes:")

for change in result["signal_plan"]["changes"]:
    print(
        f"Junction: {change['junction']} | "
        f"Action: {change['action']} | "
        f"Duration: {change['duration_seconds']} sec"
    )