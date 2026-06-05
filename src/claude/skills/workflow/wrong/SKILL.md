---
name: wrong
description: Reset and re-evaluate when current approach isn't working. Use when user says "wrong", "this isn't working", "wrong approach", "start over", "try again", "bad direction", or current solution path has hit a dead end.
allowed-tools: Read, Grep, Glob, Bash, EnterPlanMode, AskUserQuestion
---

# Wrong — Reset and Re-evaluate

{{ include "common/skills/workflow/wrong/_body.md" }}

After presenting fresh approaches and trade-offs, use AskUserQuestion to confirm the chosen path before proceeding. If a real fix is needed, use EnterPlanMode to create a proper implementation plan.
