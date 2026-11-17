# PROMPT 04 IMPLEMENTATION
## Feasibility, Novelty Verification, and Resource Access Plan

**Course:** AI Tools for Research  
**Student Name:** Sujal Rajesh Ghagare  
**Enrollment No:** MSE2026015  
**Affiliation:** M.Tech (IT), Indian Institute of Information Technology Allahabad (IIIT Allahabad)  
**Candidate Study:** Controlled Empirical Study of Claim-Level Citation Support and Passage-Anchored Grounding in LLM-Assisted Literature Reviews  
**Status:** Complete Implementation of Prompt 04 (Novelty/Feasibility Matrix and Go/No-Go Decision)

---

### 1. Candidate Study Statement
The candidate study investigates the fidelity of citation attribution in automated scientific literature synthesis. Specifically, it contrasts **Vanilla Parametric Generation**, **Standard Document-Level RAG**, and **Passage-Anchored Grounding (PAG)** across a curated benchmark of scientific synthesis queries, evaluating claim-level citation precision, citation recall, citation hallucination rate, and lexical grounding alignment.

---

### 2. Scholarly Search Strings and Neighboring Work Categories

To ensure novelty verification without fabricating non-existent publications, we formulate explicit scholarly search strings to inspect adjacent research spaces:

#### Scholarly Search Strings:
1. `("claim-level citation" OR "sentence-level attribution") AND ("literature review" OR "scholarly synthesis") AND "large language models"`
2. `("retrieval-augmented generation" OR "RAG") AND "citation hallucination" AND ("passage grounding" OR "evidence alignment")`
3. `("citation accuracy" OR "bibliographic fabrication") AND ("ChatGPT" OR "GPT-4" OR "open-weights LLM") AND "systematic review"`

#### Neighboring Work Categories Inspected:
* **Category 1: General QA Attribution Benchmarks (e.g., ALCE, ASQA):** Focus on single-fact open-domain QA (e.g., "Who invented the telephone?") rather than complex multi-document scientific literature synthesis where claims synthesize methodology and empirical findings.
* **Category 2: Empirical Audits of LLM Bibliographies (e.g., Walters & Wilder 2023, Chelli et al. 2024):** Evaluate whether generated references exist and are accurately formatted, but do not provide an automated, computationally reproducible mechanism to guarantee sentence-to-passage grounding during generation.
* **Category 3: Complex Interactive Agents (e.g., ReAct, Self-RAG):** Require expensive multi-step fine-tuning or proprietary API calls, creating a severe compute barrier for reproducible academic research on commodity hardware.

---

### 3. Novelty and Feasibility Matrix

| Published Method | VERIFIED Contribution (with Citation) | Identified Limitation | Proposed Difference in Our Study | Evidence Still Missing (Addressed Here) |
| :--- | :--- | :--- | :--- | :--- |
| **Walters & Wilder (2023)** \cite{walters2023} | Audited ChatGPT citations across disciplines; verified high rates of bibliographic hallucination ($> 30\%$). | Purely observational post-hoc audit; did not evaluate algorithmic mitigations or sentence-level claim alignment. | We introduce and evaluate an active algorithmic intervention (**Passage-Anchored Grounding**) under a controlled protocol. | Quantitative comparison between post-hoc citation and passage-anchored citation on identical queries. |
| **Lewis et al. (2020)** \cite{lewis2020rag} | Established dense retrieval coupled with parametric generators for knowledge-intensive NLP. | References are injected into context as monolithic documents; generated sentences lack explicit token/span attribution. | We enforce a strict span-level attribution constraint ($\tau$) mapping each synthesized claim to a specific passage. | Direct measurement of claim-to-passage alignment score ($S_{\text{ground}}$) in scientific literature synthesis. |
| **Gao et al. (2023)** \cite{gao2023rag} | Comprehensive survey of RAG frameworks and mitigation paradigms for knowledge cutoff and hallucination. | Survey paper; provides qualitative taxonomies rather than controlled empirical benchmarking on commodity hardware. | We implement a runnable, lightweight, zero-GPU benchmark pipeline evaluating precision, recall, and hallucination rates. | Reproducible execution logs and error typology distribution on local hardware. |
| **Asai et al. (2024)** \cite{asai2024selfrag} | Self-RAG model with reflection tokens evaluating passage support (`[IsSup]`). | Requires heavy 7B/13B parameter fine-tuning and substantial VRAM ($> 24$ GB). | We distill the passage-critique principle into a deterministic, thresholded mathematical scoring function executable on CPU. | Feasibility and accuracy of threshold-based passage filtering on local compute without neural training overhead. |

---

### 4. Resource Access, Licensing, and Availability Verification

| Resource Asset | Target Specification | Access Terms & License | Availability Status | Fallback / Mitigation Plan |
| :--- | :--- | :--- | :--- | :--- |
| **Source Corpus** | 20 canonical papers in LLMs, RAG, and Cutoff | Open Access (arXiv, PubMed, CC-BY 4.0) | **VERIFIED:** Publicly available full texts and abstracts. | Store pre-extracted, verified text passages directly in `data/corpus.json`. |
| **Query Set** | 20 representative scientific synthesis questions | Authored under CC0 public domain | **VERIFIED:** Structured in `data/queries.json`. | Fixed deterministic questions to ensure zero test-time variance. |
| **Compute Hardware** | Local CPU (Windows x64, Intel i5/i7, 8–16 GB RAM) | User's local workstation | **VERIFIED:** Python 3.12, NumPy, Pandas, Matplotlib, SciPy available. | Optimized vectorized operations in pure Python / NumPy; zero GPU requirement. |
| **Software Libraries** | `numpy`, `pandas`, `matplotlib`, `scipy` | Permissive Open Source (BSD, MIT, Apache 2.0) | **VERIFIED:** Installed and functional in environment. | Standard Python standard library fallbacks for all operations. |

---

### 5. Compute and Time Constraints Estimate

* **Target Hardware:** Single local Windows workstation (Intel CPU, no external GPU required).
* **Execution Duration:** 
  * Baseline execution: $< 5$ seconds.
  * Proposed PAG pipeline: $< 10$ seconds.
  * Complete evaluation script + plotting + CSV export: $< 20$ seconds total.
* **Development & Verification Timeframe:** Completed within the 2-hour laboratory window / 1-day milestone gate.

---

### 6. Go / No-Go Decision and Fallback Architecture

#### Final Decision: **GO**
* **Rationale:** The proposed study directly addresses Gap G2 (Claim-level citation support), builds seamlessly on the student's literature review, introduces an actionable algorithmic modification, and executes entirely on commodity CPU hardware with zero external API dependencies or GPU bottlenecks.
* **Fallback Strategy:** If any neural component encounters environment compatibility issues, the entire pipeline is built on verified deterministic lexical-semantic overlap metrics (token Jaccard, Dice, and ROUGE-L span alignment), ensuring 100% reproducibility and mathematical transparency.

**Artifact Saved:** `prompts/PROMPT_04_IMPLEMENTATION.md`
