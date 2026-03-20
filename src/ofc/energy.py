"""Energy efficiency estimation via synaptic operations (SOPs) counting.

Each spike at a LIF layer drives fan_out downstream operations.
Energy = total_SOPs * pJ_per_SOP.

Uses explicit topology mapping for ConvSNN architecture:
  conv_block1.2 (LIF) -> conv_block2.0 (Conv2d): fan_out = C * 3 * 3
  conv_block2.2 (LIF) -> fc_block.1 (Linear): fan_out = C (out_features)
  fc_block.2 (LIF) -> output.0 (Linear): fan_out = num_classes
  output.1 (LIF) -> no downstream (final)
"""

import torch.nn as nn
from spikingjelly.activation_based import neuron, layer as sj_layer


class EnergyTracker:
    """Track SOPs and estimate energy consumption with proper layer-wise counting."""

    def __init__(self, model, pj_per_sop: float = 0.9):
        raise NotImplementedError('Implementation removed for public mirror.')

    @staticmethod
    def _build_topology(model) -> dict:
        """Build LIF→downstream weight layer fan_out mapping.

        Returns:
            dict mapping LIF layer name -> downstream fan_out
        """
        raise NotImplementedError('Implementation removed for public mirror.')

    def count_sops(self, spike_counts_per_layer: dict) -> int:
        """Count total SOPs given per-layer spike counts.

        Args:
            spike_counts_per_layer: {lif_layer_name: total_spikes}

        Returns:
            total SOPs for this batch
        """
        raise NotImplementedError('Implementation removed for public mirror.')

    def update(self, spike_counts_per_layer: dict,
               timesteps_used: int, total_T: int, is_sg_mode: bool,
               batch_size: int = 0):
        """Update cumulative energy statistics.

        Args:
            spike_counts_per_layer: {layer_name: total_spikes}
            timesteps_used: actual timesteps computed
            total_T: maximum timesteps
            is_sg_mode: whether this batch used full SG
            batch_size: number of samples in this batch
        """
        raise NotImplementedError('Implementation removed for public mirror.')

    def report(self) -> dict:
        """Return summary energy statistics with normalized metrics."""
        raise NotImplementedError('Implementation removed for public mirror.')

    def reset(self):
        """Reset all accumulators."""
        raise NotImplementedError('Implementation removed for public mirror.')
