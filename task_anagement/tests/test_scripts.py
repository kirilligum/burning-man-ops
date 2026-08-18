from __future__ import annotations

import runpy
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[2]
TASK = "task_anagement/data/tasks/Clean_communal_kitchen_tables.xml"
CARD = "task_anagement/build/task-cards/Clean_communal_kitchen_tables.md"
FUEL_CARD = "task_anagement/build/task-cards/Coordinate_generator_refueling.md"
PROPANE_CARD = "task_anagement/build/task-cards/Replace_kitchen_propane_cylinder.md"
CHECKLIST = "task_anagement/build/checklists/Morning.md"
PRINT_CHECKLIST = "task_anagement/morning-checklist.md"


def run_script(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *arguments],
        cwd=REPOSITORY,
        text=True,
        capture_output=True,
        check=False,
    )


class TaskManagementScriptsTest(unittest.TestCase):
    def test_canonical_xml_validates_with_source_snapshot_present(self) -> None:
        result = run_script("task_anagement/scripts/validate.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Validated ", result.stdout)
        self.assertIn(" XML files.", result.stdout)

    def test_rendered_task_card_is_current(self) -> None:
        result = run_script(
            "task_anagement/scripts/render-task-card.py",
            "--all",
            "--check",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("task cards are current", result.stdout)

    def test_rendered_task_card_contains_linked_item_details(self) -> None:
        card = (REPOSITORY / CARD).read_text(encoding="utf-8")
        self.assertIn("Small hand brush and dustpan used on communal tables", card)
        self.assertIn("Turn the nozzle to ON", card)
        self.assertNotIn("Stash Bins", card)

    def test_rendered_item_details_humanize_references(self) -> None:
        card = (REPOSITORY / FUEL_CARD).read_text(encoding="utf-8")
        self.assertIn("At the locations marked on 📦 Camp Map", card)
        self.assertNotIn("📦 Camp_Map", card)

    def test_food_contact_surfaces_are_rinsed_before_sanitizing(self) -> None:
        cards = (
            "Clean_communal_kitchen_cooking_surfaces.md",
            "Prepare_cheese_station.md",
            "Serve_cheese_pairing.md",
            "Close_cheese_station.md",
        )
        for filename in cards:
            with self.subTest(filename=filename):
                card = (
                    REPOSITORY / "task_anagement/build/task-cards" / filename
                ).read_text(encoding="utf-8")
                rinse = card.index("potable water")
                sanitize = card.index("Food Surface Sanitizer", rinse)
                self.assertLess(rinse, sanitize)
                self.assertIn("visibly wet for 60 seconds", card)

    def test_fuel_tasks_preserve_verified_controls(self) -> None:
        fuel_card = (REPOSITORY / FUEL_CARD).read_text(encoding="utf-8")
        self.assertIn("shut down the generator before its tank is filled", fuel_card)
        self.assertIn("at least a 40-B rating is 8 to 10 feet", fuel_card)

        propane_card = (REPOSITORY / PROPANE_CARD).read_text(encoding="utf-8")
        self.assertIn("Fire Extinguishers is visible and accessible", propane_card)
        self.assertNotIn("ignition sources within 10 feet", propane_card)

    def test_rendered_checklists_are_current(self) -> None:
        result = run_script(
            "task_anagement/scripts/render-checklists.py",
            "--check",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("checklists are current", result.stdout)

    def test_morning_checklist_has_runtime_fields_and_task_link(self) -> None:
        checklist = (REPOSITORY / CHECKLIST).read_text(encoding="utf-8")
        self.assertIn(
            "| Task | When | Status | Initials | Completion time |",
            checklist,
        )
        self.assertIn("not an execution sequence", checklist)
        self.assertIn(
            "[📋 Clean communal kitchen tables]"
            "(../task-cards/Clean_communal_kitchen_tables.md)",
            checklist,
        )

        strike = (
            REPOSITORY / "task_anagement/build/checklists/Strike.md"
        ).read_text(encoding="utf-8")
        self.assertIn("After 📋 Strike sound system passes", strike)
        self.assertNotIn("📋 Strike_sound_system", strike)

    def test_morning_print_checklist_is_current_and_concise(self) -> None:
        result = run_script(
            "task_anagement/scripts/render-morning-checklist.py",
            "--check",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Morning print checklist is current", result.stdout)

        checklist = (REPOSITORY / PRINT_CHECKLIST).read_text(encoding="utf-8")
        self.assertIn("## Clean communal kitchen tables", checklist)
        self.assertIn("#### Communal Tables", checklist)
        self.assertIn("#### Lost and Found", checklist)
        self.assertIn("#### Dustpan and Brush", checklist)
        self.assertIn("#### Multisurface Cleaner", checklist)
        self.assertIn("#### Disposable Towels", checklist)
        self.assertIn("#### Trash Bins", checklist)
        self.assertIn("Small hand brush and dustpan used on communal tables", checklist)
        self.assertIn("Turn the nozzle to ON", checklist)
        self.assertIn("Get another empty container", checklist)
        self.assertIn("Before marking PASS, return each used item", checklist)
        self.assertIn("Once or more per shift", checklist)
        self.assertNotIn("☐", checklist)
        self.assertNotIn("\n\n", checklist)
        self.assertNotIn("📋", checklist)
        self.assertNotIn("📦", checklist)
        self.assertNotIn("🍳", checklist)
        self.assertNotIn("Clean_communal_kitchen_tables", checklist)
        self.assertNotIn("Communal_Tables", checklist)
        self.assertNotIn("**Checklist types:**", checklist)
        self.assertNotIn("**Who is responsible:** Dominatrix", checklist)
        self.assertNotIn("see task Clean communal kitchen tables", checklist)
        self.assertNotIn("**Why:**", checklist)
        self.assertNotIn("**Time:**", checklist)
        self.assertNotIn("### Common problems", checklist)
        self.assertNotIn("### Who to ask", checklist)
        self.assertNotIn("### Reasoning", checklist)
        self.assertNotIn("### Decisions", checklist)

    def test_historical_lookup_accepts_reference_only_decision(self) -> None:
        result = run_script(
            "task_anagement/scripts/extract-historical-decisions.py",
            TASK,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("D-114", result.stdout)
        self.assertNotIn("### D-115", result.stdout)

    def test_validator_finds_undeclared_operational_reference(self) -> None:
        validator = runpy.run_path(
            str(REPOSITORY / "task_anagement/scripts/validate.py")
        )
        task = ET.fromstring(
            "<task><resources/><steps><step>"
            "<action>Use 📦 Missing_Item.</action>"
            "</step></steps></task>"
        )
        self.assertEqual(
            validator["undeclared_operational_references"](task),
            {"📦 Missing_Item"},
        )

    def test_validator_contact_patterns_do_not_match_operational_values(self) -> None:
        validator = runpy.run_path(
            str(REPOSITORY / "task_anagement/scripts/validate.py")
        )
        patterns = validator["PROTECTED_CONTACT"].values()
        self.assertTrue(
            any(pattern.search("person@example.com") for pattern in patterns)
        )
        self.assertTrue(any(pattern.search("202-555-0100") for pattern in patterns))
        self.assertFalse(any(pattern.search("200-400 ppm") for pattern in patterns))


if __name__ == "__main__":
    unittest.main()
