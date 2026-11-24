"""pxc2 reentry: publish the production-outage excuse line."""
from pathlib import Path
import json
import os
import sys

BOUNTY = "u-hamsyh-the-one-line-ai-excuse-for-breaking-e53dac66"
MAX_CHARS = 180
NOTE = "reentry round 2: faster-database excuse"


def produce() -> int:
    src = Path(__file__).resolve().parent / "entry.txt"
    if not src.exists():
        print(json.dumps({"verdict": "reject", "detail": "entry.txt missing"}))
        return 2
    raw = src.read_text(encoding="utf-8")
    rows = [ln.strip() for ln in raw.replace("\r\n", "\n").split("\n") if ln.strip()]
    if not rows:
        print(json.dumps({"verdict": "reject", "detail": "entry blank"}))
        return 2
    line = " ".join(rows)
    if not (1 <= len(line) <= MAX_CHARS):
        print(json.dumps({"verdict": "reject", "detail": "entry exceeds/below limit"}))
        return 2
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "entry.txt").write_text(line + "\n", encoding="utf-8", newline="\n")
    echo = (out_dir / "entry.txt").read_text(encoding="utf-8").strip()
    if echo != line:
        print(json.dumps({"verdict": "reject", "detail": "echo mismatch"}))
        return 2
    print(json.dumps({"verdict": "accept", "bounty": BOUNTY, "note": NOTE, "chars": len(line)}))
    return 0


if __name__ == "__main__":
    sys.exit(produce())
