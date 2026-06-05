---
name: learn
description: Update local CLAUDE.md with strategic knowledge discovered during this session. Use when user says "learn", "save knowledge", "update claude.md", "capture learnings", or at end of significant work sessions.
allowed-tools: Read, Edit, AskUserQuestion
---

# Learn

{{ include "common/skills/workflow/learn/_body.md" }}

### 4. User Confirmation

**CRITICAL**: Use AskUserQuestion tool for granular selection. Build options dynamically:
- First option: "All knowledge" — save everything discovered
- Last option: "None" — skip saving
- Middle options: individual knowledge items (up to 2-3 most significant)

Example with 3 discoveries:
```json
{
  "questions": [{
    "question": "Which knowledge should I save to local CLAUDE.md?",
    "header": "Save",
    "options": [
      {"label": "All (3 items)", "description": "Save all discovered patterns"},
      {"label": "Testing pattern", "description": "Table-driven tests with shared fixtures"},
      {"label": "Config approach", "description": "Environment-based configuration loading"},
      {"label": "None", "description": "Skip saving, nothing worth keeping"}
    ],
    "multiSelect": false
  }]
}
```

Example with 1 discovery:
```json
{
  "questions": [{
    "question": "Save this knowledge to local CLAUDE.md?",
    "header": "Save",
    "options": [
      {"label": "Yes", "description": "Save: [brief description]"},
      {"label": "No", "description": "Skip saving"}
    ],
    "multiSelect": false
  }]
}
```

After user selection:
- "All" → save everything
- "None" → end without saving
- Specific item → save only that item
- "Other" → incorporate user's custom selection

## Important Guidelines

- Only capture genuinely new discoveries from this session
- Don't duplicate existing local or global CLAUDE.md content
- Focus on patterns observed, not specific code written
- Keep descriptions concise and actionable
- **MUST use AskUserQuestion tool for confirmation** (not plain text questions)
- If no knowledge found, exit early without asking
