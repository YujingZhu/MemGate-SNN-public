# Notice -- Public Mirror

This repository is a **public mirror** of the MemGate-SNN research project. It is provided
to accompany a paper submission and allow reviewers and the community to inspect the
architecture, interfaces, configurations, and verified results.

## What is included

- **YAML configurations** (17 configs) -- Full hyperparameter definitions for all experiments
- **Python module interfaces** -- Class/function signatures and docstrings for all `src/` modules
- **Script interfaces** -- CLI argument definitions for all 14 core scripts
- **RTL module interfaces** -- Full port declarations for all 8 Verilog modules
- **RTL parameter definitions** (`defines.vh`) -- Complete Q8.8 fixed-point constants
- **Vivado synthesis reports** -- Post-implementation utilization, timing, and power
- **Vivado TCL scripts** -- Project creation, synthesis, and implementation flows
- **Timing constraints** -- XDC constraints for Zynq-7020 at 100 MHz
- **requirements.txt** -- Python dependencies

## What is NOT included

| Category | Reason |
|----------|--------|
| Python model definitions & training loops | IP protection during review |
| OFC algorithm implementations | IP protection during review |
| RTL implementation bodies | IP protection during review |
| Testbench stimulus/verification logic | IP protection during review |
| LUT data files (`.mem`) | Regenerable from `rtl/scripts/gen_lut.py` |
| Trained model weights (`checkpoints/`) | Regenerable from full source |
| Training logs and results | Regenerable from full source |
| Paper source (`.tex`) | Under review |
| Shell scripts with credentials | Security |

## How to obtain the full source

Contact the authors. The full source will be released upon paper acceptance.
