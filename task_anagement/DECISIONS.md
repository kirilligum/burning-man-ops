# Decision Record

This file records accepted, durable decisions for the Treble Makers task system
and the working style expected from agents. It is not a backlog or a place for
tentative suggestions.

## How to use this record

- Read this file before proposing or making task-system changes.
- Treat **Accepted** decisions as constraints.
- The user's newest explicit instruction wins. When it changes a recorded
  decision, mark the old entry **Superseded** and add the replacement.
- Add a decision only after the user explicitly accepts it or asks for the
  change. Do not convert an agent suggestion into a decision.
- Update the specification, examples, and affected XML in the same change when
  an accepted decision makes them stale.
- Keep entries concise. Record the decision and its practical effect, not the
  full conversation.

Superseded entries are kept in
[HISTORICAL_DECISIONS.md](HISTORICAL_DECISIONS.md) to keep this active record
small. Do not read the historical record during ordinary task work. For a deep
dive, use the task XML's `<decisions><decision><record>` references and the
lookup command documented in `AGENTS.md`.

## Working-style decisions

### D-001 — Prefer the smallest useful system

- **Date:** 2026-08-17
- **Status:** Accepted
- **Decision:** Apply KISS. Use the fewest fields, files, relationships, and
  workflows that satisfy a demonstrated need.
- **Effect:** Do not add separate IDs, lookup entities, relationship tables,
  approval states, risk matrices, or abstraction layers without an accepted
  requirement.

### D-002 — Separate proposals from accepted changes

- **Date:** 2026-08-17
- **Status:** Accepted
- **Decision:** Clearly label suggestions. Do not silently incorporate them
  into the specification or XML before the user accepts them.
- **Effect:** When asked for feedback, give a direct recommendation first and
  keep the repository read-only unless a change is also requested.

### D-003 — Use source facts and user knowledge

- **Date:** 2026-08-17
- **Status:** Accepted
- **Decision:** Draft from the workbook, existing XML, and facts supplied by
  the user. Do not invent equipment details, locations, quantities, timings,
  thresholds, or generic safety scenarios.
- **Effect:** Mark genuinely unknown values for field testing or resolution.
  Leave a field blank when the only available text would be obvious filler. Do
  not pad procedures with obvious edge cases merely to appear complete.

### D-004 — Put information at its narrowest owner

- **Date:** 2026-08-17
- **Status:** Accepted
- **Decision:** Universal behavior belongs in global instructions; location,
  readiness, and item-specific problems belong in items; execution and
  task-specific decisions belong in tasks; on-playa results belong in the
  generated checklist.
- **Effect:** Do not duplicate item failures in every task that uses the item.

### D-005 — Match the user's language and order

- **Date:** 2026-08-17
- **Status:** Accepted
- **Decision:** Preserve agreed field names, ordering, terminology, and exact
  task or item names. Lead with the answer and keep explanations concise.
- **Effect:** Do not rename or reorder categories for theoretical consistency.
  If a normalized task name is needed, explain it once and use it everywhere.

### D-006 — Tasks are minimum by default

- **Date:** 2026-08-17
- **Status:** Accepted
- **Decision:** Start every task with the minimum resources, actions, and PASS
  criteria needed to complete and verify it.
- **Effect:** Add detail only for a concrete operational need. Do not add
  supplies, steps, expected results, problems, or safety text by default.

### D-007 — Make physical resources directly recognizable

- **Date:** 2026-08-17
- **Status:** Accepted
- **Decision:** Name required physical resources at the level at which a worker
  can recognize them directly. Do not use a kit name that hides the components
  needed for the task.
- **Effect:** A worker can identify every resource directly from the task.
  Create a separate item record for each component named by the task. A visibly
  identifiable station or group does not need to be split unnecessarily.

## System decisions

### D-101 — XML is the repository source of truth

- **Date:** 2026-08-16
- **Status:** Accepted
- **Decision:** Agents edit XML. People edit Google Sheets. Conversion between
  them must be deterministic and lossless.
- **Effect:** Import outstanding Sheet changes before XML editing and do not
  edit both surfaces concurrently.

### D-102 — The workbook is evidence, not canonical data

- **Date:** 2026-08-16
- **Status:** Accepted
- **Decision:** `Treble Makers Checklists - 2026.ods` is an archive used to
  inventory tasks and contradictions; it is not migrated wholesale.

### D-104 — One file per task or item

- **Date:** 2026-08-17
- **Status:** Accepted
- **Decision:** Store tasks under `data/tasks/` and items under `data/items/`,
  with one logical record per XML file.

### D-107 — Checklist membership uses Boolean Sheet columns

- **Date:** 2026-08-17
- **Status:** Accepted
- **Decision:** TSV and Google Sheets use one Boolean column per approved
  checklist type. XML stores only selected checklist types under
  `<checklist_types>`.
