"""Multi-seed training for statistical validation.

Runs N seeds for a given config and aggregates results.
Designed to produce mean +/- std and paired t-test data for journal submission.

Usage:
    python scripts/run_multiseed.py --config configs/mnist_ofc.yaml --seeds 42 123 456 789 1024
    python scripts/run_multiseed.py --config configs/mnist_ofc.yaml --remote
"""

import sys
import os
import argparse
import copy
import csv
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch

from src.utils.config import load_config
from src.utils.seed import set_seed
from src.utils.logger import CSVLogger
from src.models import build_model
from src.data import get_dataloaders
from src.training.trainer import Trainer


DEFAULT_SEEDS = [42, 123, 456, 789, 1024]


def run_single_seed(cfg: dict, seed: int, device: torch.device,
                    exp_name: str) -> dict:
    """Train with a single seed and return results."""
    raise NotImplementedError('Implementation removed for public mirror.')


def save_summary(results: list, output_path: str):
    """Save multi-seed summary to CSV (append if file exists, avoiding duplicate seeds).

    Uses file locking to prevent data loss when multiple processes write
    to the same summary file concurrently (parallel seed execution).
    """
    raise NotImplementedError('Implementation removed for public mirror.')


def print_summary(results: list, exp_name: str):
    """Print aggregated statistics."""
    raise NotImplementedError('Implementation removed for public mirror.')


def main():
    raise NotImplementedError('Implementation removed for public mirror.')


if __name__ == "__main__":
    main()
