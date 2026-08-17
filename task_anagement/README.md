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

## Decision record

Accepted design and working-style decisions are maintained in
[DECISIONS.md](DECISIONS.md). That record is authoritative for durable choices;
this README describes the resulting system.

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

The shift checklist will remain short. It is generated from checklist
memberships stored in each task XML, identifies assignments, and records their
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
- checklist or shift memberships stored directly on tasks;
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

Each task stores the expert to contact. If no expert is specified, the expert
is **Dominatrix**. Do not store phone numbers or other protected contact data.

## Document types

The system will produce connected documents rather than one enormous manual.

### 1. Global instructions

`global-instructions.xml` contains the short, durable instructions that apply
to every task:

- Stop and ask when instructions, equipment, or conditions do not match.
- Do not perform restricted work without authorization.
- Remove all MOOP.
- Return equipment to its labeled location.
- Restock consumables or report shortages.
- Tag broken equipment and report it.
- Leave the area ready for the next shift.
- Record completion, blockage, or escalation.

One global instruction connects every used item to its item-specific handoff
condition:

> Before marking PASS, return each used item to **Location** in the condition
> described by **Ready for next person**. If it does not match, follow **If not
> ready**.

Global instructions are automatically included in rendered task cards or their
standard completion section. Tasks do not reference them individually. If an
instruction does not apply to every task, it belongs in the applicable task
rather than this file.

### 2. Generated shift checklist

The shift checklist is generated from checklist memberships inside the task
XML. It is an index, assignment sheet, and execution record, not the full
procedure.

Example:

| Checklist | Task | Status | Initials | Time |
| --- | --- | --- | --- | --- |
| `MORNING` | Clean communal eating tables |  |  |  |
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

An item card contains only the item fields defined below. The item name is also
its identifier and should match the label placed on the physical item.

## Core data model

The field-by-field contract is maintained in the
[field dictionary](schema/field-dictionary.md).

The simplest mental models are:

> **TASK = NAME + CHECKLISTS + WHY + WHEN + TIME + RESOURCES + STEPS + PASS + PROBLEMS + EXPERT**

> **ITEM = NAME + LOCATION + READY BEFORE + READY FOR NEXT + IF NOT READY + RESPONSIBLE + PROBLEMS**

The name is the identifier for both tasks and items. Checklist memberships are
stored directly in each task. One global-instructions file provides behavior
that applies to every task.

Locations are deliberately not separate records. Each item stores its exact
physical location directly.

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
| **Task** | `task/name` | Unique task name and identifier. Start with a verb and name the outcome and place when needed, such as `Clean communal eating tables`. |
| **Checklist columns** | `checklists/checklist` | One Boolean column per approved checklist. Check every list on which the task must appear. |
| **Why** | `why` | Explain a non-obvious practical reason or consequence. Leave blank when the text would only restate the task. |
| **When** | `when` | State the time, event, or observable trigger for starting the task, such as `After dinner` or `When the bin reaches the marked line`. |
| **Time** | `time` | Realistic completion time under normal conditions, such as `10 minutes`. Leave blank until a useful value is known. |
| **What you need** | `resources/resource` | Everything required before starting: exact item names, consumables, help from other people, or a required expert. Use one resource per line, such as `Two additional people`. |
| **Steps** | `steps/step` | Numbered actions in execution order. Each step contains one physical action or observation. Include an expected result when it is not obvious and place IF/THEN text where the decision occurs. |
| **PASS when** | `passWhen/criterion` | Observable final conditions that must all be true before marking PASS. Use one criterion per line. |
| **Common problems** | `commonProblems/problem` | Likely problems not tied to one particular step. Pair each condition with a direct response, preferably as IF/THEN. |
| **Who to ask** | `expert` | Person to ask about the task. Leave blank to use **Dominatrix**. This appears after Common problems on the task card. |

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
| **Item** | `item/name` | Unique item name and identifier. Use the exact name printed on the physical item. |
| **Location** | `location` | Exact storage location using visible landmarks, container names, and shelf or side information. |
| **Ready before use** | `readyBeforeUse` | Observable condition required before someone starts using the item. |
| **Ready for next person** | `readyForNextPerson` | Observable condition in which the item must be returned, including cleaning, closing, charging, or restocking. |
| **If not ready** | `ifNotReady` | Immediate action when either ready condition is not met. State whether to stop, restock, tag, move, or notify someone. |
| **Who is responsible** | `responsible` | Person responsible for keeping the item available and resolving problems. Do not include private contact information. |
| **Common problems** | `commonProblems/problem` | Recurring problems during normal use and the direct response to each one. |

