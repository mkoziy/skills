---
name: grill-plan
description: Grill a feature idea against docs, then brainstorm it, then turn it into a docs/plans/ plan — all interactively in the main conversation. Use when the user says "grill this with docs then brainstorm and plan", "grill-plan", or wants a doc-grilled design before a plan file exists.
argument-hint: describe the feature or task
allowed-tools: Read, Glob, Grep, Bash, Skill, AskUserQuestion, Agent
---

# grill-plan

Four-phase orchestrator: grill-with-docs → brainstorm → plan → ship. Runs entirely in the main thread, not in subagents — the first three phases surface things to (or ask things of) the user directly, and a subagent's output isn't visible to them mid-run. The one exception is the critique pass in Phase 3, which is non-interactive by design (a one-shot report, not a dialogue) and is explicitly handed to a subagent below.

**Dependency**: requires the `grill-with-docs` skill to be installed (it's a separate, globally-installed skill, not part of this repo — `disable-model-invocation: true`, so it only runs when called by name, which is what Phase 1 does). If it isn't installed, tell the user and stop rather than substituting something else.

## Phase 1: Grill with docs

Invoke the `grill-with-docs` skill (Skill tool) with `$ARGUMENTS`. Let it run its full interview/ADR process. Read its output before moving on — anything it surfaces needs to fold into Phase 2, not get silently dropped.

## Phase 2: Brainstorm

Invoke the `brainstorm` skill (Skill tool), passing `$ARGUMENTS` plus a short summary of Phase 1's output as context. Let it run its normal one-question-at-a-time dialogue in full — don't shortcut it.

## Phase 3: Plan

Once brainstorm converges on a design, invoke the `make` skill (Skill tool), passing the finalized design (not the raw original ask) as context. Let `make` run its own question loop and write `docs/plans/yyyymmdd-<task-name>.md`.

Then, in this exact order:

1. **Handle `make`'s menu without letting it commit.** `make`'s own Step 3 menu commits the plan file the instant "Done" or "Implement" is picked. Don't let it: at this point in grill-plan there's no branch or issue yet (Phase 4 creates both), so that commit would land on whatever branch the session started on instead of `agent/issue-<N>`, and Phase 4's own commit step would then find nothing new to stage. Relabel "Done" as **"Continue"** and skip its commit action. "Interactive review" and "Auto review" still run normally (they don't commit). If the user picks "Implement", also skip its commit — critique still runs next, then Phase 4 creates the issue/branch/commit before implementation starts.

2. **Run the critique pass. Do this every time, no exceptions — do not skip to Phase 4 yet.** Launch a subagent (Agent tool, `subagent_type: general-purpose`) with a prompt instructing it to invoke the `critique` skill (Skill tool) against the plan file's path (`docs/plans/<plan-file>`), then return the critique's full report verbatim. Show that report to the user as-is — don't summarize, filter, or soften it. This is unconditional and runs exactly once regardless of which `make` menu option was picked or whether `make`'s own "Auto review" ran — that's a different subagent checking a different thing (plan-structure/template conformance), and does not substitute for this step. It's a one-shot report, not a loop.

3. **Only after the critique report has been shown**, let the user decide what to do with it (edit the plan directly, re-run `make`'s interactive/auto review, or proceed as-is) — then move to Phase 4.

## Phase 4: Ship

Turn the finished plan (and any ADRs Phase 1 wrote under `docs/adr/`) into a GitHub issue and a branch, so the plan doesn't just sit uncommitted on whatever branch you started on.

**Precondition**: `gh` must be authenticated (`gh auth status`) and the cwd must be inside a git repo with a GitHub remote. If either fails, tell the user and stop — don't substitute a manual issue-creation workaround.

1. **Enforce one open plan.** List `docs/plans/*.md` excluding `docs/plans/completed/`. If any file other than the one just written exists, this violates the one-open-plan rule — stop and ask the user (plain conversational text, not `AskUserQuestion`, since "move it to completed", "abandon it", or "let both stand" all need room to discuss): whether to move the older plan(s) to `docs/plans/completed/` first, or abort Phase 4 so they can deal with it themselves.
2. **Create the issue.** `gh issue create --title "<task name>" --body "<body>"` — body opens with a **TLDR** section (2-3 sentences: what this is and why), followed by the brainstormed design summary (same one handed to `make`), not the raw plan file dump. Capture the returned issue number `N`.
3. **Branch.** Same convention as `hermestrator-plan`: `agent/issue-<N>`. Use `gh issue develop <N> --name agent/issue-<N> --base <base> --checkout` instead of a plain `git checkout -b` — it links the branch to the issue so it shows up under the issue's "Development" section in the GitHub UI. Uncommitted plan/ADR files in the working tree carry over automatically.
4. **Commit and push.** Stage only the plan file and any ADR files Phase 1 created this session — never `git add -A`:
   ```bash
   git add docs/plans/<plan-file> docs/adr/<adr-files...>
   git commit -m "docs: plan for #<N> — <task title>"
   git push -u origin agent/issue-<N>
   ```
5. **Report.** Issue URL, branch name, and files committed.
