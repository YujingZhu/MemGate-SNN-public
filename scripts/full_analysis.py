"""
CHAL-SNN Full Multi-Dimensional Analysis
Generates: accuracy curves, convergence analysis, energy estimation,
           OFC confidence distribution, and LaTeX summary table.
"""
import csv
import os
import numpy as np

# ---------------------------------------------------------------------------
# Try matplotlib; fall back to Agg backend if no display
# ---------------------------------------------------------------------------
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE, 'logs')
OUT_DIR = os.path.join(BASE, 'results', 'analysis')
os.makedirs(OUT_DIR, exist_ok=True)

DATASETS = {
    'MNIST':  {'baseline': 'mnist_baseline_train_log.csv',
               'ofc':      'mnist_ofc_train_log.csv',
               'ofc_ep':   'ofc_mnist/ofc_epochs.csv'},
    'F-MNIST': {'baseline': 'fmnist_baseline_train_log.csv',
                'ofc':      'fmnist_ofc_train_log.csv',
                'ofc_ep':   'ofc_fmnist/ofc_epochs.csv'},
    'N-MNIST': {'baseline': 'nmnist_baseline_train_log.csv',
                'ofc':      'nmnist_ofc_train_log.csv',
                'ofc_ep':   'ofc_nmnist/ofc_epochs.csv'},
}

# ConvSNN topology for SOP estimation (from energy.py)
# LIF[0]->Conv2d(128,3,3): fan_out=1152
# LIF[1]->Linear(128):     fan_out=128
# LIF[2]->Linear(10):      fan_out=10
# LIF[3]->None:             fan_out=0
TOPOLOGY_FAN_OUT = [1152, 128, 10, 0]
PJ_PER_SOP = 0.9
T = 4  # timesteps


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def read_csv(path):
    raise NotImplementedError('Implementation removed for public mirror.')


def extract_acc(rows, key='test_acc'):
    raise NotImplementedError('Implementation removed for public mirror.')


def extract_epochs(rows):
    raise NotImplementedError('Implementation removed for public mirror.')


# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
data = {}
for name, files in DATASETS.items():
    bl_rows = read_csv(os.path.join(LOG_DIR, files['baseline']))
    ofc_rows = read_csv(os.path.join(LOG_DIR, files['ofc']))
    ofc_ep = read_csv(os.path.join(LOG_DIR, files['ofc_ep']))
    data[name] = {
        'bl_epochs':   extract_epochs(bl_rows),
        'bl_test_acc': extract_acc(bl_rows),
        'bl_train_acc': extract_acc(bl_rows, 'train_acc'),
        'bl_test_loss': [float(r['test_loss']) for r in bl_rows],
        'ofc_epochs':   extract_epochs(ofc_rows),
        'ofc_test_acc': extract_acc(ofc_rows),
        'ofc_train_acc': extract_acc(ofc_rows, 'train_acc'),
        'ofc_test_loss': [float(r['test_loss']) for r in ofc_rows],
        'ofc_mean':   [float(r['OFC_mean']) for r in ofc_ep],
        'ofc_std':    [float(r['OFC_std']) for r in ofc_ep],
        'ofc_theta':  [float(r['Theta']) for r in ofc_ep],
        'frac_high':  [float(r['Frac_high']) for r in ofc_ep],
    }

print("Data loaded for:", list(data.keys()))

# ===========================================================================
# FIGURE 1: Test Accuracy Curves — Baseline vs OFC (3 subplots)
# ===========================================================================
fig1, axes1 = plt.subplots(1, 3, figsize=(15, 4.5), dpi=200)
colors = {'MNIST': ('#2196F3', '#FF5722'),
          'F-MNIST': ('#4CAF50', '#E91E63'),
          'N-MNIST': ('#9C27B0', '#FF9800')}

