# PROMPT 05 IMPLEMENTATION
## Framing Research Questions, Hypotheses, and Measurable Success Criteria

**Course:** AI Tools for Research  
**Student Name:** Sujal Rajesh Ghagare  
**Enrollment No:** MSE2026015  
**Affiliation:** M.Tech (IT), Indian Institute of Information Technology Allahabad (IIIT Allahabad)  
**Verified Gap:** Gap G2 — Claim-Level Citation Support in LLM-Generated Scientific Literature Reviews  
**Status:** Complete Implementation of Prompt 05 (One-Page Problem Brief and Formal Gate G1 Submission)

---

### 1. Formal Research Problem Definition

> **Research Problem Statement:**  
> Large Language Models (LLMs) used for scientific literature review generation suffer from critical citation unreliability: while Retrieval-Augmented Generation (RAG) overcomes static knowledge cutoffs by providing external documents, standard document-level RAG frequently generates unsupported claims and misattributes statements to cited references. The fundamental problem is how to formulate and enforce a computationally lightweight, passage-anchored grounding constraint that guarantees every synthesized empirical claim is supported by a verified source passage without catastrophic loss of citation coverage.

---

### 2. Testable Research Questions and Hypotheses

#### Research Question 1 (RQ1: Claim Citation Precision)
* **Question:** Does enforcing a passage-anchored grounding constraint during scientific synthesis significantly increase the proportion of generated claims that are strictly supported by cited evidence compared to Standard Document-Level RAG and Vanilla Parametric Generation?
* **Hypothesis $H_1$:** Synthesized claims constrained by passage-anchored span alignment will achieve significantly higher claim support precision ($P_{\text{claim}} \ge 0.85$) than standard unconstrained document-level RAG ($P_{\text{claim}} \approx 0.50$) and vanilla generation ($P_{\text{claim}} \le 0.30$).
* **Variables:**
  * *Independent Variable:* Synthesis Architecture (Vanilla LLM vs. Standard Document RAG vs. Passage-Anchored Grounding [PAG]).
  * *Dependent Variable:* Claim Citation Precision ($P_{\text{claim}} \in [0, 1]$).
* **Evaluation Metric:**
  $$P_{\text{claim}} = \frac{N_{\text{fully supported claims}}}{N_{\text{total cited claims}}}$$
* **Decision Rule / Success Threshold:** Reject null hypothesis if $P_{\text{claim}}(\text{PAG}) - P_{\text{claim}}(\text{Std-RAG}) \ge 0.25$ with paired statistical significance ($p < 0.01$).
* **Contradictory Observation:** If $P_{\text{claim}}(\text{PAG}) \le P_{\text{claim}}(\text{Std-RAG})$, or if grounding constraints fail to eliminate unsupported claims, the hypothesis is falsified.

#### Research Question 2 (RQ2: Citation Hallucination & Error Reduction)
* **Question:** How effectively does passage-anchored grounding suppress distinct modes of bibliographic error, specifically fabricated references (Type I) and claim-evidence extrapolations (Type III)?
* **Hypothesis $H_2$:** Passage-anchored grounding will eliminate Type I fabrication errors ($0\%$) and reduce Type III extrapolation hallucinations by at least 60% relative to standard RAG.
* **Variables:**
  * *Independent Variable:* Grounding filter mechanism.
  * *Dependent Variable:* Citation Hallucination Rate ($H_{\text{cite}} \in [0, 1]$) and Per-Category Error Proportions.
* **Evaluation Metric:**
  $$H_{\text{cite}} = \frac{N_{\text{fabricated}} + N_{\text{unsupported claims}}}{N_{\text{total claims}}}$$
* **Decision Rule / Success Threshold:** Success if $H_{\text{cite}}(\text{PAG}) \le 0.10$ while Vanilla LLM yields $H_{\text{cite}} \ge 0.50$.
* **Contradictory Observation:** If PAG produces hallucinations at rates comparable to ungrounded models, the filtering mechanism is flawed.

