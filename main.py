"""Production-excuse line, reentry 0822 build.

Pathlib text pipeline: lift entry.txt from beside this script, keep
the first line that is not blank, enforce the 180 character gate,
stamp the line into the grader's output directory, re-read it, and
report one JSON state line.
"""
import json
import os
from pathlib import Path

SOURCE = Path(__file__).with_name("entry.txt")
DEST_NAME = "entry.txt"


def emit():
    lines = [s.replace("\r", "") for s in SOURCE.read_text(encoding="utf-8").split("\n")]
    try:
        body = next(x for x in lines if x.strip())
    except StopIteration:
        raise SystemExit("entry file holds no non-blank line")
    CEILING = 180  # sealed scorer limit for this bounty
    if len(body) > CEILING:
        raise SystemExit("gate: entry spans %d chars, over %d" % (len(body), CEILING))
    if len(body) < 1:
        raise SystemExit("gate: entry is empty")
    yard = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "output")
    yard.mkdir(parents=True, exist_ok=True)
    leaf = yard / DEST_NAME
    leaf.write_text(body, encoding="utf-8", newline="")
    if leaf.read_text(encoding="utf-8") != body:
        raise SystemExit("stored copy disagrees with source line")
    print(json.dumps({"state": "ok", "c": len(body)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(emit())
