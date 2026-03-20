"""OFC (Output Firing Consensus) module for CHAL-SNN.

Provides confidence-based hybrid learning with DNLP modulation,
adaptive thresholding, early consensus inference, and energy tracking.
"""

from .ofc_manager import OutputMembraneCapture, OutputSpikeCapture, OFCComputer
from .modulator import DNLPModulator
from .analysis import OFCLogger, OFCAnalyzer
from .energy import EnergyTracker
from .early_consensus import EarlyConsensusInference

__all__ = [
    "OutputMembraneCapture",
    "OutputSpikeCapture",
    "OFCComputer",
    "DNLPModulator",
    "OFCLogger",
    "OFCAnalyzer",
    "EnergyTracker",
    "EarlyConsensusInference",
]
