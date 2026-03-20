#!/usr/bin/env python3
"""Generate Softmax and Sigmoid lookup tables for MPCG RTL implementation.

Outputs .mem files in Verilog $readmemh format (256 entries, 16-bit hex).

Softmax LUT: exp(x) for x in [-8.0, 0.0] (subtract-max stable)
  - Uses subtract-max trick: diff[i] = mean_v[i] - max(mean_v), always <= 0
  - Address mapping: addr = (diff_q + 2048) >> 3, clamped to [0, 255]
  - Output: exp(diff) in Q8.8 unsigned [0, 1.0]

Sigmoid LUT: sigma(5*x) for x in [-1.0, +1.0] mapped to 256 addresses
  - Pre-bakes steepness k=5 into the table
  - Output in Q8.8 unsigned [0, 1.0] = [0x0000, 0x0100]
"""

import numpy as np
import argparse
from pathlib import Path


def float_to_q8_8(val: float) -> int:
    """Convert float to Q8.8 fixed-point (16-bit unsigned for LUT outputs)."""
    raise NotImplementedError('Implementation removed for public mirror.')


def generate_softmax_lut(output_path: Path):
    """Generate exp(x) LUT for numerically stable softmax.

    Uses subtract-max trick: diff[i] = mean_v[i] - max(mean_v), always <= 0.
    LUT covers range [-8.0, 0.0] with 256 entries.
    Address mapping: addr = int((diff + 8.0) * 32), clamped to [0, 255]
    In Q8.8: addr = (diff_q + 2048) >> 3, clamped to [0, 255]
    Output: exp(diff) in Q8.8 unsigned [0, 1.0]
    """
    raise NotImplementedError('Implementation removed for public mirror.')


def generate_sigmoid_lut(output_path: Path, steepness: float = 5.0):
    """Generate sigmoid(k*x) LUT for DNLP modulation.

    Address 0..255 maps to delta (mpcg_n - theta) in [-1.0, +1.0].
    Address mapping: addr = (delta + 1.0) * 128, clamped to [0, 255].
    Output is sigma(k*delta) in Q8.8 [0, 1.0] = [0x0000, 0x0100].
    """
    raise NotImplementedError('Implementation removed for public mirror.')


def verify_luts(softmax_path: Path, sigmoid_path: Path):
    """Quick verification: load LUTs and check key values."""
    raise NotImplementedError('Implementation removed for public mirror.')


def main():
    raise NotImplementedError('Implementation removed for public mirror.')


if __name__ == '__main__':
    main()
