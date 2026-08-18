# Treble Makers Task Management System

This directory is the design checkpoint for the Treble Makers task-management
and operating-instructions system.

The system is intended to turn the existing shift checklists into instructions
that a first-time camper can follow without relying on undocumented camp
knowledge, while preserving short checklists for experienced campers and shift
execution.

> A newcomer follows the procedure. A veteran uses the checklist. Everyone
> leaves the task, equipment, and area ready for the next shift.

This README describes the system as currently agreed. It is expected to change
as the schema, conversion process, procedures, and field tests are refined.
Nothing in this directory is currently an approved field procedure.

## Decision records

Accepted design and working-style decisions are maintained in
[DECISIONS.md](DECISIONS.md). Superseded decisions are preserved in
[HISTORICAL_DECISIONS.md](HISTORICAL_DECISIONS.md) for deep dives. The active
record is authoritative for current choices; this README describes the
resulting system.

Do not load the historical record during ordinary task work. A task XML links
related global decisions with `<record>` values inside its `<decisions>`
records. Use `scripts/extract-historical-decisions.py` to retrieve only the
superseded records related to a task.

## IDs and reference icons

Task and item names are canonical IDs. Replace spaces with underscores and use
the resulting ID for the XML filename without its `.xml` extension in
references. Icons are not part of IDs, but an item icon is required reference
syntax that selects the item's folder.

| Reference | Icon |
| --- | --- |
| Any task | `📋` |
| Public area item | `🌐` |
| Bar/Cheese item | `🍷` |
| Propane area item | `🔥` |
| Common area item | `🏕️` |
| Kitchen item | `🍳` |
| Private infrastructure item | `🔧` |
| Uncategorized item at `data/items/` | `📦` |

For example, `📋 Clean_communal_kitchen_tables` is a task reference and
`🍳 Multisurface_Cleaner` is a Kitchen item reference. Renderers may replace
underscores with spaces for human-facing output; the underlying ID remains
unchanged.

## Why the current workbook is not enough

The current workbook is useful to experienced campers because they know how to
expand a short prompt into the real task.

For example, an experienced camper may read:

> Communal kitchen tables clean

and already know:

- where the cleaning supplies are;
- which product to use;
- where wastewater goes;
- what happens to abandoned property;
- what “clean” looks like;
- how to restock supplies;
- who to notify if the task cannot be completed.

A newcomer sees only the desired outcome.

The workbook contains useful fragments such as exact ice quantities, generator
thresholds, escalation instructions, and instructions to disable the shower
when a large puddle cannot be fixed. Those are mixed with prompts such as:

- “Make sure the surroundings are reasonably nice.”
- “Test all buffers are functioning.”
- “Check for mechanical issues.”
- “Stage clean.”
- “Fire Pit Structure Intact and not dangerous.”

It also contains unresolved conflicts:

- Generator escalation appears at below 50%, below two-thirds, and below 70%,
  while the Dominatrix checklists use “under half.”
- The bar checklist sends crushed cans to trash, while other checklists send
  them to aluminum recycling.
- Refueling generators, replacing propane tanks, and shutting down flame
  effects appear beside routine cleaning work.
- “Check for mechanical issues” does not say what to inspect, what failure looks
  like, or what the worker may do about it.
- Some checklists tell people to add instructions during the shift or erase the
  completed checkmarks, preventing controlled revision and durable execution
  records.

The workbook also mixes operating instructions with prior-year layouts, strike
plans, contact exports, bookings, and deprecated material. The new system must
start from a deliberate allowlist of operational content, not a bulk conversion
of every tab.

## Source snapshots

`data/Treble Makers Camper Wiki.xml` is a recursive snapshot of the public
Treble Makers Camper Wiki. It preserves the visible page hierarchy, text,
lists, links, media references, and source edit times for research. It is source
evidence, not automatically approved task or item data.

The snapshot does not follow external links. Spreadsheet URLs, tracking links,
and embedded external-document URLs are omitted because they may expose camper
lists or other protected information; their visible labels remain.

## Procedure versus checklist

A procedure and a checklist are related but different documents.

- A **procedure** teaches or directs the work. The worker reads a step, performs
  that step, and continues in read-do mode.
- A **checklist** verifies critical items after the worker already knows the
  procedure or points the worker to the applicable procedure.

The shift checklist will remain short. It is generated from selected checklist
types stored in each task XML, identifies assignments, and records their
results. The task card contains the instructions and completion criteria.

## System architecture

### Canonical data flow

```text
                         human editing
                              |
                              v
                     +------------------+
                     |  Google Sheets   |
                     | editable view of |
                     | repository data  |
                     +--------+---------+
                              |
                     import / export
                              |
                              v
                     +------------------+
                     | Repository XML   |
                     | source of truth  |
                     +--------+---------+
                              |
                +-------------+-------------+
                |                           |
                v                           v
          Codex editing               validation and
                                      rendered outputs
```

