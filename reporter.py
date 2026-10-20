"""Build and render portclash reports."""

from __future__ import annotations

import json
from collections import defaultdict


def build_report(findings):
    by_port = defaultdict(list)
    for finding in findings:
        by_port[finding["port"]].append(finding)

    conflicts = []
    for port, items in sorted(by_port.items()):
        if len(items) > 1:
            conflicts.append({"port": port, "occurrences": items})

    return {
        "findings": findings,
        "total_occurrences": len(findings),
        "unique_ports": len(by_port),
        "conflicts": conflicts,
        "conflict_count": len(conflicts),
    }


def render_text(report):
    lines = [
        f"portclash: {report['total_occurrences']} port reference(s), "
        f"{report['unique_ports']} unique port(s)",
        "",
    ]
    if not report["conflicts"]:
        lines.append("No repeated ports found.")
        return "\n".join(lines) + "\n"

    lines.append(f"Repeated ports ({report['conflict_count']}):")
    for conflict in report["conflicts"]:
        lines.append(f"  port {conflict['port']}:")
        for item in conflict["occurrences"]:
            lines.append(f"    {item['file']}:{item['line']}  {item['text']}")
    return "\n".join(lines) + "\n"


def render_json(report):
    return json.dumps(report, indent=2) + "\n"
