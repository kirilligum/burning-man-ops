# Field Dictionary

This document defines the fields shared by repository XML, TSV exports, Google
Sheets, and rendered task cards. XML is canonical. Sheet headings are the
human-facing names.

Task names are globally unique identifiers using underscores instead of spaces.
An item is identified by its parent folder plus its name. Categorized items use
an area folder; uncategorized items live directly under `data/items/`. Names are
unique within a folder and may repeat in different folders. Canonical IDs and
references match exactly, including capitalization; reference icons are prefixes
and are not part of IDs.

## Task fields

| Sheet column | XML path | Type | Required | Definition |
| --- | --- | --- | --- | --- |
| **Task** | `/task/name` | Text | Yes | Unique verb-first task ID using underscores instead of spaces. Name the outcome and place when needed. |
| **Checklist type columns** | `/task/checklist_types/checklist_type` | Boolean membership | Yes | One Boolean column per approved checklist type. At least one must be `TRUE`; XML stores only selected checklist types. |
| **Area** | `/task/area` | Enum | Yes | Categorical camp area where the task and its item references belong. Use one approved area value. |
| **Why** | `/task/why` | Text | No | One short sentence describing a non-obvious practical benefit or consequence. Leave blank when it would only restate the task. |
| **When** | `/task/when` | Text | Yes | Time, event, or observable trigger for starting the task. |
| **Time** | `/task/time` | Text duration | No | Realistic duration under normal conditions, such as `10 minutes`. Leave blank until a useful value is known. |
| **What you need** | `/task/resources/resource` | Multiline text | No | Only items, materials, helpers, or required presence without which the task cannot be completed. An item reference is its area icon followed by its underscore ID; other resources remain plain text. Use one resource per line. Resolve the ID first in the task's Area folder and then directly under `data/items/`. |
| **Steps** | `/task/steps/step` | Ordered multiline structure | Yes | The fewest read-do actions needed, in execution order. At least one step is required. |
| **PASS when** | `/task/passWhen/criterion` | Multiline text | Yes | The minimum observable conditions needed to verify completion. Use one criterion per line. |
| **Common problems** | `/task/commonProblems/problem` | Multiline IF/THEN text | No | Likely task-level problems not owned by an item or tied to one step. Use one condition and response per line. |
| **Who to ask** | `/task/expert` | Text | No | Specific person or role to ask about the task. Blank or an omitted element means **Dominatrix** only when no clearer expert or reference is known. Do not include contact information. |
| **Reasoning** | `/task/reasoning/entry` | Multiline text | No | Concise rationale for the task's order, scope, or omissions. Maintainer record; not shown on the task card by default. |
| **Decisions** | `/task/decisions/decision` | Structured record list | No | Task-specific decisions that explain the accepted procedure. Each record has `date`, `status`, `text`, and `effect`; add `record` when it links to a global decision ID. Maintainer record; not shown on the task card by default. |

The Sheet task-definition field order is exactly the order above, with the
Boolean checklist-type columns immediately after **Task**, **Area** after those
columns, and **Who to ask** after **Common problems**. **Reasoning** and
**Decisions** follow the execution fields as review metadata; they are not part
of the default task card.

## Area values

| Area value | Item folder |
| --- | --- |
| Blank | `data/items/` |
| `Public area` | `data/items/public area/` |
| `Bar/Cheese` | `data/items/bar-cheese/` |
| `Propane area` | `data/items/propane area/` |
| `Common area` | `data/items/common area/` |
| `Kitchen` | `data/items/kitchen/` |
| `Private infrastructure` | `data/items/private infrastructure/` |

## Reference icons

Icons are display prefixes. They are not part of task or item IDs.

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

## Checklist-type Boolean fields

Each approved checklist has one TSV/Sheet column containing only `TRUE` or
`FALSE`. Google Sheets displays these as checkboxes. In XML, a `TRUE` value is a
`<checklist_type>` element inside `<checklist_types>`; absence means `FALSE`.

| Candidate column | XML value when `TRUE` | Meaning |
| --- | --- | --- |
| **Morning Dominatrix** | `Morning Dominatrix` | Include on the Morning Dominatrix checklist. |
| **Evening Dominatrix** | `Evening Dominatrix` | Include on the Evening Dominatrix checklist. |
| **Morning** | `Morning` | Include on the general Morning checklist. |
| **Infra Lead** | `Infra Lead` | Include on the Infra Lead checklist. |
| **Shower** | `Shower` | Include on the Shower checklist. |
| **Liaison** | `Liaison` | Include on the Liaison shift checklist. |
| **Pre-event** | `Pre-event` | Include on the checklist completed before an event. |
| **Bar** | `Bar` | Include on the Bar shift checklist. |
| **Afternoon** | `Afternoon` | Include on the Afternoon checklist. |
| **Cheese** | `Cheese` | Include on the Cheese shift checklist. |
| **Post-event** | `Post-event` | Include on the checklist completed after an event. |
| **Flame Effects** | `Flame Effects` | Include on the restricted Flame Effects checklist. |
| **Build** | `Build` | Include on the camp Build checklist. |
| **Strike** | `Strike` | Include on the camp Strike checklist. |

This is a candidate allowlist derived from the archive. The camp must confirm
which columns remain current before conversion is implemented.

## Step fields

