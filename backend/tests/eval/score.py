"""Score a reviewed eval CSV (T-008).

    python tests/eval/score.py [results/<file>.csv]   # default: latest file

Targets: positive correct ≥ 80 %, negative "not found" ≥ 90 %,
expected article cited (cited_ok) ≥ 80 %.
"""

import csv
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
TARGETS = {"positive": 0.80, "negative": 0.90}
CITATION_TARGET = 0.80


def score(rows: list[dict]) -> dict:
    result = {}
    for kind in ("positive", "negative"):
        graded = [r for r in rows if r["type"] == kind and r["correct"] in ("0", "1")]
        ungraded = sum(1 for r in rows if r["type"] == kind and r["correct"] not in ("0", "1"))
        rate = sum(r["correct"] == "1" for r in graded) / len(graded) if graded else None
        result[kind] = {"graded": len(graded), "ungraded": ungraded, "rate": rate}
    checked = [r for r in rows if r.get("cited_ok") in ("0", "1")]
    result["citation_rate"] = sum(r["cited_ok"] == "1" for r in checked) / len(checked) if checked else None
    latencies = sorted(int(r["latency_ms"]) for r in rows if r["latency_ms"])
    result["p90_latency_ms"] = (
        statistics.quantiles(latencies, n=10)[-1] if len(latencies) >= 2 else (latencies[0] if latencies else None)
    )
    return result


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else max((HERE / "results").glob("*.csv"), default=None)
    if path is None:
        print("No results file found. Run run_eval.py first.")
        return 1
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    s = score(rows)
    ok = True
    for kind, target in TARGETS.items():
        r = s[kind]
        if r["rate"] is None:
            print(f"{kind:9}: no graded rows ({r['ungraded']} ungraded)")
            ok = False
            continue
        passed = r["rate"] >= target
        ok &= passed
        print(f"{kind:9}: {r['rate']:.0%} ({r['graded']} graded, {r['ungraded']} ungraded) "
              f"target {target:.0%} → {'PASS' if passed else 'FAIL'}")
    if s["citation_rate"] is not None:
        passed = s["citation_rate"] >= CITATION_TARGET
        ok &= passed
        print(f"citation : {s['citation_rate']:.0%} target {CITATION_TARGET:.0%} → {'PASS' if passed else 'FAIL'}")
    print(f"p90 latency: {s['p90_latency_ms']} ms")
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
