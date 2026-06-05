---
name: pr
description: Comprehensive PR/issue review — analyzes architecture, tests, identifies scope creep, drafts review comment. Use when user asks to review a PR, check a PR, look at PR changes, or comment on an issue.
argument-hint: '<pr-or-issue-number>'
allowed-tools: Bash, Read, Grep, Glob, Write, AskUserQuestion, Agent
---

# PR Review

Comprehensive pull request review: architecture, tests, scope creep, review comment drafting.

## Activation Triggers

- "review pr 123", "check pr 123", "look at pr 123"
- "review the pr", "what do you think about this pr"
- "comment on issue 42", "look at issue 42"

{{ include "common/skills/review/pr/_phases01.md" }}

## Phase 1.5: Select Review Mode

After presenting the Phase 1 summary, use AskUserQuestion:

```json
{
  "questions": [{
    "question": "Review mode for PR #<number>?",
    "header": "Mode",
    "options": [
      {"label": "Full review", "description": "Clone, run tests/linter, architecture analysis, scope creep detection (Recommended)"},
      {"label": "Quick review", "description": "Diff-only, summarize what/why/size, flag obvious issues"}
    ],
    "multiSelect": false
  }]
}
```

- **Full review** → Phase 2
- **Quick review** → Quick Review path

## Quick Review Path

Lightweight review based on diff and metadata only. No worktree, no subagent.

**Q1. Read and summarize diff:**
```bash
gh pr diff <number>
```
Present: What (2-3 sentences), Why (purpose), Size (+N/-N across M files), Files changed (grouped).

**Q2. Flag obvious issues** — bugs, missing error handling, hardcoded values, TODO/FIXME added, missing tests, unrelated changes.

**Q3.** Skip to Phase 5 (Draft Review Comment).

## Phase 2: Deep Analysis via Subagent

### 2.1 Setup Worktree

```bash
git fetch origin pull/<number>/head:pr-<number>
git worktree add "/tmp/pr-review-<number>" pr-<number>
```

**Do NOT use `gh pr checkout`** — it switches the main repo's branch.

### 2.2 Launch Analysis Agent

Use Agent tool to run the full analysis. Pass all context the agent needs:

```
prompt: |
  You are reviewing PR #<number> for <repo>.

  PR metadata:
  - Title: <title>
  - Description: <body>
  - Files: <file list>
  - Discussion summary: <from Phase 1.1>

  Worktree location: /tmp/pr-review-<number>
  Repo location: <repo_path>

  Tasks:
  1. Read changed files in full from the worktree
  2. Run validation — tests, linter, race checks as appropriate for the project type
  3. Architecture analysis: over-engineering, pattern violations, error handling,
     concurrency issues, security concerns, test quality
  4. Scope creep: categorize each file as Core / Supporting / Related cleanup / Unrelated

  Do NOT clean up the worktree.

  Return a structured report:
  - Functionality: 3-5 sentences on what the PR does
  - Key decisions: notable implementation choices
  - Validation results: test pass/fail, linter issues
  - Architecture issues: list with file:line references
  - Over-engineering: specific instances with simpler alternatives
  - Scope creep: unrelated files with explanation
  - Positives: what's done well
  - Open questions: design decisions needing user input
```

### 2.3 Receive Report

The agent returns a condensed report. Present it to the user.

## Phase 3: Present Findings and Confirm Next Step

Present the agent report. Then use AskUserQuestion:

```json
{
  "questions": [{
    "question": "How would you like to proceed?",
    "header": "Continue?",
    "options": [
      {"label": "Draft review comment", "description": "Proceed to Phase 5"},
      {"label": "Investigate further", "description": "Ask agent for details on a specific finding"},
      {"label": "Done", "description": "End review without posting"}
    ],
    "multiSelect": false
  }]
}
```

## Phase 4: Resolve Open Questions

For each open question from the agent report, use AskUserQuestion with specific options. Wait for user response on each before proceeding.

## Phase 5: Draft Review Comment

**Check previous comments first** — never duplicate what the user already said.

{{ include "common/skills/review/pr/_draft-rules.md" }}

Display the complete draft before asking:

```json
{
  "questions": [{
    "question": "Post this review to PR #<number>?",
    "header": "Review",
    "options": [
      {"label": "Approve", "description": "Post review and approve"},
      {"label": "Comment", "description": "Post as review comment, no approval"},
      {"label": "Request changes", "description": "Post review requesting changes"},
      {"label": "Edit", "description": "Tell me what to change"},
      {"label": "Cancel", "description": "Discard draft"}
    ],
    "multiSelect": false
  }]
}
```

Post via:
```bash
cat > /tmp/pr-review.md << 'REVIEW_END'
<review content>
REVIEW_END
gh pr review <number> --body-file /tmp/pr-review.md --comment
```

After **Approve**, recommend merge strategy via AskUserQuestion (rebase/squash/merge based on commit quality).

## Notes

- **Never duplicate user's previous comments** — check discussion history first
- **Subagent for heavy lifting** — file reading, validation, architecture analysis runs in agent to protect context window
- **Never switch the main repo's branch during review** — use `git fetch` + worktree
- **Simplicity bias** — always ask "could this be simpler?"
- **Over-engineering is a bug** — unnecessary abstraction is as problematic as missing abstraction
