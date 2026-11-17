# PROMPT 14 IMPLEMENTATION
## Interpretation of Outcomes, Negative Results, and Methodological Limitations

**Course:** AI Tools for Research  
**Student Name:** Sujal Rajesh Ghagare  
**Enrollment No:** MSE2026015  
**Affiliation:** M.Tech (IT), Indian Institute of Information Technology Allahabad (IIIT Allahabad)  
**Measured Evidence Base:** 12 Test Queries, 3 Conditions, 108 Synthesized Claims, Raw `results.csv`  
**Status:** Complete Implementation of Prompt 14 (Results and Discussion Outline with Critical Limitations)

---

### 1. Systematic Interpretation of Research Questions

#### Research Question 1 (RQ1: Claim Citation Precision)
* **Direct Observation:** Passage-Anchored Grounding (PAG) achieved a mean claim precision $P_{\text{claim}} = 1.0000$, compared to $0.6667$ for Standard-RAG and $0.1111$ for Vanilla-LLM. Both parametric ($t = 1.99 \times 10^{16}, p < 10^{-100}$) and non-parametric ($W = 0.0, p = 4.88 \times 10^{-4}$) tests firmly reject the null hypothesis.
* **Underlying Mechanism:** Standard-RAG injects documents into the global prompt context, allowing the generator's self-attention to freely associate tokens across documents, frequently emitting assertions that are plausible in general AI discourse but absent from the specific cited paper. By enforcing span-level passage anchoring, PAG prunes unanchored assertions before emission.
* **Alternative Explanations:** The high precision of PAG partially stems from candidate claims closely mirroring extracted passage spans; in free-form generative synthesis with extensive novel phrasing, lexical alignment scores might be lower.
* **Unsupported Claims to Avoid:** We do not claim that PAG "solves all hallucinations in LLMs." It specifically eliminates passage-attribution mismatch within the retrieved context.

#### Research Question 2 (RQ2: Hallucination & Error Typology)
* **Direct Observation:** Vanilla-LLM produced 14 fabricated citations (Type I: $38.9\%$) and 18 topic mismatches (Type II: $50.0\%$), with an overall hallucination rate of $88.89\%$. Standard-RAG completely eliminated Type I fabrication ($0\%$), but suffered from $33.3\%$ Type II/III errors. PAG achieved $0.0\%$ hallucination across all error modes.
* **Mechanism:** Document retrieval anchors the bibliography in real metadata, eliminating Type I fabrication. Enforcing span verification ($\tau \ge 0.50$) eliminates Type II and III errors by verifying that every cited paper directly contains the asserted proposition.

#### Research Question 3 (RQ3: Threshold Sensitivity & Coverage Trade-Off)
* **Direct Observation:** Across $\tau \in [0.20, 0.80]$, $P_{\text{claim}}$ remained high while $R_{\text{cite}} = 1.0000$ was maintained because candidate claims were derived from verified retrieved spans.
* **Trade-Off Analysis:** While precision is preserved, higher thresholds ($\tau \ge 0.80$) restrict generative paraphrasing, favoring near-verbatim extractive synthesis over high-level conceptual abstraction.

---

### 2. Methodological Limitations & Frank Negative Findings

1. **Paraphrase Penalization:** Lexical Sorensen-Dice relies on content token overlap. If a model generates an accurate semantic synthesis using sophisticated academic synonyms (e.g. "ameliorates" instead of "reduces"), lexical Dice may score lower than a neural cross-encoder.
2. **Fluency vs. Fidelity Tension:** By prioritizing zero citation hallucination, the synthesized text in PAG adheres closely to retrieved passages, sacrificing some rhetorical prose fluidity found in unconstrained models.
3. **Corpus Scale:** SCS-Bench-20 contains 20 papers and 20 standardized queries. While statistically significant on paired tests ($p < 0.001$), evaluation on a multi-thousand paper corpus across diverse non-STEM disciplines remains an open question.

---

### 3. Three Prioritized Follow-Up Experiments

| Rank | Proposed Follow-Up Experiment | Estimated Cost / Compute | Primary Information Gained |
| :---: | :--- | :--- | :--- |
| **1** | **Neural NLI Cross-Encoder Entailment:** Replace lexical Dice with a quantized DeBERTa-v3 NLI cross-encoder ($< 500$ MB) to evaluate abstractive paraphrases. | Low ($< 2$ minutes on local CPU). | Quantifies the gap between exact lexical alignment and semantic natural language entailment. |
| **2** | **Multi-Hop Synthesis Across Contradictory Findings:** Introduce pairs of papers reporting conflicting empirical outcomes to test whether PAG preserves nuance or forces a false consensus. | Very Low (dataset curation + $< 1$ minute script run). | Directly addresses Gap G5 (Conflict-aware synthesis). |
| **3** | **Blinded Human Expert Evaluation:** Present 30 synthesized literature paragraphs to domain experts to score readability, factual trust, and coherence. | Medium (human reader time, zero GPU). | Bridges automated token metrics to human research utility. |

**Artifact Saved:** `prompts/PROMPT_14_IMPLEMENTATION.md`
