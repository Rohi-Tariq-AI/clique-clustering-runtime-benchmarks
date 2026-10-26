from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BLUE = "#2166ac"
RED = "#b2182b"
GRAY = "#4d4d4d"


def _save(fig, output: Path, stem: str, paths: list[Path]) -> None:
    for suffix in ("png", "pdf"):
        path = output / f"{stem}.{suffix}"
        fig.savefig(path, dpi=300 if suffix == "png" else None, bbox_inches="tight")
        paths.append(path)
    plt.close(fig)


def generate_figures(
    summary_path: str | Path,
    output_directory: str | Path,
    effect_path: str | Path | None = None,
    order_path: str | Path | None = None,
) -> list[Path]:
    summary = pd.read_csv(summary_path)
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    datasets = list(dict.fromkeys(summary["dataset"]))
    densities = sorted(summary["target_density"].unique())
    paths: list[Path] = []

    # Figure 1: absolute runtime, median and IQR.
    fig, axes = plt.subplots(1, len(densities), figsize=(6 * len(densities), 6), sharey=True, constrained_layout=True)
    axes = np.atleast_1d(axes)
    for ax, density in zip(axes, densities):
        subset = summary[summary["target_density"] == density]
        x = np.arange(len(datasets)); width = 0.38
        for offset, method, color in [(-width / 2, "partitioning", BLUE), (width / 2, "overlapping", RED)]:
            values = subset[subset["method"] == method].set_index("dataset").reindex(datasets)
            med = values["median_runtime_seconds"].to_numpy()
            low = med - values["q1_runtime_seconds"].to_numpy()
            high = values["q3_runtime_seconds"].to_numpy() - med
            ax.bar(x + offset, med, width, yerr=np.vstack([low, high]), capsize=3, label=method.title(), color=color)
        ax.set_yscale("log")
        ax.set_xticks(x); ax.set_xticklabels(datasets, rotation=45, ha="right")
        ax.set_title(rf"$\rho={density:.2f}$")
        ax.grid(axis="y", alpha=0.25)
    axes[0].set_ylabel("Runtime (s, median and IQR; log scale)")
    axes[0].legend(frameon=False)
    fig.suptitle("Absolute computational cost")
    _save(fig, output, "absolute_runtime_by_density", paths)

    if effect_path is not None and Path(effect_path).exists():
        effects = pd.read_csv(effect_path)

        # Figure 2: paired slowdown heatmap.
        ratio = effects.pivot(index="dataset", columns="target_density", values="median_runtime_ratio").reindex(datasets)
        fig, ax = plt.subplots(figsize=(8, 7), constrained_layout=True)
        image = ax.imshow(np.log2(ratio.values), aspect="auto", cmap="RdBu_r")
        ax.set_xticks(range(len(densities))); ax.set_xticklabels([f"{x:.2f}" for x in densities])
        ax.set_yticks(range(len(datasets))); ax.set_yticklabels(datasets)
        ax.set_xlabel("Target relative density")
        ax.set_title(r"Paired slowdown $\widehat{S}_{G,\rho}$")
        for i in range(len(datasets)):
            for j in range(len(densities)):
                ax.text(j, i, f"{ratio.iloc[i, j]:.2f}×", ha="center", va="center", color="black", fontsize=9)
        colorbar = fig.colorbar(image, ax=ax)
        colorbar.set_label(r"$\log_2(T_O/T_P)$")
        _save(fig, output, "paired_slowdown_heatmap", paths)

        # Figure 3: forest plot with robust log-IQR intervals.
        ordered = effects.sort_values(["target_density", "median_runtime_ratio"]).reset_index(drop=True)
        labels = [f"{row.dataset}, ρ={row.target_density:.2f}" for row in ordered.itertuples()]
        y = np.arange(len(ordered))
        median = ordered["median_runtime_ratio"].to_numpy()
        low = median - ordered["q1_runtime_ratio"].to_numpy()
        high = ordered["q3_runtime_ratio"].to_numpy() - median
        fig, ax = plt.subplots(figsize=(9, max(7, len(ordered) * 0.34)), constrained_layout=True)
        ax.errorbar(median, y, xerr=np.vstack([low, high]), fmt="o", color=RED, ecolor=GRAY, capsize=3)
        ax.axvline(1.0, color="black", linestyle="--", linewidth=1)
        ax.set_xscale("log")
        ax.set_yticks(y); ax.set_yticklabels(labels)
        ax.set_xlabel(r"Paired slowdown $T_O/T_P$ (median and log-IQR)")
        ax.set_title("Robust effect-size synthesis")
        ax.grid(axis="x", alpha=0.25)
        _save(fig, output, "slowdown_forest_plot", paths)

    # Figure 4: scaling against edges and triangles.
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5), constrained_layout=True)
    for ax, predictor, xlabel in [
        (axes[0], "edges", "Graph edges"),
        (axes[1], "triangles", "Graph triangles"),
    ]:
        for method, marker, color in [("partitioning", "o", BLUE), ("overlapping", "s", RED)]:
            values = summary[summary["method"] == method].groupby(["dataset", predictor], as_index=False)["median_runtime_seconds"].median()
            x = values[predictor].clip(lower=1)
            ax.scatter(x, values["median_runtime_seconds"], label=method.title(), marker=marker, s=65, color=color)
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.set_xlabel(f"{xlabel} (log scale)")
        ax.set_ylabel("Median runtime (s, log scale)")
        ax.grid(alpha=0.25)
    axes[0].legend(frameon=False)
    fig.suptitle("Descriptive computational scaling")
    _save(fig, output, "runtime_scaling", paths)

    # Figure 5: execution-order diagnostic.
    if order_path is not None and Path(order_path).exists():
        order = pd.read_csv(order_path)
        fig, ax = plt.subplots(figsize=(7, 5), constrained_layout=True)
        x = np.arange(2)
        width = 0.34
        for offset, method, color in [(-width / 2, "partitioning", BLUE), (width / 2, "overlapping", RED)]:
            values = order[order["method"] == method].set_index("execution_order").reindex([1, 2])
            ax.bar(x + offset, values["median_runtime_seconds"], width, label=method.title(), color=color)
        ax.set_xticks(x); ax.set_xticklabels(["Executed first", "Executed second"])
        ax.set_yscale("log")
        ax.set_ylabel("Median runtime (s, log scale)")
        ax.set_title("Execution-order diagnostic")
        ax.legend(frameon=False); ax.grid(axis="y", alpha=0.25)
        _save(fig, output, "execution_order_diagnostic", paths)

    return paths
