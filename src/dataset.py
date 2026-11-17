"""
Dataset loading, corpus indexing, and passage retrieval module.
Course: AI Tools for Research
Student: Sujal Rajesh Ghagare (MSE2026015)
"""

import json
import os
import re
from typing import List, Dict, Any, Optional

class DocumentStore:
    def __init__(self, corpus_path: str):
        self.corpus_path = corpus_path
        self.documents: Dict[str, Dict[str, Any]] = {}
        self.passages: List[Dict[str, Any]] = []
        self._load_corpus()

    def _load_corpus(self):
        if not os.path.exists(self.corpus_path):
            raise FileNotFoundError(f"Corpus file not found: {self.corpus_path}")
        with open(self.corpus_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for doc in data:
            doc_id = doc["id"]
            self.documents[doc_id] = doc
            # Generate passage chunks
            text = doc["text"]
            sentences = re.split(r'(?<=[.!?])\s+', text.strip())
            for idx, s in enumerate(sentences):
                if s.strip():
                    self.passages.append({
                        "doc_id": doc_id,
                        "title": doc["title"],
                        "year": doc["year"],
                        "authors": doc["authors"],
                        "passage_idx": idx,
                        "text": s.strip()
                    })

    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        return self.documents.get(doc_id)

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Rank passages by lexical overlap and term match against query tokens.
        """
        q_tokens = set(re.findall(r'\b[a-zA-Z]{3,}\b', query.lower()))
        scored = []
        for p in self.passages:
            p_tokens = set(re.findall(r'\b[a-zA-Z]{3,}\b', p["text"].lower()))
            overlap = len(q_tokens.intersection(p_tokens))
            if overlap > 0:
                score = overlap / (len(q_tokens) + 1e-6)
                scored.append((score, p))
            else:
                scored.append((0.0, p))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:top_k]]

class QuerySet:
    def __init__(self, queries_path: str):
        self.queries_path = queries_path
        self.queries: List[Dict[str, Any]] = []
        self._load_queries()

    def _load_queries(self):
        if not os.path.exists(self.queries_path):
            raise FileNotFoundError(f"Queries file not found: {self.queries_path}")
        with open(self.queries_path, "r", encoding="utf-8") as f:
            self.queries = json.load(f)

    def get_split(self, split_name: str) -> List[Dict[str, Any]]:
        return [q for q in self.queries if q.get("split") == split_name]

if __name__ == "__main__":
    store = DocumentStore("data/corpus.json")
    print(f"Loaded {len(store.documents)} documents and {len(store.passages)} passages.")
    qset = QuerySet("data/queries.json")
    print(f"Loaded {len(qset.queries)} queries ({len(qset.get_split('dev'))} dev, {len(qset.get_split('test'))} test).")
    res = store.retrieve("Retrieval-Augmented Generation RAG memory", top_k=2)
    print("Sanity retrieval check:", res[0]["doc_id"], "-", res[0]["text"][:60], "...")
