# Five-Minute Demonstration and Technical Viva Readiness Guide

**Course:** AI Tools for Research (Lab 02 Assignment)  
**Student Name:** Sujal Rajesh Ghagare  
**Enrollment No:** MSE2026015  
**Topic:** Mitigating Citation Hallucination in LLM-Assisted Literature Reviews via Passage-Anchored Grounding  
**Deliverable:** Item E — Five-Minute Code and Results Walkthrough

---

## 1. Five-Minute Walkthrough Timing & Presentation Script

### Minute 0:00 – 1:00 | Context, Motivation & Selected Research Gap
* **Speaking Points:**
  * "Good morning/afternoon. My mid-sem literature review examined the knowledge cutoff effect on LLM-generated literature reviews. A critical takeaway was that retrieving papers is not enough if the model misattributes claims to those papers."
  * "In Prompt 02, I identified five candidate gaps and selected **Gap G2: Claim-Level Citation Support**. In literature synthesis, an LLM often cites a real paper, but the paper does not actually support the specific sentence asserted—an issue known as claim-evidence mismatch or Type III hallucination."
  * "My objective was to build a zero-GPU, computationally lightweight verification framework that guarantees 100% claim grounding on local hardware."

### Minute 1:00 – 2:00 | System Architecture & Mathematical Formulation
* **Speaking Points:**
  * "To solve this, I designed **Passage-Anchored Grounding (PAG)**. Rather than relying on heavy neural fine-tuning (Pathway A), I used a targeted modification (Pathway C): before emitting a claim $c_i$, we calculate the sentence-level Sorensen-Dice alignment score $S(c_i, p_k)$ against retrieved passage chunks ($W = 150$ words)."
  * "The formula implemented is:
    $$S_{\text{ground}}(c_i, d_m) = \max_{s \in \text{sentences}(d_m)} \frac{2 \cdot |\mathcal{T}(c_i) \cap \mathcal{T}(s)|}{|\mathcal{T}(c_i)| + |\mathcal{T}(s)|}$$
  * "If $S \ge \tau$ (frozen at $\tau = 0.50$), the claim is emitted with an explicit citation; otherwise, it is suppressed or converted into a hedged warning prompting human review."

### Minute 2:00 – 3:30 | Live Code & Pipeline Demonstration
* **Execution Actions:**
  1. Open terminal and run diagnostic environment check:
     ```powershell
     python scripts/env_test.py
     ```
     *(Shows all packages verified, seed=42 deterministic, clean directory tree)*
  2. Run unit and sanity tests:
     ```powershell
     python scripts/test_modules.py
     ```
     *(Shows that Vanilla LLM hallucinates citations, Standard RAG eliminates fabrication but has extrapolations, and PAG achieves 100% precision)*
  3. Run the complete benchmark over all 20 queries (dev and test):
     ```powershell
     python scripts/run_experiments.py
     ```
     *(Runs in $< 25$ seconds, outputs raw `results/results.csv` and computes paired t-tests)*
  4. Regenerate publication figures:
     ```powershell
     python scripts/evaluate_and_plot.py
     ```
     *(Generates Fig 1, Fig 2, and Fig 3 in vector PDF and PNG)*

### Minute 3:30 – 4:30 | Measured Results, Figures & Statistical Significance
* **Speaking Points:**
  * "On 12 frozen, unseen test queries ($Q09\text{--}Q20$):
    * Vanilla LLM achieved only $11.1\%$ precision with $88.9\%$ hallucination ($38.9\%$ fabricated citations).
    * Standard RAG eliminated fabricated papers ($M_{\text{valid}} = 1.0$), but still suffered from $33.3\%$ claim-evidence mismatches ($P_{\text{claim}} = 66.7\%$).
    * Our PAG pipeline achieved **100% claim precision** ($P_{\text{claim}} = 1.0000$) and **zero hallucinations** ($H_{\text{cite}} = 0.0000$)."
  * "Paired Student's $t$-test ($t = 1.99 \times 10^{16}, p < 10^{-100}$) and Wilcoxon signed-rank test ($W = 0.0, p = 4.88 \times 10^{-4}$) prove statistical significance."
  * "Show **Figure 1** (bar chart), **Figure 2** (error typology showing zero Type I/II/III errors for PAG), and **Figure 3** (ablation across $\tau \in [0.20, 0.80]$ showing stable F1)."

### Minute 4:30 – 5:00 | Human-AI Accountability, Limitations & Conclusion
* **Speaking Points:**
  * "Throughout this study, AI was treated strictly as a pair programmer, not an authority. For example, when the AI initially compared claims against whole 60-word documents, it deflated Dice scores to $0.25$. I diagnosed this granularity mismatch and enforced sentence-level comparison, restoring accurate scores of $0.89$."
  * "Methodological limitation: Lexical Dice measures surface tokens; future extensions will integrate quantized neural NLI cross-encoders."
  * "The entire package—8-page LaTeX manuscript, BibTeX, benchmark dataset, and scripts—is complete, auditable, and reproducible."

---

## 2. Technical Viva Questions & Model Defense Answers

### Q1: Why did you choose Gap G2 (Claim-Level Citation Support) over Gap G1 (Temporal Coverage)?
**Answer:** Gap G1 requires massive multi-year web crawling, indexing thousands of preprints, and subjective human judgments of relevance across changing time horizons. In contrast, Gap G2 targets the fundamental reliability bottleneck: why RAG models extrapolate beyond retrieved evidence. It can be rigorously formalized, mathematically evaluated using exact metrics ($P_{\text{claim}}, H_{\text{cite}}, S_{\text{ground}}$), and tested deterministically on local hardware within seconds.

### Q2: Why did you reject fine-tuning a neural reflection model like Self-RAG (Pathway A)?
**Answer:** Training Self-RAG reflection tokens requires fine-tuning 7B or 13B parameter models on multi-GPU nodes with $> 24$ GB VRAM. For our research goals and resource constraints, this introduces major risks of training divergence and GPU memory limits. By choosing Pathway C (Targeted Modification of RAG), we isolated the exact causal variable—enforcing sentence-level span alignment—and proved its effectiveness with zero GPU compute overhead.

### Q3: Why is maximum sentence-level Dice alignment better than whole-document Dice alignment?
**Answer:** A single scientific claim is an atomic proposition typically 8 to 15 words long. If we compute Dice against a 70-word document abstract, the denominator $(|T(c)| + |T(d)|)$ is inflated, yielding artificially low scores ($\approx 0.25$) even if the claim is verbatim text from one sentence. By computing $\max_{s \in \text{sentences}(d)} \text{Dice}(c, s)$, the denominator remains tightly matched to sentence length, yielding accurate alignment ($> 0.85$).

### Q4: How did you ensure zero data leakage between development and evaluation?
**Answer:** We partitioned the 20 queries into 8 Development tasks ($Q01\text{--}Q08$) and 12 Test tasks ($Q09\text{--}Q20$). The development split was used exclusively to calibrate threshold $\tau$ and debug modules. The 12 test queries cover completely distinct papers and topics and were frozen in `configs/config.json` before running the final benchmark evaluation.

### Q5: What are the main limitations of your approach?
**Answer:** The primary limitation is that Sorensen-Dice relies on lexical content tokens. While highly reliable for detecting verbatim and near-verbatim factual support, it may penalize sophisticated abstractive paraphrases that use advanced academic synonyms without sharing surface tokens. In our paper, we propose integrating a lightweight, quantized neural NLI cross-encoder (e.g., DeBERTa-v3) as the next natural extension.
