## Activation Triggers

- "last tag", "last-tag", "since last tag"
- "what changed since last release"
- "commits since last tag"
- "what's new", "unreleased changes"

## Workflow

Run commands sequentially (avoid `$()` nesting in a single Bash call):

**Step 1:** Fetch tags from remote:
```bash
git fetch origin --tags
```

**Step 2:** Get the last tag:
```bash
git describe --tags --abbrev=0
```
Store this value (e.g., `v1.2.3`) for use in subsequent commands.

**Step 3:** Get commits since that tag with format `date|author|hash|subject`:
```bash
git log TAG..HEAD --format="%ad|%an|%h|%s" --date=short
```

**Step 4:** Check if all commits have the same author — extract unique authors from step 3 output.

**Step 5:** Format output:

**Single author** (one unique author in all rows):
```
Last tag: v1.2.3
Author: John Doe

| Date       | Commit  | Description                    |
|------------|---------|--------------------------------|
| 2025-12-20 | abc1234 | fix: resolve null pointer      |
| 2025-12-19 | def5678 | feat: add user authentication  |
```

**Multiple authors:**
```
Last tag: v1.2.3

| Date       | Author   | Commit  | Description                    |
|------------|----------|---------|--------------------------------|
| 2025-12-20 | John Doe | abc1234 | fix: resolve null pointer      |
| 2025-12-19 | Jane Doe | def5678 | feat: add user authentication  |
```

**No tag exists:** `No tags found in repository`

**No commits since tag:** `Last tag: v1.2.3\nNo commits since this tag`
