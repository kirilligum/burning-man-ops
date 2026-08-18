#!/usr/bin/env python3
"""Validate canonical Treble Makers task-management XML."""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TASKS = DATA / "tasks"
ITEMS = DATA / "items"

ITEM_FOLDERS = {
    "🌐": ITEMS / "public area",
    "🍷": ITEMS / "bar-cheese",
    "🔥": ITEMS / "propane area",
    "🏕️": ITEMS / "common area",
    "🍳": ITEMS / "kitchen",
    "🔧": ITEMS / "private infrastructure",
    "📦": ITEMS,
}

AREAS = {
    "Public area",
    "Bar/Cheese",
    "Propane area",
    "Common area",
    "Kitchen",
    "Private infrastructure",
}

CHECKLIST_TYPES = {
    "Morning Dominatrix",
    "Evening Dominatrix",
    "Morning",
    "Infra Lead",
    "Shower",
    "Liaison",
    "Pre-event",
    "Bar",
    "Afternoon",
    "Cheese",
    "Post-event",
    "Flame Effects",
    "Build",
    "Strike",
}

REFERENCE = re.compile(
    r"(?P<icon>📋|🌐|🍷|🔥|🏕️|🍳|🔧|📦)\s+"
    r"(?P<name>[A-Za-z0-9][A-Za-z0-9_-]*)"
)
DECISION_HEADING = re.compile(r"^###\s+(D-\d+)\s+—\s+.*$", re.MULTILINE)
DECISION_STATUS = re.compile(r"^- \*\*Status:\*\*\s+(.+)$", re.MULTILINE)


class Validation:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.parsed: dict[Path, ET.Element] = {}

    def error(self, path: Path, message: str) -> None:
        self.errors.append(f"{path.relative_to(ROOT)}: {message}")

    def parse(self, path: Path) -> ET.Element | None:
        if path in self.parsed:
            return self.parsed[path]
        try:
            root = ET.parse(path).getroot()
        except (OSError, ET.ParseError) as exc:
            self.error(path, f"invalid XML: {exc}")
            return None
        self.parsed[path] = root
        return root

    def require_text(self, path: Path, parent: ET.Element, field: str) -> str:
        value = (parent.findtext(field) or "").strip()
        if not value:
            self.error(path, f"missing {field}")
        return value


def normalized_status(value: str) -> str:
    value = value.strip()
    if value.startswith("Superseded"):
        return "Superseded"
    return value


