"""pex6: eleven-universe excuse relay. Read, verify, forward, confess."""
import json
import os
import sys
from pathlib import Path

ROOF = 180


class RelayError(Exception):
    pass


def relay(src: Path, drop: Path) -> dict:
    body = src.read_text(encoding="utf-8").strip()
    if len(body) == 0:
        raise RelayError("empty line")
    if len(body) > ROOF:
        raise RelayError(f"line is {len(body)} chars, roof is {ROOF}")
    if body.isspace():
        raise RelayError("whitespace only")
    drop.mkdir(parents=True, exist_ok=True)
    (drop / "entry.txt").write_bytes(body.encode("utf-8"))
    return {"chars": len(body), "roof": ROOF, "relayed": True}


def main():
    try:
        drop = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
        info = relay(Path(__file__).resolve().parent / "entry.txt", drop)
        state = 0
    except RelayError as boom:
        info = {"relayed": False, "fault": str(boom)}
        state = 1
    info["station"] = "pex6-relay-r11251422"
    print("VERDICT", json.dumps(info))
    return state


if __name__ == "__main__":
    sys.exit(main())