for idx, (name, d) in enumerate(data.items()):
    ax = axes1[idx]
    c_bl, c_ofc = colors[name]
    ax.plot(d['bl_epochs'], d['bl_test_acc'], '-o', color=c_bl,
            markersize=3, linewidth=1.5, label='Baseline (SG)')
    ax.plot(d['ofc_epochs'], d['ofc_test_acc'], '-s', color=c_ofc,
            markersize=3, linewidth=1.5, label='OFC (MP-OFC)')

    # Mark best accuracy
    bl_best_idx = np.argmax(d['bl_test_acc'])
    ofc_best_idx = np.argmax(d['ofc_test_acc'])
    ax.annotate(f"{d['bl_test_acc'][bl_best_idx]:.2f}%",
                xy=(d['bl_epochs'][bl_best_idx], d['bl_test_acc'][bl_best_idx]),
                fontsize=7, color=c_bl, fontweight='bold',
                xytext=(5, 8), textcoords='offset points')
    ax.annotate(f"{d['ofc_test_acc'][ofc_best_idx]:.2f}%",
                xy=(d['ofc_epochs'][ofc_best_idx], d['ofc_test_acc'][ofc_best_idx]),
                fontsize=7, color=c_ofc, fontweight='bold',
                xytext=(5, -14), textcoords='offset points')

    ax.set_xlabel('Epoch', fontsize=11)
    ax.set_ylabel('Test Accuracy (%)', fontsize=11)
    ax.set_title(name, fontsize=13, fontweight='bold')
    ax.legend(fontsize=8, loc='lower right')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0.5, 30.5)

    # Adjust y-axis for readability
    ymin = min(min(d['bl_test_acc']), min(d['ofc_test_acc']))
    ax.set_ylim(max(ymin - 2, 0), 100.5)

fig1.suptitle('Test Accuracy: Baseline vs. MP-OFC', fontsize=14, fontweight='bold', y=1.02)
fig1.tight_layout()
fig1.savefig(os.path.join(OUT_DIR, 'fig1_accuracy_curves.png'),
             bbox_inches='tight', dpi=200)
print("Saved: fig1_accuracy_curves.png")

# ===========================================================================
# FIGURE 2: Convergence Speed Analysis
# ===========================================================================
fig2, axes2 = plt.subplots(1, 3, figsize=(15, 4.5), dpi=200)

convergence_results = {}
for idx, (name, d) in enumerate(data.items()):
    ax = axes2[idx]
    bl_final = d['bl_test_acc'][-1]  # baseline final accuracy
    target_95 = bl_final * 0.95
    target_99 = bl_final * 0.99

    # Find first epoch reaching targets
    def first_epoch_above(accs, target):
        for i, a in enumerate(accs):
            if a >= target:
                return i + 1  # 1-indexed
        return None

    bl_ep95 = first_epoch_above(d['bl_test_acc'], target_95)
    ofc_ep95 = first_epoch_above(d['ofc_test_acc'], target_95)
    bl_ep99 = first_epoch_above(d['bl_test_acc'], target_99)
    ofc_ep99 = first_epoch_above(d['ofc_test_acc'], target_99)

    convergence_results[name] = {
        'bl_final': bl_final,
        'target_95': target_95, 'target_99': target_99,
        'bl_ep95': bl_ep95, 'ofc_ep95': ofc_ep95,
        'bl_ep99': bl_ep99, 'ofc_ep99': ofc_ep99,
    }

    c_bl, c_ofc = colors[name]
    ax.plot(d['bl_epochs'], d['bl_test_acc'], '-o', color=c_bl,
            markersize=3, linewidth=1.5, label='Baseline')
    ax.plot(d['ofc_epochs'], d['ofc_test_acc'], '-s', color=c_ofc,
            markersize=3, linewidth=1.5, label='OFC')

    # Draw target lines
    ax.axhline(y=target_95, color='gray', linestyle='--', alpha=0.6,
               label=f'95% of BL final ({target_95:.1f}%)')
    ax.axhline(y=target_99, color='gray', linestyle=':', alpha=0.6,
               label=f'99% of BL final ({target_99:.1f}%)')

    # Annotate convergence points
    if ofc_ep95:
        ax.axvline(x=ofc_ep95, color=c_ofc, linestyle='--', alpha=0.3)
        ax.text(ofc_ep95 + 0.3, target_95 - 1.5, f'OFC@{ofc_ep95}',
                fontsize=7, color=c_ofc)
    if bl_ep95:
        ax.axvline(x=bl_ep95, color=c_bl, linestyle='--', alpha=0.3)
        ax.text(bl_ep95 + 0.3, target_95 + 0.5, f'BL@{bl_ep95}',
                fontsize=7, color=c_bl)

    ax.set_xlabel('Epoch', fontsize=11)
    ax.set_ylabel('Test Accuracy (%)', fontsize=11)
    ax.set_title(f'{name} — Convergence', fontsize=12, fontweight='bold')
    ax.legend(fontsize=6.5, loc='lower right')
    ax.grid(True, alpha=0.3)
    ymin = min(min(d['bl_test_acc']), min(d['ofc_test_acc']))
    ax.set_ylim(max(ymin - 2, 0), 100.5)
    ax.set_xlim(0.5, 30.5)

