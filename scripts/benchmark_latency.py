"""Latency and memory benchmarking for CHAL-SNN.

Measures:
1. Forward pass timing (with and without OFC overhead)
2. Early exit performance (accuracy, fraction exiting early, effective T)
3. Peak memory during forward/backward pass
4. BPTT memory scaling with T

Usage:
    python scripts/benchmark_latency.py --config configs/mnist_ofc.yaml \
        --checkpoint checkpoints/best_conv_snn.pt --num_batches 100
"""

import sys
import os
import argparse
import time
import csv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
import numpy as np

from src.utils.config import load_config
from src.utils.seed import set_seed
from src.models import build_model
from src.data import get_dataloaders
from src.ofc import OFCComputer, OutputMembraneCapture, EarlyConsensusInference

# Number of warmup batches to discard before timing (avoids CUDA cold-start artifacts)
WARMUP_BATCHES = 10


def benchmark_forward_paired(model, test_loader, device, ofc_cfg, num_batches=100):
    """Time forward pass with and without OFC in paired back-to-back runs.

    On each batch:
    1. Warmup call (untimed) to fill CUDA kernel cache for this input
    2. Plain forward (timed) - benefits from warm kernel cache
    3. Forward + OFC (timed) - also benefits from warm kernel cache
    This eliminates both ordering bias and CUDA kernel cache asymmetry.
    """
    raise NotImplementedError('Implementation removed for public mirror.')


def benchmark_early_exit(model, test_loader, device, ofc_cfg, num_batches=100):
    """Benchmark early exit inference."""
    raise NotImplementedError('Implementation removed for public mirror.')


def benchmark_memory(model, test_loader, device, cfg):
    """Measure peak memory during forward and backward pass."""
    raise NotImplementedError('Implementation removed for public mirror.')


def benchmark_T_scaling(cfg, device, T_values=None):
    """Measure memory/time scaling with different T values."""
    raise NotImplementedError('Implementation removed for public mirror.')


def main():
    raise NotImplementedError('Implementation removed for public mirror.')


if __name__ == "__main__":
    main()
