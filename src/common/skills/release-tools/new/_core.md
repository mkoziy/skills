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
