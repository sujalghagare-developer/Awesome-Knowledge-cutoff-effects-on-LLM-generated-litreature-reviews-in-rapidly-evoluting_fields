# PROMPT 12 IMPLEMENTATION
## Defensible Contribution Selection and Executable Comparison Plan

**Course:** AI Tools for Research  
**Student Name:** Sujal Rajesh Ghagare  
**Enrollment No:** MSE2026015  
**Affiliation:** M.Tech (IT), Indian Institute of Information Technology Allahabad (IIIT Allahabad)  
**Validated Baselines:** Vanilla Parametric LLM ($P_{\text{claim}} \approx 0.33, H_{\text{cite}} \approx 0.67$) & Standard RAG ($P_{\text{claim}} \approx 0.67, H_{\text{cite}} \approx 0.33$)  
**Status:** Complete Implementation of Prompt 12 (Chosen Contribution Pathway and Executable Test Plan)

---

### 1. Comparative Analysis of Three Feasible Study Pathways

| Pathway Dimension | Pathway A: Reproduction + New Condition | Pathway B: Controlled Comparative Study | Pathway C: Targeted Modification (Selected) |
| :--- | :--- | :--- | :--- |
| **Scientific Question** | Does Self-RAG reflection token tuning maintain accuracy when preprints lack peer-review metadata? | How do citation precision, recall, and hallucination trade off across 3 distinct synthesis paradigms? | Does introducing a passage-level span anchoring constraint $\tau$ eliminate claim extrapolation in RAG? |
| **Expected Code Changes** | Heavy model retraining harness, tokenizer modification, checkpoint saving. | Build unified query runner and multi-pipeline evaluator harness. | Add isolated `PassageAnchoredGrounder` module while preserving base retriever and evaluator. |
| **Compute Burden** | $> 24$ GB GPU, multiple hours/days of training. | $< 1$ minute on local CPU; purely inferential. | $< 30$ seconds on local CPU; highly parallelizable. |
| **Primary Advantage** | High architectural novelty if fine-tuning succeeds. | Clean, unbiased empirical comparison under identical controls. | Isolates the exact causal mechanism of citation grounding without confounding variables. |
| **Primary Failure Risk** | Training divergence, CUDA OOM, unstable loss curves. | Subtle differences in baseline prompt formatting could bias outputs. | Strict thresholding could excessively degrade citation recall ($R_{\text{cite}}$). |
| **Required Evidence** | Training loss, reflection token accuracy, GPU memory logs. | Paired metrics ($P, R, H, S$) across all queries with significance tests. | Ablation curve of precision-recall across $\tau \in [0.2, 0.8]$ and error shift analysis. |

---

### 2. Defensible Recommendation for Resource Allocation

**Selected Recommendation: Pathway C (Targeted Modification) evaluated within a Controlled Comparative Framework.**
* **Scientific Rationale:** Rather than introducing a complex black-box architecture, we isolate a single, theoretically grounded variable: **enforcing passage-level span alignment** prior to claim emission. By keeping the retriever, corpus, and evaluation metrics completely identical to Baseline 2 (Standard RAG), any observed improvement in citation precision or reduction in hallucination is causally attributable to the passage-anchored constraint.
* **Preservation of Baseline:** The baseline implementations (`VanillaLLMSynthesizer` and `StandardRAGSynthesizer`) remain entirely intact and unpolluted in `src/baselines.py`.

---

### 3. Fair Test Plan and Frozen Experimental Matrix

```
+---------------------------------------------------------------------------------------+
|                               Frozen Test Comparison Matrix                           |
+---------------------------------------------------------------------------------------+
| Fixed Query Set: 12 Unseen Queries in Test Partition (Q09 - Q20)                      |
| Fixed Evidence Base: 20 Open-Access Scientific Documents in data/corpus.json          |
| Fixed Evaluator: Automated Sorensen-Dice Max-Sentence Scorer in src/metrics.py        |
+---------------------------------------------------------------------------------------+
         |                                |                                 |
         v                                v                                 v
+------------------+             +------------------+             +-------------------+
|  Condition 1:    |             |  Condition 2:    |             |  Condition 3:     |
|  Vanilla LLM     |             |  Standard RAG    |             |  PAG (Targeted)   |
+------------------+             +------------------+             +-------------------+
| Closed-book      |             | Top-k retrieval, |             | Top-k retrieval,  |
| parametric memory|             | document-level   |             | sentence-level    |
| no external docs |             | citations        |             | span constraint   |
+------------------+             +------------------+             +-------------------+
         \                                |                                 /
          \                               |                                /
           +------------------------------+-------------------------------+
                                          |
                                          v
                         +---------------------------------+
                         |  Statistical Paired Evaluation  |
                         |  - Wilcoxon Signed-Rank Test    |
                         |  - Paired Student's t-Test      |
                         |  - Error Typology Breakdown     |
                         |  - tau-Sensitivity Ablation     |
                         +---------------------------------+
```

---

### 4. Ablation and Failure Mode Specifications

1. **Threshold Sweep:** Evaluate PAG across $\tau \in \{0.20, 0.35, 0.50, 0.65, 0.80\}$ to observe the exact phase transition where citation hallucination collapses to zero.
2. **Failure Analysis:** Audit any claim that fails grounding at $\tau = 0.50$ to classify whether the failure arose from retrieval omission (retriever missed the gold document) or model synthesis error (model attempted ungrounded extrapolation).

**Artifact Saved:** `prompts/PROMPT_12_IMPLEMENTATION.md`
