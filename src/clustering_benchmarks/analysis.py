from __future__ import annotations

import numpy as np
import pandas as pd


def paired_effects(raw: pd.DataFrame) -> pd.DataFrame:
    """Compute paired runtime effects for matched repetitions.

    S = T_overlap / T_partition and L = log(S). Pairing controls for the
    dataset, density, repetition, and local execution period.
    """
    keys = ["dataset", "target_density", "repetition"]
    wide = raw.pivot_table(index=keys, columns="method", values="runtime_seconds").reset_index()
    wide = wide.dropna(subset=["partitioning", "overlapping"])
    wide["runtime_ratio"] = wide["overlapping"] / wide["partitioning"]
    wide["log_runtime_ratio"] = np.log(wide["runtime_ratio"])
    return wide


def robust_effect_summary(paired: pd.DataFrame) -> pd.DataFrame:
    """Summarize paired slowdown using the median and IQR on the log scale."""
    groups = ["dataset", "target_density"]
    rows = []
    for key, values in paired.groupby(groups, sort=False):
        log_ratio = values["log_runtime_ratio"]
        rows.append({
            "dataset": key[0],
            "target_density": key[1],
            "paired_repetitions": len(values),
            "median_runtime_ratio": float(np.exp(log_ratio.median())),
            "q1_runtime_ratio": float(np.exp(log_ratio.quantile(0.25))),
            "q3_runtime_ratio": float(np.exp(log_ratio.quantile(0.75))),
            "median_log_runtime_ratio": float(log_ratio.median()),
        })
    return pd.DataFrame(rows)


def aggregate_effects(paired: pd.DataFrame) -> pd.DataFrame:
    """Return density-specific and overall robust paired effects."""
    rows = []
    for density, values in paired.groupby("target_density", sort=True):
        logs = values["log_runtime_ratio"]
        rows.append({
            "scope": f"density_{density:.2f}",
            "n_pairs": len(values),
            "median_runtime_ratio": float(np.exp(logs.median())),
            "q1_runtime_ratio": float(np.exp(logs.quantile(0.25))),
            "q3_runtime_ratio": float(np.exp(logs.quantile(0.75))),
        })
    logs = paired["log_runtime_ratio"]
    rows.append({
        "scope": "overall",
        "n_pairs": len(paired),
        "median_runtime_ratio": float(np.exp(logs.median())),
        "q1_runtime_ratio": float(np.exp(logs.quantile(0.25))),
        "q3_runtime_ratio": float(np.exp(logs.quantile(0.75))),
    })
    return pd.DataFrame(rows)


def order_effects(raw: pd.DataFrame) -> pd.DataFrame:
    """Diagnose whether running first or second changes measured runtime."""
    return (
        raw.groupby(["method", "execution_order"], as_index=False)["runtime_seconds"]
        .agg(repetitions="count", median_runtime_seconds="median")
    )
