"""Ship the prod-excuse line for the hamsyh breaking-production bounty.

Gate: one line, 1..180 chars, not blank. Exit non-zero when invalid.
"""
from pathlib import Path
import os
import sys

LIMIT = 180
REPO = Path(__file__).resolve().parent
LINE_FILE = REPO / "entry.txt"


def measure(raw: str) -> tuple[int, bool]:
    body = raw.strip()
    return len(body), bool(body) and len(body) <= LIMIT


def stage() -> dict:
    text = LINE_FILE.read_text(encoding="utf-8").strip()
    size, ok = measure(text)
    if not ok:
        raise SystemExit(f"entry rejected by gate: {size} chars")
    target = os.environ.get("MAKEFUN_OUTPUT_DIR") or str(REPO / "output")
    Path(target).mkdir(parents=True, exist_ok=True)
    dest = Path(target) / "entry.txt"
    dest.write_text(text + "\n", encoding="utf-8")
    return {"artifact": str(dest), "chars": size, "subject": "production outage excuse"}


if __name__ == "__main__":
    print(stage())