The Google Sheet and XML are two editing surfaces for the same information,
but the committed XML is the repository source of truth.

### Synchronization rules

The conversion tools do not exist yet. When implemented, they must follow these
rules:

1. Do not edit XML and Google Sheets concurrently.
2. Before Codex edits XML, import any outstanding human changes from Google
   Sheets.
3. After Codex changes XML, validate it and export it to Google Sheets before
   humans continue editing.
4. After humans edit Google Sheets, import the changes to XML and review the XML
   diff.
5. Never silently resolve a conflict between the two surfaces.
6. Never infer a task or item name from a row number or tab position.
7. Preserve names, ordering, references, Unicode, line breaks, and empty values
   through a round trip.
8. A Sheet-to-XML-to-Sheet round trip with no edits must produce no semantic
   changes.
9. Only allowlisted tabs and columns may be imported.
10. Conversion must reject unknown references and duplicate names rather than
    guessing.

### Why XML is canonical here

The operational data is hierarchical: a task contains orientation, required
items, ordered steps, decisions, warnings, stop conditions, and completion
criteria. XML keeps those relationships explicit for Codex and repository
review. It avoids asking an LLM to reconstruct a task by mentally joining or
editing several independent TSV or JSON representations.

Google Sheets remains important because it gives camp members a familiar table
interface. The XML/Sheet converters bridge the human and Codex editing paths.

## Information that belongs in the system

The system contains operating information, not a general camp archive.

Allowed information includes:

- task definitions;
- procedure steps;
- PASS conditions;
- global instructions that apply to every task;
- item and equipment definitions;
- physical locations;
- experts stored directly on tasks, with **Dominatrix** as the default;
- checklist-type or shift memberships stored directly on tasks;
- the execution status, initials, and time recorded on playa.

Information that does not belong includes:

- phone-number or messaging-app exports;
- personal email addresses;
- travel and booking records;
- payment or card information;
- private health information;
- private incident narratives;
- credentials or API secrets;
- unrelated prior-year planning tabs.

Each task stores the expert to contact. If no specific expert or useful
reference is known, use **Dominatrix** as the fallback. Do not store phone
numbers or other protected contact data.

### Reference resolution and fallback

Use the clearest existing task, item, location, role, or global-instruction
reference whenever one is available. If a reference or required response is
unknown or unclear, ask the **Dominatrix**. This is a fallback for an unresolved
gap, not a substitute for a known reference. As the documentation becomes
clearer, replace Dominatrix fallbacks with the useful reference.

## Document types

The system will produce connected documents rather than one enormous manual.

### 1. Global instructions

`global-instructions.xml` contains exactly the short worker instructions that
apply to every task:

- Before marking PASS, return each used item to its location and leave it ready
  for the next person.
- Collect all MOOP.
- If an item, instruction, or solution is missing or unclear, ask the
  Dominatrix.

Rules for authors, such as preferring a known reference over the Dominatrix,
belong in this specification and `AGENTS.md`; they are not rendered as worker
instructions.

Global instructions are automatically included in rendered task cards or their
standard completion section. Tasks do not reference them individually. If an
instruction does not apply to every task, it belongs in the applicable task
rather than this file.

### 2. Generated shift checklist

The shift checklist is generated from checklist-type memberships inside the
task XML. It is an index, assignment sheet, and execution record, not the full
procedure.

Example:

| Checklist | Task | Status | Initials | Time |
| --- | --- | --- | --- | --- |
| `MORNING` | 📋 Clean_communal_kitchen_tables |  |  |  |
| `MORNING` | Clean cooking surfaces |  |  |  |
| `MORNING` | Empty dry waste |  |  |  |
| `MORNING` | Inspect EMT shade |  |  |  |
| `MORNING` | Read generator fuel gauge |  |  |  |

The worker performing the task marks one of:

- **PASS** — the task was performed and every PASS when condition was met.
- **BLOCKED** — the task could not be completed.
- **ESCALATED** — the task or observed condition was handed to the expert.
- **NOT APPLICABLE** — the task did not apply to that shift or condition.

This status is marked at Burning Man. It is not a document-publication status.
Each line also records the worker’s initials and completion time.

Each shift line points to its task card by task name and, when useful, page
number or QR code. Printed instructions must remain complete without the QR
code.

In the editable task TSV and Google Sheets tab, every approved checklist type
has its own Boolean column. A checked box means the task belongs to that
checklist. This avoids delimiter parsing and lets campers filter a checklist
column for `TRUE`. XML remains canonical and stores only the selected checklist
memberships.

