import networkx as nx


def create_road_network(
    congestion: float = 0,
    blocked_roads: list[tuple[str, str]] | None = None,
):
    graph = nx.Graph()

    roads = [
        ("Vijay Nagar", "Palasia", 5, congestion),
        ("Vijay Nagar", "Bhawarkua", 8, 20),
        ("Palasia", "MG Road", 4, congestion),
        ("Bhawarkua", "MG Road", 6, 20),
        ("MG Road", "Hospital", 5, congestion),
        ("Palasia", "Hospital", 10, congestion),
        ("Bhawarkua", "Hospital", 12, 20),
    ]

    blocked_roads = blocked_roads or []

    for start, end, base_time, road_congestion in roads:

        # Skip roads marked as blocked
        if (start, end) in blocked_roads or (end, start) in blocked_roads:
            continue

        congestion_multiplier = 1 + (road_congestion / 100)

        effective_time = base_time * congestion_multiplier

        graph.add_edge(
            start,
            end,
            base_time=base_time,
            congestion=road_congestion,
            travel_time=effective_time,
        )

    return graph