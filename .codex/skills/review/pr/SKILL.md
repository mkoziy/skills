---
name: pr
description: Comprehensive PR/issue review — analyzes architecture, tests, identifies scope creep, drafts review comment. Use when user asks to review a PR, check a PR, look at PR changes, or comment on an issue.
argument-hint: '<pr-or-issue-number>'
allowed-tools: Bash, Read, Grep, Glob, Write
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

Ask the user: "Review mode? (1) Full — clone, run tests, architecture analysis; (2) Quick — diff-only summary"

- **Full review** → Phase 2
- **Quick review** → Quick Review path

## Quick Review Path

**Q1. Read and summarize diff:**
```bash
gh pr diff <number>
```
Present: What (2-3 sentences), Why, Size (+N/-N across M files), Files changed.

**Q2. Flag obvious issues** — bugs, missing error handling, hardcoded values, TODO/FIXME added, missing tests, unrelated changes.

**Q3.** Skip to Phase 5 (Draft Review Comment).

## Phase 2: Deep Analysis

Create a worktree:
```bash
git fetch origin pull/<number>/head:pr-<number>
git worktree add "/tmp/pr-review-<number>" pr-<number>
```

**Do NOT use `gh pr checkout`** — it switches the main repo's branch.

Read all changed files from the worktree. Then:

1. **Validate** — run tests and linter appropriate for the project type:
```bash
cd /tmp/pr-review-<number>
# detect project type and run: go test ./..., pytest, npm test, etc.
```

2. **Architecture analysis** — over-engineering, pattern violations, error handling, concurrency, security, test quality

3. **Scope creep** — categorize each file: Core / Supporting / Related cleanup / Unrelated

Present condensed findings to the user.

## Phase 3: Present Findings

After presenting findings, ask: "How to proceed? (1) Draft review comment (2) Done — no review"

## Phase 4: Resolve Open Questions

For each design decision needing user input, ask directly and wait for response before proceeding.

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


Present the draft to the user. Ask: "Post this review? (1) Approve (2) Comment (3) Request changes (4) Edit (5) Cancel"

Post via:
```bash
cat > /tmp/pr-review.md << 'REVIEW_END'
<review content>
REVIEW_END
gh pr review <number> --body-file /tmp/pr-review.md --comment
```

After approval, ask about merge strategy (rebase/squash/merge based on commit quality).

## Notes

- **Never duplicate user's previous comments** — check discussion history first
- **Never switch the main repo's branch during review** — use `git fetch` + worktree
- **Simplicity bias** — always ask "could this be simpler?"