For field execution, the generated checklist tab expands one row for each task
and checklist membership. This gives every occurrence its own `status`,
`initials`, and `time` cells and lets campers sort or filter by the exact
checklist value. The generated rows are not a separate checklist XML source.

### 3. Task card

One task card describes one outcome from beginning through handoff. It is used
in read-do mode and contains the task fields defined below.

### 4. Item card

Reusable information about an item or piece of equipment should not be copied
into every procedure.

An item card contains only the item fields defined below. Its parent folder plus
its name is its identifier. The name is the canonical ID; a physical label is
optional, and a human-facing renderer may display the underscores as spaces.

## Core data model

The field-by-field contract is maintained in the
[field dictionary](schema/field-dictionary.md).

The simplest mental models are:

> **TASK = NAME + CHECKLIST_TYPES + AREA + WHY + WHEN + TIME + RESOURCES + STEPS + PASS + PROBLEMS + EXPERT + REASONING + DECISIONS**

> **ITEM = NAME + DESCRIPTION + OPTIONAL AREA + OPTIONAL LOCATION + OPTIONAL READY BEFORE + READY FOR NEXT + OPTIONAL IF NOT READY + RESPONSIBLE + PROBLEMS**

Task IDs are globally unique. Item IDs are unique within their parent folder
and may repeat in different folders. IDs use underscores instead of spaces.
Selected checklist types and Area are stored directly in each task. One
global-instructions file provides behavior
that applies to every task.

**Reasoning** and **Decisions** are optional maintainer records attached to the
task. They explain why the procedure is shaped this way and record accepted
task-specific choices. They are not extra execution steps and are omitted from
task cards by default. Project-wide choices remain in `DECISIONS.md`.

Every task starts in its minimum complete form. A resource, step, expected
result, PASS criterion, or problem is included only when it is needed to
perform or verify the task. Detail is added after a demonstrated operational
need, not by default.

Locations are deliberately not separate records. An area folder gives a
categorized item's categorical location; the optional **Location** field says
where to find it when that information is useful. A recognizable item that may
be found in several obvious places may omit Location. An uncategorized item
stays directly under `data/items/`.

### Planned Google Sheets tabs

One clean Google Sheets workbook should contain tables such as:

| Tab | Purpose |
| --- | --- |
| `00 START HERE` | Short editing instructions for camp members |
| `01 TASKS` | One row per task |
| `02 ITEMS` | One row per item |
| `03 GLOBAL_INSTRUCTIONS` | Instructions applied to every task |
| `04 CHECKLIST` | Generated field view with one row per task and checklist membership |
| `90 LISTS` | Dropdown values and other editor support data |

The workbook must feel like a form, not a database:

- one row represents one thing;
- one column represents one property;
- no merged cells in data tables;
- no free-form comma-separated mini-databases inside cells;
- ordered task sections use preserved line breaks inside one cell;
- checklist columns use checkboxes with Boolean values;
- resources use one entry per preserved line;
- generated and formula columns are protected from accidental edits;
- headers explain what belongs in each column;
- controlled values use dropdowns;
- headers remain frozen;
- filters help editors find related records.

Protection here prevents accidental editing. It is not a privacy mechanism.
Protected information is excluded from the system entirely.

### Task columns

The `TASKS` Sheet presents these columns in this order. The XML names shown here
describe the same information without creating duplicate identifiers.

| Sheet column | XML | Description and entry guidance |
| --- | --- | --- |
| **Task** | `task/name` | Unique task ID using underscores instead of spaces. Start with a verb and name the outcome and place when needed, such as `Clean_communal_kitchen_tables`. |
| **Checklist type columns** | `checklist_types/checklist_type` | One Boolean column per approved checklist type. Check every type on which the task must appear. |
| **Area** | `area` | Select the categorical camp area where the task and its item references belong. |
| **Why** | `why` | Explain a non-obvious practical reason or consequence. Leave blank when the text would only restate the task. |
| **When** | `when` | State the time, event, or observable trigger for starting the task, such as `After dinner` or `When the bin reaches the marked line`. |
| **Time** | `time` | Realistic completion time under normal conditions, such as `10 minutes`. Leave blank until a useful value is known. |
| **What you need** | `resources/resource` | Only what is required to complete the task: an item reference is its category icon followed by its underscore ID, such as `🍳 Multisurface_Cleaner`; other resources remain plain text. Use one resource per line. |
| **Steps** | `steps/step` | The fewest numbered actions needed, in execution order. Each step contains one physical action or observation. Include an expected result only when it is not obvious and place IF/THEN text where the decision occurs. |
| **PASS when** | `passWhen/criterion` | The minimum observable conditions needed to verify completion. Use one criterion per line. |
| **Common problems** | `commonProblems/problem` | Likely problems not tied to one particular step. Pair each condition with a direct response, preferably as IF/THEN. |
| **Who to ask** | `expert` | Person to ask about the task. Leave blank to use **Dominatrix**. This appears after Common problems on the task card. |
| **Reasoning** | `reasoning/entry` | Optional concise rationale for the task's order, scope, or omissions. One entry per line. Maintainer metadata; not shown on the task card by default. |
| **Decisions** | `decisions/decision` | A task-specific decision contains date, status, text, and effect. A shared active or historical decision is linked with only record and status. Maintainer metadata; not shown on the task card by default. |

