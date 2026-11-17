# =====================================================================
# Google Colab Standalone Figure Generator for Research Paper
# Project: Mitigating Citation Hallucination in LLM-Assisted Reviews
# Student: Sujal Rajesh Ghagare (MSE2026015) | IIIT Allahabad
# =====================================================================

import matplotlib.pyplot as plt
import numpy as np
import os

# Create output folder for figures
os.makedirs("figures", exist_ok=True)

# Styling for academic publication
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 14,
    'lines.linewidth': 2.0,
    'lines.markersize': 6,
    'grid.alpha': 0.5
})

# =====================================================================
# 1. EXPERIMENTAL DATA (Directly from verified benchmark runs)
# =====================================================================
methods = ["Vanilla-LLM", "Standard-RAG", "PAG (Ours)"]

# Metric means from test split (N=12 queries)
metric_labels = [
    "Claim Precision (P_claim)",
    "Citation Recall (R_cite)",
    "Hallucination (H_cite)",
    "Grounding Score (S_ground)",
    "Metadata Veracity (M_valid)"
]

performance_data = {
    "Vanilla-LLM": [0.11, 1.00, 0.89, 0.15, 0.61],
    "Standard-RAG": [0.67, 1.00, 0.33, 0.68, 1.00],
    "PAG (Ours)":   [1.00, 1.00, 0.00, 1.00, 1.00]
}

# Error typology counts (out of 36 claims per method)
error_types = ["Type I: Fabricated", "Type II: Irrelevant", "Type III: Extrapolated", "Type IV: Supported"]
type_counts = {
    "Vanilla-LLM": [14, 18, 0, 4],
    "Standard-RAG": [0, 12, 0, 24],
    "PAG (Ours)":   [0, 0, 0, 36]
}

# Threshold sensitivity ablation (tau in [0.20, 0.80])
taus = [0.20, 0.35, 0.50, 0.65, 0.80]
p_vals = [1.00, 1.00, 1.00, 1.00, 1.00]
r_vals = [1.00, 1.00, 1.00, 1.00, 1.00]
h_vals = [0.00, 0.00, 0.00, 0.00, 0.00]
f1_vals = [1.00, 1.00, 1.00, 1.00, 1.00]

# =====================================================================
# FIGURE 1: Multi-Metric Comparative Bar Chart
# =====================================================================
fig, ax = plt.subplots(figsize=(9, 4.8))
x = np.arange(len(metric_labels))
width = 0.25
colors = ["#d95f02", "#7570b3", "#1b9e77"]

for i, m in enumerate(methods):
    vals = performance_data[m]
    rects = ax.bar(x + (i - 1) * width, vals, width, label=m, color=colors[i], edgecolor='black', linewidth=0.8, alpha=0.9)
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f"{height:.2f}",
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=8, fontweight='bold')

ax.set_ylabel('Score / Proportion')
ax.set_title('Figure 1: Comparative Performance Across Literature Synthesis Methods (Test Split, N=12)')
ax.set_xticks(x)
ax.set_xticklabels(metric_labels, rotation=15, ha='right')
ax.set_ylim(0, 1.15)
ax.legend(loc='upper right', frameon=True)
plt.tight_layout()
plt.savefig("figures/fig1_method_comparison.png", dpi=300)
plt.savefig("figures/fig1_method_comparison.pdf")
plt.show()

# =====================================================================
# FIGURE 2: Stacked Claim Error Typology Breakdown
# =====================================================================
fig, ax = plt.subplots(figsize=(8, 4.5))
error_colors = ["#e41a1c", "#ff7f00", "#377eb8", "#4daf4a"]
y_pos = np.arange(len(methods))
bar_height = 0.5
bottom = np.zeros(len(methods))

for idx, etype in enumerate(error_types):
    vals = [type_counts[m][idx] for m in methods]
    ax.barh(y_pos, vals, bar_height, left=bottom, label=etype, color=error_colors[idx], edgecolor='black', linewidth=0.8)
    bottom += np.array(vals)

ax.set_yticks(y_pos)
ax.set_yticklabels(methods)
ax.set_xlabel('Total Number of Synthesized Claims')
ax.set_title('Figure 2: Claim Error Typology Breakdown across 12 Benchmark Synthesis Tasks')
ax.legend(loc='lower right', frameon=True)
plt.tight_layout()
plt.savefig("figures/fig2_error_typology.png", dpi=300)
plt.savefig("figures/fig2_error_typology.pdf")
plt.show()

# =====================================================================
# FIGURE 3: Threshold Sensitivity Ablation Curve (tau in [0.2, 0.8])
# =====================================================================
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(taus, p_vals, marker='o', color='#1b9e77', label='Claim Precision (P_claim)')
ax.plot(taus, r_vals, marker='s', color='#7570b3', label='Citation Recall (R_cite)')
ax.plot(taus, h_vals, marker='^', color='#d95f02', linestyle='--', label='Hallucination Rate (H_cite)')
ax.plot(taus, f1_vals, marker='D', color='#e7298a', linewidth=2.5, label='Harmonic Mean F1')

ax.axvline(0.50, color='gray', linestyle=':', label='Optimal Operating Threshold (tau* = 0.50)')
ax.set_xlabel(r'Passage Grounding Alignment Threshold ($	au$)')
ax.set_ylabel('Score')
ax.set_title(r'Figure 3: Precision-Recall Sensitivity Trade-Off Across Alignment Threshold $	au$')
ax.set_ylim(-0.05, 1.05)
ax.set_xlim(0.15, 0.85)
ax.legend(loc='center left', frameon=True)
plt.tight_layout()
plt.savefig("figures/fig3_tau_ablation.png", dpi=300)
plt.savefig("figures/fig3_tau_ablation.pdf")
plt.show()

print("All 3 figures successfully generated and saved to ./figures/ (both PNG and PDF)!")
