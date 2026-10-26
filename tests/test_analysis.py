import numpy as np
import pandas as pd
from clustering_benchmarks.analysis import paired_effects, robust_effect_summary, aggregate_effects


def test_paired_log_ratio_estimand():
    raw = pd.DataFrame([
        {"dataset":"g","target_density":0.4,"repetition":1,"method":"partitioning","runtime_seconds":1.0},
        {"dataset":"g","target_density":0.4,"repetition":1,"method":"overlapping","runtime_seconds":2.0},
        {"dataset":"g","target_density":0.4,"repetition":2,"method":"partitioning","runtime_seconds":2.0},
        {"dataset":"g","target_density":0.4,"repetition":2,"method":"overlapping","runtime_seconds":8.0},
    ])
    paired = paired_effects(raw)
    assert list(paired["runtime_ratio"]) == [2.0, 4.0]
    effect = robust_effect_summary(paired).iloc[0]
    assert np.isclose(effect["median_runtime_ratio"], np.sqrt(8.0))
    aggregate = aggregate_effects(paired)
    assert "overall" in set(aggregate["scope"])
