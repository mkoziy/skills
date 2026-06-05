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
