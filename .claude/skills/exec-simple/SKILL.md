---
name: exec-simple
description: Execute exactly one unfinished task section from a markdown plan file, then stop. Use when the user says "exec-simple", "run next task", or wants to advance a plan one step at a time without progress logging.
allowed-tools: Read, Edit, Write, Bash, Glob, Grep, Agent, TaskCreate, TaskUpdate
---


# exec-simple

Execute exactly ONE uncompleted task section from a plan file, then stop.

## Input

The argument is the path to the plan file, e.g.:

```
$exec-simple docs/plans/my-plan.md
```

If no path is given, look for a single plan file under `docs/plans/` and use it. If multiple exist, ask the user which one.

## Steps

Read the plan file. Find the FIRST `### Task N:` or `### Iteration N:` section that contains uncompleted checkboxes (`[ ]`).

If NO task section has `[ ]` but `## Success criteria`, `## Overview`, or `## Context` still has `[ ]`: either satisfy those items and mark them `[x]` if actionable, or output `<<<ALL_TASKS_DONE>>>` if they are verification-only (manual testing, deployment, etc.).

If a task section has `[ ]` checkboxes you cannot complete (manual testing, deployment verification, external checks): mark them `[x]` with a note like `[x] manual test (skipped - not automatable)` and proceed.

### STEP 0 - ANNOUNCE

Before starting work, output a brief overview (up to 200 words) explaining:
- Which task number you picked and its title
- What the task will accomplish
- Key files or components involved

### STEP 1 - IMPLEMENT

- Read the plan's Overview and Context sections to understand the work
- Implement ALL items in the current task section (all `[ ]` checkboxes under it)

### STEP 2 - VALIDATE

- Run any test and lint commands specified in the plan
- Fix any failures, repeat until all validation passes

### STEP 3 - COMPLETE

- Edit the plan file: change `[ ]` to `[x]` for each checkbox you implemented in the current task section
- If task sections are complete but `## Success criteria`, `## Overview`, or `## Context` has `[ ]` items now satisfied, mark those `[x]` too
- Commit all changes (code + updated plan) with message: `feat: <brief task description>`
- Check if any `[ ]` checkboxes remain in task sections
- If NO more `[ ]` checkboxes anywhere in the plan, output exactly: `<<<ALL_TASKS_DONE>>>`
- If more task sections have `[ ]` checkboxes, STOP - do not continue to the next section

If any phase fails after reasonable fix attempts, output exactly: `<<<TASK_FAILED>>>`

## Constraints

- Complete ONE task section per invocation - no more
- After committing, stop and let the user (or a loop) call again for the next section
- No markdown formatting in output (no **bold**, `code spans`, `# headers`) - plain text and `-` lists only
- Do not echo phase names or step numbers - just do the work
