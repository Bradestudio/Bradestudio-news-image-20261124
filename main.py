"""Entry point: draw entry.png into the output directory.

Reads $MAKEFUN_OUTPUT_DIR, else the first argument, else ./output.
Delegates all drawing to gen_image.py; no network, no clock, no
randomness, so repeated runs write identical bytes.
"""

import os
import sys

from gen_image import build


def main():
    target = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not target and len(sys.argv) > 1:
        target = sys.argv[1]
    if not target:
        target = "./output"
    os.makedirs(target, exist_ok=True)
    build(os.path.join(target, "entry.png"))


if __name__ == "__main__":
    main()