fig2.suptitle('Convergence Speed: Epochs to Reach 95%/99% of Baseline Final Acc',
              fontsize=13, fontweight='bold', y=1.02)
fig2.tight_layout()
fig2.savefig(os.path.join(OUT_DIR, 'fig2_convergence.png'),
             bbox_inches='tight', dpi=200)
print("Saved: fig2_convergence.png")

# Print convergence table
print("\n=== Convergence Speed ===")
for name, cr in convergence_results.items():
    speedup_95 = ''
    if cr['bl_ep95'] and cr['ofc_ep95']:
        diff = cr['bl_ep95'] - cr['ofc_ep95']
        speedup_95 = f"  (OFC {'faster' if diff > 0 else 'slower'} by {abs(diff)} epochs)"
    print(f"  {name}: BL_final={cr['bl_final']:.2f}%")
    print(f"    95% target ({cr['target_95']:.1f}%): BL@ep{cr['bl_ep95']}, OFC@ep{cr['ofc_ep95']}{speedup_95}")
    print(f"    99% target ({cr['target_99']:.1f}%): BL@ep{cr['bl_ep99']}, OFC@ep{cr['ofc_ep99']}")

# ===========================================================================
# FIGURE 3: Energy / SOP Estimation
# ===========================================================================
# Estimate SOPs from OFC modulation: high-confidence samples skip full SG
# Energy savings come from frac_high * (1 - min_weight) gradient reduction
# We estimate "effective spike activity" proxy via train_loss ratio

fig3, axes3 = plt.subplots(1, 3, figsize=(15, 4.5), dpi=200)

energy_results = {}
for idx, (name, d) in enumerate(data.items()):
    ax = axes3[idx]

    # Estimate SOP-based energy:
    # Baseline: all samples get full SG backprop
    # OFC: frac_high samples get min_weight(0.05) gradient, rest get full
    # Effective gradient work = (1 - frac_high) * 1.0 + frac_high * 0.05
    frac_high = np.array(d['frac_high'])
    min_weight = 0.05

    # Warmup: first 5 epochs = no modulation (all full SG)
    effective_work = np.ones(30)
    effective_work[5:] = (1 - frac_high[5:]) + frac_high[5:] * min_weight

    # Forward SOPs are same for both (same model, same data)
    # We compare relative training compute
    sg_ratio = effective_work * 100  # % of baseline compute

    ax.fill_between(range(1, 31), sg_ratio, 100, alpha=0.3, color='green',
                    label='Gradient savings')
    ax.plot(range(1, 31), sg_ratio, '-', color='green', linewidth=2,
            label='Effective gradient load (%)')
    ax.axhline(y=100, color='gray', linestyle='--', alpha=0.5, label='Baseline (100%)')
    ax.axvspan(0.5, 5.5, alpha=0.1, color='red', label='Warmup (no OFC)')

    avg_savings = (1 - effective_work[5:].mean()) * 100
    energy_results[name] = {
        'avg_savings_pct': avg_savings,
        'final_frac_high': frac_high[-1],
        'final_ofc_mean': d['ofc_mean'][-1],
        'effective_work_final': effective_work[-1] * 100,
    }

    ax.set_xlabel('Epoch', fontsize=11)
    ax.set_ylabel('Relative Gradient Load (%)', fontsize=11)
    ax.set_title(f'{name} — SG Ratio={effective_work[-1]*100:.1f}%',
                 fontsize=12, fontweight='bold')
    ax.legend(fontsize=7, loc='center right')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 110)
    ax.set_xlim(0.5, 30.5)

fig3.suptitle('Energy Efficiency: OFC Gradient Modulation Savings',
              fontsize=13, fontweight='bold', y=1.02)
fig3.tight_layout()
fig3.savefig(os.path.join(OUT_DIR, 'fig3_energy_sops.png'),
             bbox_inches='tight', dpi=200)
print("\nSaved: fig3_energy_sops.png")

print("\n=== Energy Estimation ===")
for name, er in energy_results.items():
    print(f"  {name}: avg gradient savings = {er['avg_savings_pct']:.1f}%, "
          f"final frac_high = {er['final_frac_high']*100:.1f}%, "
          f"final effective load = {er['effective_work_final']:.1f}%")