The initial checklist-column allowlist should be selected from the current
operational workbook during inventory:

| Candidate Boolean column | `TRUE` means |
| --- | --- |
| **Morning Dominatrix** | Include the task on the Morning Dominatrix checklist. |
| **Evening Dominatrix** | Include the task on the Evening Dominatrix checklist. |
| **Morning** | Include the task on the general Morning checklist. |
| **Infra Lead** | Include the task on the Infra Lead checklist. |
| **Shower** | Include the task on the Shower checklist. |
| **Liaison** | Include the task on the Liaison shift checklist. |
| **Pre-event** | Include the task on the checklist completed before an event. |
| **Bar** | Include the task on the Bar shift checklist. |
| **Afternoon** | Include the task on the Afternoon checklist. |
| **Cheese** | Include the task on the Cheese shift checklist. |
| **Post-event** | Include the task on the checklist completed after an event. |
| **Flame Effects** | Include the task on the restricted Flame Effects checklist. |
| **Build** | Include the task on the camp Build checklist. |
| **Strike** | Include the task on the camp Strike checklist. |

These are candidates, not an automatic migration of workbook tabs. The camp
must confirm which checklist types remain current.

In TSV, each checklist column contains `TRUE` or `FALSE`. In Google Sheets, the
same fields are checkboxes. In XML, a task lists only its `TRUE` memberships;
absence means `FALSE`.

### Item columns

The `ITEMS` Sheet presents these columns in this order:

| Sheet column | XML | Description and entry guidance |
| --- | --- | --- |
| **Item** | `item/name` | Short functional item ID using underscores instead of spaces and matching the XML filename, such as `Disposable_Towels`. It must be unique within its parent folder. Keep area, brand, model, size, and product numbers out of the ID. |
| **Description** | `item/description` | Optional recognizable description, brand, model, size, or product detail. Keep these details out of the item ID. |
| **Area** | Parent folder under `data/items/` | Optional categorical camp area. The converter derives it from the XML folder and exposes it as a Sheet column. Blank means the item is directly under `data/items/`. |
| **Location** | `location` | Optional storage location using visible landmarks, container names, and shelf or side information. Leave blank when the item is recognizable at the task site or may be found in multiple obvious places. |
| **Ready before use** | `readyBeforeUse` | Observable condition required before someone starts using the item. Leave blank when availability is obvious or the global instructions already cover not finding the item. |
| **Ready for next person** | `readyForNextPerson` | Observable condition in which the item must be returned, including cleaning, closing, charging, or restocking. |
| **If not ready** | `ifNotReady` | Optional item-specific action when a ready condition is not met. Leave blank when the global instructions cover the response. |
| **Who is responsible** | `responsible` | Person responsible for keeping the item available and resolving problems. Do not include private contact information. |
| **Common problems** | `commonProblems/problem` | Recurring problems during normal use and the direct response to each one. |

Each item is stored as an individual XML file under its area folder or directly
under `data/items/` when it has no category. An item resource line uses its
category icon followed by its exact underscore ID. The icon authoritatively
selects the item folder: `🍳` selects `data/items/kitchen/`, while `📦`
selects `data/items/`. Other resource lines, such as `Two additional people`,
remain plain requirements.

Use this item-name pattern:

> **Function or recognizable type**

Examples are `Multisurface_Cleaner` and `Disposable_Towels`. Keep IDs short
enough to work in references and filenames. Renderers may replace underscores
with spaces for physical labels, when used, and task cards. Put exact
replacement-product details in **If not ready**, not in the name.

Items represent supplies, not a deduplicated product catalog. The kitchen and
bar may each contain `Disposable_Towels.xml` in their own folders.
General items such as `📦 Communal_Tables`, `📦 Lost_and_Found`, and
`📦 Trash_Bins` stay directly under `data/items/`.

| Area | Item folder |
| --- | --- |
| Blank | `data/items/` |
| Public area | `data/items/public area/` |
| Bar/Cheese | `data/items/bar-cheese/` |
| Propane area | `data/items/propane area/` |
| Common area | `data/items/common area/` |
| Kitchen | `data/items/kitchen/` |
| Private infrastructure | `data/items/private infrastructure/` |

