---
name: new
description: Create a release — auto-detects GitHub/GitLab/Gitea, calculates semantic version, generates release notes from PRs/commits, shows preview for confirmation before publishing. Use when user asks to "create release", "cut release", "new release", "publish version".
allowed-tools: Bash, AskUserQuestion
---

# Release Workflow

Creates GitHub, GitLab, or Gitea releases with auto-versioning and release notes.

## Activation Triggers

- "create release", "cut release", "new release"
- "publish version", "bump version", "new version"
- "tag and release"

## Scripts

Helper scripts in `~/.claude/skills/release-tools/new/scripts/`:
- `detect-platform.sh` — outputs `github`, `gitlab`, or `gitea`
- `calc-version.sh <type>` — outputs new version (e.g., `v1.2.3`)
- `get-notes.sh <platform>` — outputs release notes grouped by type

## Workflow

### Step 1: Ask Release Type

```json
{
  "questions": [{
    "question": "What type of release is this?",
    "header": "Version",
    "options": [
      {"label": "Hotfix", "description": "Bug fixes (1.2.3 → 1.2.4)"},
      {"label": "Minor", "description": "New features (1.2.3 → 1.3.0)"},
      {"label": "Major", "description": "Breaking changes (1.2.3 → 2.0.0)"}
    ],
    "multiSelect": false
  }]
}
```

Scripts directory: `~/.claude/skills/release-tools/new/scripts` (substitute for `SCRIPTS_DIR` in the steps below).

{{ include "common/skills/release-tools/new/_core.md" }}

### Step 8: Preview and Confirm

Show the release preview:

```
=== Release Preview ===
Platform: GitHub/GitLab/Gitea
Current version: v1.2.3
New version: v1.3.0
CHANGELOG: <filename> will be updated (or "none found")

Release Notes:
--------------
<notes>
--------------
```

Then use AskUserQuestion:

```json
{
  "questions": [{
    "question": "Proceed with creating this release?",
    "header": "Release",
    "options": [
      {"label": "Yes, publish", "description": "Create tag and publish release"},
      {"label": "Cancel", "description": "Abort release"}
    ],
    "multiSelect": false
  }]
}
```

**Wait for confirmation before creating release.**

{{ include "common/skills/release-tools/new/_publish.md" }}
