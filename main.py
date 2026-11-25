"""Production excuse wrapper: verifies the apology, wraps it for the output slot."""
STAMP = "onebug-11251142-pxc3"
import json
import os
import shutil
from pathlib import Path

LANE = Path(__file__).resolve().parent
HEADROOM = 180
SORRY = ("Sorry I broke production - I ran the risk numbers and they were terrible, "
         "but the decimal looked so confident.")


def verify(body):
    trimmed = body.strip()
    if 1 <= len(trimmed) <= HEADROOM:
        return {"clear": True, "len": len(trimmed), "headroom": HEADROOM}
    return {"clear": False, "len": len(trimmed), "headroom": HEADROOM}


def wrap():
    origin = LANE / "entry.txt"
    report = verify(origin.read_text(encoding="utf-8"))
    slot = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if slot and report["clear"]:
        Path(slot).mkdir(parents=True, exist_ok=True)
        shutil.copyfile(origin, Path(slot) / "entry.txt")
    report["stamp"] = STAMP
    print(json.dumps(report))


if __name__ == "__main__":
    wrap()
