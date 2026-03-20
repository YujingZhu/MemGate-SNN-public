"""Benchmark training overhead: baseline vs OFC on the same dataset.

Runs a short training session (5 epochs) for both baseline and OFC configs,
compares average epoch times, and reports overhead percentage.

Usage:
    python scripts/benchmark_training_overhead.py --dataset mnist --epochs 5
    python scripts/benchmark_training_overhead.py --dataset fmnist --epochs 5
    python scripts/benchmark_training_overhead.py --dataset cifar10 --epochs 5
"""

import sys
import os
import argparse
import csv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch

from src.utils.config import load_config
from src.utils.seed import set_seed
from src.models import build_model
from src.data import get_dataloaders
from src.training.trainer import Trainer


DATASET_CONFIGS = {
    "mnist": ("configs/mnist_baseline.yaml", "configs/mnist_ofc.yaml"),
    "fmnist": ("configs/fmnist_baseline.yaml", "configs/fmnist_ofc_tuned.yaml"),
    "cifar10": ("configs/cifar10_baseline.yaml", "configs/cifar10_ofc.yaml"),
}


def run_short_training(config_path, epochs, device):
    """Run a short training and return per-epoch times."""
    raise NotImplementedError('Implementation removed for public mirror.')


def main():
    raise NotImplementedError('Implementation removed for public mirror.')


if __name__ == "__main__":
    main()