Each item is stored as an individual XML file under `data/items/`. A resource
line that exactly matches an item name links to that item record. Other resource
lines, such as `Two additional people`, remain plain requirements.

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
    Before marking PASS, return each used item to its Location and make sure it
    matches Ready for next person. If it does not, follow If not ready.
  </instruction>
</globalInstructions>
```

## XML representation

The exact XML schema will be refined when the first task is implemented. The
starting shape should keep the task readable and direct. Tasks reference items
by exact item name. The expert and checklist memberships are stored directly in
the task. A missing expert means **Dominatrix**.

Illustrative example:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<task>
  <name>Clean communal kitchen tables</name>

  <checklists>
    <checklist>Morning</checklist>
    <checklist>Afternoon</checklist>
  </checklists>

  <why/>
  <when>Once or more per shift</when>
  <time/>

  <resources>
    <resource>Communal Kitchen Tables</resource>
    <resource>Kitchen Cleaning Kit</resource>
    <resource>Kitchen Lost and Found</resource>
    <resource>Gray-Water IBC</resource>
    <resource>Kitchen Waste Station</resource>
  </resources>

  <steps>
    <step number="1">
      <action>Remove abandoned items from the table.</action>
      <ifThen>
        IF an item has no identifiable owner, THEN put it in Kitchen Lost and Found.
      </ifThen>
    </step>
    <step number="2">
      <action>Pick up MOOP from the tables, under the tables, and around the tables.</action>
      <expectedResult>No MOOP remains on, under, or around the tables.</expectedResult>
    </step>
    <step number="3">
      <action>Brush crumbs into the dustpan.</action>
      <expectedResult>No loose food remains.</expectedResult>
    </step>
  </steps>

  <passWhen>
    <criterion>No food or crumbs are visible.</criterion>
    <criterion>No MOOP is visible on, under, or around the tables.</criterion>
    <criterion>The table is dry.</criterion>
    <criterion>The Kitchen Cleaning Kit is ready for the next person.</criterion>
  </passWhen>

  <commonProblems/>

</task>
```

The task omits `<expert>`, so **Dominatrix** is used. Item-specific failures are
kept in their item records rather than repeated in task Common problems.

Illustrative item:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<item>
  <name>Kitchen Cleaning Kit</name>
  <location>Kitchen west wall, lower shelf, blue tote</location>
  <readyBeforeUse>Cleaner labeled and cloths clean</readyBeforeUse>
  <readyForNextPerson>All bottles closed and consumables stocked</readyForNextPerson>
  <ifNotReady>Stop using the kit and tell the Food Lead</ifNotReady>
  <responsible>Food Lead</responsible>
  <commonProblems>
    <problem>
      <condition>A bottle is leaking.</condition>
      <response>Stop using the kit and tell the Food Lead.</response>
    </problem>
  </commonProblems>
</item>
```

Expected future repository layout:

```text
task_anagement/
├── README.md
├── DECISIONS.md
├── schema/
│   ├── operations.xsd
│   └── field-dictionary.md
├── data/
│   ├── Treble Makers Camper Wiki.xml
│   ├── tasks/
│   │   └── Clean communal kitchen tables.xml
│   ├── items/
│   │   └── Kitchen Cleaning Kit.xml
│   └── global-instructions.xml
├── scripts/
│   ├── import-google-sheet
│   ├── export-google-sheet
│   ├── validate
│   └── render
└── build/
    ├── task-cards/
    ├── posters/
    └── booklet/
