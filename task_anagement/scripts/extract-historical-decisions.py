#!/usr/bin/env python3
"""Print superseded global decisions linked from a task XML file."""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


HEADING = re.compile(r"^###\s+(D-\d+)\s+—\s+.*$", re.MULTILINE)


def linked_superseded_records(task_path: Path) -> list[str]:
    root = ET.parse(task_path).getroot()
    records: list[str] = []
    for decision in root.findall("./decisions/decision"):
        status = (decision.findtext("status") or "").strip().lower()
        if status != "superseded":
            continue
        for record in decision.findall("record"):
            value = (record.text or "").strip()
            if value and value not in records:
                records.append(value)
    return records


def historical_records(history_path: Path) -> dict[str, str]:
    text = history_path.read_text(encoding="utf-8")
    matches = list(HEADING.finditer(text))
    records: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        records[match.group(1)] = text[match.start() : end].strip()
    return records


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print historical decisions linked from a task XML file."
    )
    parser.add_argument("task_xml", type=Path)
    parser.add_argument(
        "--history",
        type=Path,
        help="Historical decision file; defaults to task_anagement/HISTORICAL_DECISIONS.md.",
    )
    args = parser.parse_args()

    history_path = args.history or Path(__file__).resolve().parents[1] / "HISTORICAL_DECISIONS.md"
    try:
        record_ids = linked_superseded_records(args.task_xml)
        records = historical_records(history_path)
    except (OSError, ET.ParseError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    if not record_ids:
        print("No linked superseded decisions found.")
        return 0

    missing = [record_id for record_id in record_ids if record_id not in records]
    for index, record_id in enumerate(record_ids):
        if record_id in records:
            if index:
                print()
            print(records[record_id])

    if missing:
        print(
            "error: missing historical decision records: " + ", ".join(missing),
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
