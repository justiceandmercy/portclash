#!/usr/bin/env python3
"""portclash: find repeated or conflicting port numbers in a project."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from scanner import scan_directory
from reporter import build_report, render_text, render_json


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="portclash",
        description="Find repeated or conflicting port numbers in source and config files.",
    )
    parser.add_argument("path", nargs="?", default=".", help="project directory to scan")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--min-port", type=int, default=1, dest="min_port")
    parser.add_argument("--max-port", type=int, default=65535, dest="max_port")
    parser.add_argument("--strict", action="store_true", help="exit 1 when conflicts are found")
    args = parser.parse_args(argv)

    root = Path(args.path).resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")

    findings = scan_directory(root, args.min_port, args.max_port)
    report = build_report(findings)

    if args.format == "json":
        print(render_json(report), end="")
    else:
        print(render_text(report), end="")

    return 1 if args.strict and report["conflicts"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