# ===========================================================================
# FIGURE 4: OFC Confidence Distribution — OFC_mean, Theta, Frac_high
# ===========================================================================
fig4, axes4 = plt.subplots(2, 3, figsize=(15, 8), dpi=200)

for idx, (name, d) in enumerate(data.items()):
    epochs = list(range(1, 31))
    c_bl, c_ofc = colors[name]

    # Top row: OFC_mean and Theta
    ax_top = axes4[0, idx]
    ax_top.plot(epochs, d['ofc_mean'], '-o', color=c_ofc, markersize=3,
                linewidth=2, label='OFC Mean')
    ax_top.fill_between(epochs,
                        np.array(d['ofc_mean']) - np.array(d['ofc_std']),
                        np.minimum(np.array(d['ofc_mean']) + np.array(d['ofc_std']), 1.0),
                        alpha=0.2, color=c_ofc)
    ax_top.plot(epochs, d['ofc_theta'], '--', color='black', linewidth=1.5,
                label=r'Threshold $\theta$')
    ax_top.axvspan(0.5, 5.5, alpha=0.08, color='red')
    ax_top.set_ylabel('Confidence', fontsize=11)
    ax_top.set_title(f'{name}', fontsize=13, fontweight='bold')
    ax_top.legend(fontsize=8)
    ax_top.grid(True, alpha=0.3)
    ax_top.set_ylim(0, 1.05)
    ax_top.set_xlim(0.5, 30.5)

    # Bottom row: Frac_high
    ax_bot = axes4[1, idx]
    ax_bot.bar(epochs, np.array(d['frac_high']) * 100, color=c_ofc, alpha=0.7,
               label='Frac High (%)')
    ax_bot.axvspan(0.5, 5.5, alpha=0.08, color='red', label='Warmup')
    ax_bot.set_xlabel('Epoch', fontsize=11)
    ax_bot.set_ylabel('High-Confidence Ratio (%)', fontsize=11)
    ax_bot.legend(fontsize=8)
    ax_bot.grid(True, alpha=0.3, axis='y')
    ax_bot.set_ylim(0, 105)
    ax_bot.set_xlim(0.5, 30.5)

fig4.suptitle('OFC Confidence Distribution: Mean, Threshold, and High-Confidence Ratio',
              fontsize=14, fontweight='bold', y=1.01)
fig4.tight_layout()
fig4.savefig(os.path.join(OUT_DIR, 'fig4_ofc_confidence.png'),
             bbox_inches='tight', dpi=200)
print("Saved: fig4_ofc_confidence.png")

# ===========================================================================
# FIGURE 5: Combined 4-panel summary (for paper)
# ===========================================================================
fig5 = plt.figure(figsize=(14, 10), dpi=200)
gs = GridSpec(2, 2, figure=fig5, hspace=0.35, wspace=0.3)

# Panel (a): All accuracy curves
ax_a = fig5.add_subplot(gs[0, 0])
styles = {'MNIST': ('o', '-'), 'F-MNIST': ('s', '-'), 'N-MNIST': ('^', '-')}
for name, d in data.items():
    mk, ls = styles[name]
    c_bl, c_ofc = colors[name]
    ax_a.plot(d['bl_epochs'], d['bl_test_acc'], ls, marker=mk, color=c_bl,
              markersize=3, linewidth=1.2, label=f'{name} BL')
    ax_a.plot(d['ofc_epochs'], d['ofc_test_acc'], ls, marker=mk, color=c_ofc,
              markersize=3, linewidth=1.2, alpha=0.7, label=f'{name} OFC',
              linestyle='--')
ax_a.set_xlabel('Epoch')
ax_a.set_ylabel('Test Accuracy (%)')
ax_a.set_title('(a) Accuracy Curves', fontweight='bold')
ax_a.legend(fontsize=6, ncol=2, loc='lower right')
ax_a.grid(True, alpha=0.3)

# Panel (b): OFC mean comparison
ax_b = fig5.add_subplot(gs[0, 1])
for name, d in data.items():
    _, c_ofc = colors[name]
    ax_b.plot(range(1, 31), d['ofc_mean'], '-o', color=c_ofc, markersize=3,
              linewidth=1.5, label=name)
ax_b.set_xlabel('Epoch')
ax_b.set_ylabel('OFC Mean Confidence')
ax_b.set_title('(b) OFC Confidence Evolution', fontweight='bold')
ax_b.legend(fontsize=8)
ax_b.grid(True, alpha=0.3)
ax_b.set_ylim(0.4, 1.05)

