---
name: make
description: Create a structured implementation plan in docs/plans/ with interactive context gathering. Use when the user says "make a plan", "create implementation plan", "plan this out", or wants a docs/plans/ file drafted before implementing a feature, bug fix, refactor, or migration.
argument-hint: describe the feature or task to plan
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, AskUserQuestion, EnterPlanMode, TaskCreate, TaskUpdate, TaskList
---

# Implementation Plan Creation

Create an implementation plan in `docs/plans/yyyymmdd-<task-name>.md` with interactive context gathering.

Script and reference paths below (`scripts/...`, `references/...`) are relative to this skill's own directory, not the shell's working directory — resolve them against the directory this SKILL.md was read from before running. When launching the auto-review subagent (step 3), substitute the absolute path in for `SKILL_ROOT` inside the prompt text, since the subagent starts fresh and can't resolve it itself.

## Custom Rules Loading

Before starting, run this command via Bash tool to check for user-provided custom rules:

```bash
bash scripts/resolve-rules.sh planning-rules.md
```

If the output is non-empty, treat it as additional instructions that supplement (not replace) the built-in rules below. Apply custom rules alongside this skill's own instructions throughout the planning process — they may influence plan structure, testing approach, naming conventions, or other aspects of plan creation. Custom rules content is guidance for creating the plan, not content to embed verbatim in the output plan file.

### Rules Management

When the user asks to add, show, or clear custom planning rules, handle these operations:

- **show rules**: run `bash scripts/resolve-rules.sh planning-rules.md` and display the output. If the output is empty, tell the user no custom rules are configured at either level. Otherwise, to determine the source, check if `.claude/planning-rules.md` exists and is non-empty (project-level) — if not, the output came from user-level. Tell the user which level it came from.
- **add/update project rules**: write content to `.claude/planning-rules.md` in the current working directory.
- **add/update user rules**: first check if `$CLAUDE_PLUGIN_DATA` is set (run `echo "$CLAUDE_PLUGIN_DATA"`). If empty, tell the user that user-level rules require this skill to be installed via a Claude Code plugin marketplace, and offer project-level instead. If set, write content to `$CLAUDE_PLUGIN_DATA/planning-rules.md`.
- **clear project rules**: delete `.claude/planning-rules.md`.
- **clear user rules**: if `$CLAUDE_PLUGIN_DATA` is set, delete `$CLAUDE_PLUGIN_DATA/planning-rules.md`. If not set, tell the user user-level rules are not available.

Project-level rules (`.claude/planning-rules.md`) take precedence over user-level rules (`$CLAUDE_PLUGIN_DATA/planning-rules.md`). When both non-empty files exist, only project-level rules are loaded. Empty files are treated as absent and fall through to the next level. See `references/custom-rules.md` for full documentation on the rules mechanism.

**CRITICAL: this skill must NEVER modify its own files (SKILL.md, scripts, references). The ONLY files it may create or modify for rules management are `.claude/planning-rules.md` and `$CLAUDE_PLUGIN_DATA/planning-rules.md`. If the user asks to change the skill's behavior, create a plan for it — do not edit skill files directly.**

## Step 0: Parse Intent and Gather Context

Before asking questions, understand what the user is working on:

1. **Parse the request** to identify intent:
   - "add feature Z" / "implement W" → feature development
   - "fix bug" / "debug issue" → bug fix plan
   - "refactor X" / "improve Y" → refactoring plan
   - "migrate to Z" / "upgrade W" → migration plan
   - generic request → explore current work

2. **Gather relevant context quickly** — use direct tool calls (Read, Glob, Grep), NOT an Explore agent. Keep discovery under 30 seconds:

   **for feature development:**
   - glob for files matching the feature area (e.g., `**/*auth*`, `**/*cache*`)
   - read 1-3 most relevant files to understand existing patterns
   - check project structure with a quick `ls` of key directories

   **for bug fixing:**
   - grep for error messages or function names mentioned in the request
   - read the specific file(s) involved
   - check `git log --oneline -5` for recent changes

   **for refactoring/migration:**
   - glob for files matching the area being refactored
   - read 2-3 key files to understand current structure
   - grep for imports/references to identify dependencies

   **for generic/unclear requests:**
   - check `git status` and `git log --oneline -5`
   - read README.md or CLAUDE.md for project overview
   - `ls` the top-level directory structure

   **CRITICAL: do NOT launch an Explore agent or read more than 5 files in this step. The goal is a quick scan, not exhaustive analysis. If more context is needed, ask the user in step 1.**

