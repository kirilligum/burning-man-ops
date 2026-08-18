# Repository Guidelines

## Project Structure

`Treble Makers Checklists - 2026.ods` is source evidence; do not bulk-edit it or
treat every tab as current. `task_anagement/README.md` is the system
specification, `task_anagement/DECISIONS.md` records current accepted decisions,
and `task_anagement/HISTORICAL_DECISIONS.md` preserves superseded decisions.
`task_anagement/schema/field-dictionary.md` defines fields. Canonical XML lives
under `task_anagement/data/`.

## Decision Record and Agent Behavior

Before proposing or making task-system changes, read the specification, active
decision record, and field dictionary. Accepted decisions are constraints; the
user's newest explicit instruction wins. Do not load
`HISTORICAL_DECISIONS.md` for ordinary work because it is intentionally
long-running context. Load related history only for a deep dive.

When the user accepts, reverses, or directly requests a durable design change,
update `DECISIONS.md` and every affected specification, example, and XML file in
the same change. When a current decision is replaced, move the old entry to
`HISTORICAL_DECISIONS.md`, preserve its ID and superseded status, and add the
replacement to `DECISIONS.md`; do not erase history. Do not record tentative
agent suggestions as decisions.

When a task XML contains a superseded decision with a `<record>` such as
`D-114`, retrieve its past context with:

```bash
python3 task_anagement/scripts/extract-historical-decisions.py \
  "task_anagement/data/tasks/Clean_communal_kitchen_tables.xml"
```

The script parses the task XML and prints only the linked records from
`HISTORICAL_DECISIONS.md`. Do not read the full historical file when the task
does not link a relevant record.

Apply KISS. Use the smallest direct representation that meets an accepted need.
Do not introduce separate IDs, lookup entities, relationship tables, workflow
states, risk matrices, or abstraction layers without an explicit requirement.
Default every task to its minimum complete form. Include a resource, step,
expected result, PASS criterion, or problem only when it is needed to perform
or verify the task. Name required physical resources so workers can recognize
them directly; do not hide required components behind a kit name. Store items
under their categorical-area folder and use short functional IDs, such as
`Disposable_Towels`. Keep the area, brand, model, size, and replacement details
out of the item name. Store uncategorized items directly under `data/items/`.

Ground procedures in the workbook, existing XML, and facts supplied by the
user. Do not invent locations, equipment details, timings, quantities,
thresholds, or generic safety scenarios. Mark unknown facts for field testing.
Use the clearest existing task, item, location, role, or global-instruction
reference when one is available. If a reference or required response is
unknown or unclear, point the user or worker to the Dominatrix. Treat that as
a fallback for an unresolved gap, not as a substitute for a known reference;
replace the fallback with the useful reference as the documentation improves.
Physical labels are optional. Do not invent or require a label for an item;
mention one only when the camp has actually decided to use it.
Do not add obvious `readyBeforeUse` or `ifNotReady` text merely to say that an
item should exist or to repeat “ask the Dominatrix”; leave those fields blank
when the global instructions already cover the situation.
Keep universal instructions global, item readiness and item failures in item
files, task execution in task files, and on-playa results in the generated
checklist. Keep optional task `<reasoning>` and `<decisions>` records as concise
maintainer metadata; do not render them on task cards by default. Lead with the
answer, preserve agreed wording and order, and keep explanations concise.

## Architecture and Data Rules

Repository XML is the source of truth; Google Sheets is the human editing
surface. Import Sheet changes before XML edits, export validated XML before
people resume Sheet editing, and never resolve conflicts silently. Exclude
protected information and private contact details.

Task names are unique identifiers using underscores instead of spaces. An item's
parent folder plus its name is its identifier. Store names in `<name>` elements,
make each filename match its name, and keep one logical record per XML file. Every task stores its
categorical area and resolves item references first within that area's folder,
then directly under `data/items/`. Format XML as UTF-8 with two-space
indentation. References omit the `.xml` extension. Prefix task references with
`📋`; prefix item references with the icon for their area folder, or `📦` for
root items. Icons are not part of IDs. Task XML stores selected checklist
memberships in `<checklist_types>` using one `<checklist_type>` element per
selected type. Converters must preserve reasoning and decision records,
including their order, optional `<record>` links, and empty optional values.

## Validation Commands

There is no automated suite yet. For every change, run:

```bash
find task_anagement/data -name '*.xml' -exec xmllint --noout {} +
git diff --check
git status --short
```

Future converters must validate unique task names, item names unique within a
folder, optional item areas, references, Boolean checklist values, step
ordering, required fields, task decision-record fields and links, protected-
data exclusions, and a semantic no-change XML/Sheet/XML round trip. The
historical-decision lookup must return the linked records and fail on a missing
record ID. Add a regression test for every converter or validation bug.

## Commits and Pull Requests

Use focused Conventional Commit-style subjects such as `docs: record task
field decisions`. Pull requests should name affected tasks or items, describe
schema or sync impact, list validation, identify unresolved decisions, and
include rendered screenshots when layout changes.
