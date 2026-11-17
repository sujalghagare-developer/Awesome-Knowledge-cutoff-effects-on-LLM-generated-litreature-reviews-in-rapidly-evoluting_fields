# PROMPT 16 IMPLEMENTATION
## Demanding Technical Peer Review and Revision Log

**Course:** AI Tools for Research  
**Student Name:** Sujal Rajesh Ghagare  
**Enrollment No:** MSE2026015  
**Affiliation:** M.Tech (IT), Indian Institute of Information Technology Allahabad (IIIT Allahabad)  
**Manuscript Audited:** *Mitigating Citation Hallucination in LLM-Assisted Literature Reviews: A Controlled Study on Passage-Anchored Grounding*  
**Status:** Complete Implementation of Prompt 16 (Demanding Peer-Review Report and Revision Matrix)

---

### 1. Peer-Review Meta-Evaluation

* **Recommendation:** Minor Revision.
* **Review Summary:** The manuscript tackles a critical and timely problem in AI-assisted research: citation hallucination and claim-evidence mismatch in literature synthesis. The transition from the student's initial literature review to an empirical, zero-GPU reproducible study is commendable. The mathematical formulation of metrics is rigorous, the experimental design incorporates clean controls, and all numbers are backed by genuine code outputs. However, several methodological assumptions regarding lexical overlap and benchmark scale require careful qualification before final archiving.

---

### 2. Major Concerns and Proposed Remedies

#### Major Concern 1: Lexical Overlap vs. True Semantic Entailment (§3.2, §7.1)
* **Location:** Section 3.2 (Metric 4) and Section 7 (Limitations).
* **Why it Matters:** Sorensen-Dice measures surface token co-occurrence. A candidate claim could share high lexical overlap with a source passage while subtly reversing the logical polarity (e.g., "Method X does not improve recall" vs. "Method X improves recall"). Conversely, a valid abstractive paraphrase using academic synonyms could be unfairly penalized.
* **Remedy:** In Section 3.2 and Section 7, explicitly state that lexical Dice serves as a computationally lightweight proxy for span-level evidential adherence on local hardware. Formally identify neural Natural Language Inference (NLI) cross-encoders (e.g., DeBERTa-v3) as the natural next-stage extension.

#### Major Concern 2: Candidate Span Generation vs. Free-Form Generation (§3.4, §5.1)
* **Location:** Section 3.4 (PAG Algorithm) and Section 5.1 (Results).
* **Why it Matters:** The proposed PAG algorithm achieves $P_{\text{claim}} = 1.0000$ and $R_{\text{cite}} = 1.0000$ partly because candidate propositions are derived directly from verified retrieved passage spans. If an unconstrained generator produced speculative text, a strict threshold ($\tau = 0.50$) would prune invalid claims, likely reducing citation recall ($R_{\text{cite}}$).
* **Remedy:** Clarify the distinction in Section 5 and Section 6. Acknowledge that PAG's perfect recall is a property of its extractive-grounded candidate proposal mechanism, which intentionally avoids generating speculative ungrounded sentences.

#### Major Concern 3: Bounded Benchmark Scale (§4.1)
* **Location:** Section 4.1 (Benchmark Dataset).
* **Why it Matters:** SCS-Bench-20 consists of 20 canonical papers and 20 synthesis queries. While paired $t$-tests and Wilcoxon tests demonstrate strong statistical significance ($p < 0.001$), claims of "universal elimination of hallucination" must be bounded to the tested STEM domain.
* **Remedy:** Temper global generalization claims in the Abstract and Conclusion; explicitly delimit the operational scope to computer science, NLP, and biomedical informatics.

---

### 3. Minor Concerns
* **Minor Point 1 (Figure Resolution):** Ensure all figure labels in `fig1_method_comparison.pdf` maintain $\ge 10$ pt font for double-column legibility. (Verified: regenerated at 300 DPI and vector PDF).
* **Minor Point 2 (Notation Consistency):** Ensure that the alignment threshold is consistently referred to as $\tau$ across the text, algorithms, and figures. (Verified across manuscript).
* **Minor Point 3 (Citation Metadata Veracity):** Explicitly clarify why Standard-RAG achieves $M_{\text{valid}} = 1.0000$ despite committing $33.3\%$ claim-evidence mismatches (retrieved papers exist in the corpus, but sentences extrapolate). (Addressed in §5.3).

---

### 4. Author-Response and Manuscript Revision Table

| # | Reviewer Concern | Author Response | Implemented Manuscript Change |
| :---: | :--- | :--- | :--- |
| **R1** | Surface lexical Dice cannot detect logical negation. | We agree. While our benchmark did not encounter polarity inversions due to extractive span candidates, this is a real theoretical risk. | Added detailed discussion in §7.1 and proposed NLI cross-encoder verification as follow-up study #1. |
| **R2** | Perfect precision ($1.0000$) may appear unrealistic without explaining candidate span extraction. | The perfect precision is the direct result of the span-anchoring architecture, which only emits claims passing $\tau \ge 0.50$. | Updated §3.4 and §6.1 to detail the span proposal mechanism and explain the precision-recall trade-off. |
| **R3** | Generalization beyond STEM literature is unproven. | Accepted. The 20 papers represent AI and biomedical NLP. | Revised Abstract, §4.1, and §8 to explicitly bound claims to computer science and biomedical literature synthesis. |
| **R4** | Confirm that all random seeds and test splits were frozen prior to viewing results. | Confirmed. Test split ($Q09\text{--}Q20$) was frozen in `config.json` before running the evaluation pipeline. | Documented frozen checklist in §4.3 and `experiment_protocol.md`. |

**Artifact Saved:** `prompts/PROMPT_16_IMPLEMENTATION.md`
