---
name: grill-plan
description: Grill a feature idea against docs, then brainstorm it, then turn it into a docs/plans/ plan — all interactively in the main conversation. Use when the user says "grill this with docs then brainstorm and plan", "grill-plan", or wants a doc-grilled design before a plan file exists.
argument-hint: describe the feature or task
allowed-tools: Read, Glob, Grep, Bash, Skill
---

# grill-plan

Three-phase orchestrator: grill-with-docs → brainstorm → plan. Runs entirely in the main thread, not in subagents — all three phases surface things to (or ask things of) the user directly, and a subagent's output isn't visible to them mid-run. Only hand a phase to a subagent if a future phase here is explicitly non-interactive (none currently are).

**Dependency**: requires the `grill-with-docs` skill to be installed (it's a separate, globally-installed skill, not part of this repo — `disable-model-invocation: true`, so it only runs when called by name, which is what Phase 1 does). If it isn't installed, tell the user and stop rather than substituting something else.

## Phase 1: Grill with docs

Invoke the `grill-with-docs` skill (Skill tool) with `$ARGUMENTS`. Let it run its full interview/ADR process. Read its output before moving on — anything it surfaces needs to fold into Phase 2, not get silently dropped.

## Phase 2: Brainstorm

Invoke the `brainstorm` skill (Skill tool), passing `$ARGUMENTS` plus a short summary of Phase 1's output as context. Let it run its normal one-question-at-a-time dialogue in full — don't shortcut it.

## Phase 3: Plan

Once brainstorm converges on a design, invoke the `make` skill (Skill tool), passing the finalized design (not the raw original ask) as context. Let `make` run its own question loop and write `docs/plans/yyyymmdd-<task-name>.md`.

Stop when `make` reaches its own "what's next" menu — let the user drive that choice themselves rather than picking on their behalf.