def decision_records(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    headings = list(DECISION_HEADING.finditer(text))
    records: dict[str, str] = {}
    for index, heading in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        block = text[heading.end() : end]
        status = DECISION_STATUS.search(block)
        if status:
            records[heading.group(1)] = normalized_status(status.group(1))
    return records


def validate_item(path: Path, root: ET.Element, check: Validation) -> None:
    if root.tag != "item":
        check.error(path, f"expected <item>, found <{root.tag}>")
        return
    name = check.require_text(path, root, "name")
    if name and path.stem != name:
        check.error(path, f"filename must be {name}.xml")
    check.require_text(path, root, "readyForNextPerson")
    check.require_text(path, root, "responsible")
    for problem in root.findall("./commonProblems/problem"):
        check.require_text(path, problem, "condition")
        check.require_text(path, problem, "response")


def validate_task(
    path: Path,
    root: ET.Element,
    check: Validation,
    decisions: dict[str, str],
) -> None:
    if root.tag != "task":
        check.error(path, f"expected <task>, found <{root.tag}>")
        return

    name = check.require_text(path, root, "name")
    if name and path.stem != name:
        check.error(path, f"filename must be {name}.xml")

    area = check.require_text(path, root, "area")
    if area and area not in AREAS:
        check.error(path, f"unknown area {area!r}")
    check.require_text(path, root, "when")

    checklist_types = [
        (element.text or "").strip()
        for element in root.findall("./checklist_types/checklist_type")
    ]
    if not checklist_types:
        check.error(path, "at least one checklist_type is required")
    for checklist_type in checklist_types:
        if checklist_type not in CHECKLIST_TYPES:
            check.error(path, f"unknown checklist_type {checklist_type!r}")
    if len(checklist_types) != len(set(checklist_types)):
        check.error(path, "duplicate checklist_type")

    steps = root.findall("./steps/step")
    if not steps:
        check.error(path, "at least one step is required")
    numbers: list[int] = []
    for step in steps:
        raw_number = (step.get("number") or "").strip()
        try:
            numbers.append(int(raw_number))
        except ValueError:
            check.error(path, f"invalid step number {raw_number!r}")
        check.require_text(path, step, "action")
    if numbers and numbers != list(range(1, len(numbers) + 1)):
        check.error(path, f"step numbers must be consecutive from 1; found {numbers}")

    criteria = [
        (element.text or "").strip()
        for element in root.findall("./passWhen/criterion")
    ]
    if not criteria or any(not criterion for criterion in criteria):
        check.error(path, "at least one non-empty passWhen criterion is required")

    reference_icons = tuple(ITEM_FOLDERS) + ("📋",)
    for resource in root.findall("./resources/resource"):
        value = (resource.text or "").strip()
        if not value:
            check.error(path, "empty resource")
            continue
        if value.startswith(reference_icons) and not REFERENCE.fullmatch(value):
            check.error(path, f"malformed resource reference {value!r}")

    for decision in root.findall("./decisions/decision"):
        record = (decision.findtext("record") or "").strip()
        status = (decision.findtext("status") or "").strip()
        if record:
            allowed = {"record", "status"}
            extras = {child.tag for child in decision} - allowed
            if extras:
                check.error(
                    path,
                    f"decision reference {record} duplicates fields: {sorted(extras)}",
                )
            if not status:
                check.error(path, f"decision reference {record} is missing status")
            expected = decisions.get(record)
            if expected is None:
                check.error(path, f"decision reference {record} does not exist")
            elif normalized_status(status) != expected:
                check.error(
                    path,
                    f"decision reference {record} has status {status!r}; expected {expected!r}",
                )
            continue

        for field in ("date", "status", "text", "effect"):
            check.require_text(path, decision, field)
        if status not in {"Accepted", "Superseded", "Open"}:
            check.error(path, f"unknown task decision status {status!r}")


def validate_references(check: Validation) -> None:
    for path, root in check.parsed.items():
        if root.tag not in {"task", "item", "globalInstructions"}:
            continue
        text = " ".join(part.strip() for part in root.itertext() if part.strip())
        for match in REFERENCE.finditer(text):
            icon = match.group("icon")
            name = match.group("name")
            if icon == "📋":
                target = TASKS / f"{name}.xml"
            else:
                target = ITEM_FOLDERS[icon] / f"{name}.xml"
            if not target.is_file():
                check.error(path, f"reference {icon} {name} does not resolve")


def main() -> int:
    check = Validation()
    xml_paths = sorted(DATA.rglob("*.xml"))
    if not xml_paths:
        print("error: no XML files found", file=sys.stderr)
        return 1

    for path in xml_paths:
        check.parse(path)

    decisions = {
        **decision_records(ROOT / "HISTORICAL_DECISIONS.md"),
        **decision_records(ROOT / "DECISIONS.md"),
    }

    task_paths = sorted(TASKS.glob("*.xml"))
    item_paths = sorted(ITEMS.rglob("*.xml"))
    for path in task_paths:
        root = check.parsed.get(path)
        if root is not None:
            validate_task(path, root, check, decisions)
    for path in item_paths:
        root = check.parsed.get(path)
        if root is not None:
            validate_item(path, root, check)

    global_path = DATA / "global-instructions.xml"
    global_root = check.parsed.get(global_path)
    if global_root is None:
        check.error(global_path, "missing global-instructions.xml")
    else:
        instructions = [
            " ".join((element.text or "").split())
            for element in global_root.findall("./instruction")
        ]
        if not instructions or any(not instruction for instruction in instructions):
            check.error(global_path, "all global instructions must be non-empty")
        if len(instructions) != len(set(instructions)):
            check.error(global_path, "duplicate global instruction")

    validate_references(check)

    if check.errors:
        unique_errors = sorted(set(check.errors))
        for error in unique_errors:
            print(f"ERROR {error}", file=sys.stderr)
        print(
            f"Validation failed with {len(unique_errors)} error(s).",
            file=sys.stderr,
        )
        return 1

    print(
        f"Validated {len(task_paths)} task, {len(item_paths)} items, "
        f"and {len(xml_paths)} XML files."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
