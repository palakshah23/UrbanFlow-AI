import networkx as nx
from routing.road_network import create_road_network


def find_best_route(
    start: str,
    destination: str,
    congestion: float = 0,
    blocked_roads: list[tuple[str, str]] | None = None,
):
    graph = create_road_network(
        congestion=congestion,
        blocked_roads=blocked_roads,
    )

    route = nx.shortest_path(
        graph,
        source=start,
        target=destination,
        weight="travel_time",
    )

    travel_time = nx.shortest_path_length(
        graph,
        source=start,
        target=destination,
        weight="travel_time",
    )

    return route, travel_time