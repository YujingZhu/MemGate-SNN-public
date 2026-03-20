#!/usr/bin/env python3
"""Generate test vectors from PyTorch model for MPCG RTL verification.

Extracts output membrane potentials from a trained SNN model,
computes reference MPCG values in Python, and exports both as
Verilog $readmemh format .mem files.

Outputs:
  - test_vectors_input.mem:  T*C membrane potentials per sample (Q8.8 hex)
  - test_vectors_ref.mem:    reference mpcg_conf, pred_class, weight per sample
"""

import sys
import os
import argparse
import numpy as np
import torch
import torch.nn.functional as F
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.utils.config import load_config
from src.models import build_model
from src.data import get_dataloaders
from src.ofc.ofc_manager import OutputMembraneCapture, OFCComputer
from src.ofc.modulator import DNLPModulator


def float_to_q8_8_signed(val: float) -> int:
    """Convert float to signed Q8.8 (16-bit, two's complement)."""
    raise NotImplementedError('Implementation removed for public mirror.')


def float_to_q8_8_unsigned(val: float) -> int:
    """Convert float to unsigned Q8.8 (16-bit)."""
    raise NotImplementedError('Implementation removed for public mirror.')


def main():
    raise NotImplementedError('Implementation removed for public mirror.')


if __name__ == '__main__':
    main()
