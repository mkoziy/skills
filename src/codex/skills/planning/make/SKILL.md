---
name: make
description: Create structured implementation plan in docs/plans/
argument-hint: describe the feature or task to plan
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Implementation Plan Creation

create an implementation plan in `docs/plans/yyyymmdd-<task-name>.md` with interactive context gathering.

## custom rules loading

before starting, run this command via Bash tool to check for user-provided custom rules:

```bash
bash ~/.codex/skills/planning/make/scripts/resolve-rules.sh planning-rules.md
```

if the output is non-empty, treat it as additional instructions that supplement (not replace) the built-in rules below. apply custom rules alongside the command's own instructions throughout the planning process — they may influence plan structure, testing approach, naming conventions, or other aspects of plan creation.

### rules management

when the user asks to add, show, or clear custom planning rules, handle these operations:

- **show rules**: run `bash ~/.codex/skills/planning/make/scripts/resolve-rules.sh planning-rules.md` and display the output. if empty, report no custom rules configured.
- **add/update project rules**: write content to `.codex/planning-rules.md` in the current working directory.
- **clear project rules**: delete `.codex/planning-rules.md`.

{{ include "common/skills/planning/make/_step0.md" }}

## step 1: present context and ask focused questions

show the discovered context, then ask questions **one at a time** — output the question as text and wait for the user's reply before proceeding:

"based on your request, i found: [context summary]"

1. "what is the main goal?" — provide a suggested answer based on discovered intent, wait for reply
2. "which components/files are involved?" — list discovered files/areas as options, wait for reply
3. "any specific requirements or limitations?" — wait for reply
4. "do you prefer TDD (tests first) or regular (code first, then tests)?" — wait for reply
5. "short descriptive title for the plan?" — provide a suggested name, wait for reply

after all answers received, synthesize responses into plan context.

{{ include "common/skills/planning/make/_step1-5.md" }}

{{ include "common/skills/planning/make/_plan-template.md" }}

## step 3: next steps

after creating the file, tell user: "created plan: `docs/plans/yyyymmdd-<task-name>.md`"

ask: "what's next? options: (1) interactive review — open plan in editor for annotation, (2) auto review — ai plan-review analysis, (3) implement — commit plan and start, (4) done — commit plan only"

- **interactive review**: check if `revdiff` is installed (`which revdiff`).
  - **if revdiff is available**: run `~/.codex/skills/planning/make/scripts/launch-plan-review.sh <plan-file-path>` via Bash.
    when annotation output is present:
    1. read each annotation — the line number and comment describe what the user wants changed
    2. revise the plan file to address each annotation
    3. run `~/.codex/skills/planning/make/scripts/launch-plan-review.sh <plan-file-path>` again
    4. repeat until no output
  - **if revdiff is not available**: fall back to `~/.codex/skills/planning/make/scripts/plan-annotate.py <plan-file-path>` via Bash.
    when diff output is present:
    1. read the diff — added lines (+) are user annotations, removed lines (-) are deletions
    2. revise the plan file to address each change
    3. run `~/.codex/skills/planning/make/scripts/plan-annotate.py <plan-file-path>` again
    4. repeat until no diff output
  when the annotation loop completes, ask again without "interactive review"
- **auto review**: analyse the plan for completeness, scope, missing tasks, and risk. report findings, then ask again without "auto review"
- **implement**: commit plan with message `docs: add <topic> implementation plan`, then ask: "implementation mode? (1) interactive — implement task by task now, (2) done — just commit"
  - **interactive**: begin implementing task 1 in this session. mark todos completed immediately, run tests after each task
- **done**: commit plan with message `docs: add <topic> implementation plan`, stop

{{ include "common/skills/planning/make/_enforcement.md" }}
