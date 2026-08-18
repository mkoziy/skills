---
name: grill-plan
description: Grill a feature idea against docs, then brainstorm it, then turn it into a docs/plans/ plan — all interactively in the main conversation. Use when the user says "grill this with docs then brainstorm and plan", "grill-plan", or wants a doc-grilled design before a plan file exists.
argument-hint: describe the feature or task
allowed-tools: Read, Glob, Grep, Bash, Skill, AskUserQuestion
---

# grill-plan

Four-phase orchestrator: grill-with-docs → brainstorm → plan → ship. Runs entirely in the main thread, not in subagents — the first three phases surface things to (or ask things of) the user directly, and a subagent's output isn't visible to them mid-run. Only hand a phase to a subagent if a future phase here is explicitly non-interactive (none currently are).

**Dependency**: requires the `grill-with-docs` skill to be installed (it's a separate, globally-installed skill, not part of this repo — `disable-model-invocation: true`, so it only runs when called by name, which is what Phase 1 does). If it isn't installed, tell the user and stop rather than substituting something else.

## Phase 1: Grill with docs

Invoke the `grill-with-docs` skill (Skill tool) with `$ARGUMENTS`. Let it run its full interview/ADR process. Read its output before moving on — anything it surfaces needs to fold into Phase 2, not get silently dropped.

## Phase 2: Brainstorm

Invoke the `brainstorm` skill (Skill tool), passing `$ARGUMENTS` plus a short summary of Phase 1's output as context. Let it run its normal one-question-at-a-time dialogue in full — don't shortcut it.

## Phase 3: Plan

Once brainstorm converges on a design, invoke the `make` skill (Skill tool), passing the finalized design (not the raw original ask) as context. Let `make` run its own question loop and write `docs/plans/yyyymmdd-<task-name>.md`.

Let `make` reach its own "what's next" menu and let the user drive that choice themselves rather than picking on their behalf. Once that resolves (auto-review applied, interactive work paused, or "done" picked), continue to Phase 4.

## Phase 4: Ship

Turn the finished plan (and any ADRs Phase 1 wrote under `docs/adr/`) into a GitHub issue and a branch, so the plan doesn't just sit uncommitted on whatever branch you started on.

**Precondition**: `gh` must be authenticated (`gh auth status`) and the cwd must be inside a git repo with a GitHub remote. If either fails, tell the user and stop — don't substitute a manual issue-creation workaround.

1. **Enforce one open plan.** List `docs/plans/*.md` excluding `docs/plans/completed/`. If any file other than the one just written exists, this violates the one-open-plan rule — stop and ask the user (plain conversational text, not `AskUserQuestion`, since "move it to completed", "abandon it", or "let both stand" all need room to discuss): whether to move the older plan(s) to `docs/plans/completed/` first, or abort Phase 4 so they can deal with it themselves.
2. **Create the issue.** `gh issue create --title "<task name>" --body "<design summary>"` — body is the brainstormed design summary (same one handed to `make`), not the raw plan file dump. Capture the returned issue number `N`.
3. **Branch.** Same convention as `hermestrator-plan`: `agent/issue-<N>`, created from the base branch (`git fetch origin <base>`, `git checkout -b agent/issue-<N> origin/<base>`). Uncommitted plan/ADR files in the working tree carry over automatically.
4. **Commit and push.** Stage only the plan file and any ADR files Phase 1 created this session — never `git add -A`:
   ```bash
   git add docs/plans/<plan-file> docs/adr/<adr-files...>
   git commit -m "docs: plan for #<N> — <task title>"
   git push -u origin agent/issue-<N>
   ```
5. **Report.** Issue URL, branch name, and files committed.
