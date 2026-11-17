# PROMPT 18 IMPLEMENTATION
## Audit the Human-AI Collaboration and Research Integrity

**Course:** AI Tools for Research  
**Student Name:** Sujal Rajesh Ghagare  
**Enrollment No:** MSE2026015  
**Affiliation:** M.Tech (IT), Indian Institute of Information Technology Allahabad (IIIT Allahabad)  
**Deliverable:** Research Integrity Report and Reflective Account of Human Decisions  
**Status:** Complete Implementation of Prompt 18 (AI Provenance Report, Limitations Audit, Human Decision Log)

---

### 1. Executive Summary
This document fulfills **Prompt 18 (Phase VI: Human-AI Accountability)** of the research project. It provides an honest, auditable account of how AI tools were utilized during the research journey, identifies three concrete failures and manual human corrections, and articulates which conceptual conclusions depended strictly on human reasoning.

---

### 2. Structured AI Activity Register

```
+---------------------------------------------------------------------------------------+
|                             AI Collaboration Dimension                                |
+---------------------------------------------------------------------------------------+
|  Task: Ideation & Scaffolding       --> AI proposed options; Human selected Gap G2    |
|  Task: Mathematical Metric Coding   --> AI proposed document Dice; Human fixed to span|
|  Task: Debugging Path & Key Errors  --> Human diagnosed tracebacks and corrected code |
|  Task: Manuscript Drafting          --> AI drafted sections; Human verified numbers  |
+---------------------------------------------------------------------------------------+
```

| Phase | Activity | Tool / Prompt | AI Proposal | Human Intervention & Decision | Outcome |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Phase I** | Gap Selection | Prompt 03 | Outlined 5 theoretical gaps. | Chose Gap G2 (Claim-level support) for minimal compute and high mathematical rigor. | Focused, tractable scope established. |
| **Phase II** | Architecture | Prompt 07 | Proposed full neural fine-tuning. | Rejected GPU training; mandated zero-GPU deterministic span verification. | Lightweight pipeline executable in $< 30$ seconds. |
| **Phase III** | Metric Logic | Prompt 09 | Compared claim against whole abstract. | Identified granularity mismatch; forced maximum sentence-level alignment. | Dice alignment on genuine claims increased from $0.26 \rightarrow 0.89$. |
| **Phase III** | Script Debugging | Prompt 11 | Missed package root path. | Added `sys.path.insert(0, ...)` to scripts. | Resolved `ModuleNotFoundError`. |
| **Phase IV** | Data Analysis | Prompt 13 | Summarized results. | Audited all numbers against raw `results.csv`; added Wilcoxon and paired $t$-tests. | 100% data traceability achieved. |
| **Phase V** | Paper Writing | Prompt 15 | Drafted academic prose. | Verified all BibTeX DOIs; ensured no fabricated metrics or literature claims. | Flawless LaTeX manuscript matching code outputs. |

---

### 3. Three Verified Examples of AI Limitations and Purposeful Human Corrections

1. **AI Metric Granularity Error (Sentence vs. Document):** The AI computed token overlap between a 9-token claim and a 60-token abstract, producing an artificially deflated Dice score of $0.26$. The student intervened to compute sentence-level alignment:
   $$S(c_i, d) = \max_{s \in \text{sentences}(d)} \text{Dice}(c_i, s)$$
   restoring accurate scoring ($0.89$).
2. **AI Execution Path Assumption:** The AI failed to account for Python's default `sys.path` when running scripts from subfolders, causing `ModuleNotFoundError`. The student introduced absolute project root resolution.
3. **AI Deserialization Crash:** The AI used hardcoded two-decimal string keys (`"0.20"`) to index JSON dictionaries generated from float numbers (`"0.2"`), causing a runtime `KeyError`. The student corrected the parser to handle dynamic dictionary keys.

---

### 4. Human Intellectual Ownership and Vibe Coding Lessons

* **Core Intellectual Insight:** The realization that Standard RAG's failure is not retrieval failure, but **self-attention interpolation across disparate documents** that generates convincing yet unsupported claims.
* **Vibe Coding Reflection:** Vibe coding is powerful for rapid prototyping, but treacherous if accepted without micro-unit tests and line-by-line verification. Research integrity demands that every number in a research paper traces back to an auditable line in a verified execution log.

**Artifact Saved:** `prompts/PROMPT_18_IMPLEMENTATION.md` and `ai_assistance_log.md`
