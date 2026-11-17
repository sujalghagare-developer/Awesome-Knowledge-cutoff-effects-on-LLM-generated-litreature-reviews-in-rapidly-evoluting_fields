# SCS-Bench-20: Scholarly Citation Support Benchmark

## 1. Overview
`SCS-Bench-20` is a curated, verified scientific synthesis benchmark specifically designed to evaluate claim-level citation support, hallucination rate, and passage grounding in LLM-assisted literature reviews. It contains 20 authentic open-access research papers and 20 standardized scientific synthesis queries.

## 2. Directory Structure and Files
* `corpus.json`: Document store containing 20 canonical papers across AI, RAG, and Citation Reliability. Each record provides:
  * `id`: Unique paper identifier (e.g. `lewis2020rag`).
  * `title`: Canonical paper title.
  * `authors`: Full author list.
  * `year`: Publication year.
  * `venue`: Journal or conference venue.
  * `doi`: Official DOI string.
  * `is_post_cutoff`: Boolean indicating publication relative to typical pre-training cutoff boundaries.
  * `text`: Verbatim excerpts and abstract evidence passages.
* `queries.json`: 20 standardized research queries across 4 subdomains:
  * 8 development queries (`split: dev`) used for parameter threshold calibration.
  * 12 evaluation queries (`split: test`) frozen for zero-touch final benchmark reporting.

## 3. Licensing and Access
All source paper texts and abstracts are published under open access or Creative Commons licenses (CC-BY 4.0 / arXiv non-exclusive distribution license). The curated benchmark and query annotations are released under the MIT License for educational and research reproduction.