### Global instructions

`data/global-instructions.xml` is a single canonical file. Every instruction in
it applies to every task and is automatically included by the renderer. There
is no per-task relationship table for global instructions.

The `GLOBAL_INSTRUCTIONS` Sheet has one column, **Instruction**. Each row is one
direct instruction that applies to every task. Conditional or task-specific
instructions belong in Steps or Common problems instead.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<globalInstructions>
  <instruction>
    Before marking PASS, return each used item to its location and leave it
    ready for the next person.
  </instruction>
  <instruction>Collect all MOOP.</instruction>
  <instruction>
    If an item, instruction, or solution is missing or unclear, ask the
    Dominatrix.
  </instruction>
</globalInstructions>
```

## XML representation

The field dictionary defines the canonical XML shape. The current examples are
the actual files, not copies embedded in this specification:

- `data/tasks/Clean_communal_kitchen_tables.xml`
- `data/items/Communal_Tables.xml`
- `data/items/Lost_and_Found.xml`
- `data/items/Trash_Bins.xml`
- `data/items/kitchen/Disposable_Towels.xml`
- `data/items/kitchen/Dustpan_and_Brush.xml`
- `data/items/kitchen/Multisurface_Cleaner.xml`
- `data/global-instructions.xml`

Task XML stores the expert, Area, checklist memberships, execution fields, and
optional maintainer metadata. An item reference contains the folder-selecting
icon and exact underscore ID. A missing expert means **Dominatrix**. Shared
active or historical decisions are linked with `record` and `status`; their
text remains in the applicable decision record.

Expected repository layout:

```text
task_anagement/
├── README.md
├── DECISIONS.md
├── HISTORICAL_DECISIONS.md
├── schema/
│   └── field-dictionary.md
├── data/
│   ├── Treble Makers Camper Wiki.xml
│   ├── tasks/
│   │   └── Clean_communal_kitchen_tables.xml
│   ├── items/
│   │   ├── Communal_Tables.xml
│   │   ├── Lost_and_Found.xml
│   │   ├── Trash_Bins.xml
│   │   ├── public area/
│   │   ├── bar-cheese/
│   │   ├── propane area/
│   │   ├── common area/
│   │   ├── kitchen/
│   │   │   ├── Disposable_Towels.xml
│   │   │   ├── Dustpan_and_Brush.xml
│   │   │   └── Multisurface_Cleaner.xml
│   │   └── private infrastructure/
│   └── global-instructions.xml
├── scripts/
│   ├── extract-historical-decisions.py
│   ├── validate.py
│   └── render-task-card.py
├── tests/
│   └── test_scripts.py
└── build/
    └── task-cards/
        └── Clean_communal_kitchen_tables.md
