#!/usr/bin/env python3
import argparse
from clustering_benchmarks.benchmark import run_benchmarks

parser = argparse.ArgumentParser()
parser.add_argument("--config", default="benchmark_config.yaml")
args = parser.parse_args()
raw, summary, validations = run_benchmarks(args.config)
print(f"Measured runs: {len(raw)}")
print(f"Summary rows: {len(summary)}")
print(f"Validation groups: {len(validations)}")