- **Effect:** Do not use a delimited checklist cell or a separate checklist
  relationship file.

### D-108 — Global instructions use one shared XML file

- **Date:** 2026-08-17
- **Status:** Accepted
- **Decision:** Instructions that apply to every task live in
  `data/global-instructions.xml` and are rendered automatically.

### D-109 — Execution status is runtime data

- **Date:** 2026-08-16
- **Status:** Accepted
- **Decision:** `PASS`, `BLOCKED`, `ESCALATED`, `NOT APPLICABLE`, initials, and
  completion time are marked by the worker in the generated checklist at
  Burning Man. They are not publication statuses.

### D-110 — Exclude protected information

- **Date:** 2026-08-16
- **Status:** Accepted
- **Decision:** Do not store phone exports, private incident details, bookings,
  payments, credentials, secrets, or private contact information.

### D-112 — Keep uncategorized items at the item root

- **Date:** 2026-08-18
- **Status:** Accepted
- **Decision:** Store categorized items in their categorical area folder. Store
  an item that does not belong to an area directly under `data/items/`.
- **Effect:** Root items have a blank **Area** value in TSV and Google Sheets.
  `📦 Communal_Tables`, `📦 Lost_and_Found`, and `📦 Trash_Bins` are root
  items. Item references resolve through their category icon as defined by
  D-128.

### D-113 — Keep task reasoning and decisions in task XML

- **Date:** 2026-08-18
- **Status:** Accepted
- **Decision:** Add optional `<reasoning>` entries and `<decisions>` records to
  each task XML. A reasoning entry records a concise rationale. A task-specific
  decision contains `date`, `status`, `text`, and `effect`.
- **Effect:** Maintainers and Codex can review why a task is shaped a certain
  way and which task-specific choices were accepted without adding prose to
  the read-do procedure. Renderers omit these fields from task cards by
  default. Operational IF/THEN branches remain in the relevant step.
  Project-wide choices remain in this file.

### D-115 — Use Trash Bins as the waste destination

- **Date:** 2026-08-18
- **Status:** Accepted
- **Decision:** Use **📦 Trash_Bins** as the item ID and waste destination for
  this task.
- **Effect:** The task and its examples refer to the individual destination as
  **📦 Trash_Bins** without an `.xml` extension.

### D-116 — Omit rare item preconditions covered by global escalation

- **Date:** 2026-08-18
- **Status:** Accepted
- **Decision:** Leave an item's **Ready before use** field blank when the
  condition is rare and the global instruction already says to escalate any
  problem to the Dominatrix.
- **Effect:** Do not spend procedure space describing unlikely damage or other
  rare pre-use conditions. Keep the field available for items where a normal
  pre-use check is useful.

### D-117 — Separate active and historical decision records

- **Date:** 2026-08-18
- **Status:** Accepted
- **Decision:** Keep current accepted decisions in `DECISIONS.md` and move
  superseded entries to `HISTORICAL_DECISIONS.md`. Task XML may link a past
  decision with a `<record>` ID.
- **Effect:** Agents read the smaller active record by default. For a deep dive,
  `extract-historical-decisions.py` parses the task XML and prints only the
  linked historical records.

### D-118 — Use underscore IDs and shared reference icons

- **Date:** 2026-08-18
- **Status:** Accepted
- **Decision:** Replace spaces with underscores in task and item names and
  filenames. References use the ID without the `.xml` extension. Prefix task
  references with `📋`. Prefix item references with one icon determined by the
  item's area folder; use `📦` for uncategorized root items.
- **Effect:** IDs are safe to use in filenames and references without quoting.
  Icons identify the reference type or item category and are not part of the
  canonical ID. The current item icon mapping is `Public area=🌐`,
  `Bar/Cheese=🍷`, `Propane area=🔥`, `Common area=🏕️`, `Kitchen=🍳`,
  `Private infrastructure=🔧`, and uncategorized=`📦`.

### D-119 — Name task checklist-type elements explicitly

- **Date:** 2026-08-18
- **Status:** Accepted
- **Decision:** Store selected checklist memberships in each task under
  `<checklist_types>`, with one `<checklist_type>` child for each selected
  checklist type.
- **Effect:** The XML distinguishes the collection of checklist types from an
  individual checklist type. Google Sheets still exposes one Boolean column per
  checklist type, and generated field checklists use the selected values.

### D-120 — Collect MOOP for every task

- **Date:** 2026-08-18
- **Status:** Accepted
- **Decision:** Add `Collect all MOOP.` to the shared global instructions.
- **Effect:** Every task includes MOOP collection as a completion requirement;
  task-specific MOOP locations or destinations remain in the task XML.

