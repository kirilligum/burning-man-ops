# Historical Decision Record

This file contains superseded decisions from the Treble Makers task system.
It preserves context without making the active decision record larger for
ordinary work.

Do not read this file by default. When a task XML contains a superseded
`<decisions><decision><record>` reference, use:

```bash
python3 task_anagement/scripts/extract-historical-decisions.py \
  "task_anagement/data/tasks/Clean_communal_kitchen_tables.xml"
```

The command reads the task XML, extracts its linked superseded decision IDs,
and prints only the matching records from this file.

## Working-style decisions

### D-008 — Identify exact products or exact preparation processes

- **Date:** 2026-08-17
- **Status:** Superseded by D-009
- **Decision:** Identify a purchased item with the manufacturer or store
  product title, size, and product number when available. If an item is made by
  camp, document its exact ingredients, quantities, and preparation steps.
- **Effect:** Do not use generic names such as `table cleaner` when a specific
  product must be obtained. Put multi-step preparation in its own task rather
  than hiding it in an item name.

### D-009 — Use short location-first item names

- **Date:** 2026-08-17
- **Status:** Superseded by D-111
- **Decision:** Name an item by its location and function or recognizable type,
  such as `Kitchen Multisurface Cleaner` or `Kitchen Disposable Towels`. Keep
  brand, model, size, and product numbers out of the name.
- **Effect:** The name matches the short physical label and remains readable in
  task steps. Put an exact replacement product in **If not ready** when needed.
  If the same supply is stocked in different locations, create separate items,
  such as `Kitchen Disposable Towels` and `Bar Disposable Towels`. Do not add a
  shared product catalog.

## System decisions

### D-103 — Names are identifiers

- **Date:** 2026-08-17
- **Status:** Superseded by D-111
- **Decision:** Tasks and items have one unique `<name>` field and no separate
  ID or title. Each XML filename matches its `<name>` exactly plus `.xml`.
- **Effect:** References use the exact name. Renaming updates the filename and
  every reference together.

### D-105 — Task field order

- **Date:** 2026-08-17
- **Status:** Superseded by D-111
- **Decision:** Task fields are **Task**, Boolean checklist columns, **Why**,
  **When**, **Time**, **What you need**, **Steps**, **PASS when**, **Common
  problems**, and **Who to ask**, in that order.
- **Effect:** **Who to ask** defaults to **Dominatrix**. Steps contain one
  action or observation, optional expected result, and decisions where they
  occur.

### D-106 — Item field order

- **Date:** 2026-08-17
- **Status:** Superseded by D-111
- **Decision:** Item fields are **Item**, **Location**, **Ready before use**,
  **Ready for next person**, **If not ready**, **Who is responsible**, and
  **Common problems**, in that order.

### D-111 — Organize tasks and items by categorical area

- **Date:** 2026-08-17
- **Status:** Superseded by D-112
- **Decision:** Every task has one **Area** selected from **Public area**,
  **Bar/Cheese**, **Propane area**, **Common area**, **Kitchen**, and **Private
  infrastructure**. Store item XML in the corresponding `data/items/` folder;
  use `bar-cheese/` for **Bar/Cheese** because `/` is a path separator.
- **Effect:** Item names contain only the short function or recognizable type,
  such as `Multisurface Cleaner` or `Disposable Towels`. An item's area folder
  plus name is its identifier, so the same name may exist in multiple area
  folders. A task resolves its item references within its area. **Area** appears
  after checklist columns on tasks and after **Item** on Sheet item rows.

### D-114 — Use Stash Bins as the waste destination

- **Date:** 2026-08-18
- **Status:** Superseded by D-115
- **Decision:** Use **Stash Bins** as the item name and waste destination for
  this task.
- **Effect:** Superseded by the correction to **Trash Bins**.

### D-122 — Escalate only unclear problems globally

- **Date:** 2026-08-18
- **Status:** Superseded by D-129
- **Decision:** The global escalation instruction is: `If a problem occurs and
  the solution is not clear, tell the Dominatrix.`
- **Effect:** D-129 consolidates missing items, unclear instructions, and
  unclear solutions into one worker-facing instruction. Item and task records
  still provide a concrete response whenever one is known.

### D-132 — Keep one prioritized open-question queue

- **Date:** 2026-08-18
- **Status:** Superseded by D-133
- **Decision:** Store unresolved questions requiring the user or a camp expert
  in `ask_me/README.md`, ordered from highest to lowest operational priority.
- **Effect:** D-133 replaces the single generic queue with multiple descriptive,
  timestamped question files under `ask_me/`.
