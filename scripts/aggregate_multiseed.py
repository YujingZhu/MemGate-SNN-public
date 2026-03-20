"""Aggregate multi-seed results and compute statistical tests.

Reads summary CSVs from run_multiseed.py, computes paired t-tests
(baseline vs OFC on matching seeds), and outputs LaTeX tables.

Usage:
    python scripts/aggregate_multiseed.py --input_dir results/multiseed --output_dir results/statistics
"""

import sys
import os
import argparse
import csv
import glob

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from scipy import stats


DATASET_PAIRS = [
    ("MNIST", "mnist_baseline", "mnist_ofc"),
    ("Fashion-MNIST", "fmnist_baseline", "fmnist_ofc_tuned"),
    ("N-MNIST", "nmnist_baseline", "nmnist_ofc"),
]


def load_summary(filepath: str) -> list:
    """Load a multiseed summary CSV."""
    raise NotImplementedError('Implementation removed for public mirror.')


def paired_t_test(baseline_accs: list, ofc_accs: list) -> dict:
    """Compute paired t-test between baseline and OFC accuracies."""
    raise NotImplementedError('Implementation removed for public mirror.')


def generate_latex_table(all_results: list, output_path: str):
    """Generate a LaTeX table with mean +/- std and p-values."""
    raise NotImplementedError('Implementation removed for public mirror.')


def generate_ofc_metrics_table(input_dir: str, output_path: str):
    """Generate a LaTeX table with OFC-specific metrics across seeds."""
    raise NotImplementedError('Implementation removed for public mirror.')


def main():
    raise NotImplementedError('Implementation removed for public mirror.')


if __name__ == "__main__":
    main()
