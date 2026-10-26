# Runtime Cost of Overlapping Clique-Based Clustering

A controlled, paired benchmark of **partitioning** and **overlapping** clustering with user-specified relative density.

## Primary estimand

For matched repetition \(r\):

\[
S_{G,\rho,r}=\frac{T_O(G,\rho,r)}{T_P(G,\rho,r)}.
\]

The reported slowdown is

\[
\widehat{S}_{G,\rho}=\exp\!\left(\operatorname{median}_r \log S_{G,\rho,r}\right),
\]

with exponentiated log-IQR as robust dispersion.

## Design

```text
8 graphs × 3 density targets × 2 methods × 8 measured repetitions
= 384 measured executions
```

- 2 untimed warm-ups
- exact 4:4 execution-order balance
- `perf_counter()` around `fit()` only
- paired analysis by graph, density, and repetition
- first-cluster and density-state invariants checked

## Run

```bash
python -m pip install -e .
python scripts/run_all_benchmarks.py --config benchmark_config.yaml
python scripts/generate_figures.py
```

## Scientific outputs

```text
results/raw_runs.csv
results/paired_runtime_effects.csv
results/effect_size_summary.csv
results/aggregate_effects.csv
results/execution_order_diagnostic.csv
results/validation_results.json
results/environment.json
```

## Figures

1. Median runtime with IQR by density
2. Paired slowdown-ratio heatmap
3. Slowdown forest plot with robust intervals
4. Runtime scaling with edges and triangles
5. Execution-order diagnostic

See `docs/SCIENTIFIC_DESIGN.md` for equations and interpretation.
