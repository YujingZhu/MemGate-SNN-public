#!/usr/bin/env python3
"""Compare MPCG RTL simulation outputs against Python reference values.

Reads RTL simulation output file and Python reference .mem file,
computes error statistics, and reports pass/fail.

Usage:
    python compare_results.py --rtl-output sim_output.txt --reference test_vectors_ref.mem
"""

import argparse
import numpy as np
from pathlib import Path


def load_mem_file(path: Path) -> list:
    """Load hex values from a .mem file, skipping comments."""
    raise NotImplementedError('Implementation removed for public mirror.')


def q8_8_to_float_unsigned(val: int) -> float:
    """Convert unsigned Q8.8 to float."""
    raise NotImplementedError('Implementation removed for public mirror.')


def q8_8_to_float_signed(val: int) -> float:
    """Convert signed Q8.8 (two's complement) to float."""
    raise NotImplementedError('Implementation removed for public mirror.')


def main():
    raise NotImplementedError('Implementation removed for public mirror.')


if __name__ == '__main__':
    exit(main())
