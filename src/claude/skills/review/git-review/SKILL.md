---
name: git-review
description: Interactive git diff annotation review. Opens diff in editor via tmux/kitty/wezterm overlay, user annotates directly, Claude reads annotations and fixes code in a loop. Activates on "git review", "review changes", "review my changes", "annotate changes", "interactive review".
allowed-tools: Bash, Read, Edit, Write
---

# Git Review

Interactive annotation-based code review using editor overlays.

## Activation Triggers

- "git review", "review changes", "review my changes"
- "annotate changes", "interactive review"
- "review diff", "annotate diff"

## Workflow

### Step 1: Run the Script

```bash
python3 ~/.claude/skills/review/git-review/scripts/git-review.py [base_ref]
```

- No arguments: auto-detects uncommitted changes or branch vs default branch
- With argument: diffs against the specified ref (branch, tag, commit, `HEAD~3`)

{{ include "common/skills/review/git-review/_body.md" }}