3. **Synthesize findings** into a brief context summary (3-5 bullet points):
   - what the project is and primary language/framework
   - which files/areas are relevant to the request
   - key patterns or conventions observed

## Step 1: Present Context and Ask Focused Questions

Show the discovered context, then ask questions **one at a time** using the AskUserQuestion tool:

"Based on your request, I found: [context summary]"

**Ask questions one at a time (do not overwhelm with multiple questions):**

1. **plan purpose**: use AskUserQuestion - "What is the main goal?"
   - provide multiple choice with suggested answer based on discovered intent
   - wait for response before next question

2. **scope**: use AskUserQuestion - "Which components/files are involved?"
   - provide multiple choice with suggested discovered files/areas
   - wait for response before next question

3. **constraints**: use AskUserQuestion - "Any specific requirements or limitations?"
   - can be open-ended if constraints vary widely
   - wait for response before next question

4. **testing approach**: use AskUserQuestion - "Do you prefer TDD or regular approach?"
   - options: "TDD (tests first)" and "Regular (code first, then tests)"
   - store preference for reference during implementation
   - wait for response before next question

5. **plan title**: use AskUserQuestion - "Short descriptive title?"
   - provide suggested name based on intent

After all questions answered, synthesize responses into plan context.

## Step 1.5: Explore Approaches

Once the problem is understood, propose implementation approaches:

1. **propose 2-3 different approaches** with trade-offs for each
2. **lead with recommended option** and explain reasoning
3. **present conversationally** - not a formal document yet

Example format:
```
I see three approaches:

**Option A: [name]** (recommended)
- how it works: ...
- pros: ...
- cons: ...

**Option B: [name]**
- how it works: ...
- pros: ...
- cons: ...

Which direction appeals to you?
```

Use AskUserQuestion tool to let user select preferred approach before creating the plan.

**Skip this step** if:
- the implementation approach is obvious (single clear path)
- user explicitly specified how they want it done
- it's a bug fix with clear solution

## Step 2: Create Plan File

Check `docs/plans/` for existing files, then create `docs/plans/yyyymmdd-<task-name>.md` (use current date):

### Plan Structure

