# PROMPT 08 IMPLEMENTATION
## Configure and Test the Coding Environment

**Course:** AI Tools for Research  
**Student Name:** Sujal Rajesh Ghagare  
**Enrollment No:** MSE2026015  
**Affiliation:** M.Tech (IT), Indian Institute of Information Technology Allahabad (IIIT Allahabad)  
**Task:** Research Environment Setup, Diagnostics, and Repository Structure Verification  
**Status:** Complete Implementation of Prompt 08 (Environment Verification Log and Structured Repository)

---

### 1. Environment Specification and Dependencies

The research workspace is configured for deterministic, local execution on commodity hardware running Python 3.12. All required scientific dependencies are specified with minimum version bounds in `requirements.txt`:

```text
numpy>=1.26.0
pandas>=2.2.0
matplotlib>=3.8.0
scipy>=1.12.0
```

Installation command executed:
```powershell
pip install -r requirements.txt
```

---

### 2. Structured Repository Tree

The project hierarchy strictly follows the canonical structure mandated in Section 9 of the assignment specification:

```text
AITR_Lab02_Project/
├── configs/
│   └── config.json              # Frozen hyperparameters and experiment paths
├── data/
│   ├── README.md                # Data documentation, licensing, and schema
│   ├── corpus.json              # 20 verified scientific papers & passages
│   └── queries.json             # 20 standardized scientific synthesis queries
├── notebooks/                   # Interactive exploratory notebooks
├── src/
│   ├── __init__.py
│   ├── dataset.py               # Data loading, tokenization, passage chunking
│   ├── baselines.py             # Vanilla LLM & Document-Level RAG baselines
│   ├── passage_grounding.py     # Passage-Anchored Grounding (PAG) module
│   └── metrics.py               # Precision, recall, hallucination, Dice alignment
├── scripts/
│   ├── env_test.py              # Environment diagnostic verification test
│   ├── run_experiments.py       # Main experimental execution pipeline
│   └── evaluate_and_plot.py     # Statistical computation and figure generation
├── results/
│   ├── results.csv              # Raw per-query evaluation measurements
│   ├── summary_metrics.json     # Aggregated mean, std, and p-values
│   ├── run.log                  # Execution runtime log
│   └── figures/                 # Publication-quality charts (PNG and PDF)
├── paper/
│   ├── main.tex                 # LaTeX manuscript (IEEE/ACM style, 6-10 pages)
│   ├── references.bib           # Verified BibTeX citations
│   └── figures/                 # Vector and high-resolution paper plots
├── prompts/                     # Prompt 03 through 18 implementation artifacts
├── requirements.txt             # Verified dependency manifest
├── research_decisions.md        # Literature-to-experiment decision log
├── baseline_validation.md       # Baseline audit and discrepancy report
├── experiment_protocol.md       # Frozen experimental protocol
├── ai_assistance_log.md         # Responsible AI and research-integrity audit
└── README.md                    # Public-ready reproduction instructions
```

---

### 3. Actual Console Verification Output

The diagnostic test script `scripts/env_test.py` was executed directly on the system. The exact console output is recorded below:

```text
============================================================
  RESEARCH ENVIRONMENT DIAGNOSTIC & VERIFICATION TEST
============================================================
[1] Operating System: Windows 11 (Architecture: AMD64)
[2] Python Version:   3.12.4 (C:\Program Files\Python312\python.exe)

[3] Library Compatibility & Import Verification:
    - numpy        : INSTALLED (version 2.2.6)
    - pandas       : INSTALLED (version 2.3.2)
    - matplotlib   : INSTALLED (version 3.10.5)
    - scipy        : INSTALLED (version 1.16.1)

[4] Deterministic Seed Control Test:
    - Seed Determinism: PASSED (Deterministic outputs verified)

[5] Project Repository Directory Structure Check:
    - Directory configs            : EXISTS
    - Directory data               : EXISTS
    - Directory notebooks          : EXISTS
    - Directory src                : EXISTS
    - Directory scripts            : EXISTS
    - Directory results            : EXISTS
    - Directory results/figures    : EXISTS
    - Directory paper              : EXISTS
    - Directory paper/figures      : EXISTS
    - Directory prompts            : EXISTS

[6] Configuration File Test:
    - configs\config.json : VALID JSON (Project: AITR_Lab02_MSE2026015_CitationGrounding)

============================================================
  VERIFICATION RESULT: ALL CHECKS PASSED (STATUS: READY)
============================================================
```

### 4. Verification Assessment
* **Library Compatibility:** All mathematical, dataframe, and visualization packages are active and confirmed compatible.
* **Deterministic Random Seed Control:** NumPy pseudo-random generator state preserves determinism under seed `42`.
* **Path Resolution:** Directory tree and configuration mappings are fully operational.

**Artifact Saved:** `prompts/PROMPT_08_IMPLEMENTATION.md`
