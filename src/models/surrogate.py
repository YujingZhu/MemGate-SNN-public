"""Surrogate gradient factory for SNN training."""

from spikingjelly.activation_based import surrogate


def get_surrogate(name: str, alpha: float = 2.0):
    """Return a surrogate gradient function by name.

    Args:
        name: 'atan' or 'rectangular'
        alpha: sharpness parameter

    Returns:
        A surrogate gradient callable for LIFNode.
    """
    raise NotImplementedError('Implementation removed for public mirror.')