```markdown
# [Plan Title]

## Overview
- clear description of the feature/change being implemented
- problem it solves and key benefits
- how it integrates with existing system

## Context (from discovery)
- files/components involved: [list from step 0]
- related patterns found: [patterns discovered]
- dependencies identified: [dependencies]

## Development Approach
- **testing approach**: [TDD / Regular - from user preference in planning]
- complete each task fully before moving to the next
- make small, focused changes
- **CRITICAL: every task MUST include new/updated tests** for code changes in that task
  - tests are not optional - they are a required part of the checklist
  - write unit tests for new functions/methods
  - write unit tests for modified functions/methods
  - add new test cases for new code paths
  - update existing test cases if behavior changes
  - tests cover both success and error scenarios
- **CRITICAL: all tests must pass before starting next task** - no exceptions
- **CRITICAL: update this plan file when scope changes during implementation**
- run tests after each change
- maintain backward compatibility

## Testing Strategy
- **unit tests**: required for every task (see Development Approach above)
- **e2e tests**: if project has UI-based e2e tests (Playwright, Cypress, etc.):
  - UI changes → add/update e2e tests in same task as UI code
  - backend changes supporting UI → add/update e2e tests in same task
  - treat e2e tests with same rigor as unit tests (must pass before next task)
  - store e2e tests alongside unit tests (or in designated e2e directory)
  - example: if task implements new form field, add e2e test checking form submission

## Progress Tracking
- mark completed items with `[x]` immediately when done
- add newly discovered tasks with ➕ prefix
- document issues/blockers with ⚠️ prefix
- update plan if implementation deviates from original scope
- keep plan in sync with actual work done

## Solution Overview
- high-level approach and architecture chosen
- key design decisions and rationale
- how it fits into the existing system

## Technical Details
- data structures and changes
- parameters and formats
- processing flow

## What Goes Where
- **Implementation Steps** (`[ ]` checkboxes): tasks achievable within this codebase - code changes, tests, documentation updates
- **Post-Completion** (no checkboxes): items requiring external action - manual testing, changes in consuming projects, deployment configs, third-party verifications

## Implementation Steps

<!--
Task structure guidelines:
- Each task = ONE logical unit (one function, one endpoint, one component)
- Use specific descriptive names, not generic "[Core Logic]" or "[Implementation]"
- Each task MUST have a **Files:** block listing files to Create/Modify (before checkboxes)
- Aim for ~5 checkboxes per task (more is OK if logically atomic)
- **CRITICAL: number ALL tasks with concrete sequential integers** - the two trailing tasks below are shown as "Task N-1" and "Task N" where N is a PLACEHOLDER for the total task count, NOT literal text. Substitute real numbers continuing the sequence from your last implementation task (e.g. with 14 implementation tasks they become "Task 15: Verify acceptance criteria" and "Task 16: ... Update documentation"). NEVER write the literal strings "Task N-1" or "Task N" into the plan.
- **CRITICAL: Each task MUST end with writing/updating tests before moving to next**
  - tests are not optional - they are a required deliverable of every task
  - write tests for all NEW code added in this task
  - write tests for all MODIFIED code in this task
  - include both success and error scenarios in tests
  - list tests as SEPARATE checklist items, not bundled with implementation

Example (NOTICE: Files block + tests as separate checklist items):

### Task 1: Add password hashing utility

**Files:**
- Create: `src/auth/hash`
- Create: `src/auth/hash_test`

- [ ] create `src/auth/hash` with HashPassword and VerifyPassword functions
- [ ] implement bcrypt-based hashing with configurable cost
- [ ] write tests for HashPassword (success + error cases)
- [ ] write tests for VerifyPassword (success + error cases)
- [ ] run tests - must pass before task 2

### Task 2: Add user registration endpoint

**Files:**
- Create: `src/api/users`
- Modify: `src/api/router`
- Create: `src/api/users_test`

- [ ] create `POST /api/users` handler in `src/api/users`
- [ ] add input validation (email format, password strength)
- [ ] integrate with password hashing utility
- [ ] write tests for handler success case with table-driven cases
- [ ] write tests for handler error cases (invalid input, missing fields)
- [ ] run tests - must pass before task 3
-->

### Task 1: [specific name - what this task accomplishes]

**Files:**
- Create: `exact/path/to/new_file`
- Modify: `exact/path/to/existing`

- [ ] [specific action with file reference - code implementation]
- [ ] [specific action with file reference - code implementation]
- [ ] write tests for new/changed functionality (success cases)
- [ ] write tests for error/edge cases
- [ ] run tests - must pass before next task

<!-- replace "N-1" and "N" below with the actual next sequential numbers continuing from your last implementation task - do NOT emit the literal letter N -->
### Task N-1: Verify acceptance criteria
- [ ] verify all requirements from Overview are implemented
- [ ] verify edge cases are handled
- [ ] run full test suite: `<project test command>`
- [ ] run e2e tests if project has them: `<project e2e test command>`
- [ ] verify test coverage meets project standard

### Task N: [Final] Update documentation
- [ ] update README.md if needed
- [ ] update CLAUDE.md if new patterns discovered
- [ ] move this plan to `docs/plans/completed/`

## Post-Completion
*Items requiring manual intervention or external systems - no checkboxes, informational only*

**Manual verification** (if applicable):
- manual UI/UX testing scenarios
- performance testing under load
- security review considerations

**External system updates** (if applicable):
- consuming projects that need updates after this library change
- configuration changes in deployment systems
- third-party service integrations to verify
```

## Step 3: Next Steps

After creating the file, tell user: "created plan: `docs/plans/yyyymmdd-<task-name>.md`"

Then use AskUserQuestion:

```json
{
  "questions": [{
    "question": "Plan created. What's next?",
    "header": "Next step",
    "options": [
      {"label": "Interactive review", "description": "Open plan in editor for manual annotation and feedback loop"},
      {"label": "Auto review", "description": "Launch an AI plan-review subagent for automated analysis"},
      {"label": "Implement", "description": "Commit plan and start implementing"},
      {"label": "Done", "description": "Commit plan, no further action"}
    ],
    "multiSelect": false
  }]
}
```

