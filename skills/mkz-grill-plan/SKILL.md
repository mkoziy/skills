---
name: mkz-grill-plan
description: Grill a feature idea against docs, then brainstorm it, then turn it into a docs/plans/ plan — all interactively in the main conversation. Use when the user says "grill this with docs then brainstorm and plan", "grill-plan", or wants a doc-grilled design before a plan file exists.
argument-hint: describe the feature or task
allowed-tools: Read, Glob, Grep, Bash, Skill, AskUserQuestion, Agent
---

# grill-plan

Four-phase orchestrator: mkz-grill-with-docs → brainstorm → plan → ship. Runs entirely in the main thread, not in subagents — the first three phases surface things to (or ask things of) the user directly, and a subagent's output isn't visible to them mid-run. The one exception is Phase 3's plan review, which `mkz-make` itself hands to subagents internally (a one-shot Auto review plus a critique pass, both non-interactive by design).

**Dependency**: requires the sibling `mkz-grill-with-docs` skill, which in turn requires the separately installed `domain-modeling` skill. If either is unavailable, tell the user and stop rather than substituting something else.

**Also uses**: `mkz-grill-brainstorm`, a sibling of this repo's `mkz-brainstorm` skill kept solely for grill-plan's Phase 2 (also `disable-model-invocation: true`). Don't call `mkz-brainstorm` from grill-plan — use `mkz-grill-brainstorm`.

## Phase 1: Grill with docs

Invoke the `mkz-grill-with-docs` skill (Skill tool) with `$ARGUMENTS`. Let it run its full interview/ADR process. Read its output before moving on — anything it surfaces needs to fold into Phase 2, not get silently dropped.

## Phase 2: Brainstorm

Invoke the `mkz-grill-brainstorm` skill (Skill tool) — not `mkz-brainstorm` — passing `$ARGUMENTS` plus a short summary of Phase 1's output as context. It's grill-plan's own variant: same one-question-at-a-time dialogue, but it auto-picks the recommended approach instead of asking, and stops after the design is validated instead of running its own next-steps menu. Let it run in full — don't shortcut it.

## Phase 3: Plan

Once brainstorm converges on a design, list every ADR created in Phase 1 and invoke the `mkz-make` skill (Skill tool), passing the finalized design (not the raw original ask) and those exact relative paths as context. Instruct it to add an `## ADRs` section to the plan with a Markdown link to every listed ADR; this is mandatory whenever Phase 1 created ADRs. Also instruct it to skip Step 0's testing-approach question ("TDD or regular approach?") and default to Regular (code first, then tests) without asking — grill-plan's design phase already covered testing strategy in Phase 3's design sections, so re-asking here is redundant. Let `mkz-make` run the rest of its question loop and write `docs/plans/yyyymmdd-<task-name>.md`. `mkz-make` then automatically runs its own Auto review and critique passes against the plan (its Step 3) before presenting a menu — let both run and show their reports; that's the same critique pass grill-plan used to spawn separately, so there's no second one to run here anymore.

**Handle `mkz-make`'s menu without letting it commit.** `mkz-make`'s own Step 4 menu commits the plan file the instant "Done" or "Implement" is picked. Don't let it: at this point in grill-plan there's no branch or issue yet (Phase 4 creates both), so that commit would land on whatever branch the session started on instead of `agent/issue-<N>`, and Phase 4's own commit step would then find nothing new to stage. Relabel "Done" as **"Continue"** and skip its commit action. "Interactive review" still runs normally (it doesn't commit). If the user picks "Implement", also skip its commit — let Phase 4 create the issue/branch/commit before implementation starts.

Once the menu resolves this way, move to Phase 4.

## Phase 4: Ship

Turn the finished plan (and any ADRs Phase 1 wrote under `docs/adr/`) into a GitHub issue and a branch, so the plan doesn't just sit uncommitted on whatever branch you started on.

**Precondition**: `gh` must be authenticated (`gh auth status`) and the cwd must be inside a git repo with a GitHub remote. If either fails, tell the user and stop — don't substitute a manual issue-creation workaround.

1. **Enforce one open plan.** List `docs/plans/*.md` excluding `docs/plans/completed/`. If any file other than the one just written exists, this violates the one-open-plan rule — stop and ask the user (plain conversational text, not `AskUserQuestion`, since "move it to completed", "abandon it", or "let both stand" all need room to discuss): whether to move the older plan(s) to `docs/plans/completed/` first, or abort Phase 4 so they can deal with it themselves.
2. **Create the issue.** `gh issue create --title "<task name>" --body "<body>"` — body opens with a **TLDR** section (2-3 sentences: what this is and why), followed by the brainstormed design summary (same one handed to `mkz-make`), not the raw plan file dump. Capture the returned issue number `N`.
3. **Branch.** Same convention as `mkz-hermestrator-plan`: `agent/issue-<N>`. Use `gh issue develop <N> --name agent/issue-<N> --base <base> --checkout` instead of a plain `git checkout -b` — it links the branch to the issue so it shows up under the issue's "Development" section in the GitHub UI. Uncommitted plan/ADR files in the working tree carry over automatically.
4. **Commit and push.** Stage only the plan file and any ADR files Phase 1 created this session — never `git add -A`:
   ```bash
   git add docs/plans/<plan-file> docs/adr/<adr-files...>
   git commit -m "docs: plan for #<N> — <task title>"
   git push -u origin agent/issue-<N>
   ```
5. **Report.** Issue URL, branch name, and files committed.
