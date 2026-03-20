"""Main training entry point for CHAL-SNN."""

import sys
import os
import argparse

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch

from src.utils.config import load_config
from src.utils.seed import set_seed
from src.utils.logger import CSVLogger
from src.models import build_model
from src.data import get_dataloaders
from src.training.trainer import Trainer


def main():
    raise NotImplementedError('Implementation removed for public mirror.')


if __name__ == "__main__":
    main()