```

Validate and render all tasks with:

```bash
python3 -m unittest discover -s task_anagement/tests -p 'test_*.py'
python3 task_anagement/scripts/validate.py
python3 task_anagement/scripts/render-task-card.py --all
```

Use the render command with `--all --check` to verify that every committed card
matches the canonical XML without rewriting it.

## Task-card content and order

Every task card should follow the same scanning order.

1. Task
2. Checklist memberships
3. Area
4. Why
5. When
6. Time
7. What you need
8. Steps
9. PASS when
10. Finish, including global instructions and item handoff conditions
11. Common problems
12. Who to ask, showing **Dominatrix** when no other expert is specified

Each step contains one physical action or observation. Expected results and
IF/THEN decisions appear inside the applicable step rather than in separate
sections. Reasoning and Decisions are maintainer metadata and are not shown on
the default task card.

## What to keep, move, and add

### Keep on the task card

- task name, selected checklist types, and Area;
- a specific When;
- only required resources and actions;
- only the PASS conditions needed to verify completion;
- Why, Time, expected results, problems, and a non-default expert only when they
  add useful information.

Reasoning and Decisions stay in the task XML as maintainer metadata. They are
available for review and Codex editing but are omitted from the default field
task card unless a maintainer explicitly requests them.

### Move to shared records

- reusable refill, maintenance, and replacement information belongs on the
  item record;
- long background explanations belong in a reference document;
- frequently encountered exceptions should become IF/THEN branches at the
  relevant step.

## Treble Makers controlled-language standard

### 1. Use one name for each thing

Do not alternate between “water tank,” “tote,” “IBC,” and “reservoir.” Select an
exact ID, such as `Gray-Water_IBC`. A rendered physical label is optional. Its
parent folder plus that ID is its identifier; do not add a second code.

### 2. Title tasks with a verb, object, and place

Weak: `Kitchen tables`

Better ID: `Clean_communal_kitchen_tables`

### 3. Start steps with an action verb

Prefer verbs such as Remove, Read, Place, Wipe, Close, Return, and Report.

### 4. Put one action or observation in each step

Weak:

> Clean the table, return everything, and tell the Dominatrix if anything is
> missing.

Better:

1. Wipe the tabletop with cleaner.
2. Return 🍳 Multisurface_Cleaner to its listed location.
3. Report missing supplies to the Shift Lead.

### 5. Do not use “check” by itself

Every inspection must state:

1. what to inspect;
2. how to inspect it;
3. what PASS looks like;
4. what to do when it does not pass.

### 6. Replace subjective adjectives with visible states

Weak:

> Make the surroundings reasonably nice.

Better:

> Collect all MOOP. Move bicycles outside the marked aisle. Put eligible
> abandoned items in `📦 Lost_and_Found`. PASS: the aisle and seating entrances
> are clear.

### 7. Put the condition before the response

> IF the pump does not start, THEN close the shower and attach the OUT OF
> SERVICE sign.

### 8. Put warnings before hazardous actions

> WARNING — PRESSURIZED GAS. Only the authorized operator may open this valve.

### 9. Use exact quantities, intervals, and thresholds

Replace words such as “low,” “enough,” “regularly,” “mostly full,” and “soon”
with observable values. Conflicting values must be resolved by the task expert
before the procedure is used.

### 10. Use four standard scanning words

- **STOP** — halt the task
- **DO NOT** — prohibited action
- **PASS** — acceptable state
- **IF / THEN** — exception or decision

### 11. Bold only what helps execution

Prefer:

> Close the **red valve V-03**.

Avoid bolding or capitalizing an entire paragraph.

### 12. Keep sentences short and active

Use one principal idea per sentence and remove unnecessary words. Approximately
12–15 words per quick-card sentence is a useful target, not a hard limit.

### 13. Keep humor outside the critical sequence

Camp personality and humor can remain in titles, motivation lines, footers, and
etiquette posters. Do not put jokes between critical valve, chemical, lifting,
sanitation, or structural steps.

## Visual and physical design

Use pictures and words together where they improve execution.

Pictures are most useful for:

- locating objects;
- identifying connectors;
- showing orientation;
- showing assembly order;
- distinguishing correct and incorrect states;
- showing the final PASS state.

Text remains necessary for:

- invisible conditions;
- quantities;
- timing;
- warnings;
- decisions;
- chemical instructions;
- escalation.

Visual rules:

- show one meaningful state change per image;
- preserve the same viewing direction across related images;
- use stable part labels;
- use arrows only for actual movement;
- include final-state and right/wrong images when useful;
- compare every image with the real equipment;
- require the task expert to validate safety-critical visuals.

An image model may simplify a photograph into line art. It must not invent a
connector, valve, cable route, anchor, pole length, fastening method, tool, or
protective device. Actual photographs or manually traced diagrams are preferred
for flame, fuel, electrical, and structural work.

Printed output should use a station system:

- kitchen board for kitchen cards;
- bar board for bar cards;
- shower board for shower cards;
- generator station for inspection and operator cards;
- shade storage for build, inspection, repair, and strike cards;
- central shift board for assignments and execution status.

Starting physical-production targets to field-test include:

- one task per letter/A4 page or two-page spread;
- 16–18 point task-card body text;
- larger station-poster text;
- matte lamination to reduce headlamp glare;
- high contrast and generous blank space;
- no meaning conveyed by color alone;
- wet-erase or grease pencil with a tethered writing tool;
- reflective or glow markings on asset locations;
- QR codes only as secondary references;
- complete offline instructions in print.

Every printed page should show its task name.

## Pilot 1: 📋 Clean communal kitchen tables

This is the first complete pilot because it is frequent, observable, and low
risk. Its canonical source is
`data/tasks/Clean_communal_kitchen_tables.xml`; its field-facing output is
`build/task-cards/Clean_communal_kitchen_tables.md`.

The task appears on the **Morning** and **Afternoon** checklists, matching the
two workbook occurrences. **Why** and **Time** remain blank intentionally.
The task uses six linked item records, and the rendered card assembles their
locations, readiness conditions, concrete responses, and common problems so a
worker does not need to read raw XML.

The selected cleaner is **Clorox Free & Clear Multi Surface Cleaner, Spray
Bottle, Fragrance Free, 32 fl oz (UPC 044600603346)**. [Clorox directs
users](https://www.clorox.com/products/clorox-free-clear-multi-surface-cleaner/)
to turn the nozzle to ON, spray the soiled area, and wipe with a towel or cloth;
no rinse is required. The product cleans but does not disinfect.

The selected disposable towel is **WypAll PowerClean L40 Extra Absorbent
Towels, White, 12 x 12.5 in, 56 Count (05701)**.
[Kimberly-Clark identifies product 05701](https://www.kcprofessional.com/en-us/products/wiping-and-cleaning/process-cleaning/heavy-duty-cleaning-cloth/wypall%C2%AE-powerclean%E2%84%A2-l40-extra-absorbent-towels/05701)
as a 56-count pack suitable for food-preparation cleaning.

The source, linked items, decision references, and generated card now pass the
repository validator. The procedure becomes field-approved only after a camper
successfully completes it using the rendered card at the actual station.

## EMT shade procedures

The EMT shade must not be represented by one vague checklist row. Build,
inspection, repair, and strike are separate tasks:

- Assemble EMT shade
- Inspect EMT shade
- Repair EMT shade
- Strike EMT shade

### Assemble EMT shade status

The current workbook does not contain enough information to create a buildable
procedure. The following must be captured from the actual structure:

- structure geometry and orientation;
- tube lengths and tube labels;
- fitting topology and fitting labels;
- fastener and connection method;
- anchor type, quantity, placement, and connection;
- covering attachment method;
- required tools and protective equipment;
- approved crew size and roles;
- coordinated lifting sequence;
- wind and weather limits;
- final inspection criteria;
- approved drawing and manifest.

The initial build phases are expected to be:

1. Prepare the site.
2. Inventory and lay out components.
3. Assemble the roof frame.
4. Attach the covering at the validated stage and raise the structure.
5. Anchor, brace, inspect, and hand off.

This outline is an observation framework, not a field procedure. The real task
must be recorded while the Build Lead performs it, then validated against the
actual structure.

Expected STOP conditions include:

- missing or mismatched drawing or components;
- bent tubes or damaged fittings;
- interference with an emergency or service lane;
- wind catching the roof covering;
- communication made unreliable by dust or noise;
- an anchor that will not hold;
- an unstable unsupported section;
- a person beneath an unsupported frame;
- loss of coordinated control by the Build Lead;
- an impaired or physically unable worker.

### Inspect EMT shade starting point

A trained camper can perform a defined inspection without being authorized to
change the structure.

1. Inspect the covering for tears, loose edges, and excessive flapping.
2. Inspect every visible fitting for movement, cracks, or missing fasteners.
3. Inspect every leg and foot for bending, movement, or sinking.
4. Inspect every anchor and strap for loosening, damage, and abrasion.
5. Inspect for puddles, softened ground, sharp hardware, and blocked paths.
6. Compare questionable components with the PASS/FAIL photographs.
7. If a structural component fails, clear the affected area and notify the
   Build Lead. Do not improvise a repair.

The exact inspection points and PASS/FAIL photographs must come from the actual
approved structure.

## Flame, fuel, electrical, and mechanical tasks

The current Flame Effect Checklist is source material, not a newcomer-facing
procedure. It contains equipment-specific valve sequences, pressure values,
ambiguous component names, and unresolved decisions.

Before it can be used, the system owner must provide:

- actual equipment photographs;
- exact valve and component names;
- validated startup sequence;
- validated normal shutdown sequence;
- validated emergency shutdown sequence;
- operating limits;
- stop conditions;
- designated operator requirements;
- final-state verification.

An ordinary post-event checklist should not say “shut off flame effects — turn
off valves.” It should point to the authorized task and ask the shift worker to
verify its recorded completion without operating the valves.

The same separation applies to generator work:

- gauge inspection and reporting may be one task;
- refueling is a separate authorized task;
- troubleshooting and repair are separate authorized tasks.

## Initial validation

Validation should begin with practical errors that would make a task ambiguous
or impossible to render:

- duplicate task names or duplicate item names within one folder;
- an item reference whose icon does not resolve to an item with that name in
  the icon's folder;
- a missing required task or item column;
- a task with no selected checklist, Area, When, numbered Steps, or PASS when
  conditions;
- a categorized item outside an approved area folder;
- an item with no Ready for next person value;
- an unknown XML checklist membership or a non-Boolean Sheet checklist value;
- duplicate or invalid step numbering;
- a task-specific decision missing its date, status, text, or effect;
- a shared decision reference missing its record or status;
- a task decision `<record>` that is not found in the active or historical
  decision record;
- an unknown task decision status;
- a step using “check” without an inspection target or expected state;
- unresolved placeholders in a field-ready task;
- missing stop or escalation information where the task requires it;
- protected information in any import or XML file;
- a non-lossless XML/Sheet/XML round trip.

Controlled-language phrases such as “make sure,” “reasonably,” “properly,”
“some,” “enough,” “if necessary,” and “as needed” should initially produce
warnings for human review rather than automatic rejection.

## Production workflow

### 1. Inventory and normalize

Extract every actionable line from the allowlisted operational tabs in the ODS.
Merge true duplicates and record contradictions. Do not resolve contradictions
silently.

### 2. Assign decisions and ownership

Assign each unresolved decision to the relevant expert.

### 3. Observe the actual task

Have an experienced camper perform the work while another person records:

- video and photographs;
- tools and materials used;
- actual order;
- decisions and branches;
- common shortcuts and errors;
- failure conditions;
- the final acceptable state.

When experienced campers use different methods, the task expert selects one
canonical method.

### 4. Draft XML first

Create the task hierarchy and references in XML. Resolve terminology, sequence,
PASS when conditions, failures, and escalation before producing illustrations.

### 5. Prove Google Sheets conversion

Export the pilot XML to the clean Google Sheet. Have a human edit it, import it
back into XML, and verify that the repository diff contains only the intended
changes.

### 6. Conduct a no-coaching novice test

Give a newcomer the card, the actual equipment, and the required materials. The
observer does not explain unless safety requires intervention.

Record:

- where the worker stops;
- what they misinterpret;
- what they cannot locate;
- what they do in the wrong order;
- what they believe “done” means;
- every question they ask.

For a routine task, the initial target is:

- three newcomers complete it without verbal coaching;
- no safety-critical error occurs;
- all PASS when conditions are met;
- each person identifies when and to whom they should escalate.

Authorized tasks are not self-teaching tests. They require supervised training
and task-expert involvement.

### 7. Test under realistic conditions

Test the printout:

- under a headlamp;
- with appropriate gloves;
- in background noise;
- at the real station;
- with actual storage boxes;
- when the station is somewhat disorganized.

### 8. Produce visuals and outputs

Create expert-validated visuals only after the text and physical process are
stable. Render task cards, station posters, and the booklet from the same XML.

### 9. Revise from field evidence

Review a task when equipment or storage changes, a near miss occurs, a user
cannot complete it, the real procedure changes, or an external requirement
changes.

## Recommended implementation sequence

1. Keep the ODS unchanged as source evidence.
2. Validate the canonical kitchen-table task and its linked items.
3. Render the kitchen-table task card from XML.
4. Conduct the kitchen-table field test using the rendered card.
5. Revise the XML from observed problems and render again.
6. Implement XML-to-Google-Sheets export and the matching import only after the
   pilot fields are stable.
7. Prove a no-change XML/Sheet/XML round trip.
8. Add the next routine task.
9. Add restricted inspection tasks only after the routine format is proven.

## Open decisions

These must be resolved by the relevant experts rather than guessed by Codex:

- one generator escalation threshold and its measurement point;
- the aluminum-can disposal and recycling rule;
- the exact scope of generator gauge inspection versus refueling;
- the exact scope of propane inspection versus tank replacement;
- lost-and-found exceptions for food, trash, chemicals, sharps, and unsafe
  objects;
- gray-water routing and full-capacity response;
- actual shade geometry, hardware, anchors, and build sequence;
- actual flame-effect component names and operating procedures;
- what “mechanical issue” means for each inspected asset;
- the final allowlist of Boolean checklist-type columns;
- the final set of Sheet tabs and XML files after the pilot round trip.

## External references

External sources help identify hazards, regulations, and document-design
practices. They do not replace equipment-specific procedures or expert
validation.

Current operational and provisional-product research is recorded in
[SOURCES.md](SOURCES.md). The references below cover the documentation system
itself.

- [NASA: Human factors of flight-deck checklists](https://ntrs.nasa.gov/citations/19910017830)
- [NASA: Designing flightdeck procedures](https://ntrs.nasa.gov/citations/20160013263)
- [OSHA: Job Hazard Analysis](https://www.osha.gov/publications/publication-products?publication_title=job+hazard+analysis+guide)
- [GOV.UK functional standards writing style guide](https://www.gov.uk/government/publications/handbook-for-standard-managers/functional-standards-writing-style-guide)
- [Rodriguez: diagrammatic procedural instructions](https://journals.sagepub.com/doi/10.1177/154193120104500703)
- [Burning Man Survival Guide 2026: Leave No Trace](https://survival.burningman.org/leave-no-trace/what-to-pack-and-what-to-leave-at-home/)
- [Burning Man Survival Guide 2026: food and beverage permits](https://survival.burningman.org/rules-and-regulations/health-permits-are-required-for-food-and-beverage-service/)
- [Burning Man: securing structures](https://burningman.org/black-rock-city/preparation/camping-tips/securing-your-structure/)
- [Google Sheets API: read and write values](https://developers.google.com/workspace/sheets/api/guides/values)
- [Google Apps Script: extend Sheets](https://developers.google.com/apps-script/guides/sheets)
- [Google Sheets: protection and hiding are not security boundaries](https://support.google.com/docs/answer/1218656)
