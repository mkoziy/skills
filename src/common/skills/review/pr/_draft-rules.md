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