### D-121 — Omit obvious item problems

- **Date:** 2026-08-18
- **Status:** Accepted
- **Decision:** Do not repeat an obvious item problem when the global escalation
  instruction already gives the correct response.
- **Effect:** Keep item **Common problems** limited to non-obvious,
  item-specific responses that require separate instruction.

### D-123 — Use Dominatrix only as the unknown-reference fallback

- **Date:** 2026-08-18
- **Status:** Accepted
- **Decision:** Use the clearest available task, item, location, role, or
  global-instruction reference. Ask the Dominatrix when the required reference
  or response is unknown or unclear.
- **Effect:** Dominatrix is a fallback for unresolved documentation gaps. As a
  useful reference becomes available, replace the fallback with that reference.

### D-124 — Physical item labels are optional

- **Date:** 2026-08-18
- **Status:** Accepted
- **Decision:** Do not assume that camp items have physical labels. Use the
  item's location and recognizable form; mention a label only when it is known
  to be present or intentionally added.
- **Effect:** Item IDs remain canonical repository references without requiring
  a physical labeling project.

### D-125 — Keep obvious item readiness global

- **Date:** 2026-08-18
- **Status:** Accepted
- **Decision:** Omit `readyBeforeUse` and `ifNotReady` when they only say that
  an item should be available or repeat the global instruction to ask the
  Dominatrix when the item cannot be found.
- **Effect:** Keep item records focused on non-obvious readiness conditions and
  concrete item-specific responses.

### D-126 — Handle multisurface-cleaner replacement and spraying

- **Date:** 2026-08-18
- **Status:** Accepted
- **Decision:** Keep the cleaner handoff condition to the bottle containing
  cleaner. If it does not spray, turn the nozzle from `OFF` to `ON`. When it
  must be replaced, ask the Dominatrix where to find the replacement, dispose
  of the old bottle in `📦 Trash_Bins`, and get the replacement.
- **Effect:** Do not make the normal handoff depend on the nozzle's OFF state;
  keep that state in the concrete common-problem response.

### D-127 — Keep item IDs short and descriptions detailed

- **Date:** 2026-08-18
- **Status:** Accepted
- **Decision:** Add an optional item `<description>` for recognizable details,
  brand, model, size, or product information. Keep those details out of the
  item name and filename.
- **Effect:** `Multisurface_Cleaner` remains the item ID while its exact Clorox
  product details live in `<description>`.

### D-128 — Resolve item references by their icon

- **Date:** 2026-08-18
- **Status:** Accepted
- **Decision:** The icon at the start of an item reference determines the item
  folder. The remaining underscore name is the item ID within that folder.
- **Effect:** `🍳 Multisurface_Cleaner` resolves only to
  `data/items/kitchen/Multisurface_Cleaner.xml`; `📦 Trash_Bins` resolves only
  to `data/items/Trash_Bins.xml`. References remain deterministic when the same
  item name exists in more than one area.

### D-129 — Keep global worker instructions minimal

- **Date:** 2026-08-18
- **Status:** Accepted
- **Decision:** Global XML contains only instructions that every worker must
  apply to every task. Authoring rules stay in the specification and
  `AGENTS.md`.
- **Effect:** Every task tells the worker to return used items ready for the
  next person, collect MOOP, and ask the Dominatrix when an item, instruction,
  or solution is missing or unclear. D-129 supersedes D-122's narrower wording.

### D-130 — Allow an item to omit Location

- **Date:** 2026-08-18
- **Status:** Accepted
- **Decision:** Item **Location** is optional when the item is recognizable at
  the task site or may be found in multiple obvious places.
- **Effect:** `Trash_Bins` may omit `<location>`. Keep a location whenever it
  materially helps a newcomer find the item.

### D-131 — Reference shared decisions without copying them

- **Date:** 2026-08-18
- **Status:** Accepted
- **Decision:** A task-specific decision keeps its full fields in task XML. A
  decision already stored in the active or historical decision record is
  linked from a task with only `record` and `status`.
- **Effect:** Task XML retains traceability without loading duplicated decision
  text. The historical lookup continues to use superseded record links.

### D-133 — Use descriptive timestamped question files

- **Date:** 2026-08-18
- **Status:** Accepted
- **Decision:** Store each question batch in its own Markdown file under
  `ask_me/`. Use a descriptive `snake_case` name followed by a timestamp from
  `date -Is`, replacing colons with hyphens for filename portability.
- **Effect:** Multiple question files can coexist without a generic
  `ask_me/README.md`. Questions remain coordination records rather than
  decisions or canonical operational data. Do not store protected runtime
  details in them.

## Open decisions

Open operational questions remain in timestamped files under `ask_me/`. They
are not decisions until the user or relevant camp expert resolves them.
