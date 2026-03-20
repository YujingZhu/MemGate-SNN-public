"""Training and evaluation loops for SNN models."""

import os
import time
import torch
import torch.nn as nn
from torch.optim import Adam
from torch.optim.lr_scheduler import CosineAnnealingLR
from spikingjelly.activation_based import neuron

from .metrics import accuracy
from src.utils.hooks import SpikeMonitor


class Trainer:

    def __init__(self, model, train_loader, test_loader, cfg: dict,
                 device: torch.device = None, ofc_callback=None):
        raise NotImplementedError('Implementation removed for public mirror.')

    def _reset_epoch_ofc_stats(self):
        raise NotImplementedError('Implementation removed for public mirror.')

    def _get_ofc_input(self):
        """Get the appropriate input for OFC computation based on mode."""
        raise NotImplementedError('Implementation removed for public mirror.')

    def train_epoch(self, epoch: int) -> dict:
        raise NotImplementedError('Implementation removed for public mirror.')

    @torch.no_grad()
    def evaluate(self) -> dict:
        raise NotImplementedError('Implementation removed for public mirror.')

    def save_checkpoint(self, path: str, epoch: int, test_acc: float):
        raise NotImplementedError('Implementation removed for public mirror.')

    def fit(self, logger=None):
        """Run full training loop."""
        raise NotImplementedError('Implementation removed for public mirror.')
