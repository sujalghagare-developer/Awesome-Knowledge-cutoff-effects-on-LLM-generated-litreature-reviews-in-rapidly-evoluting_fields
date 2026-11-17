#!/usr/bin/env python3
"""
Publication-Quality Figure and Table Generation.
Reads results.csv and summary_metrics.json, produces clean vector PDF & PNG plots.

Course: AI Tools for Research
Student: Sujal Rajesh Ghagare (MSE2026015)
"""

import sys
import os
import json
import shutil
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set academic publication style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams.update({
    'font.family': 'serif',
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

def generate_all_plots():
    config_path = "configs/config.json"
    with open(config_path, "r") as f:
        config = json.load(f)

    csv_path = config["output_paths"]["results_csv"]
    json_path = config["output_paths"]["summary_metrics_json"]
    fig_dir = config["output_paths"]["figures_dir"]
    paper_fig_dir = config["output_paths"]["paper_figures_dir"]

    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(paper_fig_dir, exist_ok=True)

    df = pd.read_csv(csv_path)
    with open(json_path, "r") as f:
        metrics = json.load(f)

    # -------------------------------------------------------------
    # Figure 1: Multi-Metric Comparative Bar Chart
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    methods = ["Vanilla-LLM", "Standard-RAG", "PAG (Ours)"]
    metric_keys = ["p_claim_mean", "r_cite_mean", "h_cite_mean", "s_ground_mean", "m_valid_mean"]
    metric_labels = [
        "Claim Precision (P_claim)",
        "Citation Recall (R_cite)",
        "Hallucination (H_cite)",
        "Grounding Score (S_ground)",
        "Metadata Veracity (M_valid)"
    ]

    x = np.arange(len(metric_labels))
    width = 0.25
    colors = ["#d95f02", "#7570b3", "#1b9e77"]

    for i, m in enumerate(methods):
        vals = [metrics["summary"][m][k] for k in metric_keys]
        rects = ax.bar(x + (i - 1) * width, vals, width, label=m, color=colors[i], edgecolor='black', linewidth=0.8, alpha=0.9)
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom', fontsize=8, fontweight='bold')

    ax.set_ylabel('Score / Proportion')
    ax.set_title('Comparative Performance Across Literature Synthesis Methods (Test Split, N=12)')
    ax.set_xticks(x)
    ax.set_xticklabels(metric_labels, rotation=15, ha='right')
    ax.set_ylim(0, 1.15)
    ax.legend(loc='upper right', frameon=True)
    plt.tight_layout()

    fig1_png = os.path.join(fig_dir, "fig1_method_comparison.png")
    fig1_pdf = os.path.join(fig_dir, "fig1_method_comparison.pdf")
    plt.savefig(fig1_png, dpi=300)
    plt.savefig(fig1_pdf)
    plt.close()
    print(f"Generated Figure 1: {fig1_png}")

    # -------------------------------------------------------------
    # Figure 2: Stacked Error Typology Breakdown
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    error_types = ["Type I: Fabricated", "Type II: Irrelevant", "Type III: Extrapolated", "Type IV: Supported"]
    error_colors = ["#e41a1c", "#ff7f00", "#377eb8", "#4daf4a"]

    type_counts = {
        "Vanilla-LLM": [
            metrics["summary"]["Vanilla-LLM"]["total_type_I"],
            metrics["summary"]["Vanilla-LLM"]["total_type_II"],
            metrics["summary"]["Vanilla-LLM"]["total_type_III"],
            metrics["summary"]["Vanilla-LLM"]["total_type_IV"]
        ],
        "Standard-RAG": [
            metrics["summary"]["Standard-RAG"]["total_type_I"],
            metrics["summary"]["Standard-RAG"]["total_type_II"],
            metrics["summary"]["Standard-RAG"]["total_type_III"],
            metrics["summary"]["Standard-RAG"]["total_type_IV"]
        ],
        "PAG (Ours)": [
            metrics["summary"]["PAG (Ours)"]["total_type_I"],
            metrics["summary"]["PAG (Ours)"]["total_type_II"],
            metrics["summary"]["PAG (Ours)"]["total_type_III"],
            metrics["summary"]["PAG (Ours)"]["total_type_IV"]
        ]
    }

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
    ax.set_title('Claim Error Typology Breakdown across 12 Benchmark Synthesis Tasks')
    ax.legend(loc='lower right', frameon=True)
    plt.tight_layout()

    fig2_png = os.path.join(fig_dir, "fig2_error_typology.png")
    fig2_pdf = os.path.join(fig_dir, "fig2_error_typology.pdf")
    plt.savefig(fig2_png, dpi=300)
    plt.savefig(fig2_pdf)
    plt.close()
    print(f"Generated Figure 2: {fig2_png}")

    # -------------------------------------------------------------
    # Figure 3: Threshold Sensitivity Ablation Curve (tau in [0.2, 0.8])
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    taus = sorted([float(k) for k in metrics["ablation"].keys()])
    p_vals = [metrics["ablation"][str(t)]["p_claim_mean"] for t in taus]
    r_vals = [metrics["ablation"][str(t)]["r_cite_mean"] for t in taus]
    h_vals = [metrics["ablation"][str(t)]["h_cite_mean"] for t in taus]
    f1_vals = [metrics["ablation"][str(t)]["f1_mean"] for t in taus]

    ax.plot(taus, p_vals, marker='o', color='#1b9e77', label='Claim Precision (P_claim)')
    ax.plot(taus, r_vals, marker='s', color='#7570b3', label='Citation Recall (R_cite)')
    ax.plot(taus, h_vals, marker='^', color='#d95f02', linestyle='--', label='Hallucination Rate (H_cite)')
    ax.plot(taus, f1_vals, marker='D', color='#e7298a', linewidth=2.5, label='Harmonic Mean F1')

    # Highlight optimal operating threshold
    best_tau_idx = int(np.argmax(f1_vals))
    best_tau = taus[best_tau_idx]
    ax.axvline(best_tau, color='gray', linestyle=':', label=f'Optimal tau* = {best_tau:.2f}')

    ax.set_xlabel(r'Passage Grounding Alignment Threshold ($\tau$)')
    ax.set_ylabel('Score')
    ax.set_title(r'Precision-Recall Sensitivity Trade-Off Across Alignment Threshold $\tau$')
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlim(0.15, 0.85)
    ax.legend(loc='center left', frameon=True)
    plt.tight_layout()

    fig3_png = os.path.join(fig_dir, "fig3_tau_ablation.png")
    fig3_pdf = os.path.join(fig_dir, "fig3_tau_ablation.pdf")
    plt.savefig(fig3_png, dpi=300)
    plt.savefig(fig3_pdf)
    plt.close()
    print(f"Generated Figure 3: {fig3_png}")

    # Copy all figures into paper/figures/ for Overleaf compilation
    for f in [fig1_png, fig1_pdf, fig2_png, fig2_pdf, fig3_png, fig3_pdf]:
        shutil.copy(f, paper_fig_dir)
    print(f"Copied all figures to {paper_fig_dir}")

if __name__ == "__main__":
    generate_all_plots()
