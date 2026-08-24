import json
import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.retrieval import search
from app.services.reference_expand import get_references
from app.services.metadata import get_metadata

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
EVAL_FILE = os.environ.get("EVAL_DATA_FILE", os.path.join(BASE_DIR, "data", "sample_procurement_tenders_eval.json"))

def evaluate():
    if not os.path.exists(EVAL_FILE):
        print(f"Error: Eval file not found at {EVAL_FILE}")
        return

    with open(EVAL_FILE, "r") as f:
        tenders = json.load(f)

    print(f"\n{'='*75}")
    print(f"📊 BIS STANDARDS RECOMMENDATION ENGINE — BENCHMARK EVALUATION HARNESS")
    print(f"{'='*75}")
    print(f"Benchmark Testset: {len(tenders)} Real-world Multi-Domain Public Tenders\n")

    top1_hits = 0
    top3_hits = 0
    total_ground_truth_primaries = 0
    reciprocal_ranks = []
    qco_correct_count = 0
    latencies = []

    for i, tender in enumerate(tenders, 1):
        tender_id = tender.get("tender_id")
        portal = tender.get("portal")
        title = tender.get("title")
        input_text = tender.get("input_text")
        gt = tender.get("ground_truth", {})
        gt_primaries = gt.get("primary_standards", [])
        gt_qco = gt.get("mandatory_qco", False)

        total_ground_truth_primaries += len(gt_primaries)

        start_time = time.time()
        results = search(input_text, top_k=5)
        elapsed_ms = (time.time() - start_time) * 1000
        latencies.append(elapsed_ms)

        retrieved_ids = [r["standard_id"] for r in results]

        # Calculate rank of first ground truth match
        first_match_rank = None
        for rank, rid in enumerate(retrieved_ids, 1):
            if any(gt_p.split(":")[0].strip() == rid.split(":")[0].strip() for gt_p in gt_primaries):
                if first_match_rank is None:
                    first_match_rank = rank

        # Top-1 Check
        if first_match_rank == 1:
            top1_hits += 1
            reciprocal_ranks.append(1.0)
        elif first_match_rank:
            reciprocal_ranks.append(1.0 / first_match_rank)
        else:
            reciprocal_ranks.append(0.0)

        # Top-3 Recall Check (how many ground truth primaries retrieved in top 3)
        top3_retrieved = retrieved_ids[:3]
        matches_in_top3 = sum(
            1 for gt_p in gt_primaries
            if any(gt_p.split(":")[0].strip() == rid.split(":")[0].strip() for rid in top3_retrieved)
        )
        top3_hits += matches_in_top3

        # Check QCO correctness on top 1 recommendation
        top1_qco_flag = False
        if results:
            meta = get_metadata(results[0]["standard_id"])
            if meta:
                top1_qco_flag = meta.get("is_mandatory_qco", False)
        if top1_qco_flag == gt_qco:
            qco_correct_count += 1

        print(f"[{i}/{len(tenders)}] Tender Ref: {tender_id} ({portal})")
        print(f"   Title: {title[:70]}...")
        print(f"   Ground Truth Primaries: {gt_primaries}")
        retrieved_summary = [f"{r['standard_id']} ({r['similarity']:.1%})" for r in results[:3]]
        print(f"   Top-3 Retrieved:        {retrieved_summary}")
        print(f"   First Match Rank:       #{first_match_rank} (Latency: {elapsed_ms:.1f}ms)")
        print(f"   QCO Mandatory Check:    {'✓ MATCH (' + str(gt_qco) + ')' if top1_qco_flag == gt_qco else '✗ MISMATCH'}\n")

    mrr = sum(reciprocal_ranks) / len(reciprocal_ranks) if reciprocal_ranks else 0.0
    top1_acc = (top1_hits / len(tenders)) * 100
    top3_recall = (top3_hits / total_ground_truth_primaries) * 100
    qco_acc = (qco_correct_count / len(tenders)) * 100
    avg_latency = sum(latencies) / len(latencies) if latencies else 0.0

    print(f"{'='*75}")
    print(f"🎯 BENCHMARK RESULTS SUMMARY")
    print(f"{'='*75}")
    print(f"• Total Tenders Evaluated:     {len(tenders)}")
    print(f"• Top-1 Accuracy:              {top1_acc:.1f}% ({top1_hits}/{len(tenders)})")
    print(f"• Top-3 Recall (Ground Truth): {top3_recall:.1f}% ({top3_hits}/{total_ground_truth_primaries})")
    print(f"• MRR (Mean Reciprocal Rank):  {mrr:.3f}")
    print(f"• QCO Mandatory Accuracy:      {qco_acc:.1f}%")
    print(f"• Avg Retrieval Latency:       {avg_latency:.1f} ms")
    print(f"{'='*75}\n")

if __name__ == "__main__":
    evaluate()
