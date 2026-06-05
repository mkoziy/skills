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

{{ include "common/skills/review/pr/_phases01.md" }}

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

{{ include "common/skills/review/pr/_draft-rules.md" }}

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