| XML field | Type | Required | Definition |
| --- | --- | --- | --- |
| `step/@number` | Positive integer | Yes | Sequential display order beginning with `1`. |
| `action` | Text | Yes | One physical action or observation beginning with an action verb. |
| `expectedResult` | Text | No | Observable result when the action's outcome is not obvious. |
| `ifThen` | Text | No | Decision placed at the step where it occurs, written as `IF … THEN …`. |

The **Steps** Sheet cell uses this deterministic layout:

```text
1. Action
   EXPECTED: Observable result
   IF condition, THEN response
2. Next action
```

## Item fields

| Sheet column | XML path | Type | Required | Definition |
| --- | --- | --- | --- | --- |
| **Item** | `/item/name` | Text | Yes | Short functional item ID using underscores instead of spaces and matching the XML filename, such as `Disposable_Towels`. Keep area, brand, model, size, and product numbers out of the ID. The ID must be unique within its parent folder. |
| **Description** | `/item/description` | Text | No | Recognizable description, brand, model, size, or product detail. Keep these details out of the item ID. |
| **Area** | Parent folder under `data/items/` | Enum | No | Categorical camp area. It is derived from the XML folder and exported as a Sheet column; it is not duplicated inside the item XML. Blank means the item is stored directly under `data/items/`. |
| **Location** | `/item/location` | Text | Yes | Storage location using landmarks and labels when available. Labels are optional. |
| **Ready before use** | `/item/readyBeforeUse` | Text | No | Observable state required before someone uses the item. Leave blank when availability is obvious or the global instructions already cover not finding the item. |
| **Ready for next person** | `/item/readyForNextPerson` | Text | Yes | Observable state in which the item must be returned. |
| **If not ready** | `/item/ifNotReady` | Text | No | Immediate item-specific action when a ready condition is not met. Leave blank when the global instructions cover the response. |
| **Who is responsible** | `/item/responsible` | Text | Yes | Person responsible for keeping the item available and resolving problems. Do not include contact information. |
| **Common problems** | `/item/commonProblems/problem` | Multiline IF/THEN text | No | Recurring item-specific problems and their direct responses. |

## Problem fields

Every task or item problem contains both fields:

| XML field | Required | Definition |
| --- | --- | --- |
| `condition` | Yes | Observable problem, without a hidden conclusion or vague adjective. |
| `response` | Yes | Immediate action to take when the condition occurs. |

The Sheet cell renders each problem as `IF [condition], THEN [response]`, one
problem per line.

## Task reasoning and decision records

These are optional maintainer fields. They preserve why a task is shaped a
certain way and which task-specific choices were accepted without adding prose
to the read-do procedure.

```xml
<reasoning>
  <entry>Remove dry debris before wet cleaning so cleaner is used only when needed.</entry>
</reasoning>
<decisions>
  <decision>
    <date>2026-08-18</date>
    <status>Accepted</status>
    <text>Use a final MOOP sweep after conditional spot-cleaning.</text>
    <effect>Keep the final sweep last so it catches material displaced during cleaning.</effect>
  </decision>
</decisions>
```

`reasoning/entry` is one concise rationale per entry. Each `decisions/decision`
must contain the four child fields `date`, `status`, `text`, and `effect`. The
optional `record` child links to a global decision ID such as `D-114` when the
task decision has a corresponding entry in `DECISIONS.md` or
`HISTORICAL_DECISIONS.md`. `status` is one of `Accepted`, `Superseded`, or
`Open`; only `Accepted` records govern the current task. Project-wide decisions
remain in `task_anagement/DECISIONS.md`. These records explain the procedure;
an operational branch still belongs in a step's `ifThen` field. Converters must
preserve these records, including order and empty optional values.

## Global-instruction field

| Sheet column | XML path | Type | Required | Definition |
| --- | --- | --- | --- | --- |
| **Instruction** | `/globalInstructions/instruction` | Text | Yes | One direct instruction that applies to every task. Task-specific or conditional instructions do not belong here. |

## Generated execution fields

These fields appear in the generated **CHECKLIST** Sheet and are not task
definition fields.

| Sheet column | Type | Editable on playa | Definition |
| --- | --- | --- | --- |
| **Checklist** | Generated text | No | Checklist that caused this task occurrence to appear. |
| **Task** | Generated text | No | Exact task name and link to its task card. |
| **Status** | Enum | Yes | Blank until worked, then `PASS`, `BLOCKED`, `ESCALATED`, or `NOT APPLICABLE`. |
| **Initials** | Text | Yes | Initials of the person who worked the task. |
| **Completion time** | Time | Yes | Time the person finished, blocked, or escalated the task; distinct from task **Time**, which is expected duration. |

## General value rules

- Trim leading and trailing whitespace while preserving meaningful line breaks.
- Reject spaces in task and item IDs. Replace each space with `_`; do not put
  the reference icon or `.xml` extension in the ID.
- Reject duplicate task names, duplicate item names within one folder, and item
  references missing from both the task's Area folder and the item root.
- Permit the same item name in different folders. Resolve the task's Area
  folder before the item root.
- Do not derive names from row numbers or positions.
- Do not place multiple resources, criteria, or problems on one line.
- Empty optional fields remain empty; converters do not invent content.
- Never store phone numbers, credentials, private incident details, or other
  protected information.
