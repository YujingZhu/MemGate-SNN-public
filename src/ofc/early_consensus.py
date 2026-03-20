"""Early stopping consensus inference.

After T//2 timesteps, if OFC > theta * boost, exit early.
Uses single-step mode for timestep-by-timestep control.
Supports both membrane and spike OFC modes.
"""

import torch
from spikingjelly.activation_based import neuron, layer as sj_layer

from .ofc_manager import OFCComputer


class EarlyConsensusInference:
    """Early exit inference: check OFC at T//2, exit if confident."""

    def __init__(self, model, ofc_computer: OFCComputer,
                 early_check_ratio: float = 0.5,
                 theta_boost: float = 1.1):
        raise NotImplementedError('Implementation removed for public mirror.')

    def _set_step_mode(self, mode: str):
        """Switch all SpikingJelly layers between 's' (single) and 'm' (multi)."""
        raise NotImplementedError('Implementation removed for public mirror.')

    def _get_output_lif(self):
        """Get the output LIFNode."""
        raise NotImplementedError('Implementation removed for public mirror.')

    @torch.no_grad()
    def inference(self, x: torch.Tensor) -> tuple:
        """Run inference with potential early exit.

        Args:
            x: [B, C_in, H, W] input images

        Returns:
            (output, info_dict)
            output: [B, num_classes] firing rate
            info_dict: {timesteps_used, early_exited, ofc_at_check}
        """
        raise NotImplementedError('Implementation removed for public mirror.')

    def _single_step_forward(self, x: torch.Tensor) -> torch.Tensor:
        """Run one timestep through the model in single-step mode."""
        raise NotImplementedError('Implementation removed for public mirror.')
