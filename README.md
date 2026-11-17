# Passage-Anchored Grounding for Verifiable LLM Literature Reviews

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Reproducibility: 100%](https://img.shields.io/badge/reproducibility-verified-brightgreen.svg)]()

> **Course:** AI Tools for Research (Post Mid-Sem Assignment / Lab 02)  
> **Student:** Sujal Rajesh Ghagare  
> **Enrollment Number:** MSE2026015  
> **Institution:** Indian Institute of Information Technology Allahabad (IIIT Allahabad)

---

## 1. Problem Statement & Research Overview

When Large Language Models (LLMs) synthesize academic literature reviews, they face two critical vulnerabilities:
1. **Temporal Knowledge Cutoff:** Models cannot account for publications occurring after pre-training boundaries.
2. **Citation Hallucination & Claim Mismatch:** While standard Retrieval-Augmented Generation (RAG) fetches real papers, it frequently extrapolates beyond the retrieved context, attributing claims to cited papers that do not actually support them.

This repository implements **Passage-Anchored Grounding (PAG)**, a lightweight, deterministic verification framework that enforces sentence-level Sorensen-Dice span alignment ($S \ge \tau$) against retrieved passages prior to claim emission. PAG achieves **100% claim citation precision** ($P_{\text{claim}} = 1.0000$) and completely eliminates bibliographic fabrication (Type I) and claim-evidence extrapolations (Type III) with zero GPU compute overhead.

---

## 2. Repository Layout

```text
AITR_Lab02_Project/
├── configs/
│   └── config.json              # Frozen hyperparameters and paths
├── data/
│   ├── README.md                # Dataset documentation & licensing
│   ├── corpus.json              # 20 canonical verified papers & passages
│   └── queries.json             # 20 standardized scientific synthesis queries
├── notebooks/                   # Interactive exploration notebooks
├── src/
│   ├── __init__.py
│   ├── dataset.py               # Data loading and passage indexing
│   ├── baselines.py             # Vanilla-LLM & Standard-RAG baselines
│   ├── passage_grounding.py     # Passage-Anchored Grounding module
│   └── metrics.py               # Mathematical evaluation metrics
├── scripts/
│   ├── env_test.py              # Environment diagnostic verification
│   ├── run_experiments.py       # Main experiment execution runner
│   └── evaluate_and_plot.py     # Figure and statistical plot generator
├── results/
│   ├── results.csv              # Raw per-query evaluation measurements
│   ├── summary_metrics.json     # Aggregated distributions & p-values
│   ├── run.log                  # Execution runtime log
│   └── figures/                 # Generated PDF and PNG research plots
├── paper/
│   ├── main.tex                 # Publication manuscript (ACM/IEEE style)
│   ├── references.bib           # Verified BibTeX citations
│   └── figures/                 # Vector figures for LaTeX compilation
├── prompts/                     # Complete Prompt 01-18 implementation logs
├── requirements.txt             # Verified dependency manifest
├── research_decisions.md        # Literature-to-experiment decision register
├── baseline_validation.md       # Baseline audit and discrepancy report
├── experiment_protocol.md       # Frozen experimental protocol
├── ai_assistance_log.md         # Responsible AI audit & human decisions
└── README.md                    # Project documentation
```

---

## 3. Quickstart & Environment Setup

### Prerequisites
* Operating System: Windows 10/11, macOS, or Linux.
* Python: Version $\ge 3.10$ (Tested on Python 3.12.4).
* Hardware: Standard commodity CPU (Zero GPU required; $< 100$ MB RAM).

### Installation
```bash
# Clone the repository
git clone https://github.com/sujalghagare-developer/Awesome-Knowledge-cutoff-effects-on-LLM-generated-litreature-reviews-in-rapidly-evoluting_fields.git
cd AITR_Lab02_MSE2026015_CitationGrounding

# Install verified dependencies
pip install -r requirements.txt
```

### Environment Verification
Run the automated diagnostic suite to verify package compatibility and random seed determinism:
```bash
python scripts/env_test.py
```
*Expected Output:* `VERIFICATION RESULT: ALL CHECKS PASSED (STATUS: READY)`

---

## 4. Reproducing Experimental Results

Execute the complete experimental pipeline across all 20 queries (dev and test partitions) and threshold sweeps:
```bash
python scripts/run_experiments.py
```
* Runtime: $\approx 15\text{--}25$ seconds on local CPU.
* Outputs generated: `results/results.csv`, `results/summary_metrics.json`, `results/run.log`.

Generate publication-quality vector (`.pdf`) and raster (`.png`) research plots:
```bash
python scripts/evaluate_and_plot.py
```
* Generated figures:
  * `results/figures/fig1_method_comparison.pdf` / `.png`
  * `results/figures/fig2_error_typology.pdf` / `.png`
  * `results/figures/fig3_tau_ablation.pdf` / `.png`

---

## 5. Measured Benchmark Results

| Model Paradigm | Claim Precision ($P_{\text{claim}} \uparrow$) | Citation Recall ($R_{\text{cite}} \uparrow$) | Hallucination Rate ($H_{\text{cite}} \downarrow$) | Grounding Score ($S_{\text{ground}} \uparrow$) | Metadata Veracity ($M_{\text{valid}} \uparrow$) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Vanilla-LLM** | $0.1111 \pm 0.1641$ | $1.0000$ | $0.8889 \pm 0.1641$ | $0.1499 \pm 0.1706$ | $0.6111$ |
| **Standard-RAG** | $0.6667 \pm 0.0000$ | $1.0000$ | $0.3333 \pm 0.0000$ | $0.6751 \pm 0.0152$ | $1.0000$ |
| **PAG (Ours)** | $\mathbf{1.0000 \pm 0.0000}$ | $\mathbf{1.0000}$ | $\mathbf{0.0000 \pm 0.0000}$ | $\mathbf{1.0000 \pm 0.0000}$ | $\mathbf{1.0000}$ |

*Statistical Significance:* Paired Student's $t$-test ($t = 1.99 \times 10^{16}, p < 10^{-100}$) and Wilcoxon signed-rank test ($W = 0.0000, p = 4.88 \times 10^{-4}$) confirm overwhelming statistical superiority over baselines.

---

## 6. Minimum Reproduction Checklist for a Second Student

1. [ ] Verify Python version is $\ge 3.10$ using `python --version`.
2. [ ] Install dependencies with `pip install -r requirements.txt`.
3. [ ] Run `python scripts/env_test.py` to confirm all directory paths and seeds match.
4. [ ] Run `python scripts/test_modules.py` to confirm unit tests pass.
5. [ ] Execute `python scripts/run_experiments.py` to regenerate `results/results.csv`.
6. [ ] Execute `python scripts/evaluate_and_plot.py` to verify figures match reported plots.
7. [ ] Confirm that `summary_metrics.json` reports $P_{\text{claim}} = 1.0000$ for PAG.

---

## 7. License and Attribution

* Code & Scripts: [MIT License](LICENSE).
* Dataset & Benchmark Annotations: Creative Commons Attribution 4.0 International (CC-BY 4.0).
* Citation:
```bibtex
@article{ghagare2026grounding,
  author    = {Ghagare, Sujal Rajesh},
  title     = {Mitigating Citation Hallucination in LLM-Assisted Literature Reviews: A Controlled Study on Passage-Anchored Grounding},
  journal   = {AI Tools for Research Laboratory Monographs},
  institution = {Indian Institute of Information Technology Allahabad},
  year      = {2026}
}
```
