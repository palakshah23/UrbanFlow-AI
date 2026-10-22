
from pathlib import Path
import math

import networkx as nx
import osmnx as ox


GRAPH_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "indore_drive.graphml"
)


def load_network():
    if not GRAPH_PATH.exists():
        raise FileNotFoundError(
            f"Road network file not found: {GRAPH_PATH}"
        )

    return ox.load_graphml(filepath=GRAPH_PATH)


def haversine_m(lat1, lon1, lat2, lon2):
    earth_radius = 6_371_000

    lat1, lon1, lat2, lon2 = map(
        math.radians, [lat1, lon1, lat2, lon2]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    return 2 * earth_radius * math.asin(
        math.sqrt(min(1.0, a))
    )


def nearest_node(graph, lat, lon):
    return ox.distance.nearest_nodes(
        graph, X=lon, Y=lat
    )


def calculate_route(graph, start_lat, start_lon, end_lat, end_lon):
    start = nearest_node(graph, start_lat, start_lon)
    end = nearest_node(graph, end_lat, end_lon)

    return nx.shortest_path(
        graph, start, end, weight="length"
    )


def route_distance(graph, route):
    total_meters = 0.0

    for u, v in zip(route[:-1], route[1:]):
        edges = graph.get_edge_data(u, v)

        if not edges:
            raise ValueError(f"Missing road edge: {u} -> {v}")

        total_meters += min(
            float(edge.get("length", 0))
            for edge in edges.values()
        )

    return round(total_meters / 1000, 3)


def route_geometry(graph, route):
    coordinates = []

    for node in route:
        data = graph.nodes[node]
        coordinates.append([
            float(data["y"]),
            float(data["x"]),
        ])

    return coordinates


def close_road_segment(
    graph,
    closure_lat,
    closure_lon,
    closure_radius=150,
    protected_nodes=None,
):
    closed_graph = graph.copy()
    protected_nodes = set(protected_nodes or [])

    nodes_to_remove = []

    for node, data in graph.nodes(data=True):
        distance = haversine_m(
            closure_lat,
            closure_lon,
            float(data["y"]),
            float(data["x"]),
        )

        if distance <= closure_radius and node not in protected_nodes:
            nodes_to_remove.append(node)

    closed_graph.remove_nodes_from(nodes_to_remove)

    print(
        f"Simulated closure: {len(nodes_to_remove)} "
        f"road nodes removed within {closure_radius} m"
    )

    return closed_graph, nodes_to_remove


def compare_routes(
    start_lat,
    start_lon,
    end_lat,
    end_lon,
    closure_lat,
    closure_lon,
    closure_radius=150,
):
    graph = load_network()

    start_node = nearest_node(graph, start_lat, start_lon)
    end_node = nearest_node(graph, end_lat, end_lon)

    normal_route = calculate_route(
        graph, start_lat, start_lon, end_lat, end_lon
    )

    normal_distance = route_distance(graph, normal_route)
    normal_geometry = route_geometry(graph, normal_route)

    closed_graph, removed_nodes = close_road_segment(
        graph,
        closure_lat,
        closure_lon,
        closure_radius,
        protected_nodes={start_node, end_node},
    )

    closure_intersects_route = any(
        node in set(removed_nodes) for node in normal_route
    )

    try:
        alternative_route = calculate_route(
            closed_graph,
            start_lat,
            start_lon,
            end_lat,
            end_lon,
        )

        alternative_distance = route_distance(
            closed_graph, alternative_route
        )
        alternative_geometry = route_geometry(
            closed_graph, alternative_route
        )

        route_changed = alternative_route != normal_route

        simulation_status = (
            "alternative_route_found"
            if route_changed
            else (
                "closure_does_not_intersect_route"
                if not closure_intersects_route
                else "route_unchanged"
            )
        )

    except (nx.NetworkXNoPath, nx.NodeNotFound):
        alternative_route = None
        alternative_distance = None
        alternative_geometry = None
        route_changed = False
        simulation_status = "no_alternative_route"

    distance_change = (
        round(alternative_distance - normal_distance, 3)
        if alternative_distance is not None
        else None
    )

    return {
        "normal_route": normal_route,
        "normal_distance_km": normal_distance,
        "normal_geometry": normal_geometry,
        "alternative_route": alternative_route,
        "alternative_distance_km": alternative_distance,
        "alternative_geometry": alternative_geometry,
        "distance_change_km": distance_change,
        "closure_intersects_route": closure_intersects_route,
        "closure_nodes_removed": len(removed_nodes),
        "route_changed": route_changed,
        "simulation_status": simulation_status,
    }