```

This is a proposed layout, not a requirement to create every directory before
the first pilot proves what is needed.

## Task-card content and order

Every task card should follow the same scanning order.

1. Task
2. Checklist memberships
3. Why
4. When
5. Time
6. What you need
7. Steps
8. PASS when
9. Common problems
10. Who to ask, showing **Dominatrix** when no other expert is specified

Each step contains one physical action or observation. Expected results and
IF/THEN decisions appear inside the applicable step rather than in separate
sections.

## What to keep, move, and add

### Keep on the task card

- exact item names;
- checklist memberships;
- observable physical instructions;
- visible or measurable PASS conditions;
- one-line Why and specific When;
- realistic Time and complete resources;
- common problems and who to ask.

### Move to shared records

- reusable refill, maintenance, and replacement information belongs on the
  item record;
- long background explanations belong in a reference document;
- frequently encountered exceptions should become IF/THEN branches at the
  relevant step.

## Treble Makers controlled-language standard

### 1. Use one name for each thing

Do not alternate between “water tank,” “tote,” “IBC,” and “reservoir.” Select an
exact name, such as `Gray-Water IBC`, and place the same name on the physical
item. That name is also its identifier; do not add a second code.

### 2. Title tasks with a verb, object, and place

Weak: `Kitchen tables`

Better: `Clean communal eating tables — kitchen`

### 3. Start steps with an action verb

Prefer verbs such as Remove, Read, Place, Wipe, Close, Return, and Report.

### 4. Put one action or observation in each step

Weak:

> Clean the table, return everything, and tell the Dominatrix if anything is
> missing.

Better:

1. Wipe the tabletop with the approved cleaner.
2. Return the `Kitchen Cleaning Kit` to its listed location.
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

> Remove all MOOP. Move bicycles outside the marked aisle. Put eligible
> abandoned items in `Lost and Found`. PASS: the aisle and seating entrances
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

## Pilot 1: Clean communal kitchen tables

This is the recommended first pilot because it is frequent, observable, and
relatively low-risk. It will expose problems with labels, locations, chemicals,
gray water, lost-and-found rules, PASS when conditions, restocking, and handoff.

The following is a prototype, not an approved procedure.

### Clean communal kitchen tables

- **Morning:** Yes
- **Afternoon:** Yes

#### Why

_Blank._

#### When

Once or more per shift.

#### Time

_Blank._

#### What you need

- Kitchen Cleaning Kit
- Brush and dustpan
- MOOP bag
- Gray-Water IBC
- Kitchen Lost and Found

#### Steps

1. Ask active users to remove their belongings.
2. Move eligible abandoned items according to the camp lost-and-found rule.
3. Pick up MOOP from the tables, under the tables, and around the tables. Put it
   in the correct waste container.
4. Brush dry crumbs and dust into the dustpan. Do not brush debris onto the
   playa.
5. Clean the tabletop and edges with the approved product until visible dirt,
   food, oil, and sticky residue are gone.
6. Sanitize designated food-contact surfaces with the camp-approved product and
   observe its required contact time.
7. Allow the surface to dry as directed by the product label.
8. Put all used liquid into the gray-water system. Do not put wastewater on the
   playa.
9. Return every item to its listed location.
10. Report low, empty, missing, leaking, or damaged supplies.

#### PASS when

- No food, crumbs, oil, or sticky residue is visible on the tables.
- No MOOP is visible on, under, or around the tables.
- The table is dry and immediately usable.
- Only approved communal items remain on the table.
- No cleaning equipment remains in the eating area.
- No cleaning liquid or wastewater reached the playa.
- The cleaning kit is returned and ready for the next shift.
- Missing or damaged supplies were reported.

#### Common problems

No task-specific common problems are currently defined. Problems with the
tables, cleaning kit, lost-and-found container, gray-water container, or waste
station belong to those item records.

#### Who to ask

Dominatrix

Before field use, the Food Lead must resolve the exact products, contact times,
locations, lost-and-found exceptions, gray-water method, and food-service
requirements.

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

- duplicate task or item names;
- an item name referenced by a task that does not exist;
- a missing required task or item column;
- a task with no selected checklist, When, numbered Steps, or PASS when
  conditions;
- an item with no Location, Ready before use, or Ready for next person value;
- an unknown XML checklist membership or a non-Boolean Sheet checklist value;
- duplicate or invalid step numbering;
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

Give a newcomer the card, labeled equipment, and required materials. The
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

1. Preserve the ODS unchanged as source evidence.
2. Create a contradiction and open-decision register.
3. Define the minimum XML schema needed for `Clean communal eating tables`.
4. Create `Clean communal eating tables.xml` with unresolved values clearly
   marked.
5. Implement one XML-to-Google-Sheets export path.
6. Implement the matching Google-Sheets-to-XML import path.
7. Prove a no-change round trip.
8. Conduct the kitchen-table field test.
9. Add MOOP collection and shower inspection.
10. Add generator gauge inspection to prove inspection-versus-intervention
    separation.
11. Add EMT shade inspection.
12. Add rendering only after the first task structure is stable.
13. Document the real EMT build before creating its field procedure.

## Open decisions

These must be resolved by the relevant experts rather than guessed by Codex:

- one generator escalation threshold and its measurement point;
- the aluminum-can disposal and recycling rule;
- the exact scope of generator gauge inspection versus refueling;
- the exact scope of propane inspection versus tank replacement;
- lost-and-found exceptions for food, trash, chemicals, sharps, and unsafe
  objects;
- approved kitchen cleaning and sanitizing products;
- chemical contact times and required protective equipment;
- gray-water routing and full-capacity response;
- actual shade geometry, hardware, anchors, and build sequence;
- actual flame-effect component names and operating procedures;
- what “mechanical issue” means for each inspected asset;
- the final allowlist of Boolean checklist columns;
- the final set of Sheet tabs and XML files after the pilot round trip.

## External references

External sources help identify hazards, regulations, and document-design
practices. They do not replace equipment-specific procedures or expert
validation.

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
