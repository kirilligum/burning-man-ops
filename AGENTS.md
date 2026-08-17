# Repository Guidelines

## Project Structure

`Treble Makers Checklists - 2026.ods` is source evidence; do not bulk-edit it or
treat every tab as current. `task_anagement/README.md` is the system
specification, `task_anagement/DECISIONS.md` records accepted decisions, and
`task_anagement/schema/field-dictionary.md` defines fields. Canonical XML lives
under `task_anagement/data/`.

## Decision Record and Agent Behavior

Before proposing or making task-system changes, read the specification,
decision record, and field dictionary. Accepted decisions are constraints; the
user's newest explicit instruction wins.

When the user accepts, reverses, or directly requests a durable design change,
update `DECISIONS.md` and every affected specification, example, and XML file in
the same change. Mark replaced decisions **Superseded**; do not erase history.
Do not record tentative agent suggestions as decisions.

Apply KISS. Use the smallest direct representation that meets an accepted need.
Do not introduce separate IDs, lookup entities, relationship tables, workflow
states, risk matrices, or abstraction layers without an explicit requirement.

Ground procedures in the workbook, existing XML, and facts supplied by the
user. Do not invent locations, equipment details, timings, quantities,
thresholds, or generic safety scenarios. Mark unknown facts for field testing.
Keep universal instructions global, item readiness and item failures in item
files, task execution in task files, and on-playa results in the generated
checklist. Lead with the answer, preserve agreed wording and order, and keep
explanations concise.

## Architecture and Data Rules

Repository XML is the source of truth; Google Sheets is the human editing
surface. Import Sheet changes before XML edits, export validated XML before
people resume Sheet editing, and never resolve conflicts silently. Exclude
protected information and private contact details.

Task and item names are their identifiers. Store names in `<name>` elements,
use the exact name for references and filenames, and keep one logical record
per XML file. Format XML as UTF-8 with two-space indentation.

## Validation Commands

There is no automated suite yet. For every change, run:

```bash
find task_anagement/data -name '*.xml' -exec xmllint --noout {} +
git diff --check
git status --short
```

Future converters must validate unique names, references, Boolean checklist
values, step ordering, required fields, protected-data exclusions, and a
semantic no-change XML/Sheet/XML round trip. Add a regression test for every
converter or validation bug.

## Commits and Pull Requests

Use focused Conventional Commit-style subjects such as `docs: record task
field decisions`. Pull requests should name affected tasks or items, describe
schema or sync impact, list validation, identify unresolved decisions, and
include rendered screenshots when layout changes.
