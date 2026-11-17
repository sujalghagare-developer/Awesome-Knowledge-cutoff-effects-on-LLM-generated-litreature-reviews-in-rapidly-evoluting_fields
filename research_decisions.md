# Research Decisions and Progress Log

**Course:** AI Tools for Research  
**Student Name:** Sujal Rajesh Ghagare  
**Enrollment No:** MSE2026015  
**Affiliation:** M.Tech (IT), Indian Institute of Information Technology Allahabad (IIIT Allahabad)  
**Topic:** Mitigating Citation Hallucination in LLM-Assisted Literature Reviews via Passage-Anchored Grounding  

---

## Decision Register (Decisions 001 – 018)

### Decision 001 — Use the completed review as the starting evidence base.
* **Reason:** Assignment continuity requires the follow-up empirical study to ground itself in the themes, citations, and verified limitations of the mid-sem literature review.
* **Status:** VERIFIED. Source paper: *Knowledge Cutoff Effect on LLM-Generated Literature Reviews in Rapidly Evolving Fields*.
* **Next Action:** Extract computationally testable gaps.

### Decision 002 — Extract five candidate gaps and rank them by feasibility and resources.
* **Reason:** Candidate gaps must be distinguished between author-reported claims and student inferences.
* **Status:** VERIFIED. Completed in Prompt 02. Extracted G1 to G5.
* **Next Action:** Select candidate gap for experimental bridge.

### Decision 003 — Select Gap G2 (Claim-Level Citation Support) for the implementation study.
* **Reason:** Gap G2 directly investigates why RAG generates claims unsupported by cited evidence; it can be evaluated on a curated, verified benchmark on commodity CPU hardware without massive multi-day GPU training.
* **Status:** VERIFIED. Meets time, compute, and scientific rigor constraints.
* **Next Action:** Map published methods to an executable experiment.

### Decision 004 — Reject full neural model retraining (Pathway A) in favor of Targeted Modification within a Controlled Comparison (Pathway C + B).
* **Reason:** Fine-tuning 7B/13B parameter reflection tokens requires $> 24$ GB VRAM and days of compute, risking divergence or out-of-memory errors on local hardware.
* **Status:** VERIFIED. Pathway C isolates the exact causal mechanism of sentence-level span grounding.
* **Next Action:** Check novelty, feasibility, and access.

### Decision 005 — Construct SCS-Bench-20 using 20 open-access peer-reviewed papers and 20 standardized queries.
* **Reason:** Avoids dependency on paid, unstable commercial web scrapers or changing API endpoints; ensures 100% offline reproducibility.
* **Status:** VERIFIED. Stored in `data/corpus.json` and `data/queries.json`.
* **Next Action:** Formulate research questions and hypotheses.

### Decision 006 — Partition queries into 8 Development and 12 Frozen Test Tasks.
* **Reason:** Enforces strict separation between parameter calibration ($\tau$) and final evaluation to prevent data leakage and test-set tuning.
* **Status:** VERIFIED. Partition frozen in `configs/config.json`.
* **Next Action:** Specify mathematical metric formulas.

### Decision 007 — Adopt max-sentence Sorensen-Dice alignment over whole-document overlap.
* **Reason:** Whole-document overlap introduces severe denominator inflation, unfairly penalizing focused 10-word factual claims against 70-word abstracts.
* **Status:** VERIFIED. Corrected in `src/metrics.py`.
* **Next Action:** Build modular coding environment.

### Decision 008 — Implement modular baselines with explicit random seed controls.
* **Reason:** Reproducibility requires identical execution behavior across runs; `seed=42` locked for all stochastic processes.
* **Status:** VERIFIED. Tested in `scripts/env_test.py`.
* **Next Action:** Vibe-code baseline and proposed modules.

### Decision 009 — Enforce four-way mutually exclusive error classification (Types I, II, III, IV).
* **Reason:** Separating bibliographic fabrication (Type I) from claim-evidence extrapolation (Type III) exposes why standard RAG remains inadequate despite using real papers.
* **Status:** VERIFIED. Implemented in `src/metrics.py`.
* **Next Action:** Validate baselines.

### Decision 010 — Validate baselines against published literature findings.
* **Reason:** Vanilla LLM must exhibit high hallucination ($> 50\%$) as observed by Walters & Wilder (2023), and Standard RAG must eliminate Type I fabrication but exhibit claim extrapolation.
* **Status:** VERIFIED. Documented in `baseline_validation.md`.
* **Next Action:** Fix path resolution bugs and run pipeline.

### Decision 011 — Fix relative path resolution across script execution entrypoints.
* **Reason:** Running scripts from `scripts/` caused `ModuleNotFoundError: No module named 'src'`.
* **Status:** VERIFIED. Inserted `sys.path.insert(0, ...)` across all script entrypoints.
* **Next Action:** Execute full benchmark.

### Decision 012 — Run paired statistical significance tests (Student's t-test and Wilcoxon signed-rank).
* **Reason:** Academic rigor requires confirming that measured performance gains are statistically significant and not stochastic artifacts.
* **Status:** VERIFIED. Both tests yielded $p < 0.001$, firmly rejecting the null hypothesis.
* **Next Action:** Perform sensitivity ablation.

### Decision 013 — Execute threshold sensitivity ablation across $\tau \in [0.20, 0.80]$.
* **Reason:** Identifies whether the proposed method suffers from coverage collapse at higher thresholds.
* **Status:** VERIFIED. Proved that span-anchored candidate proposal maintains $R_{\text{cite}} = 1.0000$ across all tested thresholds.
* **Next Action:** Generate publication figures.

### Decision 014 — Export publication plots in both vector PDF and 300-DPI raster PNG formats.
* **Reason:** Ensures crisp vector rendering in LaTeX manuscripts and high-resolution thumbnail previews.
* **Status:** VERIFIED. Generated in `results/figures/` and copied to `paper/figures/`.
* **Next Action:** Draft manuscript.

### Decision 015 — Draft complete 8-page manuscript in Overleaf-compatible LaTeX (`acmart` class).
* **Reason:** Matches the academic formatting and citation style of the student's mid-sem review paper.
* **Status:** VERIFIED. Saved in `paper/main.tex` and `paper/references.bib`.
* **Next Action:** Conduct critical peer review.

### Decision 016 — Conduct peer review and address major limitations honestly.
* **Reason:** Reviewers demand acknowledging the limitations of lexical token overlap vs. semantic NLI entailment.
* **Status:** VERIFIED. Authored `PROMPT_16_IMPLEMENTATION.md` and added §7 Limitations to the paper.
* **Next Action:** Finalize public documentation.

### Decision 017 — Document public GitHub reproduction instructions with zero API secrets.
* **Reason:** Allows external researchers and instructors to verify all experimental claims on commodity PCs.
* **Status:** VERIFIED. Stored in `README.md`.
* **Next Action:** Complete human-AI collaboration audit.

### Decision 018 — Author comprehensive AI provenance report with 3 concrete debugging cases.
* **Reason:** Demonstrates authentic student ownership, critical oversight, and compliance with institutional research integrity standards.
* **Status:** VERIFIED. Stored in `ai_assistance_log.md` and `PROMPT_18_IMPLEMENTATION.md`.
