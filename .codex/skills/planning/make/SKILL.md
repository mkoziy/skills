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

## step 0: parse intent and gather context

before asking questions, understand what the user is working on:

1. **parse user's command arguments** to identify intent:
   - "add feature Z" / "implement W" → feature development
   - "fix bug" / "debug issue" → bug fix plan
   - "refactor X" / "improve Y" → refactoring plan
   - "migrate to Z" / "upgrade W" → migration plan
   - generic request → explore current work

2. **gather relevant context quickly** — use direct tool calls (Read, Glob, Grep). keep discovery under 30 seconds:

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

   **CRITICAL: do NOT read more than 5 files in this step. the goal is a quick scan, not exhaustive analysis. if more context is needed, ask the user in step 1.**

3. **synthesize findings** into a brief context summary (3-5 bullet points):
   - what the project is and primary language/framework
   - which files/areas are relevant to the request
   - key patterns or conventions observed


## step 1: present context and ask focused questions

show the discovered context, then ask questions **one at a time** — output the question as text and wait for the user's reply before proceeding:

"based on your request, i found: [context summary]"

1. "what is the main goal?" — provide a suggested answer based on discovered intent, wait for reply
2. "which components/files are involved?" — list discovered files/areas as options, wait for reply
3. "any specific requirements or limitations?" — wait for reply
4. "do you prefer TDD (tests first) or regular (code first, then tests)?" — wait for reply
5. "short descriptive title for the plan?" — provide a suggested name, wait for reply

after all answers received, synthesize responses into plan context.

## step 1.5: explore approaches

once the problem is understood, propose implementation approaches:

1. **propose 2-3 different approaches** with trade-offs for each
2. **lead with recommended option** and explain reasoning
3. **present conversationally** - not a formal document yet

example format:
```
i see three approaches:

**Option A: [name]** (recommended)
- how it works: ...
- pros: ...
- cons: ...

**Option B: [name]**
- how it works: ...
- pros: ...
- cons: ...

which direction appeals to you?
```

wait for user's direction before creating the plan.

**skip this step** if:
- the implementation approach is obvious (single clear path)
- user explicitly specified how they want it done
- it's a bug fix with clear solution


## step 2: create plan file

check `docs/plans/` for existing files, then create `docs/plans/yyyymmdd-<task-name>.md` (use current date):

### plan structure

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

## execution enforcement

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

this ensures each task is solid before building on top of it.

## key principles

- **one question at a time** - do not overwhelm user with multiple questions in a single message
- **multiple choice preferred** - easier to answer than open-ended when possible
- **DRY, YAGNI ruthlessly** - avoid unnecessary duplication and features, keep scope minimal (but prefer duplication over premature abstraction when it reduces coupling)
- **lead with recommendation** - have an opinion, explain why, but let user decide
- **explore alternatives** - always propose 2-3 approaches before settling (unless obvious)
- **duplication vs abstraction** - when code repeats, ask user: prefer duplication (simpler, no coupling) or abstraction (DRY but adds complexity)? explain trade-offs before deciding

