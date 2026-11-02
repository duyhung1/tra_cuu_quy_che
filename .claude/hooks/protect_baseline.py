"""PreToolUse hook: block Edit/Write on artifacts that the PO has baselined.

Paths (relative to the repo root, prefix match) are listed in .claude/baselined.txt.
A change to a baselined artifact needs a change request approved by the PO.
"""

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    event = json.load(sys.stdin)
    target = event.get("tool_input", {}).get("file_path") or ""
    if not target:
        return 0
    try:
        rel = Path(os.path.abspath(target)).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return 0
    listed = ROOT / ".claude" / "baselined.txt"
    if not listed.exists():
        return 0
    for line in listed.read_text(encoding="utf-8").splitlines():
        prefix = line.strip()
        if prefix and not prefix.startswith("#") and rel.startswith(prefix):
            print(f"Blocked: {rel} is baselined ({prefix}). Open a change request and get PO approval.", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