#### Research Question 3 (RQ3: Precision-Coverage Sensitivity Trade-Off)
* **Question:** What is the mathematical relationship between the passage-anchoring threshold $\tau \in [0.2, 0.8]$ and the trade-off between claim citation precision ($P_{\text{claim}}$) and citation coverage ($R_{\text{cite}}$)?
* **Hypothesis $H_3$:** As the alignment threshold $\tau$ increases, precision $P_{\text{claim}}$ exhibits monotonic growth while citation coverage $R_{\text{cite}}$ decays sublinearly, defining an optimal operating Pareto threshold at $\tau^* \approx 0.50$.
* **Variables:**
  * *Independent Variable:* Grounding verification threshold $\tau \in [0.2, 0.8]$.
  * *Dependent Variable:* Harmonic mean $F_{\beta = 1}(P_{\text{claim}}, R_{\text{cite}})$.
* **Evaluation Metric:** Balanced Grounding F1-score:
  $$F_1 = 2 \cdot \frac{P_{\text{claim}} \cdot R_{\text{cite}}}{P_{\text{claim}} + R_{\text{cite}}}$$
* **Decision Rule / Success Threshold:** Identification of a stable convex maximum in $F_1$ over $\tau \in [0.4, 0.6]$.
* **Contradictory Observation:** If increasing $\tau$ collapses citation coverage ($R_{\text{cite}} < 0.20$) without increasing precision, threshold filtering is inappropriate for scholarly synthesis.

---

### 3. Separation of Investigated vs. Demonstrated Contributions

* **Already Demonstrated in Literature (Not Claimed as Novel):**
  * LLMs hallucinate citations and exhibit knowledge cutoffs (Walters & Wilder 2023, Alkaissi & McFarlane 2023).
  * RAG improves factual recall in open-domain QA (Lewis et al. 2020).
  * Self-RAG can train 7B/13B models to critique passages (Asai et al. 2024).
* **Investigated Contribution in This Study (Our Research Focus):**
  * A controlled comparative evaluation of sentence-level passage-anchored constraints versus document-level RAG on identical scientific literature review queries.
  * A computationally lightweight, deterministic passage-grounding algorithm executable on local CPU with zero GPU training requirements.
  * A formal mathematical sensitivity analysis of the precision-coverage trade-off governed by threshold $\tau$.

---

### 4. Gate G1: One-Page Research Brief

| Field (Assignment Specification §11) | Project Information |
| :--- | :--- |
| **Review Topic and Key Papers** | Knowledge Cutoff and Citation Reliability in LLM-Generated Literature Reviews; Lewis et al. (2020) \cite{lewis2020rag}, Asai et al. (2024) \cite{asai2024selfrag}, Walters & Wilder (2023) \cite{walters2023}, Chelli et al. (2024) \cite{chelli2024}, Gao et al. (2023) \cite{gao2023rag}. |
| **Research Gap** | Gap G2: LLMs frequently generate citations that fail to support substantive claims; document-level RAG provides papers but fails to enforce sentence-to-passage alignment. |
| **Research Question** | To what extent does Passage-Anchored Grounding (PAG) improve claim citation precision ($P_{\text{claim}}$) and eliminate citation hallucination ($H_{\text{cite}}$) compared to Standard RAG and Vanilla LLM synthesis? |
| **Study Pathway** | Pathway B/C: Controlled comparative study of a targeted modification (Passage-Anchored Grounding filter). |
| **Dataset or Measurement Setup** | Curated benchmark corpus of 20 verified open-access scholarly papers and 20 standardized scientific synthesis queries; gold evidence passages verified from original sources. |
| **Baseline / Comparators** | Baseline 1: Vanilla Parametric LLM Generation (no retrieval).<br>Baseline 2: Standard Document-Level RAG (post-hoc bibliography). |
| **Primary Metric and Control** | Primary Metric: Claim Citation Support Precision ($P_{\text{claim}}$) and Hallucination Rate ($H_{\text{cite}}$).<br>Controlled Factors: Identical query set, fixed evaluation rubric, constant prompt length. |
| **Computing and Risks** | Hardware: Standard local PC CPU; Execution time $< 30$ seconds. Risks: Low; deterministic scoring eliminates API timeout or rate-limit risks. |
| **First Executable Milestone** | Smallest working baseline: Data loading script and baseline generation module producing initial unconstrained outputs and automated sanity tests. |

**Artifact Saved:** `prompts/PROMPT_05_IMPLEMENTATION.md`
