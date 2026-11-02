"""Layering: api → modules → ports ← adapters. Only app/core/wiring.py picks adapters."""

import ast
from pathlib import Path

APP = Path(__file__).resolve().parents[2] / "app"
SDKS = ("fastapi", "anthropic", "boto3", "botocore", "httpx", "pymupdf")


def _imports(path: Path) -> list[str]:
    names: list[str] = []
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            names += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.append(node.module)
    return names


def _offenders(folders: tuple[str, ...], banned: tuple[str, ...]) -> list[str]:
    return [
        f"{p.relative_to(APP)}: {n}"
        for folder in folders
        for p in (APP / folder).rglob("*.py")
        for n in _imports(p)
        if any(n == b or n.startswith(f"{b}.") for b in banned)
    ]


def test_only_wiring_imports_adapters():
    assert _offenders(("api", "modules", "worker", "domain", "ports"), ("app.adapters",)) == []


def test_modules_domain_and_ports_do_not_import_sdks():
    assert _offenders(("modules", "domain", "ports"), SDKS) == []


def test_domain_imports_nothing_from_app():
    assert _offenders(("domain",), ("app.core", "app.models", "app.modules", "app.ports", "app.worker")) == []
