#!/usr/bin/env python3

import argparse
from pathlib import Path

parser = argparse.ArgumentParser(
    prog="rename_lowercase.py",
    description="Recursively rename all files and directories to lowercase"
)
parser.add_argument(
    "directory",
    help="Directory to start renaming files from"
)

args = parser.parse_args()

root = Path(args.directory)

for p in root.glob("**/*"):
    if p.parent != root:
        p = Path(str(p.parent).lower()) / p.name

    p.rename(p.parent / str(p.name).lower())
