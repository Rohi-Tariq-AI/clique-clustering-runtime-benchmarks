from pathlib import Path
import pandas as pd
from clustering_benchmarks.datasets import load_graph
from clustering_benchmarks.statistics import summarize_runs

ROOT = Path(__file__).resolve().parents[1]

def test_dataset_loading():
    graph = load_graph(ROOT / "data/gml/karate.gml", "gml")
    assert graph.number_of_nodes() == 34
    assert graph.number_of_edges() == 78

def test_statistics_summary():
    raw = pd.DataFrame([
        {"dataset":"x","target_density":0.4,"method":"partitioning","nodes":3,"edges":3,"triangles":1,"runtime_seconds":1.0},
        {"dataset":"x","target_density":0.4,"method":"partitioning","nodes":3,"edges":3,"triangles":1,"runtime_seconds":2.0},
        {"dataset":"x","target_density":0.4,"method":"overlapping","nodes":3,"edges":3,"triangles":1,"runtime_seconds":4.0},
        {"dataset":"x","target_density":0.4,"method":"overlapping","nodes":3,"edges":3,"triangles":1,"runtime_seconds":6.0},
    ])
    summary = summarize_runs(raw)
    assert len(summary) == 2
    assert set(summary["runtime_ratio"]) == {5.0 / 1.5}
