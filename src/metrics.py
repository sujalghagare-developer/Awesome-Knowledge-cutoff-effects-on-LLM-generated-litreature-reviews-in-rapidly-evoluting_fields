"""
Evaluation metrics for claim-level citation support, hallucination rate, and lexical grounding.
Course: AI Tools for Research
Student: Sujal Rajesh Ghagare (MSE2026015)
"""

import re
from typing import List, Dict, Any, Set, Tuple

STOPWORDS: Set[str] = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
    "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both",
    "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't",
    "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't",
    "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll",
    "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's",
    "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on",
    "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own",
    "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some",
    "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then",
    "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this",
    "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we",
    "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's",
    "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with",
    "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your",
    "yours", "yourself", "yourselves"
}

def extract_content_tokens(text: str) -> Set[str]:
    """Tokenize text into lowercase alphabetic words and remove stopwords."""
    raw_tokens = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    return {t for t in raw_tokens if t not in STOPWORDS}

def dice_similarity(text_a: str, text_b: str) -> float:
    """Compute Sorensen-Dice lexical similarity coefficient."""
    tokens_a = extract_content_tokens(text_a)
    tokens_b = extract_content_tokens(text_b)
    if not tokens_a or not tokens_b:
        return 0.0
    intersection = len(tokens_a.intersection(tokens_b))
    return (2.0 * intersection) / (len(tokens_a) + len(tokens_b))

def jaccard_similarity(text_a: str, text_b: str) -> float:
    """Compute Jaccard token overlap index."""
    tokens_a = extract_content_tokens(text_a)
    tokens_b = extract_content_tokens(text_b)
    if not tokens_a or not tokens_b:
        return 0.0
    intersection = len(tokens_a.intersection(tokens_b))
    union = len(tokens_a.union(tokens_b))
    return intersection / union if union > 0 else 0.0

def score_claim_against_document(claim_text: str, doc_text: str) -> float:
    """
    Maximal sentence-level Dice alignment between claim and document sentences.
    """
    doc_sentences = re.split(r'(?<=[.!?])\s+', doc_text.strip())
    best = 0.0
    for s in doc_sentences:
        if s.strip():
            score = dice_similarity(claim_text, s)
            if score > best:
                best = score
    return best

def evaluate_claim_support(
    claim_text: str,
    cited_keys: List[str],
    corpus_docs: Dict[str, Any],
    threshold: float = 0.50
) -> Tuple[str, float, str]:
    """
    Evaluate a single claim against cited documents:
    Returns (error_type, max_dice_score, best_matched_ref)
    Error types:
      - 'TYPE_I_FABRICATION': Citation key does not exist in verified corpus.
      - 'TYPE_II_IRRELEVANT': Citation exists, but max sentence alignment < 0.20 (topic mismatch).
      - 'TYPE_III_UNSUPPORTED': Citation exists, but 0.20 <= alignment < threshold (unsupported claim extrapolation).
      - 'TYPE_IV_SUPPORTED': Citation exists and alignment >= threshold.
    """
    if not cited_keys:
        return "UNCITED", 0.0, ""

    # Check for fabricated references (Type I)
    for key in cited_keys:
        if key not in corpus_docs:
            return "TYPE_I_FABRICATION", 0.0, key

    # Score alignment against cited documents
    best_score = 0.0
    best_key = cited_keys[0]
    for key in cited_keys:
        doc_text = corpus_docs[key]["text"]
        score = score_claim_against_document(claim_text, doc_text)
        if score > best_score:
            best_score = score
            best_key = key

    if best_score >= threshold:
        return "TYPE_IV_SUPPORTED", best_score, best_key
    elif best_score >= 0.20:
        return "TYPE_III_UNSUPPORTED", best_score, best_key
    else:
        return "TYPE_II_IRRELEVANT", best_score, best_key

def evaluate_review_synthesis(
    claims: List[Dict[str, Any]],
    corpus_docs: Dict[str, Any],
    threshold: float = 0.50
) -> Dict[str, Any]:
    """
    Compute full evaluation metrics across synthesized claims.
    claims format: [{"text": str, "citations": [str]}]
    """
    total_claims = len(claims)
    if total_claims == 0:
        return {
            "num_claims": 0, "p_claim": 0.0, "r_cite": 0.0, "h_cite": 0.0,
            "s_ground": 0.0, "m_valid": 0.0, "f1": 0.0,
            "type_I": 0, "type_II": 0, "type_III": 0, "type_IV": 0
        }

    cited_claims = 0
    supported_claims = 0
    fabricated_citations = 0
    unsupported_claims = 0
    irrelevant_claims = 0
    total_citations_cited = 0
    valid_citations_cited = 0
    grounding_scores = []

    for c in claims:
        text = c["text"]
        cites = c.get("citations", [])
        if cites:
            cited_claims += 1
            total_citations_cited += len(cites)
            for k in cites:
                if k in corpus_docs:
                    valid_citations_cited += 1

            status, score, _ = evaluate_claim_support(text, cites, corpus_docs, threshold)
            grounding_scores.append(score)

            if status == "TYPE_IV_SUPPORTED":
                supported_claims += 1
            elif status == "TYPE_III_UNSUPPORTED":
                unsupported_claims += 1
            elif status == "TYPE_II_IRRELEVANT":
                irrelevant_claims += 1
            elif status == "TYPE_I_FABRICATION":
                fabricated_citations += 1

    # Precision: proportion of cited claims that are supported
    p_claim = supported_claims / cited_claims if cited_claims > 0 else 0.0
    # Recall: proportion of total claims that are supported by citation
    r_cite = cited_claims / total_claims if total_claims > 0 else 0.0
    # Hallucination rate: (Type I + Type II + Type III) / total_claims
    h_cite = (fabricated_citations + unsupported_claims + irrelevant_claims) / total_claims if total_claims > 0 else 0.0
    # Mean grounding score
    s_ground = sum(grounding_scores) / len(grounding_scores) if grounding_scores else 0.0
    # Metadata validity
    m_valid = valid_citations_cited / total_citations_cited if total_citations_cited > 0 else 0.0
    # F1
    f1 = (2.0 * p_claim * r_cite) / (p_claim + r_cite) if (p_claim + r_cite) > 0 else 0.0

    return {
        "num_claims": total_claims,
        "num_cited_claims": cited_claims,
        "p_claim": round(p_claim, 4),
        "r_cite": round(r_cite, 4),
        "h_cite": round(h_cite, 4),
        "s_ground": round(s_ground, 4),
        "m_valid": round(m_valid, 4),
        "f1": round(f1, 4),
        "type_I": fabricated_citations,
        "type_II": irrelevant_claims,
        "type_III": unsupported_claims,
        "type_IV": supported_claims
    }

if __name__ == "__main__":
    import json
    with open("data/corpus.json", "r") as f:
        docs = {d["id"]: d for d in json.load(f)}

    test_claims = [
        {
            "text": "Retrieval-Augmented Generation models combine parametric and non-parametric memory for language generation.",
            "citations": ["lewis2020rag"]
        },
        {
            "text": "Self-RAG utilizes quantum annealing to achieve zero hallucination across all benchmarks.",
            "citations": ["asai2024selfrag"]
        },
        {
            "text": "Hyper-Transformer 9000 achieves 99.9% precision on scientific literature review.",
            "citations": ["invented_author_2025"]
        }
    ]
    res = evaluate_review_synthesis(test_claims, docs, threshold=0.50)
    print("Sanity Metrics Evaluation:")
    for k, v in res.items():
        print(f"  {k:<18}: {v}")
