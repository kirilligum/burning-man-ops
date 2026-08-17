# Field Dictionary

This document defines the fields shared by repository XML, TSV exports, Google
Sheets, and rendered task cards. XML is canonical. Sheet headings are the
human-facing names.

Task and item names are their identifiers. They are unique within their record
type and matched exactly, including capitalization. Renaming one requires every
reference and its XML filename to change together.

## Task fields

| Sheet column | XML path | Type | Required | Definition |
| --- | --- | --- | --- | --- |
| **Task** | `/task/name` | Text | Yes | Unique verb-first task name and identifier. Name the outcome and place when needed. |
| **Checklist columns** | `/task/checklists/checklist` | Boolean membership | Yes | One Boolean column per approved checklist. At least one must be `TRUE`; XML stores only `TRUE` memberships. |
| **Why** | `/task/why` | Text | No | One short sentence describing a non-obvious practical benefit or consequence. Leave blank when it would only restate the task. |
| **When** | `/task/when` | Text | Yes | Time, event, or observable trigger for starting the task. |
| **Time** | `/task/time` | Text duration | No | Realistic duration under normal conditions, such as `10 minutes`. Leave blank until a useful value is known. |
| **What you need** | `/task/resources/resource` | Multiline text | No | Only items, materials, helpers, or required presence without which the task cannot be completed. Name physical resources so each can be recognized directly. If a kit name hides required components, list those components separately. Use one resource per line. An exact item name links to that item. |
| **Steps** | `/task/steps/step` | Ordered multiline structure | Yes | The fewest read-do actions needed, in execution order. At least one step is required. |
| **PASS when** | `/task/passWhen/criterion` | Multiline text | Yes | The minimum observable conditions needed to verify completion. Use one criterion per line. |
| **Common problems** | `/task/commonProblems/problem` | Multiline IF/THEN text | No | Likely task-level problems not owned by an item or tied to one step. Use one condition and response per line. |
| **Who to ask** | `/task/expert` | Text | No | Person to ask about the task. Blank or an omitted element means **Dominatrix**. Do not include contact information. |

The Sheet and task card order is exactly the order above, with the Boolean
checklist columns immediately after **Task** and **Who to ask** after **Common
problems**.

## Checklist Boolean fields

Each approved checklist has one TSV/Sheet column containing only `TRUE` or
`FALSE`. Google Sheets displays these as checkboxes. In XML, a `TRUE` value is a
`<checklist>` element; absence means `FALSE`.

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
| **Item** | `/item/name` | Text | Yes | Unique item name and identifier, matching the physical label. For a purchased item, use its exact product title, size, and manufacturer or store product number when available. For a camp-made item, use its exact physical label and document preparation in the task that makes it. |
| **Location** | `/item/location` | Text | Yes | Storage location using visible labels and landmarks. |
| **Ready before use** | `/item/readyBeforeUse` | Text | Yes | Observable state required before someone uses the item. |
| **Ready for next person** | `/item/readyForNextPerson` | Text | Yes | Observable state in which the item must be returned. |
| **If not ready** | `/item/ifNotReady` | Text | Yes | Immediate action when either ready condition is not met. |
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
- Reject duplicate task or item names and unknown exact-name references.
- Do not derive names from row numbers or positions.
- Do not place multiple resources, criteria, or problems on one line.
- Empty optional fields remain empty; converters do not invent content.
- Never store phone numbers, credentials, private incident details, or other
  protected information.
