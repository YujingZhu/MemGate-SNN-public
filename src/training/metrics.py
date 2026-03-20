"""Training metrics for SNN monitoring."""

import torch


def accuracy(output: torch.Tensor, target: torch.Tensor) -> float:
    """Compute classification accuracy.

    Args:
        output: [B, num_classes] firing rates
        target: [B] ground truth labels

    Returns:
        Accuracy as a float in [0, 1].
    """
    raise NotImplementedError('Implementation removed for public mirror.')


def firing_rate(spikes: torch.Tensor) -> float:
    """Compute mean firing rate from spike tensor.

    Args:
        spikes: binary spike tensor of any shape

    Returns:
        Mean firing rate as a float.
    """
    raise NotImplementedError('Implementation removed for public mirror.')
