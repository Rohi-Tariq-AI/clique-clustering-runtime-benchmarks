from __future__ import annotations

import pandas as pd


def summarize_runs(raw: pd.DataFrame) -> pd.DataFrame:
    keys = ["dataset", "target_density", "method", "nodes", "edges", "triangles"]
    summary = (
        raw.groupby(keys, as_index=False)["runtime_seconds"]
        .agg(
            repetitions="count",
            median_runtime_seconds="median",
            q1_runtime_seconds=lambda values: values.quantile(0.25),
            q3_runtime_seconds=lambda values: values.quantile(0.75),
            minimum_runtime_seconds="min",
            maximum_runtime_seconds="max",
        )
    )
    summary["iqr_runtime_seconds"] = (
        summary["q3_runtime_seconds"] - summary["q1_runtime_seconds"]
    )

    pivot = summary.pivot_table(
        index=["dataset", "target_density"],
        columns="method",
        values="median_runtime_seconds",
    )
    if {"partitioning", "overlapping"}.issubset(pivot.columns):
        ratios = (pivot["overlapping"] / pivot["partitioning"]).rename("runtime_ratio")
        summary = summary.merge(ratios.reset_index(), on=["dataset", "target_density"], how="left")
    return summary
