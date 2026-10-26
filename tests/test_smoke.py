from pathlib import Path
from graph_clustering import OptimizedPartitioningCliqueClusterer, OverlappingCliqueClusterer
from clustering_benchmarks.datasets import load_graph
from clustering_benchmarks.validation import first_clusters_equal, disjoint_starting_triangles

ROOT = Path(__file__).resolve().parents[1]

def test_karate_scientific_invariants():
    graph = load_graph(ROOT / "data/gml/karate.gml", "gml")
    p = OptimizedPartitioningCliqueClusterer(0.40, mode="corrected").fit(graph)
    o = OverlappingCliqueClusterer(0.40, mode="corrected").fit(graph)
    assert first_clusters_equal(p, o)
    assert disjoint_starting_triangles(o)
