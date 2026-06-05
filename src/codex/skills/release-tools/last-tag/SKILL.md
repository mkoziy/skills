---
name: last-tag
description: Show commits since the last tag in a formatted table. Use when user asks "what changed since last release", "commits since last tag", "last-tag", "what's new", or wants to see recent unreleased changes.
allowed-tools: Bash
---

# Last Tag — Commits Since Last Release

{{ include "common/skills/release-tools/last-tag/_body.md" }}

## Interactive Details

After displaying the table, ask: "Show commit details? (1) All commits; (2) None; (3) Specific commit hash"

**If "All commits"**: For each commit run:
```bash
git show --stat --format="Commit: %h%nAuthor: %an <%ae>%nDate: %ad%n%n%s%n%n%b" --date=short HASH
```

**If "None"**: End.

**If specific hash**: Run the same `git show` for that commit only.
