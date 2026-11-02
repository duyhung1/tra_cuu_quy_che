import importlib.util
from pathlib import Path


def load(name):
    path = Path(__file__).parents[1] / "eval" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_score_rates_and_ungraded():
    score = load("score").score
    rows = [
        {"type": "positive", "correct": "1", "latency_ms": "1000"},
        {"type": "positive", "correct": "0", "latency_ms": "2000"},
        {"type": "positive", "correct": "", "latency_ms": "3000"},
        {"type": "negative", "correct": "1", "latency_ms": "4000"},
    ]
    s = score(rows)
    assert s["positive"] == {"graded": 2, "ungraded": 1, "rate": 0.5}
    assert s["negative"]["rate"] == 1.0
    assert s["p90_latency_ms"] is not None


def test_not_found_detection():
    is_nf = load("run_eval").is_not_found
    assert is_nf("Không tìm thấy thông tin này trong tài liệu.")
    assert not is_nf("Tạm ứng 30%.")
