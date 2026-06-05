---
name: new
description: Create a release — auto-detects GitHub/GitLab/Gitea, calculates semantic version, generates release notes from PRs/commits, shows preview for confirmation before publishing. Use when user asks to "create release", "cut release", "new release", "publish version".
allowed-tools: Bash
---

# Release Workflow

Creates GitHub, GitLab, or Gitea releases with auto-versioning and release notes.

## Activation Triggers

- "create release", "cut release", "new release"
- "publish version", "bump version", "new version"
- "tag and release"

## Scripts

Helper scripts in `~/.codex/skills/release-tools/new/scripts/`:
- `detect-platform.sh` — outputs `github`, `gitlab`, or `gitea`
- `calc-version.sh <type>` — outputs new version (e.g., `v1.2.3`)
- `get-notes.sh <platform>` — outputs release notes grouped by type

## Workflow

### Step 1: Ask Release Type

Ask the user: "What type of release? (1) Hotfix — bug fixes (1.2.3 → 1.2.4); (2) Minor — new features (1.2.3 → 1.3.0); (3) Major — breaking changes (1.2.3 → 2.0.0)"

Wait for response before continuing.

Scripts directory: `~/.codex/skills/release-tools/new/scripts` (substitute for `SCRIPTS_DIR` in the steps below).

### Step 2: Detect Platform

```bash
platform=$(sh SCRIPTS_DIR/detect-platform.sh)
```

### Step 3: Validate Prerequisites

```bash
# working tree must be clean
if [ -n "$(git status --porcelain)" ]; then
    echo "error: uncommitted changes — commit or stash first"
fi

git fetch origin --tags
```

### Step 4: Get Current Version

```bash
last_tag=$(git describe --tags --abbrev=0 --match "v*" 2>/dev/null || echo "none")
```

### Step 5: Calculate New Version

```bash
new_version=$(sh SCRIPTS_DIR/calc-version.sh <release_type>)
```

Verify tag doesn't already exist:
```bash
if git rev-parse "$new_version" &>/dev/null; then
    echo "error: tag $new_version already exists"
fi
```

### Step 6: Generate Release Notes

```bash
notes=$(sh SCRIPTS_DIR/get-notes.sh "$platform")
```

**Post-processing (Claude must do this before presenting):**
- Deduplicate entries with same description (PRs and their commits often duplicate)
- Prefer PR entries over commit entries when duplicated (PR has #number and @author)

Output format:
```
**New Features**
- add user authentication #45 @username

**Improvements**
- refactor auth module abc1234

**Bug Fixes**
- resolve login timeout #46 @username
```

### Step 7: Check and Update CHANGELOG

```bash
changelog=""
for f in CHANGELOG.md changelog.md CHANGELOG; do
    [ -f "$f" ] && changelog="$f" && break
done
```

If changelog exists:
1. Use the exact detected filename (never hardcode "CHANGELOG.md")
2. Read the file to understand its format (Keep a Changelog, simple list, etc.)
3. Add new version section at the top matching the existing format
4. Commit the changelog update:
```bash
git add "$changelog"
git commit -m "docs: update changelog for $new_version"
```


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

Ask: "Proceed with creating this release? (1) Yes, publish; (2) Cancel"

**Wait for confirmation before creating release.**

### Step 9: Create Release

Only after user confirms:

**GitHub:**
```bash
gh release create "$new_version" \
    --title "Version ${new_version#v}" \
    --notes "$notes"
```

**GitLab:**
```bash
glab release create "$new_version" \
    --name "Version ${new_version#v}" \
    --notes "$notes"
```

**Gitea:**
```bash
tea release create \
    --tag "$new_version" \
    --title "Version ${new_version#v}" \
    --note "$notes"
```

### Step 10: Report Result

Show new version, release URL, and confirm it was published.

## Edge Cases

| Case | Handling |
|------|----------|
| No previous tags | Default version based on type |
| Pre-release tag (v1.2.3-rc1) | Strip suffix, use base version |
| No PRs/MRs found | Show commits only |
| Tag already exists | Error and abort |
| No CHANGELOG file | Skip changelog update |
| Unknown CHANGELOG format | Ask user or use simple `## vX.Y.Z` format |

## Notes

- Tag format: `vX.Y.Z`
- Title format: `Version X.Y.Z`
- Entry format: `- description #123 @author` (PRs) or `- description abc1234` (commits)
- Grouped by type: New Features (feat), Improvements (refactor/perf/chore/docs), Bug Fixes (fix), Other
- Conventional commit prefix stripped from description for cleaner output
- Always show preview and get confirmation before publishing

