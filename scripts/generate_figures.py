#!/usr/bin/env python3
import argparse
from clustering_benchmarks.plots import generate_figures

parser = argparse.ArgumentParser()
parser.add_argument("--summary", default="results/benchmark_summary.csv")
parser.add_argument("--effects", default="results/effect_size_summary.csv")
parser.add_argument("--order", default="results/execution_order_diagnostic.csv")
parser.add_argument("--output", default="figures")
args = parser.parse_args()
for path in generate_figures(args.summary, args.output, args.effects, args.order):
    print(path)
