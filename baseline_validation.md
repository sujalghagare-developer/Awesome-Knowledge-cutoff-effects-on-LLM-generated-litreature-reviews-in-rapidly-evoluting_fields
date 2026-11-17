# Baseline Reproduction and Validation Report
**Project:** AITR_Lab02_MSE2026015_CitationGrounding  
**Student:** Sujal Rajesh Ghagare (MSE2026015)  
**Status:** VALIDATED & FROZEN

## 1. Audited Baselines
1. **Vanilla Parametric LLM Synthesizer:** Replicates closed-book generation relying solely on internal weights (Walters & Wilder 2023).
2. **Standard Document-Level RAG:** Replicates retrieve-then-read framework (Lewis et al. 2020) with unconstrained sentence generation.

## 2. Validation Status Register
* **Data Partitioning:** VERIFIED (8 Dev queries, 12 Test queries, zero document leakage).
* **Corpus Veracity:** VERIFIED (20 open-access peer-reviewed papers with verified DOIs).
* **Seed Determinism:** VERIFIED (NumPy and Random seeds set to 42; runs produce identical outputs).
* **Metric Alignment:** VERIFIED (Max sentence-level Sorensen-Dice calibrated on Dev set).
* **Error Typology:** VERIFIED (Type I: Fabrication, Type II: Irrelevant, Type III: Unsupported, Type IV: Supported).

## 3. Discrepancy & Adaptation Notes
* Dense neural DPR retriever adapted to lexical token-match retriever to eliminate GPU dependency and maintain local execution speed (< 500 ms).
* Manual human claim audit adapted to automated thresholded token Dice scoring ($S \ge 0.50$), validated against human labels on the development partition.
