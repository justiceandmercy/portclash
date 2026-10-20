"""Scan source and config files for port assignments."""

from __future__ import annotations

import os
import re
from pathlib import Path

IGNORED_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "build",
    ".tox",
}

TEXT_SUFFIXES = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".json", ".yaml", ".yml",
    ".toml", ".ini", ".cfg", ".env", ".conf", ".sh", ".go", ".rb",
    ".java", ".properties",
}

PORT_PATTERNS = [
    re.compile(r"\bport\b\s*[:=]\s*[\"']?(\d{2,5})[\"']?", re.IGNORECASE),
    re.compile(r"\blisten\s*\(\s*(\d{2,5})\s*\)", re.IGNORECASE),
    re.compile(r":(\d{2,5})\b"),
]


def _is_port(value: int, minimum: int = 1, maximum: int = 65535) -> bool:
    return minimum <= value <= maximum


def scan_line(line: str, minimum: int = 1, maximum: int = 65535):
    results = []
    seen = set()
    for pattern in PORT_PATTERNS:
        for match in pattern.finditer(line):
            value = int(match.group(1))
            if not _is_port(value, minimum, maximum):
                continue
            if value in seen:
                continue
            seen.add(value)
            results.append(value)
    return results


def scan_file(path: Path, minimum: int = 1, maximum: int = 65535):
    findings = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return findings
    for number, line in enumerate(text.splitlines(), 1):
        for port in scan_line(line, minimum, maximum):
            findings.append({
                "file": str(path),
                "line": number,
                "port": port,
                "text": line.strip(),
            })
    return findings


def scan_directory(root: Path, minimum: int = 1, maximum: int = 65535):
    findings = []
    root = Path(root)
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in IGNORED_DIRS and not d.startswith("."))
        for filename in sorted(filenames):
            path = Path(dirpath) / filename
            if filename.startswith(".env"):
                # env files are useful for port config; allow them
                pass
            if path.suffix.lower() not in TEXT_SUFFIXES and filename not in {".env", "Dockerfile", "Makefile"}:
                continue
            findings.extend(scan_file(path, minimum, maximum))
    return findings
