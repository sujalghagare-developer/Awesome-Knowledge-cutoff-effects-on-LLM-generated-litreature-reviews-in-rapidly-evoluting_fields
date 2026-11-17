# PROMPT 06 IMPLEMENTATION
## Dataset and Baseline Validation Sheet

**Course:** AI Tools for Research  
**Student Name:** Sujal Rajesh Ghagare  
**Enrollment No:** MSE2026015  
**Affiliation:** M.Tech (IT), Indian Institute of Information Technology Allahabad (IIIT Allahabad)  
**Research Question:** To what extent does Passage-Anchored Grounding (PAG) improve claim citation precision ($P_{\text{claim}}$) and eliminate citation hallucination ($H_{\text{cite}}$) in LLM-assisted literature reviews?  
**Status:** Complete Implementation of Prompt 06 (Dataset & Baseline Validation Sheet)

---

### 1. Primary Dataset Specification

To ensure rigorous, leak-free, and reproducible experimentation on commodity hardware, we establish the **Scholarly Citation Support Benchmark (SCS-Bench-20)**.

| Parameter | Specification |
| :--- | :--- |
| **Official Source** | Open-access peer-reviewed literature and preprint repositories (arXiv, PubMed, Nature/Springer Open Access). Papers match the verified bibliography of the review paper. |
| **File Structure** | Structured JSON files in repository: `data/corpus.json` (document store with verified IDs, titles, authors, years, DOIs, and full-text evidence passages) and `data/queries.json` (20 standardized research synthesis queries). |
| **Corpus Scale** | 20 canonical papers across AI, NLP, Information Retrieval, and Biomedical NLP (10 pre-cutoff foundational papers, 10 post-cutoff recent breakthroughs). |
| **Licensing / Terms** | Creative Commons Attribution (CC-BY 4.0) and Open Access Academic Fair Use. |
| **Compute Requirement** | Negligible ($< 5$ MB memory footprint, $< 10$ ms disk I/O, pure CPU execution). |
| **Common Pitfalls** | *Data truncation:* Summarizing entire papers at document level obscures sentence-level contradictions.<br>*Temporal contamination:* Evaluating post-cutoff models with unversioned web search. |

---

### 2. Comparator Baselines and Controls

We configure two standard baseline comparators alongside the proposed method:

#### Baseline 1: Vanilla Parametric Generator (`Vanilla-LLM`)
* **Mechanism:** Closed-book generation relying solely on internal model weights without external document retrieval.
* **Citation Mechanism:** Model freely generates bibliographic references and attributions from parametric memory.
* **Expected Failure Mode:** Severe citation hallucination (Type I non-existent citations, fabricated DOIs) and outdated facts past the knowledge cutoff.
* **Verification Source:** Corresponds to the baseline observed by Walters & Wilder (2023) \cite{walters2023} and Chelli et al. (2024) \cite{chelli2024}.

#### Baseline 2: Standard Document-Level RAG (`Doc-RAG`)
* **Mechanism:** Open-book generation with top-$k$ document retrieval (BM25 / lexical retriever). The retrieved documents are concatenated into the prompt context.
* **Citation Mechanism:** The model synthesizes an integrated literature summary and appends a bibliography or document-level citations (e.g., "[1]", "[2]") at paragraph/document ends.
* **Expected Failure Mode:** While cited papers genuinely exist in the prompt, individual synthesized sentences frequently extrapolate beyond the retrieved text (Type III claim-evidence mismatch).
* **Verification Source:** Corresponds to the standard RAG paradigm formulated by Lewis et al. (2020) \cite{lewis2020rag}.

#### Proposed Comparator: Passage-Anchored Grounding (`PAG`)
* **Mechanism:** Hierarchical passage chunking and span-level alignment. Every emitted claim sentence $c_i$ is explicitly bound to a retrieved passage $p_k$. A claim is emitted if and only if its lexical-semantic alignment score $S(c_i, p_k)$ meets the threshold:
  $$S(c_i, p_k) \ge \tau \quad (\tau = 0.50)$$
  Claims failing this criterion are rewritten to conservative hedged statements or suppressed, eliminating unsupported extrapolations.

---

### 3. Evaluation Design & Leakage Prevention Protocol

```
+-----------------------------------------------------------------------------+
|                          Data Partitioning Protocol                         |
+-----------------------------------------------------------------------------+
|  Benchmark: 20 Curated Scholarly Synthesis Queries across 4 Scientific Subdomains  |
|  - Domain A: LLMs & Knowledge Boundaries (5 queries)                        |
|  - Domain B: RAG & Dense Retrieval Architectures (5 queries)                |
|  - Domain C: Citation Reliability & Hallucination Mitigation (5 queries)     |
|  - Domain D: Multi-Document Evidence Synthesis & Verification (5 queries)   |
+-----------------------------------------------------------------------------+
                                      |
            +-------------------------+-------------------------+
            |                                                   |
            v                                                   v
+-----------------------+                           +-----------------------+
|  Development Split    |                           |     Frozen Test Split |
|     (8 queries)       |                           |       (12 queries)    |
+-----------------------+                           +-----------------------+
| Used for threshold    |                           | Strict zero-touch eval|
| calibration of \tau   |                           | for final reported    |
| (k-fold validation)   |                           | research metrics      |
+-----------------------+                           +-----------------------+
```

#### Leakage Risks and Mitigations:
1. **Document-Level Leakage:** Queries in the test split never query papers included in the development tuning prompt examples.
2. **Temporal Leakage:** Papers are indexed with their exact publication year (2020–2024); evaluations specifically assess whether models claim pre-cutoff techniques as the current state of the art.
3. **Prompt Leakage:** Evaluator scripts use frozen deterministic scoring functions that do not share state across queries.

---

### 4. Independent Verification Checklist

- [x] **Data Veracity:** Every paper in `data/corpus.json` has a verified DOI, true publication year, and authentic excerpt text directly extracted from the original paper.
- [x] **Reproducible Baselines:** Baselines are implemented with explicit seeds (`seed=42`) and deterministic retrieval rankings.
- [x] **Metric Directionality:** $P_{\text{claim}}$ (Higher is better), $H_{\text{cite}}$ (Lower is better), $S_{\text{ground}}$ (Higher is better).
- [x] **Auditability:** Every claim evaluated can be printed alongside its source text and computed score.

**Artifact Saved:** `prompts/PROMPT_06_IMPLEMENTATION.md`
