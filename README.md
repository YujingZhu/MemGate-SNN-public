# MemGate-SNN

**Membrane-Potential Confidence Gating for Energy-Efficient Spiking Neural Networks**

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![PyTorch 2.0+](https://img.shields.io/badge/PyTorch-2.0%2B-ee4c2c.svg)](https://pytorch.org/)
[![SpikingJelly](https://img.shields.io/badge/SpikingJelly-0.0.0.0.14-green.svg)](https://github.com/fangwei123456/spikingjelly)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Surrogate-gradient training treats every sample identically, yet spiking neurons already carry a per-sample confidence signal in their membrane potentials — available at zero cost and previously unexploited.

**MemGate-SNN** introduces **MPCG (Membrane-Potential Confidence Gating)**, the first framework to extract zero-cost per-sample confidence from output-layer membrane potentials in SNNs — without additional parameters, forward passes, or architectural changes. A synthesizable Verilog co-processor on Zynq-7020 FPGA occupies <3% of fabric with <2 mW inference power.


> **Public Mirror**: This repository is a public mirror of an active research project.
> Core implementations (model definitions, training loops, OFC algorithms, RTL logic)
> are replaced with interface stubs. YAML configurations, synthesis reports, and
> documentation are preserved. See [NOTICE.md](NOTICE.md) for details.


---

## Highlights

- **Iso-accuracy**: statistically equivalent to SG baselines ($p > 0.05$ on MNIST / Fashion-MNIST)
- **Zero inference cost**: MPCG reduces to a single argmax at deployment
- **Interpretable confidence**: 93.7–99.8% high-confidence ratio across four benchmarks
- **Minimal overhead**: <13% training cost; no extra parameters or forward passes
- **Hardware validated**: synthesizable Verilog RTL on Zynq-7020 (100 MHz timing closure)
- **OOD detection**: AUROC = 0.985 (MNIST vs. Fashion-MNIST) at zero cost
- **Calibrated**: ECE = 0.005 on MNIST membrane confidence

## Key Results

### Multi-Seed Statistical Validation

Evaluated on RTX 4080 SUPER. MNIST / F-MNIST / N-MNIST: 5 seeds; CIFAR-10: 3 seeds.

| Dataset | Baseline (%) | MPCG (%) | Delta | p-value | Frac High |
|:---|:---:|:---:|:---:|:---:|:---:|
| MNIST | 99.27 +/- 0.04 | 99.25 +/- 0.03 | -0.02 | 0.289 (ns) | 99.8% |
| Fashion-MNIST | 88.72 +/- 0.15 | 88.57 +/- 0.09 | -0.15 | 0.113 (ns) | 93.7% |
| N-MNIST | 98.41 +/- 0.08 | 98.31 +/- 0.07 | -0.10 | <0.001 | 99.2% |
| CIFAR-10 | 84.11 +/- 0.17 | 83.48 +/- 0.09 | -0.63 | — | 95.3% |

> **ns** = not significant. MPCG maintains iso-accuracy while providing interpretable confidence metrics, energy monitoring, and OOD detection — capabilities absent from standard SG training.

### Energy Efficiency

Rectangular surrogate reduces synaptic energy by **25–43%** at the cost of accuracy on harder datasets. A curriculum schedule (ATan -> Rectangular) recovers Fashion-MNIST to 87.23%.

| Surrogate | MNIST Energy | F-MNIST Energy | N-MNIST Energy |
|:---|:---:|:---:|:---:|
| ATan (baseline) | 23.1 uJ | 25.7 uJ | 24.0 uJ |
| Rectangular | 16.3 uJ (-25%) | 16.9 uJ (-33%) | 12.8 uJ (-43%) |

### Training Overhead

| Dataset | Baseline (s/epoch) | MPCG (s/epoch) | Overhead |
|:---|:---:|:---:|:---:|
| MNIST | 14.21 | 15.08 | +6.1% |
| Fashion-MNIST | 14.25 | 15.13 | +6.2% |
| CIFAR-10 | 17.29 | 19.41 | +12.3% |

### FPGA Co-Processor (Zynq-7020, 100 MHz)

| Mode | LUT | FF | BRAM | DSP | Power |
|:---|:---:|:---:|:---:|:---:|:---:|
| Training | 1,365 (2.6%) | 1,628 (1.5%) | 11 (3.9%) | 3 (1.4%) | 53 mW |
| Inference | 358 (0.67%) | 229 | 0 | 0 | <2 mW |

---

## Quick Start

### Installation

```bash
conda create -n memgate python=3.9
conda activate memgate
pip install -r requirements.txt
```

### Train

```
# Training requires the full source code.
# This public mirror contains interface stubs only.
# Contact the authors for access.
```

### Evaluate

```bash
python scripts/eval.py --config configs/mnist_ofc.yaml \
    --checkpoint checkpoints/best_mnist_ofc.pt
```

---

## Architecture

### ConvSNN (953K params — MNIST, Fashion-MNIST, N-MNIST)

```
Input [B, C, H, W]
  |  direct encoding: repeat T=4 --> [T, B, C, H, W]
  |
  +-- Conv(C_in, 128) -> BN -> LIF -> AvgPool  ]
  +-- Conv(128, 128)   -> BN -> LIF -> AvgPool  ] x2
  +-- Flatten -> FC(128) -> LIF                  ]
  +-- FC(10) -> LIF                              ] x2
  |
  +-- mean firing rate over T --> [B, 10] --> CrossEntropy
```

### ConvSNN-4L (2.1M params — CIFAR-10)

```
Input [B, 3, 32, 32]
  |
  +-- Conv(3, 64)    -> BN -> LIF -> AvgPool
  +-- Conv(64, 128)  -> BN -> LIF -> AvgPool
  +-- Conv(128, 256) -> BN -> LIF -> AvgPool
  +-- Conv(256, 256) -> BN -> LIF
  +-- Flatten -> FC(256) -> LIF
  +-- FC(10) -> LIF
```

All layers use LIF neurons (tau=2.0, ATan surrogate alpha=2.0, SpikingJelly multi-step mode).

### MPCG Pipeline

```
Forward pass                     MPCG pipeline (training only)
============                     ============================

LIF output layer                 1. Hook captures pre-threshold
    |                               membrane V[T, B, 10]
    v                                        |
mean firing rate                 2. mean(V, dim=T) -> softmax -> max
    |                               = MPCG confidence per sample
    v                                        |
CE loss  <--- w_n (weight) ---   3. Adaptive threshold theta via EMA
                                    (cold-start at 0.7 for 100 batches)
                                             |
                                 4. DNLP sigmoid maps confidence
                                    to per-sample loss weight w_n
                                    high conf -> w ~ 0.05 (attenuate)
                                    low  conf -> w ~ 1.00 (full SG)
```

At **inference**, MPCG reduces to `argmax` — **zero additional cost**.

---

## Configurations

All behavior is controlled by YAML configs in `configs/`. 17 configs span four datasets and multiple modes:

| Config | Dataset | MPCG | Surrogate | Epochs | Notes |
|:---|:---|:---:|:---|:---:|:---|
| `mnist_baseline.yaml` | MNIST | Off | ATan | 30 | |
| `mnist_ofc.yaml` | MNIST | On | ATan | 30 | |
| `mnist_ofc_rectangular.yaml` | MNIST | On | Rectangular | 30 | |
| `fmnist_baseline.yaml` | Fashion-MNIST | Off | ATan | 50 | |
| `fmnist_ofc_tuned.yaml` | Fashion-MNIST | On | ATan | 50 | **Primary config** (k=3, w_min=0.15) |
| `fmnist_ofc_rectangular.yaml` | Fashion-MNIST | On | Rectangular | 50 | |
| `fmnist_ofc_curriculum.yaml` | Fashion-MNIST | On | ATan->Rect | 25 | Curriculum schedule |
| `nmnist_baseline.yaml` | N-MNIST | Off | ATan | 30 | |
| `nmnist_ofc.yaml` | N-MNIST | On | ATan | 30 | |
| `nmnist_ofc_rectangular.yaml` | N-MNIST | On | Rectangular | 30 | |
| `cifar10_baseline.yaml` | CIFAR-10 | Off | ATan | 100 | B=256, lr=5e-4 |
| `cifar10_ofc.yaml` | CIFAR-10 | On | ATan | 100 | B=256, lr=5e-4 |
| `cifar10_ofc_rectangular.yaml` | CIFAR-10 | On | Rectangular | 100 | |

<details>
<summary>MPCG hyperparameters</summary>

| Parameter | Default | Description |
|:---|:---:|:---|
| `ofc.mode` | `membrane` | Confidence source (membrane potential softmax) |
| `ofc.warmup_epochs` | 5 | Pure SG epochs before gating activates |
| `ofc.beta` | 0.9 | Threshold multiplier: theta = EMA x beta |
| `ofc.steepness` | 5.0 | Sigmoid sharpness in DNLP (3.0 for F-MNIST) |
| `ofc.min_weight` | 0.05 | Floor gradient weight (0.15 for F-MNIST) |
| `ofc.theta_mode` | `ema` | Threshold mode: `ema` or `fixed` |
| `ofc.pj_per_sop` | 0.9 | Energy per synaptic op (pJ, 45nm) |

</details>

---

## Datasets

| Dataset | Source | Channels | Resolution | Loader |
|:---|:---|:---:|:---:|:---|
| MNIST | torchvision | 1 | 28x28 | `src/data/mnist.py` |
| Fashion-MNIST | torchvision | 1 | 28x28 | `src/data/fashion_mnist.py` |
| N-MNIST | SpikingJelly | 2 (polarity) | 34x34 -> 28x28 | `src/data/n_mnist.py` |
| CIFAR-10 | torchvision | 3 | 32x32 | `src/data/cifar10.py` |

> **N-MNIST** requires manual download of `Train.zip` and `Test.zip` from the [original source](https://www.garrickorchard.com/datasets/n-mnist). Place in `data/download/`. SpikingJelly converts events to frames on first load.

---

## Scripts Reference

### Core

| Script | Description |
|:---|:---|
| `scripts/train.py` | Training entry point (config-driven) |
| `scripts/eval.py` | Evaluation with spike monitoring |

### Multi-Seed & Ablation

| Script | Description |
|:---|:---|
| `scripts/run_multiseed.py` | Run N seeds per config |
| `scripts/aggregate_multiseed.py` | Aggregate results + paired t-test |
| `scripts/run_ablation.py` | LOCO ablation (leave-one-component-out) |

### Analysis & Visualization

| Script | Description |
|:---|:---|
| `scripts/full_analysis.py` | Multi-dataset comparison -> PNG + LaTeX |
| `scripts/analyze_ofc.py` | OFC plots (CDF, histogram, theta curve) |
| `scripts/paper_figures.py` | IEEE / AICAS paper-quality figures |
| `scripts/per_class_ofc.py` | Per-class OFC heatmap + confusion matrix |
| `scripts/calibration_analysis.py` | Reliability diagrams + ECE |
| `scripts/ood_detection.py` | OOD detection (AUROC) |

### Benchmarking

| Script | Description |
|:---|:---|
| `scripts/benchmark_training_overhead.py` | Training overhead measurement |
| `scripts/benchmark_latency.py` | Inference latency + memory |
| `scripts/energy_comparison.py` | Cross-config energy comparison |
| `scripts/sweep_ofc.py` | Hyperparameter sensitivity sweep |

<details>
<summary>Usage examples</summary>

```bash
# Multi-seed experiment (5 seeds)
python scripts/run_multiseed.py --config configs/mnist_ofc.yaml \
    --seeds 42 123 456 789 1024

# Aggregate with statistical testing
python scripts/aggregate_multiseed.py --input_dir results/multiseed

# LOCO ablation study
python scripts/run_ablation.py --epochs 30 --datasets mnist fmnist

# Paper figures (IEEE double-column)
python scripts/paper_figures.py --output-dir results/paper_figures

# Paper figures (AICAS single-column, 3.5")
python scripts/paper_figures.py --aicas --output-dir results/aicas_figures

```

</details>

---

## Hardware RTL

The `rtl/` directory contains a synthesizable Verilog implementation of the MPCG co-processor targeting Xilinx Zynq-7020 (28 nm, `xc7z020clg400-1`) at 100 MHz.

```
rtl/
├── src/                        # Verilog RTL modules
│   ├── mpcg_top.v              # Top-level 3-block pipeline
│   ├── temporal_accumulator.v  # Block 1: mean membrane over T cycles
│   ├── softmax_lut.v           # BRAM-based exp() lookup
│   ├── div_pipe16.v            # 16-stage pipelined restoring divider
│   ├── argmax_comparator.v     # Predicted class extraction
│   ├── ema_theta.v             # EMA threshold with cold-start warmup
│   ├── sigmoid_lut.v           # BRAM-based sigmoid for DNLP
│   ├── dnlp_modulator.v        # Per-sample loss weight computation
│   └── defines.vh              # Shared macros (Q8.8, NUM_CLASSES=10)
├── tb/
│   └── tb_mpcg_top.v           # Functional testbench
├── scripts/
│   ├── gen_lut.py              # Generate softmax/sigmoid LUT .mem files
│   ├── gen_test_vectors.py     # Golden test vector generation
│   ├── compare_results.py      # RTL vs FP32 comparison
│   └── quantization_check.py   # Q8.8 error analysis
└── vivado/
    ├── project.tcl             # Vivado project creation
    ├── synth_only.tcl          # Synthesis flow
    ├── impl_only.tcl           # Implementation flow
    └── constraints.xdc         # Timing constraints (100 MHz)
```

**Design highlights:**
- **Q8.8 fixed-point** (16-bit signed) throughout; mean confidence error <0.5% vs. FP32
- **16-stage pipelined divider** resolves critical path (WNS = +0.198 ns at 100 MHz)
- **Two 256-entry BRAMs** for exp() and sigmoid (1 KB total)
- **Clock gating**: Block 3 + EMA branch gated during inference -> <2 mW
- **Latency**: 37 cycles (training), 16 cycles (inference)

```bash
# Rebuild LUTs and test vectors
cd rtl/scripts
python gen_lut.py
python gen_test_vectors.py

# Run Vivado synthesis (requires Vivado 2024.1+)
cd rtl/vivado
vivado -mode batch -source project.tcl
vivado -mode batch -source synth_only.tcl
vivado -mode batch -source impl_only.tcl
```

---

## LOCO Ablation

Leave-One-Component-Out ablation isolates each MPCG component's contribution:

| Variant | MNIST | F-MNIST | Key Finding |
|:---|:---:|:---:|:---|
| Full (control) | 99.25% | 88.64% | — |
| No_warmup | 99.26% | 88.65% | Warmup has negligible impact |
| No_floor (w_min=0) | 99.26% | 88.53% | Floor stabilizes F-MNIST |
| Fixed_theta (0.7) | 99.26% | 88.53% | EMA helps on harder tasks |
| Spike_mode | 99.19% | 88.62% | MPCG degenerates (~0.01) |
| **No_modul (k=0.01)** | **99.27%** | **88.76%** | **Highest accuracy** |

**Key insight**: `No_modul` achieves the highest accuracy on both datasets, confirming that membrane-potential confidence monitoring — not gradient modulation — is the core contribution. The gating mechanism serves as a deployable accuracy-energy knob.

---

## Project Structure

```
CHAL-SNN/
├── configs/                    # 17 YAML experiment configurations
├── scripts/                    # 29 training, analysis, and benchmark scripts
├── src/
│   ├── data/                   # Dataset loaders (MNIST, F-MNIST, N-MNIST, CIFAR-10)
│   ├── models/
│   │   ├── conv_snn.py         # ConvSNN (953K) + ConvSNN-4L (2.1M)
│   │   ├── fc_snn.py           # FC-SNN (535K, debug)
│   │   └── surrogate.py        # ATan / Rectangular surrogate gradients
│   ├── ofc/
│   │   ├── ofc_manager.py      # Membrane capture + confidence computation
│   │   ├── modulator.py        # DNLP per-sample loss weighting
│   │   ├── energy.py           # Topology-based SOP energy tracking
│   │   ├── analysis.py         # OFC logging + visualization
│   │   └── early_consensus.py  # Early-exit inference
│   ├── training/
│   │   ├── trainer.py          # Training loop (standard + MPCG-augmented)
│   │   └── metrics.py          # Accuracy utilities
│   └── utils/                  # Config, seeding, hooks, CSV logging
├── rtl/                        # Synthesizable Verilog (Zynq-7020 FPGA)
├── checkpoints/                # Saved model weights (gitignored)
├── logs/                       # Training + OFC logs (gitignored)
├── results/                    # Analysis outputs (gitignored)
├── data/                       # Datasets (gitignored)
├── requirements.txt
```

---

## Citation

If you find this work useful, please cite:

```bibtex
@inproceedings{memgate2026,
  title     = {{MemGate-SNN}: Membrane-Potential Confidence Gating for
               Energy-Efficient Spiking Neural Networks},
  author    = {Anonymous},
  booktitle = {IEEE International Conference on Artificial Intelligence
               Circuits and Systems (AICAS)},
  year      = {2026}
}
```

## License

This project is released under the MIT License.
