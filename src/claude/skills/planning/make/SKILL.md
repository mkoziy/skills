---
name: make
description: Create structured implementation plan in docs/plans/
argument-hint: describe the feature or task to plan
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, AskUserQuestion, Task, EnterPlanMode, TaskCreate, TaskUpdate, TaskList
---

# Implementation Plan Creation

create an implementation plan in `docs/plans/yyyymmdd-<task-name>.md` with interactive context gathering.

## custom rules loading

before starting, run this command via Bash tool to check for user-provided custom rules:

```bash
bash ~/.claude/skills/planning/make/scripts/resolve-rules.sh planning-rules.md
```

if the output is non-empty, treat it as additional instructions that supplement (not replace) the built-in rules below. apply custom rules alongside the command's own instructions throughout the planning process — they may influence plan structure, testing approach, naming conventions, or other aspects of plan creation. custom rules content is guidance for creating the plan, not content to embed verbatim in the output plan file.

### rules management

when the user asks to add, show, or clear custom planning rules, handle these operations:

- **show rules**: run `bash ~/.claude/skills/planning/make/scripts/resolve-rules.sh planning-rules.md` and display the output. if the output is empty, tell the user no custom rules are configured at project level. to determine the source, check if `.claude/planning-rules.md` exists and is non-empty (project-level).
- **add/update project rules**: write content to `.claude/planning-rules.md` in the current working directory.
- **clear project rules**: delete `.claude/planning-rules.md`.

project-level rules (`.claude/planning-rules.md`) take effect when present.

**CRITICAL: this skill must NEVER modify its own files (commands, skills, agents, scripts, references). the ONLY files it may create or modify for rules management are `.claude/planning-rules.md`. if the user asks to change the skill's behavior, create a plan for it — do not edit skill files directly.**

{{ include "common/skills/planning/make/_step0.md" }}

## step 1: present context and ask focused questions

show the discovered context, then ask questions **one at a time** using the AskUserQuestion tool:

"based on your request, i found: [context summary]"

**ask questions one at a time (do not overwhelm with multiple questions):**

1. **plan purpose**: use AskUserQuestion - "what is the main goal?"
   - provide multiple choice with suggested answer based on discovered intent
   - wait for response before next question

2. **scope**: use AskUserQuestion - "which components/files are involved?"
   - provide multiple choice with suggested discovered files/areas
   - wait for response before next question

3. **constraints**: use AskUserQuestion - "any specific requirements or limitations?"
   - can be open-ended if constraints vary widely
   - wait for response before next question

4. **testing approach**: use AskUserQuestion - "do you prefer TDD or regular approach?"
   - options: "TDD (tests first)" and "Regular (code first, then tests)"
   - store preference for reference during implementation
   - wait for response before next question

5. **plan title**: use AskUserQuestion - "short descriptive title?"
   - provide suggested name based on intent

after all questions answered, synthesize responses into plan context.

{{ include "common/skills/planning/make/_step1-5.md" }}

{{ include "common/skills/planning/make/_plan-template.md" }}

## step 3: next steps

after creating the file, tell user: "created plan: `docs/plans/yyyymmdd-<task-name>.md`"

then use AskUserQuestion:

```json
{
  "questions": [{
    "question": "Plan created. What's next?",
    "header": "Next step",
    "options": [
      {"label": "Interactive review", "description": "Open plan in editor for manual annotation and feedback loop"},
      {"label": "Auto review", "description": "Launch AI plan-review agent for automated analysis"},
      {"label": "Implement", "description": "Commit plan and start implementing"},
      {"label": "Done", "description": "Commit plan, no further action"}
    ],
    "multiSelect": false
  }]
}
```

- **Interactive review**: check if `revdiff` is installed (`which revdiff`).
  - **if revdiff is available**: run `~/.claude/skills/planning/make/scripts/launch-plan-review.sh <plan-file-path>` via Bash.
    the script opens revdiff TUI showing the plan with syntax highlighting. user adds line-level annotations.
    on quit, annotations are output to stdout in structured format:
    ```
    ## filename:line ( )
    annotation comment text
    ```
    when annotation output is present:
    1. read each annotation — the line number and comment describe what the user wants changed
    2. revise the plan file to address each annotation
    3. run `~/.claude/skills/planning/make/scripts/launch-plan-review.sh <plan-file-path>` via Bash
    4. repeat until no output (user quit without annotations)
  - **if revdiff is not available**: fall back to `~/.claude/skills/planning/make/scripts/plan-annotate.py <plan-file-path>` via Bash.
    the script opens a copy of the plan in $EDITOR via terminal overlay. if the user makes annotations,
    it outputs a unified diff to stdout. when diff output is present:
    1. read the diff carefully — added lines (+) are user annotations, removed lines (-) are deletions, modified lines show requested changes
    2. revise the plan file to address each annotation
    3. run `~/.claude/skills/planning/make/scripts/plan-annotate.py <plan-file-path>` via Bash
    4. repeat until no diff output (user closed editor without changes)
  when the annotation loop completes, ask again with the remaining options (minus "Interactive review")
- **Auto review**: launch plan-review agent (Task tool with subagent_type=plan-review). After review completes, ask again with the same options (minus "Auto review")
- **Implement**: commit plan with message like "docs: add <topic> implementation plan", then ask implementation mode:
  ```json
  {
    "questions": [{
      "question": "Implementation mode?",
      "header": "Mode",
      "options": [
        {"label": "Interactive", "description": "Implement task by task in this session"},
        {"label": "Autonomous", "description": "Run /planning:exec for autonomous execution with reviews"}
      ],
      "multiSelect": false
    }]
  }
  ```
  - **Interactive**: begin implementing task 1 interactively in this session. Use TodoWrite tool to track progress and mark todos completed immediately (do not batch)
  - **Autonomous**: invoke `/planning:exec <plan-file-path>` for autonomous execution with multi-phase review
- **Done**: commit plan with message like "docs: add <topic> implementation plan", stop

{{ include "common/skills/planning/make/_enforcement.md" }}
