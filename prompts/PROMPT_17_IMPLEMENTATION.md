# PROMPT 17 IMPLEMENTATION
## Reproducible GitHub Documentation and Repository Manifest

**Course:** AI Tools for Research  
**Student Name:** Sujal Rajesh Ghagare  
**Enrollment No:** MSE2026015  
**Affiliation:** M.Tech (IT), Indian Institute of Information Technology Allahabad (IIIT Allahabad)  
**Deliverable:** Public-Ready Research Repository and Reproduction Instructions  
**Status:** Complete Implementation of Prompt 17 (README.md, Reproduction Guide, Security & Integrity Audit)

---

### 1. Repository Documentation Structure

The repository documentation has been compiled in `README.md` at the project root. It provides:
1. **Problem Statement & Research Overview:** Formalization of the knowledge cutoff and citation hallucination problem in automated scientific literature synthesis.
2. **Directory Architecture:** Detailed project layout adhering to assignment guidelines.
3. **Environment Setup & Verification:** Exact package versions and automated diagnostic script execution instructions.
4. **Benchmark Protocol (SCS-Bench-20):** Documentation of the 20-paper corpus and 20 standardized research synthesis queries.
5. **Exact Reproduction Commands:** Step-by-step commands to re-run experiments and regenerate publication figures.
6. **Summary of Measured Findings:** Transparent tables displaying precision, recall, hallucination rate, and statistical tests.
7. **Second-Student Reproduction Checklist:** 7-point audit checklist for independent validation.

---

### 2. Genuinely Executed Reproduction Commands

All commands below have been tested and verified directly within the environment:

```powershell
# 1. Diagnostic Verification Test
python scripts/env_test.py

# 2. Modular Unit & Sanity Test
python scripts/test_modules.py

# 3. Main Benchmark Execution Pipeline
python scripts/run_experiments.py

# 4. Publication Figure & PDF Generation
python scripts/evaluate_and_plot.py
```

---

### 3. Security, Privacy, and License Audit

Prior to public release, the repository underwent an explicit security and privacy audit:
* **Zero API Secrets:** No API keys, passwords, or personal access tokens are stored in configuration files or code. The pipeline runs entirely offline on local CPU.
* **No Restricted Data:** All corpus texts are derived from open-access scientific preprints and articles published under CC-BY 4.0 or Open Access terms.
* **Realistic Filepaths:** All script filepaths utilize relative directory resolution (`os.path.join`, `sys.path.insert`), ensuring seamless execution across Windows, Linux, and macOS platforms.

**Artifact Saved:** `prompts/PROMPT_17_IMPLEMENTATION.md` and `README.md`
