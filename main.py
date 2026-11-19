#!/usr/bin/env python3
"""Entry point for the make.fun news-image-20261119 bounty.

The finished picture, entry.png, is committed next to this file.
Running main.py copies it to $MAKEFUN_OUTPUT_DIR/entry.png (or
/output/entry.png when the variable is unset). Standard library
only, no network, and the output is byte-for-byte entry.png on
every run.
"""

import os
import shutil
import sys


def main():
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    dest_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(dest_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(dest_dir, "entry.png"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
