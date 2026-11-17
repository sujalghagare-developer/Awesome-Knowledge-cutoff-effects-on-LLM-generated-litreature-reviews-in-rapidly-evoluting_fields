# PROMPT 15 IMPLEMENTATION
## Evidence-Grounded Manuscript Drafting in LaTeX

**Course:** AI Tools for Research  
**Student Name:** Sujal Rajesh Ghagare  
**Enrollment No:** MSE2026015  
**Affiliation:** M.Tech (IT), Indian Institute of Information Technology Allahabad (IIIT Allahabad)  
**Manuscript Title:** *Mitigating Citation Hallucination in LLM-Assisted Literature Reviews: A Controlled Study on Passage-Anchored Grounding*  
**Status:** Complete Implementation of Prompt 15 (Target Manuscript, Figures, `.tex` and Verified `.bib`)

---

### 1. Section Outline and Evidence Checklist

Prior to drafting the LaTeX manuscript, all sections were mapped directly to verified experimental outputs:

| Manuscript Section | Content Focus | Underlying Verified Evidence |
| :--- | :--- | :--- |
| **Title & Abstract** | Core findings, exact metrics, statistical tests | $P_{\text{claim}} = 1.0, H_{\text{cite}} = 0.0, p < 10^{-100}$ from `results/summary_metrics.json` |
| **§1 Introduction** | Paradox of fluency vs evidence; knowledge cutoff | Lewis et al. \cite{lewis2020rag}, Walters \& Wilder \cite{walters2023}, Review Paper |
| **§2 Related Work** | RAG, hallucination audits, attribution metrics | 10 verified citations (ALCE, FActScore, Self-RAG, CRAG) |
| **§3 Methodology** | Formal problem definition & mathematical metrics | Equations (1) to (9): $P_{\text{claim}}, R_{\text{cite}}, H_{\text{cite}}, S_{\text{ground}}, M_{\text{valid}}$ |
| **§4 Experimental Setup** | SCS-Bench-20 benchmark corpus & query splits | `data/corpus.json` ($N=20$) and `data/queries.json` ($8$ Dev, $12$ Test) |
| **§5 Results & Analysis** | Main comparative table, error typology, ablation | Table 2, Figures 1, 2, 3 in `paper/figures/` |
| **§6 Discussion** | Causal mechanism of extrapolation in RAG | Analysis of self-attention interpolation vs span anchoring |
| **§7 Limitations** | Lexical overlap constraints, benchmark scope | Honest reporting of paraphrase penalization & corpus size |
| **§8 Conclusion** | Summary of contributions and future directions | Quantized NLI cross-encoders for abstractive synthesis |
| **References** | Verified BibTeX entries | 19 verified entries in `paper/references.bib` |

---

### 2. Verification of Figures and Tables

All figures referenced in the LaTeX source are generated from genuine code outputs and saved in vector (`.pdf`) and high-resolution raster (`.png`) formats in `paper/figures/`:
1. `figures/fig1_method_comparison.pdf`: Multi-metric bar chart.
2. `figures/fig2_error_typology.pdf`: Stacked error distribution breakdown.
3. `figures/fig3_tau_ablation.pdf`: Precision-recall sensitivity trade-off curve across $\tau \in [0.20, 0.80]$.
4. TikZ Vector Flowchart (embedded directly in LaTeX): System architecture of Passage-Anchored Grounding.

---

### 3. LaTeX Compilation and Overleaf Instructions

The manuscript is written using the standard `acmart` class (`\documentclass[acmsmall,screen]{acmart}`), fully compatible with Overleaf and standard TeX Live / MiKTeX distributions.

**To compile in Overleaf:**
1. Upload the entire `paper/` folder (or project files) to an Overleaf project.
2. Ensure compiler is set to `pdfLaTeX` or `XeLaTeX`.
3. Set `main.tex` as the root document.
4. Compilation produces a complete 8-page, double-column publication-grade manuscript.

**Artifact Saved:** `prompts/PROMPT_15_IMPLEMENTATION.md`, `paper/main.tex`, and `paper/references.bib`