# Panel (c): Frac_high comparison
ax_c = fig5.add_subplot(gs[1, 0])
x = np.arange(1, 31)
width = 0.25
for i, (name, d) in enumerate(data.items()):
    _, c_ofc = colors[name]
    ax_c.bar(x + (i - 1) * width, np.array(d['frac_high']) * 100,
             width, color=c_ofc, alpha=0.7, label=name)
ax_c.set_xlabel('Epoch')
ax_c.set_ylabel('Frac High (%)')
ax_c.set_title('(c) High-Confidence Ratio', fontweight='bold')
ax_c.legend(fontsize=8)
ax_c.grid(True, alpha=0.3, axis='y')

# Panel (d): OFC_std comparison (difficulty indicator)
ax_d = fig5.add_subplot(gs[1, 1])
for name, d in data.items():
    _, c_ofc = colors[name]
    ax_d.plot(range(1, 31), d['ofc_std'], '-o', color=c_ofc, markersize=3,
              linewidth=1.5, label=name)
ax_d.set_xlabel('Epoch')
ax_d.set_ylabel('OFC Std (Confidence Spread)')
ax_d.set_title('(d) Confidence Spread (Higher = Harder Task)', fontweight='bold')
ax_d.legend(fontsize=8)
ax_d.grid(True, alpha=0.3)

fig5.suptitle('CHAL-SNN: MP-OFC Multi-Dataset Analysis', fontsize=15, fontweight='bold')
fig5.savefig(os.path.join(OUT_DIR, 'fig5_paper_summary.png'),
             bbox_inches='tight', dpi=200)
print("Saved: fig5_paper_summary.png")

# ===========================================================================
# LaTeX Summary Table
# ===========================================================================
print("\n" + "=" * 80)
print("LaTeX Summary Table")
print("=" * 80)

latex = r"""
\begin{table}[htbp]
\centering
\caption{CHAL-SNN: Multi-Dataset Experimental Results with MP-OFC}
\label{tab:results}
\resizebox{\textwidth}{!}{%
\begin{tabular}{l|cc|cc|cc|cc}
\toprule
\multirow{2}{*}{\textbf{Dataset}} &
\multicolumn{2}{c|}{\textbf{Best Test Acc (\%)}} &
\multicolumn{2}{c|}{\textbf{Convergence (ep to 95\%)}} &
\multicolumn{2}{c|}{\textbf{OFC Confidence}} &
\multicolumn{2}{c}{\textbf{Gradient Efficiency}} \\
& Baseline & OFC & Baseline & OFC &
OFC Mean & Frac High &
SG Ratio & Savings \\
\midrule
"""

for name, d in data.items():
    bl_best = max(d['bl_test_acc'])
    ofc_best = max(d['ofc_test_acc'])
    cr = convergence_results[name]
    er = energy_results[name]

    bl_ep = cr['bl_ep95'] if cr['bl_ep95'] else '--'
    ofc_ep = cr['ofc_ep95'] if cr['ofc_ep95'] else '--'

    latex += (f"{name} & {bl_best:.2f} & {ofc_best:.2f} & "
              f"{bl_ep} & {ofc_ep} & "
              f"{er['final_ofc_mean']:.4f} & {er['final_frac_high']*100:.1f}\\% & "
              f"{er['effective_work_final']:.1f}\\% & {er['avg_savings_pct']:.1f}\\% \\\\\n")

latex += r"""\bottomrule
\end{tabular}%
}
\begin{tablenotes}\small
\item MP-OFC: Membrane-Potential Output Firing Consensus.
SG Ratio: effective gradient compute relative to baseline.
Convergence: first epoch reaching 95\% of baseline final accuracy.
Warmup: 5 epochs of pure SG before OFC modulation begins.
\end{tablenotes}
\end{table}
"""

print(latex)

# Save LaTeX to file
with open(os.path.join(OUT_DIR, 'results_table.tex'), 'w') as f:
    f.write(latex)
print(f"Saved: results_table.tex")

# ===========================================================================
# Final console summary
# ===========================================================================
print("\n" + "=" * 80)
print("ANALYSIS COMPLETE — All outputs saved to:", OUT_DIR)
print("=" * 80)
print("\nGenerated files:")
for f in sorted(os.listdir(OUT_DIR)):
    fpath = os.path.join(OUT_DIR, f)
    size = os.path.getsize(fpath)
    print(f"  {f:40s} {size:>10,} bytes")
