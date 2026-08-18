#!/usr/bin/env python3
"""Render the concise Morning print checklist from canonical task XML."""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from render_helpers import humanize_references, item_for_reference, text


ROOT = Path(__file__).resolve().parents[1]
CHECKLIST_TYPE = "Morning"
TASKS = (
    ROOT / "data" / "tasks" / "Clean_communal_kitchen_tables.xml",
)
DEFAULT_OUTPUT = ROOT / "morning-checklist.md"


def humanize(value: str) -> str:
    return humanize_references(value, keep_icons=False)


def render_item(reference: str, item: ET.Element, task_name: str) -> list[str]:
    lines = [f"#### {humanize(reference)}"]
    scalar_fields = (
        ("Description", "description"),
        ("Location", "location"),
        ("Ready before use", "readyBeforeUse"),
        ("Ready for next person", "readyForNextPerson"),
        ("If not ready", "ifNotReady"),
        ("Who is responsible", "responsible"),
    )
    for label, path in scalar_fields:
        value = text(item.find(path))
        if not value:
            continue
        if path == "ifNotReady" and f"📋 {task_name}" in value:
            continue
        if path == "responsible" and value == "Dominatrix":
            continue
        lines.append(f"**{label}:** {humanize(value)}")

    problems = item.findall("./commonProblems/problem")
    rendered_problems = [
        (text(problem.find("condition")), text(problem.find("response")))
        for problem in problems
    ]
    rendered_problems = [
        (condition, response)
        for condition, response in rendered_problems
        if condition or response
    ]
    if rendered_problems:
        lines.append("**Common problems:**")
        for condition, response in rendered_problems:
            if condition and response:
                lines.append(
                    f"- **IF** {humanize(condition).rstrip('.')} "
                    f"**THEN** {humanize(response)}"
                )
            elif condition:
                lines.append(f"- **IF** {humanize(condition)}")
            else:
                lines.append(f"- {humanize(response)}")
    return lines


def render_task(task_path: Path) -> list[str]:
    task = ET.parse(task_path).getroot()
    task_name = text(task.find("name"))
    checklist_types = [
        text(element)
        for element in task.findall("./checklist_types/checklist_type")
        if text(element)
    ]
    if CHECKLIST_TYPE not in checklist_types:
        raise ValueError(f"{task_name} is not assigned to {CHECKLIST_TYPE}")

    lines = [f"## {task_name.replace('_', ' ')}"]

    scalar_fields = (
        ("Area", "area"),
        ("Why", "why"),
        ("When", "when"),
        ("Time", "time"),
    )
    for label, path in scalar_fields:
        value = text(task.find(path))
        if value:
            lines.append(f"**{label}:** {humanize(value)}")

    resources = [
        text(element)
        for element in task.findall("./resources/resource")
        if text(element)
    ]
    if resources:
        lines.append("### What you need")
        lines.extend(f"- {humanize(resource)}" for resource in resources)

    steps = task.findall("./steps/step")
    if steps:
        lines.append("### Steps")
        for step in steps:
            number = step.get("number", "")
            action = text(step.find("action"))
            if action:
                lines.append(f"{number}. {humanize(action)}")
            expected = text(step.find("expectedResult"))
            if expected:
                lines.append(f"   **EXPECTED:** {humanize(expected)}")
            branch = text(step.find("ifThen"))
            if branch:
                lines.append(f"   **IF/THEN:** {humanize(branch)}")

    criteria = [
        text(element)
        for element in task.findall("./passWhen/criterion")
        if text(element)
    ]
    if criteria:
        lines.append("### PASS when")
        lines.extend(f"- {humanize(criterion)}" for criterion in criteria)

    problems = task.findall("./commonProblems/problem")
    rendered_problems = [
        (text(problem.find("condition")), text(problem.find("response")))
        for problem in problems
    ]
    rendered_problems = [
        (condition, response)
        for condition, response in rendered_problems
        if condition or response
    ]
    if rendered_problems:
        lines.append("### Common problems")
        for condition, response in rendered_problems:
            if condition:
                lines.append(f"- **IF:** {humanize(condition)}")
            if response:
                lines.append(f"  **THEN:** {humanize(response)}")

    expert = text(task.find("expert"))
    if expert:
        lines.extend(("### Who to ask", humanize(expert)))

    lines.append("### Finish")
    global_root = ET.parse(ROOT / "data" / "global-instructions.xml").getroot()
    lines.extend(
        f"- {humanize(text(instruction))}"
        for instruction in global_root.findall("./instruction")
        if text(instruction)
    )

    item_lines = ["### Items"]
    for reference in resources:
        item = item_for_reference(reference)
        if item is not None:
            item_lines.extend(render_item(reference, item, task_name))
    if len(item_lines) > 1:
        lines.extend(item_lines)

    return lines


def render() -> str:
    lines = [
        "<!-- Generated from canonical task XML. Do not edit this file directly. -->",
        f"# {CHECKLIST_TYPE} checklist",
    ]
    for task_path in TASKS:
        lines.extend(render_task(task_path))
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail instead of writing when the generated output is stale.",
    )
    args = parser.parse_args()

    try:
        rendered = render()
    except (OSError, ET.ParseError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.check:
        try:
            current = DEFAULT_OUTPUT.read_text(encoding="utf-8")
        except OSError:
            current = ""
        if current != rendered:
            print(f"error: rendered checklist is stale: {DEFAULT_OUTPUT}", file=sys.stderr)
            return 1
        print("Morning print checklist is current.")
        return 0

    DEFAULT_OUTPUT.write_text(rendered, encoding="utf-8")
    print(f"Rendered {DEFAULT_OUTPUT.relative_to(ROOT.parent)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
