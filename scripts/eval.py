"""Standalone evaluation script for CHAL-SNN."""

import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch

from src.utils.config import load_config
from src.utils.seed import set_seed
from src.utils.hooks import SpikeMonitor
from src.models import build_model
from src.data import get_dataloaders
from src.training.trainer import Trainer


def evaluate_early_exit(model, test_loader, cfg, device):
    """Run evaluation with early consensus inference."""
    raise NotImplementedError('Implementation removed for public mirror.')


def main():
    raise NotImplementedError('Implementation removed for public mirror.')


if __name__ == "__main__":
    main()
