"""LOCO (Leave-One-Component-Out) ablation study for MP-OFC.

Runs ablation variants on MNIST and Fashion-MNIST to isolate
the contribution of each MP-OFC component.

Variants:
  1. full       - Full MP-OFC (control)
  2. no_warmup  - warmup_epochs=0
  3. no_floor   - min_weight=0.0
  4. fixed_theta- theta_mode='fixed' (no EMA adaptive threshold)
  5. spike_mode - mode='spike' (legacy spike-count OFC)
  6. no_modul   - steepness=0.01 (monitor-only, no effective modulation)

Usage:
    python scripts/run_ablation.py --epochs 30 --output_dir results/ablation
    python scripts/run_ablation.py --epochs 1 --datasets mnist  # dry-run
"""

import sys
import os
import argparse
import copy
import csv
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
import numpy as np

from src.utils.config import load_config
from src.utils.seed import set_seed
from src.models import build_model
from src.data import get_dataloaders
from src.training.trainer import Trainer


# Ablation variants: name -> config overrides
ABLATION_VARIANTS = {
    "full": {},  # control: no overrides
    "no_warmup": {"ofc.warmup_epochs": 0},
    "no_floor": {"ofc.min_weight": 0.0},
    "fixed_theta": {"ofc.theta_mode": "fixed"},
    "spike_mode": {"ofc.mode": "spike"},
    "no_modul": {"ofc.steepness": 0.01},
}

DATASET_CONFIGS = {
    "mnist": "configs/mnist_ofc.yaml",
    "fmnist": "configs/fmnist_ofc_tuned.yaml",
}


def apply_overrides(cfg: dict, overrides: dict) -> dict:
    """Apply dotted-key overrides to config dict."""
    raise NotImplementedError('Implementation removed for public mirror.')


def run_variant(base_config: str, variant_name: str, overrides: dict,
                epochs: int, seed: int, device: torch.device,
                dataset_name: str) -> dict:
    """Run a single ablation variant."""
    raise NotImplementedError('Implementation removed for public mirror.')


def save_results(results: list, output_path: str):
    """Save ablation results to CSV."""
    raise NotImplementedError('Implementation removed for public mirror.')


def plot_ablation_bar(results: list, output_path: str):
    """Generate grouped bar chart of ablation results."""
    raise NotImplementedError('Implementation removed for public mirror.')


def print_summary(results: list):
    """Print ablation summary table."""
    raise NotImplementedError('Implementation removed for public mirror.')


def main():
    raise NotImplementedError('Implementation removed for public mirror.')


if __name__ == "__main__":
    main()
