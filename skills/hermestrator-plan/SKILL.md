---
name: hermestrator-plan
description: Turn a GitHub issue into a ready-to-implement plan on an agent/issue-<N> branch, for mkoziy/hermestrator's poller/worker pipeline to pick up. Use when the user says "plan issue <N>", "prep ticket <N> for hermestrator", "hermestrator-plan <N>", or wants a GitHub issue turned into a docs/plans/ plan file on an agent/issue branch.
argument-hint: <issue-number> [additional context or doc links]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, AskUserQuestion, Skill
---

# hermestrator-plan

Turn a GitHub issue into a ready-to-implement plan file, committed and pushed on the branch [mkoziy/hermestrator](https://github.com/mkoziy/hermestrator)'s poller/worker pipeline expects.

This skill is the missing upstream half of hermestrator: hermestrator's poller finds issues labeled `agent-ready` with an `agent/issue-<N>` branch that already has a plan under `docs/plans/`, and triggers a worker to implement it. This skill produces exactly that — branch, plan, label — and stops there. Implementation happens later, in hermestrator's worker, or via this repo's own `exec` skill if you're doing it yourself.

## Dependencies

- `make` skill (this repo) — plan authoring; also runs an Auto review and a `critique` pass on the plan automatically before this skill sees its menu
- `gh` CLI, authenticated, with access to the target repo

## Arguments

`$ARGUMENTS` — `<issue-number>` optionally followed by free text: extra context, doc links, or clarifications not already in the issue. Example: `42 also see docs/architecture.md#billing for the batch API constraints`.

## Preconditions

Before starting, verify (fail fast with a clear message if any fail):
- cwd is inside a git repository — `git rev-parse --show-toplevel`
- `gh` is authenticated — `gh auth status`
- the issue exists and belongs to this repo's `gh` remote — `gh issue view <N> --json number,title,body,labels,url,state`
- if the issue is closed, confirm with the user before proceeding (don't silently plan a closed ticket)

## Step 1: Resolve the Issue

Run `gh issue view <N> --json title,body,labels,url,state` and capture title, body, labels, URL. Treat any trailing free text in `$ARGUMENTS` as additional context to fold in alongside the issue body — not a replacement for it.

## Step 2: Branch

Determine the base branch (default `main`; check `gh repo view --json defaultBranchRef` if unsure).

- Branch name is always `agent/issue-<N>` — the exact name hermestrator's poller looks for (`scripts/github-ticket-poller.sh` in hermestrator).
- Check if it exists locally (`git branch --list agent/issue-<N>`) or on the remote (`git ls-remote --heads origin agent/issue-<N>`).
  - **Doesn't exist**: `gh issue develop <N> --name agent/issue-<N> --base <base> --checkout` — links the branch to the issue so it shows up under the issue's "Development" section in the GitHub UI, and checks it out locally.
  - **Exists locally**: `git checkout agent/issue-<N>` and `git pull`.
  - **Exists on remote only**: `git checkout -b agent/issue-<N> origin/agent/issue-<N>`.
- Check `docs/plans/` on this branch (excluding `docs/plans/completed/`) for an existing `.md` file from a prior run of this skill. If one exists, ask the user in plain conversational text (not `AskUserQuestion` — this is a real judgment call, not a fixed choice) whether to replace it or keep both before continuing.

## Step 3: Draft the Plan

Invoke the `make` skill (via the Skill tool), passing as context: the issue title, body, URL, and any extra text from `$ARGUMENTS`. Let `make` run its normal question loop (its Step 0-1.5) and write `docs/plans/yyyymmdd-<task-name>.md` (its Step 2) — do not skip its interactive questions; they're the primary way the plan gets grounded in what the user actually wants, not just what the issue says. `make` then automatically runs an Auto review and a `critique` pass against the plan (its Step 3) before presenting its "what's next" menu (its Step 4) — let both run; the critique report produced here is what Step 4 below triages, so there's no separate critique to launch.

When `make`'s menu appears, relabel "Done" as **"Continue"** and skip its commit action — this skill's own Step 5 commit uses a message tied to the issue number, and letting `make` commit here would land the wrong message before the Q&A triage below has had a chance to fix anything. Skip **Interactive review** too (opens an editor/TUI, wrong fit here). If the user somehow picks **Implement**, that's still too early — the Q&A loop below hasn't run yet — so skip its commit the same way and proceed to the triage below.

## Step 4: Triage and Q&A

Take the critique report `make` already produced above — full report (Verdict, Critical Issues, Blind Spots, Effort Reality Check, Prioritized Actions). Don't run `critique` a second time against the same plan; nothing has changed since `make` ran it.

Go through its findings one at a time, Critical Issues first:

- **Auto-fixable** — the fix is derivable from context already in hand (the issue, the plan, the repo's own code/conventions): apply it directly to the plan file. Examples: a task missing a test-file path inferable from repo conventions, an internal contradiction between two tasks, a vague success criterion the issue actually specifies elsewhere.
- **Needs the user** — the fix requires information, a preference, or a scope decision only the user has (a product/scope call, a choice between two valid approaches, an assumption about an external system `critique` can't verify): raise it as a plain conversational message, not a locked `AskUserQuestion`. Explain what `critique` flagged and why it matters, then let the dialogue run — the user may ask what you mean, push back, or want more context before answering. Keep the thread open until they've given enough to act on, then apply the fix to the plan and move to the next item.

No re-run of `critique` after fixes are applied — one pass, not a loop.

## Step 5: Commit and Push

Once every finding has been auto-fixed or resolved through the Q&A loop:

```bash
git add docs/plans/<plan-file>
git commit -m "docs: plan for #<N> — <issue title>"
git push -u origin agent/issue-<N>
```

## Step 6: Label

Use AskUserQuestion (this one genuinely is a fixed choice):

```json
{
  "questions": [
    {
      "question": "Mark this issue agent-ready now, so hermestrator's poller picks it up on its next run?",
      "header": "agent-ready",
      "options": [
        {"label": "Yes, now", "description": "gh issue edit <N> --add-label agent-ready"},
        {"label": "Not yet", "description": "Leave the plan pushed but unlabeled — add it manually later when ready."}
      ],
      "multiSelect": false
    },
    {
      "question": "Route this issue to a specific coding agent, or use hermestrator's repo default?",
      "header": "Agent routing",
      "options": [
        {"label": "Repo default", "description": "No routing label added — hermestrator uses its configured default (ralphex-codex unless set otherwise)."},
        {"label": "agent-pi", "description": "gh issue edit <N> --add-label agent-pi"},
        {"label": "agent-codex", "description": "gh issue edit <N> --add-label agent-codex"}
      ],
      "multiSelect": false
    }
  ]
}
```

Apply the chosen labels via `gh issue edit <N> --add-label <label>`.

## Step 7: Report

Summarize: branch name, plan file path, whether it's labeled `agent-ready`, and (if labeled) that hermestrator's poller will pick it up on its next scheduled run.

## Key Principles

- This skill authors a plan; it never implements. Implementation is `exec`'s job, or hermestrator's worker downstream.
- Never batch commits — one commit at the end, after the plan is actually finished.
- Never silently overwrite an existing plan on the branch — always ask first.
- Clarifications are a conversation, not a form — let the user push back before locking in an answer.
