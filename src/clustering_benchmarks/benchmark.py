from __future__ import annotations

import gc
import json
from pathlib import Path
from time import perf_counter
import pandas as pd
import yaml

from graph_clustering import OptimizedPartitioningCliqueClusterer, OverlappingCliqueClusterer
from graph_clustering.triangles import find_triangles
from .datasets import load_graph
from .environment import write_environment
from .statistics import summarize_runs
from .analysis import paired_effects, robust_effect_summary, aggregate_effects, order_effects
from .validation import first_clusters_equal, disjoint_starting_triangles, density_states_consistent


def _timed_fit(method: str, graph, density: float, mode: str):
    cls = OptimizedPartitioningCliqueClusterer if method == "partitioning" else OverlappingCliqueClusterer
    gc.collect()
    start = perf_counter()
    result = cls(density, mode=mode).fit(graph)
    return result, perf_counter() - start


def run_benchmarks(config_path: str | Path) -> tuple[pd.DataFrame, pd.DataFrame, list[dict]]:
    config_path = Path(config_path).resolve()
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    root = config_path.parent
    settings = config["benchmark"]
    warmups = int(settings["warmup_runs"])
    repetitions = int(settings["measured_runs"])
    mode = settings.get("mode", "corrected")
    methods = config.get("methods", ["partitioning", "overlapping"])
    densities = [float(value) for value in config["densities"]]

    raw_rows: list[dict] = []
    validations: list[dict] = []

    for item in config["datasets"]:
        dataset = item["name"]
        graph = load_graph(root / item["path"], item["format"])
        triangle_count = len(find_triangles(graph, mode=mode))

        for density in densities:
            # Untimed warm-up calls.
            for warmup in range(warmups):
                order = methods if warmup % 2 == 0 else list(reversed(methods))
                for method in order:
                    _timed_fit(method, graph.copy(), density, mode)

            baseline = {}
            for repetition in range(1, repetitions + 1):
                order = methods if repetition % 2 == 1 else list(reversed(methods))
                for order_position, method in enumerate(order, start=1):
                    result, elapsed = _timed_fit(method, graph.copy(), density, mode)
                    baseline[method] = result
                    clustered = set().union(*(set(c.nodes) for c in result.clusters)) if result.clusters else set()
                    overlapping_count = len(getattr(result, "overlapping_nodes", ()))
                    unclustered_count = len(getattr(result, "unclustered_nodes", ()))
                    raw_rows.append({
                        "dataset": dataset,
                        "target_density": density,
                        "method": method,
                        "repetition": repetition,
                        "execution_order": order_position,
                        "runtime_seconds": elapsed,
                        "nodes": graph.number_of_nodes(),
                        "edges": graph.number_of_edges(),
                        "triangles": triangle_count,
                        "cluster_count": len(result.clusters),
                        "clustered_node_count": len(clustered),
                        "overlapping_node_count": overlapping_count,
                        "unclustered_node_count": unclustered_count,
                    })

            validations.append({
                "dataset": dataset,
                "target_density": density,
                "first_cluster_equal": first_clusters_equal(baseline["partitioning"], baseline["overlapping"]),
                "disjoint_overlapping_starts": disjoint_starting_triangles(baseline["overlapping"]),
                "partitioning_density_consistent": density_states_consistent(baseline["partitioning"]),
                "overlapping_density_consistent": density_states_consistent(baseline["overlapping"]),
            })

    raw = pd.DataFrame(raw_rows)
    summary = summarize_runs(raw)
    output = root / config.get("output_directory", "results")
    output.mkdir(parents=True, exist_ok=True)
    paired = paired_effects(raw)
    effects = robust_effect_summary(paired)
    aggregate = aggregate_effects(paired)
    order = order_effects(raw)

    raw.to_csv(output / "raw_runs.csv", index=False)
    summary.to_csv(output / "benchmark_summary.csv", index=False)
    paired.to_csv(output / "paired_runtime_effects.csv", index=False)
    effects.to_csv(output / "effect_size_summary.csv", index=False)
    aggregate.to_csv(output / "aggregate_effects.csv", index=False)
    order.to_csv(output / "execution_order_diagnostic.csv", index=False)
    (output / "benchmark_summary.json").write_text(summary.to_json(orient="records", indent=2), encoding="utf-8")
    (output / "validation_results.json").write_text(json.dumps(validations, indent=2), encoding="utf-8")
    write_environment(output / "environment.json")
    return raw, summary, validations
