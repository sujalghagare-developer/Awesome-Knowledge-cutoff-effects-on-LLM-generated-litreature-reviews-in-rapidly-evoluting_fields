# AI Provenance and Research Integrity Audit Log

**Project:** AITR_Lab02_MSE2026015_CitationGrounding  
**Student:** Sujal Rajesh Ghagare (MSE2026015)  
**Affiliation:** M.Tech (IT), IIIT Allahabad  
**Course:** AI Tools for Research  

---

## 1. Structured AI-Assistance Activity Register

| # | Research Task | AI Assistance / Proposal | Human Critical Decision & Action | Verification Method | Outcome |
| :-: | :--- | :--- | :--- | :--- | :--- |
| **01** | Gap Selection | AI outlined all 5 candidate gaps from review. | Selected Gap G2 (Claim-level citation support) to minimize computational overhead while maximizing mathematical rigor. | Reviewed feasibility matrix against commodity hardware constraints. | Finalized Pathway C (Targeted Modification: Passage-Anchored Grounding). |
| **02** | Metric Scoring Formulation | AI initially suggested evaluating claims against full document text. | Rejected whole-document Dice comparison due to token count inflation; mandated sentence-level maximum alignment. | Unit tested with authentic sentences from `lewis2020rag`. | Alignment score restored from $0.25 \rightarrow 0.89$ on true claims. |
| **03** | Python Path Resolution | AI generated script imports without path prefixes, causing `ModuleNotFoundError`. | Intervened to add `sys.path.insert(0, ...)` to ensure cross-platform execution. | Re-ran script via terminal to verify clean exit code 0. | Script execution succeeded across all modules. |
| **04** | Dictionary Key Formatting | AI attempted to access float threshold string `'0.20'`, causing a runtime `KeyError`. | Analyzed `summary_metrics.json` structure, identified `'0.2'`, and updated parser. | Re-executed `evaluate_and_plot.py`. | Generated all 3 publication figures in vector PDF and PNG. |
| **05** | Manuscript Drafting | AI generated draft text for LaTeX manuscript. | Audited all tables, numbers, and citations against raw `results.csv`; removed speculative claims of global generalizability. | Cross-checked numbers against `summary_metrics.json`. | Zero discrepancy between code outputs and LaTeX claims. |

---

## 2. Three Concrete Examples of AI Limitations and Purposeful Human Corrections

### Example 1: Resolving Token Granularity Mismatch in Lexical Overlap
* **The AI Limitation:** When prompted to write a Sorensen-Dice alignment metric, the AI compared a single 9-token claim sentence directly against the entire 60-token document abstract. Because the denominator was $(9 + 60) = 69$, even a perfectly matching claim received a score of $18/69 \approx 0.26$, misclassifying supported claims as unsupported.
* **Human Correction:** The student recognized that claims represent atomic propositions matching individual sentences or passage spans. The student instructed the AI to implement `score_claim_against_document()`:
  $$S(c_i, d) = \max_{s \in \text{sentences}(d)} \text{Dice}(c_i, s)$$
* **Verification & Result:** The alignment score for genuine claims increased from $0.26 \rightarrow 0.89$, accurately matching human judgment.

### Example 2: Module Import Failure on Subfolder Execution
* **The AI Limitation:** The AI generated standalone test scripts in `scripts/` assuming that running `python scripts/test_modules.py` would automatically include the parent workspace directory. It crashed with `ModuleNotFoundError: No module named 'src'`.
* **Human Correction:** The student diagnosed the standard Python import path behavior and enforced explicit relative root path injection:
  ```python
  import sys, os
  sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
  ```
* **Verification & Result:** Test scripts executed reliably across all environments without requiring global environment modifications.

### Example 3: Ablation Key String Deserialization Mismatch
* **The AI Limitation:** In `evaluate_and_plot.py`, the AI assumed threshold float keys would serialize as two-decimal strings (e.g. `"0.20"`), resulting in an immediate `KeyError: '0.20'`.
* **Human Correction:** The student inspected the raw `summary_metrics.json` file, observed that Python's default float string conversion produced `"0.2"`, and revised the plotting script to iterate dynamically over `metrics["ablation"].keys()`.
* **Verification & Result:** Plotting script generated high-resolution figures without crashes.

---

## 3. Reflections on Vibe Coding and Research Integrity

* **What was learned about vibe coding:** Vibe coding dramatically accelerates boilerplate generation, configuration schemas, and visualization scripts. However, it requires intense human vigilance regarding semantic subtleties—such as token granularity, denominator definitions, and data leakage. AI cannot be trusted as an authority on mathematical correctness or experimental truth.
* **Which conclusions depended on human reasoning:**
  1. The strategic decision to isolate Gap G2 and choose a zero-GPU targeted modification.
  2. The realization that standard RAG's failure stems from self-attention interpolation across disparate context documents.
  3. The candid articulation of methodological limitations, including lexical overlap paraphrase penalties.
* **Remaining risks:** Lexical overlap cannot detect logical polarity reversals (negations) in adversarial contexts. Future systems must integrate neural NLI cross-encoders.
