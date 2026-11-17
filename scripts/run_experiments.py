#!/usr/bin/env python3
"""
Main Experimental Execution Pipeline.
Executes Vanilla-LLM, Standard-RAG, and Passage-Anchored Grounding (PAG)
across the frozen benchmark, computes statistical significance, and exports results.csv.

Course: AI Tools for Research
Student: Sujal Rajesh Ghagare (MSE2026015)
"""

import sys
import os
import json
import logging
import pandas as pd
import numpy as np
from scipy import stats

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.dataset import DocumentStore, QuerySet
from src.baselines import VanillaLLMSynthesizer, StandardRAGSynthesizer
from src.passage_grounding import PassageAnchoredGrounder
from src.metrics import evaluate_review_synthesis

def setup_logging(log_path: str):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    logging.basicConfig(
        filename=log_path,
        filemode="w",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger("").addHandler(console)

def run_all_experiments():
    config_path = "configs/config.json"
    with open(config_path, "r") as f:
        config = json.load(f)

    log_file = "results/run.log"
    setup_logging(log_file)
    logging.info("Starting controlled benchmark evaluation...")
    logging.info(f"Loaded configuration from {config_path}")

    doc_store = DocumentStore(config["dataset"]["corpus_path"])
    query_set = QuerySet(config["dataset"]["queries_path"])
    corpus_dict = doc_store.documents

    test_queries = query_set.get_split("test")
    dev_queries = query_set.get_split("dev")
    logging.info(f"Loaded {len(doc_store.documents)} corpus documents.")
    logging.info(f"Loaded {len(dev_queries)} dev queries and {len(test_queries)} test queries.")

    seed = config["random_seed"]
    top_k = config["retrieval"]["top_k"]
    default_tau = config["grounding"]["default_threshold"]

    vanilla_model = VanillaLLMSynthesizer(seed=seed)
    std_rag_model = StandardRAGSynthesizer(top_k=top_k, seed=seed)
    pag_model = PassageAnchoredGrounder(top_k=top_k, threshold=default_tau)

    records = []

    # 1. Evaluate Primary Test Split across 3 Methods
    logging.info("\n--- Evaluating Test Partition (12 Unseen Queries) ---")
    for q in test_queries:
        qid = q["id"]
        q_text = q["query"]
        subdomain = q["subdomain"]

        # Run Vanilla
        c_vanilla = vanilla_model.synthesize(q, doc_store)
        m_vanilla = evaluate_review_synthesis(c_vanilla, corpus_dict, threshold=default_tau)
        m_vanilla.update({"query_id": qid, "subdomain": subdomain, "method": "Vanilla-LLM", "split": "test", "tau": default_tau})
        records.append(m_vanilla)

        # Run Standard RAG
        c_rag = std_rag_model.synthesize(q, doc_store)
        m_rag = evaluate_review_synthesis(c_rag, corpus_dict, threshold=default_tau)
        m_rag.update({"query_id": qid, "subdomain": subdomain, "method": "Standard-RAG", "split": "test", "tau": default_tau})
        records.append(m_rag)

        # Run Proposed PAG
        c_pag = pag_model.synthesize(q, doc_store)
        m_pag = evaluate_review_synthesis(c_pag, corpus_dict, threshold=default_tau)
        m_pag.update({"query_id": qid, "subdomain": subdomain, "method": "PAG (Ours)", "split": "test", "tau": default_tau})
        records.append(m_pag)

        logging.info(f"Query {qid} [{subdomain}]: Vanilla P={m_vanilla['p_claim']} | Std-RAG P={m_rag['p_claim']} | PAG P={m_pag['p_claim']}")

    df_test = pd.DataFrame(records)

    # 2. Run Threshold Sensitivity Ablation on Test Split for PAG
    logging.info("\n--- Running Threshold Sensitivity Ablation (tau in [0.20, 0.80]) ---")
    ablation_records = []
    thresholds = config["grounding"]["ablation_thresholds"]
    for tau in thresholds:
        pag_abl = PassageAnchoredGrounder(top_k=top_k, threshold=tau)
        for q in test_queries:
            c_abl = pag_abl.synthesize(q, doc_store)
            m_abl = evaluate_review_synthesis(c_abl, corpus_dict, threshold=tau)
            m_abl.update({
                "query_id": q["id"],
                "subdomain": q["subdomain"],
                "method": f"PAG_tau_{tau:.2f}",
                "split": "test",
                "tau": tau
            })
            ablation_records.append(m_abl)
            records.append(m_abl)

    df_all = pd.DataFrame(records)
    results_csv_path = config["output_paths"]["results_csv"]
    df_all.to_csv(results_csv_path, index=False)
    logging.info(f"\nSaved raw per-query evaluation records to {results_csv_path}")

    # 3. Statistical Analysis & Hypothesis Testing
    logging.info("\n--- Statistical Hypothesis Testing ---")
    v_prec = df_test[df_test["method"] == "Vanilla-LLM"]["p_claim"].values
    r_prec = df_test[df_test["method"] == "Standard-RAG"]["p_claim"].values
    p_prec = df_test[df_test["method"] == "PAG (Ours)"]["p_claim"].values

    v_hall = df_test[df_test["method"] == "Vanilla-LLM"]["h_cite"].values
    r_hall = df_test[df_test["method"] == "Standard-RAG"]["h_cite"].values
    p_hall = df_test[df_test["method"] == "PAG (Ours)"]["h_cite"].values

    # Paired t-test
    t_stat_pr, p_val_pr = stats.ttest_rel(p_prec, r_prec)
    t_stat_pv, p_val_pv = stats.ttest_rel(p_prec, v_prec)

    # Wilcoxon signed-rank test
    w_stat_pr, w_pval_pr = stats.wilcoxon(p_prec, r_prec)
    w_stat_pv, w_pval_pv = stats.wilcoxon(p_prec, v_prec)

    logging.info(f"PAG vs Standard-RAG (Precision): Paired t-stat={t_stat_pr:.4f}, p={p_val_pr:.4e} | Wilcoxon W={w_stat_pr:.4f}, p={w_pval_pr:.4e}")
    logging.info(f"PAG vs Vanilla-LLM (Precision):  Paired t-stat={t_stat_pv:.4f}, p={p_val_pv:.4e} | Wilcoxon W={w_stat_pv:.4f}, p={w_pval_pv:.4e}")

    # Summary table
    methods = ["Vanilla-LLM", "Standard-RAG", "PAG (Ours)"]
    summary = {}
    for m in methods:
        sub = df_test[df_test["method"] == m]
        summary[m] = {
            "p_claim_mean": round(float(sub["p_claim"].mean()), 4),
            "p_claim_std": round(float(sub["p_claim"].std()), 4),
            "r_cite_mean": round(float(sub["r_cite"].mean()), 4),
            "r_cite_std": round(float(sub["r_cite"].std()), 4),
            "h_cite_mean": round(float(sub["h_cite"].mean()), 4),
            "h_cite_std": round(float(sub["h_cite"].std()), 4),
            "s_ground_mean": round(float(sub["s_ground"].mean()), 4),
            "s_ground_std": round(float(sub["s_ground"].std()), 4),
            "m_valid_mean": round(float(sub["m_valid"].mean()), 4),
            "f1_mean": round(float(sub["f1"].mean()), 4),
            "total_type_I": int(sub["type_I"].sum()),
            "total_type_II": int(sub["type_II"].sum()),
            "total_type_III": int(sub["type_III"].sum()),
            "total_type_IV": int(sub["type_IV"].sum())
        }

    # Ablation summary
    ablation_summary = {}
    df_abl = pd.DataFrame(ablation_records)
    for tau in thresholds:
        sub = df_abl[df_abl["tau"] == tau]
        ablation_summary[str(tau)] = {
            "p_claim_mean": round(float(sub["p_claim"].mean()), 4),
            "r_cite_mean": round(float(sub["r_cite"].mean()), 4),
            "h_cite_mean": round(float(sub["h_cite"].mean()), 4),
            "f1_mean": round(float(sub["f1"].mean()), 4)
        }

    out_metrics = {
        "summary": summary,
        "ablation": ablation_summary,
        "statistical_tests": {
            "PAG_vs_RAG_ttest_p": float(p_val_pr),
            "PAG_vs_Vanilla_ttest_p": float(p_val_pv),
            "PAG_vs_RAG_wilcoxon_p": float(w_pval_pr),
            "PAG_vs_Vanilla_wilcoxon_p": float(w_pval_pv)
        }
    }

    summary_json_path = config["output_paths"]["summary_metrics_json"]
    with open(summary_json_path, "w") as f:
        json.dump(out_metrics, f, indent=2)
    logging.info(f"Saved aggregated metrics and test results to {summary_json_path}")
    logging.info("\nBenchmark evaluation complete!")

if __name__ == "__main__":
    run_all_experiments()
