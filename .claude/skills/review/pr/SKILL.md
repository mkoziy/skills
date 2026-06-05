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

## Phase 0: Detect PR vs Issue

Determine if the target is a PR or an issue. If a URL is provided, check for `/pull/` or `/issues/`. If just a number:

```bash
gh pr view <number> --json number 2>/dev/null && echo "PR" || echo "ISSUE"
```

- **PR** → proceed with full PR review workflow
- **Issue** → use the Issue Comment Flow below

### Issue Comment Flow

1. Fetch issue details and discussion:
```bash
gh issue view <number> --json title,body,author,state,labels,comments,createdAt
```

2. Read the full discussion — understand what was reported, what others said, linked PRs

3. Investigate the codebase if the issue references specific code, files, or behavior

4. Draft a comment addressing the issue — analysis of root cause, proposed approach, questions for clarification, or next steps

5. Confirm with user before posting:
```bash
gh issue comment <number> --body-file /tmp/issue-comment.md
```

---

## Phase 1: Fetch PR Metadata and Discussion History

Get PR number from `$ARGUMENTS`. If not provided, list recent PRs and ask user to select:

```bash
gh pr list --limit 5 --state all
gh pr view <number> --json title,body,additions,deletions,changedFiles,files,author,state,headRefName
gh pr view <number> --json comments,reviews
```

Capture: title, body, files, scope (additions/deletions), author, state, discussion history.

### 1.1 Analyze Discussion History

```bash
gh api repos/{owner}/{repo}/issues/<number>/comments --jq '.[] | "[\(.user.login)] \(.body)"'
gh api repos/{owner}/{repo}/pulls/<number>/comments --jq '.[] | "[\(.user.login) on \(.path):\(.line)] \(.body)"'
gh api repos/{owner}/{repo}/pulls/<number>/reviews --jq '.[] | "[\(.user.login) - \(.state)] \(.body)"'
```

Get inline review comments (where suggestions live):
```bash
gh api repos/{owner}/{repo}/pulls/<number>/comments --jq '.[] | "[\(.user.login) on \(.path):\(.line // .original_line)]\n\(.body)\n---"'
```

Summarize:
- What issues were raised by reviewers?
- What was addressed vs still open?
- Valid automated review findings (Copilot, etc.)?

**Do not re-raise issues already discussed and resolved.**

### 1.2 Check Merge Status

```bash
gh pr view <number> --json mergeable,mergeStateStatus,statusCheckRollup
```

Report: mergeable status, CI status, whether conflicts exist.

Print summary:
```
PR #<number>: <title>
Author: <author> | State: <state>
+<additions>/-<deletions> across <changedFiles> files
Merge status: <mergeable> | <mergeStateStatus>
CI: <pass/fail summary>

Discussion: <N> comments, <M> reviews
- Resolved: <list>
- Open: <list>
```


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

## Draft Comment Rules

**Apply writing-style skill** — direct, brief, no AI-speak. See `review:writing-style`.

**CRITICAL: Don't restate what the PR does.** The author knows what they built. Focus only on issues, questions, and LGTM.

**CRITICAL: Never duplicate what the user already said in previous comments.** Check the discussion history from Phase 1.1 and exclude anything the user already posted.

**Only add sections if there are actual issues:**

- **Issues** — test failures, linter errors, bugs (numbered list)
- **Questions** — unclear design decisions, missing context
- **Complexity concerns** — if over-engineered, suggest simpler alternative

**For clean PRs, just "LGTM" is fine.**

**Code suggestions**: always show proper error handling — never ignore errors even in snippets.

Good examples:
```
LGTM
```
```
lgtm. one minor thing — `loadPatterns` could filter in a single pass, not a blocker
```
```
couple issues:

1. test failure in `TestFoo` — looks like missing mock setup
2. linter complains about unused param on line 42

otherwise looks good
```

After posting approval, analyze commits and recommend merge strategy:

```bash
gh pr view <number> --json commits --jq '.commits[] | "\(.oid[:8]) \(.messageHeadline)"'
```

- **Rebase and merge**: clean commits, each meaningful
- **Squash and merge**: messy commits (wip, fixup, typo fixes, "address review")
- **Merge commit**: meaningful merge history worth preserving (rare)

## Cleanup

After review is complete (posted or cancelled):

```bash
git worktree remove "/tmp/pr-review-<number>" --force 2>/dev/null || true
git branch -D pr-<number> 2>/dev/null || true
```


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