- **Interactive review**: check if `revdiff` is installed (`which revdiff`).
  - **if revdiff is available**: run `scripts/launch-plan-review.sh <plan-file-path>` via Bash.
    the script opens revdiff TUI showing the plan with syntax highlighting. user adds line-level annotations.
    on quit, annotations are output to stdout in structured format:
    ```
    ## filename:line ( )
    annotation comment text
    ```
    when annotation output is present:
    1. read each annotation — the line number and comment describe what the user wants changed
    2. revise the plan file to address each annotation
    3. run `scripts/launch-plan-review.sh <plan-file-path>` via Bash
    4. repeat until no output (user quit without annotations)
  - **if revdiff is not available**: fall back to `scripts/plan-annotate.py <plan-file-path>` via Bash.
    the script opens a copy of the plan in $EDITOR via terminal overlay. if the user makes annotations,
    it outputs a unified diff to stdout. when diff output is present:
    1. read the diff carefully — added lines (+) are user annotations, removed lines (-) are deletions, modified lines show requested changes
    2. revise the plan file to address each annotation
    3. run `scripts/plan-annotate.py <plan-file-path>` via Bash
    4. repeat until no diff output (user closed editor without changes)
  when the annotation loop completes, ask again with the remaining options (minus "Interactive review")
- **Auto review**: read `references/agents/plan-review.txt` from this skill's own directory, substitute `SKILL_ROOT` in its content with this skill's absolute directory path, then launch it as a subagent via the Agent tool with `subagent_type: general-purpose`, passing the resolved text as the prompt plus the plan file path. After it returns, show its findings to the user, then ask again with the same options (minus "Auto review")
- **Implement**: commit plan with message like "docs: add <topic> implementation plan", then ask implementation mode:
  ```json
  {
    "questions": [{
      "question": "Implementation mode?",
      "header": "Mode",
      "options": [
        {"label": "Interactive", "description": "Implement task by task in this session"},
        {"label": "Autonomous", "description": "Run the exec skill for autonomous execution with reviews"}
      ],
      "multiSelect": false
    }]
  }
  ```
  - **Interactive**: begin implementing task 1 interactively in this session. Use TaskCreate/TaskUpdate to track progress and mark tasks completed immediately (do not batch)
  - **Autonomous**: invoke the `exec` skill with `<plan-file-path>` for autonomous execution with multi-phase review
- **Done**: commit plan with message like "docs: add <topic> implementation plan", stop

## Execution Enforcement

**CRITICAL testing rules during implementation:**

1. **after completing code changes in a task**:
   - STOP before moving to next task
   - add tests for all new functionality
   - update tests for modified functionality
   - run project test command
   - mark completed items with `[x]` in plan file

2. **if tests fail**:
   - fix the failures before proceeding
   - do NOT move to next task with failing tests
   - do NOT skip test writing

3. **only proceed to next task when**:
   - all task items completed and marked `[x]`
   - tests written/updated
   - all tests passing

4. **plan tracking during implementation**:
   - update checkboxes immediately when tasks complete
   - add ➕ prefix for newly discovered tasks
   - add ⚠️ prefix for blockers
   - modify plan if scope changes significantly

5. **on completion**:
   - verify all checkboxes marked
   - run final test suite
   - move plan to `docs/plans/completed/`
   - create directory if needed: `mkdir -p docs/plans/completed`

6. **partial implementation exception**:
   - if a task provides partial implementation where tests cannot pass until a later task:
     - still write the tests as part of this task (required)
     - add TODO comment in test code explaining the dependency
     - mark the test checkbox as completed with note: `[x] write tests ... (fails until Task X)`
     - do NOT skip test writing or defer until later
   - when the dependent task completes, remove the TODO comment and verify tests pass

This ensures each task is solid before building on top of it.

## Key Principles

- **one question at a time** - do not overwhelm user with multiple questions in a single message
- **multiple choice preferred** - easier to answer than open-ended when possible
- **DRY, YAGNI ruthlessly** - avoid unnecessary duplication and features, keep scope minimal (but prefer duplication over premature abstraction when it reduces coupling)
- **lead with recommendation** - have an opinion, explain why, but let user decide
- **explore alternatives** - always propose 2-3 approaches before settling (unless obvious)
- **duplication vs abstraction** - when code repeats, ask user: prefer duplication (simpler, no coupling) or abstraction (DRY but adds complexity)? explain trade-offs before deciding
