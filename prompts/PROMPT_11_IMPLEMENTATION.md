# PROMPT 11 IMPLEMENTATION
## Debugging Using Actual Evidence and Runtime Tracebacks

**Course:** AI Tools for Research  
**Student Name:** Sujal Rajesh Ghagare  
**Enrollment No:** MSE2026015  
**Affiliation:** M.Tech (IT), Indian Institute of Information Technology Allahabad (IIIT Allahabad)  
**Task:** Diagnostic Traceback Analysis, Minimal Safe Corrections, and Edge-Case Hardening  
**Status:** Complete Implementation of Prompt 11 (Corrected Code, Tested Fix, Debugging Log)

---

### 1. Case 01: Python Path Resolution Failure (`ModuleNotFoundError`)

#### A. Actual Observed Traceback
```text
Traceback (most recent call last):
  File "C:\Users\Hp\OneDrive\Desktop\AITR_Lab02_Project\scripts\test_modules.py", line 5, in <module>
    from src.dataset import DocumentStore, QuerySet
ModuleNotFoundError: No module named 'src'
```

#### B. Evidence vs. Hypotheses
* **Confirmed Evidence:** When executing `python scripts/test_modules.py`, Python sets `sys.path[0]` to the directory containing the script (`scripts/`), omitting the project root directory.
* **Hypothesis:** Adding the project root to `sys.path` programmatically will resolve the module import without requiring system-wide environment variable changes.

#### C. Minimal Safe Correction
Inserted path resolution block at the top of script entrypoints:
```python
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
```

#### D. Verification Output
Re-running `python scripts/test_modules.py` executed successfully without module errors.

---

### 2. Case 02: Whole-Document Lexical Granularity Mismatch

#### A. Observed Unexpected Behavior
In the initial draft of `src/metrics.py`, a perfectly factual claim extracted from `lewis2020rag` ("Retrieval-Augmented Generation models combine parametric and non-parametric memory for language generation") produced an unexpectedly low Sorensen-Dice score of $0.26$, misclassifying a supported claim as unsupported.

#### B. Root Cause Analysis
* **Confirmed Evidence:** The claim sentence contained 9 content tokens, while the full abstract document contained 62 content tokens. The intersection was 9, yielding:
  $$\text{Dice} = \frac{2 \times 9}{9 + 62} = \frac{18}{71} \approx 0.2535 < 0.50$$
* **Hypothesis:** A claim asserts an atomic proposition that matches a single sentence or span within a paper, not the entire document simultaneously. Measuring alignment against individual sentences within the document will correctly reflect passage support.

#### C. Minimal Safe Correction
Implemented `score_claim_against_document()` in `src/metrics.py`:
```python
def score_claim_against_document(claim_text: str, doc_text: str) -> float:
    doc_sentences = re.split(r'(?<=[.!?])\s+', doc_text.strip())
    best = 0.0
    for s in doc_sentences:
        if s.strip():
            score = dice_similarity(claim_text, s)
            if score > best:
                best = score
    return best
```

#### D. Verification Output
Alignment score for the identical claim increased from $0.2535 \rightarrow 0.8889$, accurately classifying the claim as **TYPE_IV_SUPPORTED**.

---

### 3. Edge-Case Hardening: Zero Citations and Empty String Handling

We hardened `src/metrics.py` against edge cases:
1. **Empty Citation List:** Returns `"UNCITED"` with score `0.0` without triggering unhandled index exceptions.
2. **Division-by-Zero Guards:** Precision and recall calculations incorporate explicit denominator checks:
   ```python
   p_claim = supported_claims / cited_claims if cited_claims > 0 else 0.0
   ```
3. **Empty Text Queries:** `extract_content_tokens("")` safely returns an empty set `{}` and Dice similarity returns `0.0` rather than raising a `ZeroDivisionError`.

**Artifact Saved:** `prompts/PROMPT_11_IMPLEMENTATION.md`
