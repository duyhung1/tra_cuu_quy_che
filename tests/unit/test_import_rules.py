"""TASK-001: only app/wiring.py imports adapters; domain/services stay framework-free (SAD §2.3)."""

import ast
from pathlib import Path

APP = Path(__file__).resolve().parents[2] / "app"


def _imports(path: Path) -> list[str]:
    out = []
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            out += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            out.append(node.module)
    return out


def _offenders(folders, banned):
    return [f"{p.relative_to(APP)}: {n}" for f in folders for p in (APP / f).rglob("*.py")
            for n in _imports(p) if any(n == b or n.startswith(b + ".") for b in banned)]


def test_only_wiring_imports_adapters():
    assert _offenders(("domain", "services"), ("app.adapters",)) == []
    assert not any(n.startswith("app.adapters") for n in _imports(APP / "main.py"))


def test_domain_and_services_do_not_import_frameworks():
    assert _offenders(("domain", "services"), ("fastapi", "pymupdf", "sqlite3", "starlette")) == []
