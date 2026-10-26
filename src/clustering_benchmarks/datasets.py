from __future__ import annotations

from pathlib import Path
import networkx as nx


def load_graph(path: str | Path, graph_format: str) -> nx.Graph:
    """Load and standardize an undirected, unweighted, simple graph."""
    path = Path(path)
    if graph_format == "gml":
        try:
            graph = nx.read_gml(path, label="id")
        except Exception:
            graph = nx.read_gml(path)
    elif graph_format == "edge_list":
        try:
            graph = nx.read_edgelist(path, nodetype=int, create_using=nx.Graph())
        except Exception:
            graph = nx.read_edgelist(path, create_using=nx.Graph())
    else:
        raise ValueError(f"Unsupported graph format: {graph_format}")

    clean = nx.Graph()
    clean.add_nodes_from(graph.nodes())
    clean.add_edges_from((u, v) for u, v in graph.edges() if u != v)
    return clean
