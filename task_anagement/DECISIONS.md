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

### D-103 — Names are identifiers

- **Date:** 2026-08-17
- **Status:** Accepted
- **Decision:** Tasks and items have one unique `<name>` field and no separate
  ID or title. Each XML filename matches its `<name>` exactly plus `.xml`.
- **Effect:** References use the exact name. Renaming updates the filename and
  every reference together.

### D-104 — One file per task or item

- **Date:** 2026-08-17
- **Status:** Accepted
- **Decision:** Store tasks under `data/tasks/` and items under `data/items/`,
  with one logical record per XML file.

### D-105 — Task field order

- **Date:** 2026-08-17
- **Status:** Accepted
- **Decision:** Task fields are **Task**, Boolean checklist columns, **Why**,
  **When**, **Time**, **What you need**, **Steps**, **PASS when**, **Common
  problems**, and **Who to ask**, in that order.
- **Effect:** **Who to ask** defaults to **Dominatrix**. Steps contain one
  action or observation, optional expected result, and decisions where they
  occur.

### D-106 — Item field order

- **Date:** 2026-08-17
- **Status:** Accepted
- **Decision:** Item fields are **Item**, **Location**, **Ready before use**,
  **Ready for next person**, **If not ready**, **Who is responsible**, and
  **Common problems**, in that order.

### D-107 — Checklist membership uses Boolean Sheet columns

- **Date:** 2026-08-17
- **Status:** Accepted
- **Decision:** TSV and Google Sheets use one Boolean column per approved
  checklist. XML stores only selected checklist memberships.
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

## Open decisions

Open operational questions remain in the specification's **Open decisions**
section. They are not decisions until the user or relevant camp expert resolves
them.
