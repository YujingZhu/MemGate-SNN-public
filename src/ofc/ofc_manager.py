"""OFC (Output Firing Consensus) computation and adaptive threshold.

Supports two modes:
- 'membrane' (default): Uses continuous membrane potentials for confidence.
  OFC = max(softmax(mean_potential)) — always non-degenerate.
- 'spike' (legacy): Uses binary spike counts. OFC = S_winner / S_total.
  Unreliable with small T (e.g., T=4).
"""

import torch
import torch.nn.functional as F
from spikingjelly.activation_based import neuron


class OutputMembraneCapture:
    """Forward hook on the output LIFNode to capture membrane inputs [T, B, C].

    Captures the pre-threshold input to the LIF neuron (continuous-valued),
    which is always informative regardless of spike sparsity.
    Also captures output spikes for energy tracking.
    """

    def __init__(self, model):
        raise NotImplementedError('Implementation removed for public mirror.')

    def _attach(self, model):
        raise NotImplementedError('Implementation removed for public mirror.')

    def _hook(self, module, input, output):
        # input[0] shape: [T, B, num_classes] — pre-threshold membrane input
        # output shape: [T, B, num_classes] — binary spikes
        raise NotImplementedError('Implementation removed for public mirror.')

    @property
    def membrane_input(self) -> torch.Tensor:
        """Return captured membrane input [T, B, C]."""
        raise NotImplementedError('Implementation removed for public mirror.')

    @property
    def spikes(self) -> torch.Tensor:
        """Return captured output spikes [T, B, C]."""
        raise NotImplementedError('Implementation removed for public mirror.')

    def remove(self):
        raise NotImplementedError('Implementation removed for public mirror.')


# Keep legacy alias for backward compatibility
OutputSpikeCapture = OutputMembraneCapture


class OFCComputer:
    """OFC computation with adaptive dynamic threshold.

    Supports 'membrane' mode (softmax on mean membrane potential)
    and legacy 'spike' mode (spike count ratio).
    """

    def __init__(self, mode: str = 'membrane', beta: float = 0.9,
                 ema_decay: float = 0.99, cold_start_batches: int = 100,
                 cold_start_theta: float = 0.7,
                 min_spike_threshold: int = 5,
                 theta_mode: str = 'ema'):
        raise NotImplementedError('Implementation removed for public mirror.')

    def compute_ofc(self, data: torch.Tensor) -> torch.Tensor:
        """Compute per-sample OFC values.

        Args:
            data: [T, B, C] tensor — membrane input (membrane mode) or spikes (spike mode)

        Returns:
            ofc_values: [B] OFC in [0, 1]
        """
        raise NotImplementedError('Implementation removed for public mirror.')

    def _compute_membrane_ofc(self, membrane_input: torch.Tensor) -> torch.Tensor:
        """Membrane-potential OFC: softmax confidence on mean potential."""
        raise NotImplementedError('Implementation removed for public mirror.')

    def _compute_spike_ofc(self, output_spikes: torch.Tensor) -> torch.Tensor:
        """Legacy spike-count OFC: S_winner / S_total."""
        raise NotImplementedError('Implementation removed for public mirror.')

    def update_threshold(self, ofc_batch_mean: float):
        """Update running average and dynamic threshold via EMA."""
        raise NotImplementedError('Implementation removed for public mirror.')

    @property
    def theta(self) -> float:
        """Current dynamic threshold."""
        raise NotImplementedError('Implementation removed for public mirror.')

    def get_decisions(self, ofc_values: torch.Tensor) -> torch.Tensor:
        """Return bool mask: True = high-confidence (OFC > theta)."""
        raise NotImplementedError('Implementation removed for public mirror.')
