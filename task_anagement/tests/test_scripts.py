from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[2]
TASK = "task_anagement/data/tasks/Clean_communal_kitchen_tables.xml"
CARD = "task_anagement/build/task-cards/Clean_communal_kitchen_tables.md"


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
            TASK,
            "--output",
            CARD,
            "--check",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Task card is current", result.stdout)

    def test_rendered_task_card_contains_linked_item_details(self) -> None:
        card = (REPOSITORY / CARD).read_text(encoding="utf-8")
        self.assertIn("Small hand brush and dustpan used on communal tables", card)
        self.assertIn("Turn the nozzle to ON", card)
        self.assertNotIn("Stash Bins", card)

    def test_historical_lookup_accepts_reference_only_decision(self) -> None:
        result = run_script(
            "task_anagement/scripts/extract-historical-decisions.py",
            TASK,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("D-114", result.stdout)
        self.assertNotIn("### D-115", result.stdout)


if __name__ == "__main__":
    unittest.main()
