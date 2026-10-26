from pathlib import Path
import pandas as pd
from clustering_benchmarks.plots import generate_figures


def test_scientific_figures(tmp_path):
    summary = pd.DataFrame([
        {"dataset":"g","target_density":0.4,"method":"partitioning","edges":10,"triangles":2,"median_runtime_seconds":1.0,"q1_runtime_seconds":0.9,"q3_runtime_seconds":1.1},
        {"dataset":"g","target_density":0.4,"method":"overlapping","edges":10,"triangles":2,"median_runtime_seconds":2.0,"q1_runtime_seconds":1.8,"q3_runtime_seconds":2.2},
    ])
    effects = pd.DataFrame([{"dataset":"g","target_density":0.4,"median_runtime_ratio":2.0,"q1_runtime_ratio":1.8,"q3_runtime_ratio":2.2}])
    order = pd.DataFrame([
        {"method":"partitioning","execution_order":1,"median_runtime_seconds":1.0},
        {"method":"partitioning","execution_order":2,"median_runtime_seconds":1.1},
        {"method":"overlapping","execution_order":1,"median_runtime_seconds":2.0},
        {"method":"overlapping","execution_order":2,"median_runtime_seconds":2.1},
    ])
    summary_path = tmp_path / "summary.csv"; summary.to_csv(summary_path, index=False)
    effect_path = tmp_path / "effects.csv"; effects.to_csv(effect_path, index=False)
    order_path = tmp_path / "order.csv"; order.to_csv(order_path, index=False)
    paths = generate_figures(summary_path, tmp_path / "figures", effect_path, order_path)
    assert len(paths) == 10
    assert all(path.exists() for path in paths)
