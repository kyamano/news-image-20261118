"""Entry program for make.fun news-image-20261118.

Writes the competition image to the output directory. The image
(entry.png, beside this file) is a one-page newspaper infographic
summing up the world news of Wednesday 18 November 2026; it was
drawn by generate.py in this repository. This program only copies
it, byte for byte, so the two grader runs always agree.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
/output:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
MAX_BYTES = 1_048_576  # the gate: at most 1 MiB
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main() -> None:
    data = SOURCE.read_bytes()
    if len(data) > MAX_BYTES:
        raise SystemExit(f"entry.png is {len(data)} bytes, over the 1 MiB gate")
    if not data.startswith(PNG_MAGIC):
        raise SystemExit("entry.png is not a PNG file")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(data)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    print(f"wrote {target} ({len(data)} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
