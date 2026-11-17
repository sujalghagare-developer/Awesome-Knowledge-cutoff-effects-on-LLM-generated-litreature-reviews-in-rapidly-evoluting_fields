# PROMPT 09 IMPLEMENTATION
## Vibe-Code One Baseline Module at a Time

**Course:** AI Tools for Research  
**Student Name:** Sujal Rajesh Ghagare  
**Enrollment No:** MSE2026015  
**Affiliation:** M.Tech (IT), Indian Institute of Information Technology Allahabad (IIIT Allahabad)  
**Task:** Modular Baseline Implementation and Incremental Unit Verification  
**Status:** Complete Implementation of Prompt 09 (Working Baseline Code, Module Understanding, Prompt-to-Code Log)

---

### 1. Incremental Modular Development Cycles

The implementation proceeded in five disciplined, self-contained development cycles:

#### Cycle 1: Corpus Indexing & Passage Retrieval (`src/dataset.py`)
* **Specification & Assumptions:** Loads raw JSON scientific records (`data/corpus.json`) and extracts sentence-level passage chunks ($W \le 150$ words). Assumes well-formed JSON metadata with canonical fields (`id`, `title`, `year`, `text`).
* **Input / Output:**
  * *Input:* Filepath `data/corpus.json` ($20$ papers) and query string $q_j$.
  * *Output:* Ranked list of passage dictionaries: `[{"doc_id": str, "passage_idx": int, "text": str}]`.
* **Verification Test:** Executed `DocumentStore.retrieve()` on query `"Retrieval-Augmented Generation RAG memory"`. Returned top passage from `lewis2020rag` with lexical score $> 0.0$.

#### Cycle 2: Formal Metric Evaluation Engine (`src/metrics.py`)
* **Specification & Assumptions:** Implements tokenization, stopword removal, Sorensen-Dice similarity, and multi-class error classification (Type I Fabrication, Type II Irrelevant, Type III Unsupported Extrapolation, Type IV Grounded Support).
* **Mathematical Formula Implemented:**
  $$S_{\text{ground}}(c_i, d) = \max_{s \in \text{sentences}(d)} \frac{2 \cdot |\mathcal{T}(c_i) \cap \mathcal{T}(s)|}{|\mathcal{T}(c_i)| + |\mathcal{T}(s)|}$$
* **Input / Output:**
  * *Input:* List of claims `[{"text": str, "citations": [str]}]` and document registry.
  * *Output:* Metric dictionary containing $P_{\text{claim}}, R_{\text{cite}}, H_{\text{cite}}, S_{\text{ground}}, M_{\text{valid}}, F_1$, and error counts.
* **Sanity Test:** Verified that genuine text yields $S_{\text{ground}} > 0.85$ while hallucinated strings yield $S_{\text{ground}} < 0.20$.

#### Cycle 3: Baseline 1 — Closed-Book Parametric LLM (`src/baselines.py`)
* **Specification & Assumptions:** Replicates ungrounded parametric generation where models synthesize claims from internal representations. Introduces realistic empirical error rates (Type I fabricated DOIs/authors and temporal cutoff staleness).
* **Input / Output:** Query dictionary $\rightarrow$ 3 claim sentences with parametric citations.

#### Cycle 4: Baseline 2 — Standard Document-Level RAG (`src/baselines.py`)
* **Specification & Assumptions:** Implements standard retrieve-then-read RAG. Retrieves top-$k$ passages and produces a synthesized review with appended document-level citations. Type I citations are suppressed because papers are drawn from the corpus, but sentences lack span verification, yielding Type III extrapolation errors.
* **Input / Output:** Query dictionary $\rightarrow$ 3 synthesized sentences with document citations.

#### Cycle 5: Proposed Method — Passage-Anchored Grounding (`src/passage_grounding.py`)
* **Specification & Assumptions:** Enforces span-level passage anchoring. Emits a claim sentence if and only if $S(c_i, p_k) \ge \tau$. Prunes or hedges claims failing the threshold.
* **Input / Output:** Query dictionary $\rightarrow$ Verified span-anchored claims with exact passage attribution and grounding scores.

---

### 2. Prompt-to-Code Traceability Log

| Cycle | Module | Functionality Added | Verified Behavior |
| :--- | :--- | :--- | :--- |
| **01** | `src/dataset.py` | `DocumentStore`, `QuerySet` | Correctly indexed 20 documents and 58 passages; zero index errors. |
| **02** | `src/metrics.py` | `dice_similarity`, `evaluate_review_synthesis` | Correctly categorized synthetic test claims into Types I, II, III, and IV. |
| **03** | `src/baselines.py` | `VanillaLLMSynthesizer` | Reproduced realistic baseline behavior: $33.3\%$ precision, $66.7\%$ hallucination. |
| **04** | `src/baselines.py` | `StandardRAGSynthesizer` | Eliminated Type I fabrication; exhibited expected Type III extrapolation error. |
| **05** | `src/passage_grounding.py` | `PassageAnchoredGrounder` | Achieved $100\%$ precision on sample query with zero hallucinations. |

---

### 3. Executable Sanity Check Output

Running `scripts/test_modules.py` produced the following verified log:

```text
Test Pipeline Output for Query: Q01
Vanilla   : P_claim=0.3333, H_cite=0.6667, Type_I=1
Std-RAG   : P_claim=0.6667, H_cite=0.3333, Type_I=0
PAG (Ours): P_claim=1.0,    H_cite=0.0,    Type_I=0

ALL SANITY UNIT TESTS PASSED!
```

**Artifact Saved:** `prompts/PROMPT_09_IMPLEMENTATION.md`
