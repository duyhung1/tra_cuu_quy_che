"""Run the golden set in-process and score it automatically (TASK-011, PRD RC-2).

    .venv/Scripts/python tests/golden/run_golden.py [--out docs/07-verification/evidence/<run-id>]

Uses a fresh temporary database, uploads the sample documents, asks every question and writes
golden-results.json + golden-summary.md. TCQC_TODAY is fixed to the golden set's "today".
"""

import argparse
import json
import os
import statistics
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
HERE = Path(__file__).parent


def grade(item: dict, body: dict) -> tuple[bool, list[str]]:
    why = []
    if "answer" not in body:
        return False, [f"error {body.get('code')}"]
    if item["type"] == "negative":
        ok = body["found"] is False and body["answer"].startswith("Không tìm thấy") and not body["sources"]
        return ok, [] if ok else ["expected not-found"]
    if not body["found"]:
        return False, ["answered not-found"]
    first = body["sources"][0] if body["sources"] else {}
    if first.get("doc_number") != item["expect_doc"] or first.get("article") != item["expect_article"]:
        why.append(f"[1] = {first.get('doc_number')} {first.get('article')}")
    for s in item.get("expect_contains", []):
        if s not in body["answer"]:
            why.append(f"missing «{s}»")
    for s in item.get("expect_not_contains", []):
        if s in body["answer"]:
            why.append(f"contains «{s}»")
    return not why, why


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    golden = json.loads((HERE / "golden.json").read_text(encoding="utf-8"))
    tmp = tempfile.mkdtemp(prefix="tcqc-golden-")
    os.environ["TCQC_DB"] = str(Path(tmp) / "golden.db")
    os.environ["TCQC_LOG"] = str(Path(tmp) / "app.log")
    os.environ["TCQC_TODAY"] = golden["today"]

    from fastapi.testclient import TestClient

    from app.config import get_settings
    from app.main import create_app
    from tests.fixtures.make_pdfs import HERE as PDFS
    from tests.fixtures.make_pdfs import write_all

    write_all()
    client = TestClient(create_app(get_settings()), raise_server_exceptions=False)
    files = [("files", (p.name, p.read_bytes(), "application/pdf")) for p in sorted((PDFS / "sample").glob("*.pdf"))]
    up = client.post("/api/documents", files=files).json()

    rows = []
    for item in golden["items"]:
        r = client.post("/api/ask", json={"question": item["question"]})
        body = r.json()
        ok, why = grade(item, body)
        rows.append({"id": item["id"], "type": item["type"], "faq": item.get("faq", False), "question": item["question"],
                     "http": r.status_code, "found": body.get("found"), "latency_ms": body.get("latency_ms"),
                     "first_source": (body.get("sources") or [{}])[0], "answer": body.get("answer"),
                     "correct": ok, "why": why})

    def rate(sel):
        xs = [r for r in rows if sel(r)]
        return (sum(r["correct"] for r in xs), len(xs))

    pos = rate(lambda r: r["type"] != "negative")
    conf = rate(lambda r: r["type"] == "conflict")
    fut = rate(lambda r: r["type"] == "future")
    neg = rate(lambda r: r["type"] == "negative")
    faq = rate(lambda r: r["faq"])
    lat = sorted(r["latency_ms"] for r in rows if r["latency_ms"] is not None)
    p90 = statistics.quantiles(lat, n=10)[-1] if len(lat) >= 2 else lat[0]
    log_text = Path(os.environ["TCQC_LOG"]).read_text(encoding="utf-8")
    db_bytes = Path(os.environ["TCQC_DB"]).read_bytes()
    leaks = [it["question"] for it in golden["items"]
             if it["question"] in log_text or it["question"].encode("utf-8") in db_bytes]
    summary = {
        "today": golden["today"], "upload": up["items"],
        "MET-002 positive (incl. conflict/future)": pos, "MET-003 conflict": conf, "future (AC-013/015)": fut,
        "MET-004 negative": neg, "MET-007 faq": faq, "MET-006 p90_latency_ms": p90, "NFR-003 leaks": leaks,
        "threshold": os.environ.get("TCQC_THRESHOLD", "2.0"), "min_coverage": os.environ.get("TCQC_MIN_COVERAGE", "0.5"),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    for r in rows:
        verdict = "PASS" if r["correct"] else "FAIL"
        print(f"{r['id']:5} {r['type']:9} {verdict} {r['latency_ms'] or 0:>4} ms  {'; '.join(r['why'])}")
    if args.out:
        out = Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
        (out / "golden-results.json").write_text(json.dumps({"summary": summary, "rows": rows}, ensure_ascii=False, indent=1),
                                                 encoding="utf-8")
        (out / "app.log").write_text(log_text, encoding="utf-8")
    ok = pos[0] / pos[1] >= 0.8 and conf[0] == conf[1] and neg[0] / neg[1] >= 0.9 and faq[0] / faq[1] >= 0.8
    ok = ok and p90 <= 30000 and not leaks
    print("RC-2:", "PASS" if ok else "FAIL")
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
