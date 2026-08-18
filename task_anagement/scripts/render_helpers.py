"""Shared XML helpers for Markdown renderers."""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "data" / "items"
ITEM_FOLDERS = {
    "🌐": ITEMS / "public area",
    "🍷": ITEMS / "bar-cheese",
    "🔥": ITEMS / "propane area",
    "🏕️": ITEMS / "common area",
    "🍳": ITEMS / "kitchen",
    "🔧": ITEMS / "private infrastructure",
    "📦": ITEMS,
}
REFERENCE = re.compile(
    r"(?P<icon>📋|🌐|🍷|🔥|🏕️|🍳|🔧|📦)\s+"
    r"(?P<name>[A-Za-z0-9][A-Za-z0-9_-]*)"
)


def text(element: ET.Element | None) -> str:
    if element is None:
        return ""
    return " ".join("".join(element.itertext()).split())


def humanize_references(value: str, *, keep_icons: bool) -> str:
    def replace(match: re.Match[str]) -> str:
        icon = f"{match.group('icon')} " if keep_icons else ""
        return f"{icon}{match.group('name').replace('_', ' ')}"

    return REFERENCE.sub(replace, value)


def item_for_reference(value: str) -> ET.Element | None:
    match = REFERENCE.fullmatch(value)
    if not match or match.group("icon") == "📋":
        return None
    path = ITEM_FOLDERS[match.group("icon")] / f"{match.group('name')}.xml"
    return ET.parse(path).getroot()
