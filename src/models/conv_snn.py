"""ConvSNN: Convolutional Spiking Neural Network.

Architecture:
    Input [B,C_in,H,W] -> repeat T -> [T,B,C_in,H,W]
    -> Conv2d(C_in,C,3,pad=1) -> BN2d -> LIF -> AvgPool2d(2)    # H/2 x W/2
    -> Conv2d(C,C,3,pad=1) -> BN2d -> LIF -> AvgPool2d(2)        # H/4 x W/4
    -> Flatten -> Linear(C*H/4*W/4, C) -> LIF
    -> Linear(C, num_classes) -> LIF
    -> mean(dim=T) -> [B,num_classes]
"""

import torch
import torch.nn as nn
from spikingjelly.activation_based import neuron, layer

from .surrogate import get_surrogate


class ConvSNN(nn.Module):

    def __init__(self, channels: int = 128, in_channels: int = 1,
                 tau: float = 2.0, T: int = 4,
                 surrogate_name: str = "atan", surrogate_alpha: float = 2.0,
                 num_classes: int = 10, input_size: int = 28,
                 num_conv_blocks: int = 2):
        raise NotImplementedError('Implementation removed for public mirror.')

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: [B, C_in, H, W] input images

        Returns:
            [B, num_classes] firing rate output
        """
        raise NotImplementedError('Implementation removed for public mirror.')

    def reset(self):
        """Reset all neuron states (must call between batches)."""
        raise NotImplementedError('Implementation removed for public mirror.')
