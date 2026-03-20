"""OOD detection via MPCG confidence scores.

Demonstrates that MPCG serves as a zero-cost OOD detector by comparing
confidence distributions on in-distribution (MNIST) vs out-of-distribution
(Fashion-MNIST with MNIST normalization) data.

Outputs:
  - 2-panel figure: (a) MPCG histograms, (b) ROC curve
  - OOD metrics CSV (AUROC, etc.)
"""

import sys
import os
import argparse
import csv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.utils.config import load_config
from src.utils.seed import set_seed
from src.models import build_model
from src.ofc.ofc_manager import OutputMembraneCapture, OFCComputer

# IEEE format
IEEE_SINGLE_COL = 3.5
FONT_SIZE = 10
DPI = 300

plt.rcParams.update({
    "font.size": FONT_SIZE,
    "axes.labelsize": FONT_SIZE,
    "axes.titlesize": FONT_SIZE,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "figure.dpi": DPI,
    "savefig.dpi": DPI,
    "font.family": "serif",
})


def collect_mpcg(model, capture, ofc_computer, dataloader, device):
    """Collect per-sample MPCG values.

    Returns:
        mpcg_values: [N] numpy array of MPCG confidence scores
        predictions: [N] numpy array of predicted classes
    """
    raise NotImplementedError('Implementation removed for public mirror.')


def compute_auroc_numpy(id_scores, ood_scores):
    """Compute AUROC using numpy (no sklearn dependency).

    ID samples are positive (label=1), OOD are negative (label=0).
    Higher MPCG = more likely ID.

    Returns:
        auroc: float
        fpr: numpy array (false positive rates)
        tpr: numpy array (true positive rates)
    """
    raise NotImplementedError('Implementation removed for public mirror.')


def plot_ood_results(id_mpcg, ood_mpcg, fpr, tpr, auroc, output_path):
    """2-panel figure: (a) MPCG histograms, (b) ROC curve."""
    raise NotImplementedError('Implementation removed for public mirror.')


def main():
    raise NotImplementedError('Implementation removed for public mirror.')


# Need import for get_dataloaders
from src.data import get_dataloaders


if __name__ == "__main__":
    main()
