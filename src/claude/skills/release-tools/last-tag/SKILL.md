---
name: last-tag
description: Show commits since the last tag in a formatted table. Use when user asks "what changed since last release", "commits since last tag", "last-tag", "what's new", or wants to see recent unreleased changes.
allowed-tools: Bash, AskUserQuestion
---

# Last Tag — Commits Since Last Release

{{ include "common/skills/release-tools/last-tag/_body.md" }}

## Interactive Details

After displaying the table, use AskUserQuestion:

```json
{
  "questions": [{
    "question": "Show commit details?",
    "header": "Details",
    "options": [
      {"label": "All commits", "description": "Show full details for each commit"},
      {"label": "None", "description": "Skip details"},
      {"label": "Specific commit", "description": "Enter commit hash to inspect"}
    ],
    "multiSelect": false
  }]
}
```

**If "All commits"**: For each commit run:
```bash
git show --stat --format="Commit: %h%nAuthor: %an <%ae>%nDate: %ad%n%n%s%n%n%b" --date=short HASH
```

**If "None"**: End.

**If "Specific commit"** or user enters hash via "Other": Run the same `git show` for that commit only.
