"""FC-SNN: Fully Connected Spiking Neural Network (debugging baseline).

Architecture:
    784 -> Linear(512) -> LIF -> Linear(256) -> LIF -> Linear(10) -> LIF
"""

import torch
import torch.nn as nn
from spikingjelly.activation_based import neuron, layer

from .surrogate import get_surrogate


class FCSNN(nn.Module):

    def __init__(self, tau: float = 2.0, T: int = 4,
                 surrogate_name: str = "atan", surrogate_alpha: float = 2.0,
                 num_classes: int = 10):
        raise NotImplementedError('Implementation removed for public mirror.')

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: [B, 1, 28, 28] input images

        Returns:
            [B, num_classes] firing rate output
        """
        raise NotImplementedError('Implementation removed for public mirror.')

    def reset(self):
        raise NotImplementedError('Implementation removed for public mirror.')
