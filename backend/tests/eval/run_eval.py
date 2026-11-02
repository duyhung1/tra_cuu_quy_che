"""Run the golden set against a running API (T-008).

    python tests/eval/run_eval.py --base-url http://localhost:8000

Writes results/<timestamp>.csv. The `correct` column of positive questions is
filled in by a human reviewer; then run score.py.
Negative questions are scored automatically: correct when the answer says the
information was not found. For positive questions with `expected_article`, the
`cited_ok` column says whether that article is among the returned sources.
"""

import argparse
import csv
import datetime as dt
import sys
from pathlib import Path

import httpx
import yaml

HERE = Path(__file__).parent
NOT_FOUND_MARKER = "không tìm thấy"


def is_not_found(answer: str) -> bool:
    return NOT_FOUND_MARKER in answer.lower()


def cited_ok(item: dict, sources: list[dict]) -> str:
    expected = item.get("expected_article")
    if not expected:
        return ""
    return "1" if any(s.get("article") == expected for s in sources) else "0"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://localhost:8000")
    parser.add_argument("--golden", default=str(HERE / "golden.yaml"))
    args = parser.parse_args()

    items = yaml.safe_load(Path(args.golden).read_text(encoding="utf-8"))
    out_dir = HERE / "results"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / f"{dt.datetime.now():%Y%m%d-%H%M%S}.csv"

    rows = []
    with httpx.Client(base_url=args.base_url, timeout=120) as client:
        for item in items:
            resp = client.post("/api/v1/ask", json={"question": item["question"]})
            if resp.status_code == 200:
                body = resp.json()
                answer, latency, sources = body["answer"], body["latency_ms"], body.get("sources", [])
            else:
                answer, latency, sources = f"ERROR {resp.status_code}: {resp.text[:200]}", "", []
            correct = ""
            if item["type"] == "negative":
                correct = "1" if is_not_found(answer) else "0"
            rows.append({
                "id": item["id"], "type": item["type"], "question": item["question"],
                "expected_answer": item.get("expected_answer", ""), "answer": answer,
                "latency_ms": latency, "cited_ok": cited_ok(item, sources), "correct": correct,
            })
            print(f"{item['id']:8} {item['type']:9} {latency!s:>6} ms  {answer[:80]!r}")

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nSaved {out_path}. Fill the 'correct' column (0/1) for positive rows, then run score.py.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
