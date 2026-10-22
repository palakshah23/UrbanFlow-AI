import osmnx as ox
from pathlib import Path


GRAPH_PATH = Path("data/indore_drive.graphml")


def download_indore_network():
    """
    Download and cache the Indore driving road network.
    """

    GRAPH_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    print("🌐 Downloading Indore driving network...")

    # Indore approximate bounding box
    # west, south, east, north
    bbox = (
        75.70,
        22.55,
        75.95,
        22.82
    )

    graph = ox.graph_from_bbox(
        bbox=bbox,
        network_type="drive"
    )

    print("✅ Indore road network downloaded.")

    ox.save_graphml(
        graph,
        filepath=GRAPH_PATH
    )

    print(
        f"💾 Network saved to: {GRAPH_PATH}"
    )

    return graph


def load_indore_network():
    """
    Load the cached Indore road network.
    Download it if the cache does not exist.
    """

    if GRAPH_PATH.exists():

        print(
            "📂 Loading cached Indore road network..."
        )

        graph = ox.load_graphml(
            GRAPH_PATH
        )

        print("✅ Road network loaded.")

        return graph

    return download_indore_network()