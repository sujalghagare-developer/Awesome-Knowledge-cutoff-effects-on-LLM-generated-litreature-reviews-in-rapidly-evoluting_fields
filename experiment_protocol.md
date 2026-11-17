# Frozen Experimental Evaluation Protocol

**Project:** AITR_Lab02_MSE2026015_CitationGrounding  
**Student:** Sujal Rajesh Ghagare (MSE2026015)  
**Status:** FROZEN & EXECUTED  

---

## 1. Frozen Parameters and Settings

```json
{
  "random_seed": 42,
  "retrieval": {
    "top_k": 3,
    "passage_window_words": 150
  },
  "grounding": {
    "default_threshold": 0.50,
    "ablation_thresholds": [0.20, 0.35, 0.50, 0.65, 0.80]
  },
  "splits": {
    "dev": ["Q01", "Q02", "Q03", "Q04", "Q05", "Q06", "Q07", "Q08"],
    "test": ["Q09", "Q10", "Q11", "Q12", "Q13", "Q14", "Q15", "Q16", "Q17", "Q18", "Q19", "Q20"]
  }
}
```

---

## 2. Metric Specifications & Directionality
1. **Claim Citation Precision ($P_{\text{claim}}$) [$\uparrow$]:** Proportion of cited claims supported by source text.
2. **Citation Recall ($R_{\text{cite}}$) [$\uparrow$]:** Proportion of claims backed by at least one citation.
3. **Citation Hallucination Rate ($H_{\text{cite}}$) [$\downarrow$]:** Proportion of claims that are fabricated, irrelevant, or unsupported.
4. **Lexical Grounding Score ($S_{\text{ground}}$) [$\uparrow$]:** Sentence-level Sorensen-Dice coefficient between claim and source passage.
5. **Metadata Veracity ($M_{\text{valid}}$) [$\uparrow$]:** Fraction of cited references that exist in authoritative registry.

---

## 3. Protocol Change Logging Rule
Any proposed alteration to the scoring logic, query texts, or partition boundaries after protocol freezing must be formally logged in `research_decisions.md` with explicit scientific justification prior to execution.
