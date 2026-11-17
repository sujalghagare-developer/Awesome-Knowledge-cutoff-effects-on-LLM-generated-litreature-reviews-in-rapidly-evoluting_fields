"""
Unit and Sanity Tests for Baselines and Grounding Pipeline.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.dataset import DocumentStore, QuerySet
from src.baselines import VanillaLLMSynthesizer, StandardRAGSynthesizer
from src.passage_grounding import PassageAnchoredGrounder
from src.metrics import evaluate_review_synthesis

def test_full_pipeline():
    doc_store = DocumentStore("data/corpus.json")
    query_set = QuerySet("data/queries.json")
    corpus_dict = doc_store.documents

    dev_queries = query_set.get_split("dev")
    sample_q = dev_queries[0]

    vanilla = VanillaLLMSynthesizer(seed=42)
    std_rag = StandardRAGSynthesizer(top_k=3, seed=42)
    pag = PassageAnchoredGrounder(top_k=3, threshold=0.50)

    c_vanilla = vanilla.synthesize(sample_q, doc_store)
    c_rag = std_rag.synthesize(sample_q, doc_store)
    c_pag = pag.synthesize(sample_q, doc_store)

    m_vanilla = evaluate_review_synthesis(c_vanilla, corpus_dict, threshold=0.50)
    m_rag = evaluate_review_synthesis(c_rag, corpus_dict, threshold=0.50)
    m_pag = evaluate_review_synthesis(c_pag, corpus_dict, threshold=0.50)

    print("Test Pipeline Output for Query:", sample_q["id"])
    print(f"Vanilla   : P_claim={m_vanilla['p_claim']}, H_cite={m_vanilla['h_cite']}, Type_I={m_vanilla['type_I']}")
    print(f"Std-RAG   : P_claim={m_rag['p_claim']}, H_cite={m_rag['h_cite']}, Type_I={m_rag['type_I']}")
    print(f"PAG (Ours): P_claim={m_pag['p_claim']}, H_cite={m_pag['h_cite']}, Type_I={m_pag['type_I']}")

    assert m_pag["p_claim"] > m_vanilla["p_claim"], "PAG precision must exceed Vanilla"
    assert m_pag["h_cite"] < m_vanilla["h_cite"], "PAG hallucination rate must be lower than Vanilla"
    print("\nALL SANITY UNIT TESTS PASSED!")

if __name__ == "__main__":
    test_full_pipeline()
