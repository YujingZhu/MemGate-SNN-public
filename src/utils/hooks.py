"""Spike monitoring hooks for SNN layers.

Phase 2 will extend these hooks to support OFC competitive mechanisms.
"""

from spikingjelly.activation_based import neuron


class SpikeMonitor:
    """Register forward hooks on all LIFNode layers to record spike counts."""

    def __init__(self, model):
        raise NotImplementedError('Implementation removed for public mirror.')

    def _register(self):
        raise NotImplementedError('Implementation removed for public mirror.')

    def _make_hook(self, name: str):
        raise NotImplementedError('Implementation removed for public mirror.')

    def get_rates(self) -> dict:
        raise NotImplementedError('Implementation removed for public mirror.')

    def remove(self):
        raise NotImplementedError('Implementation removed for public mirror.')
