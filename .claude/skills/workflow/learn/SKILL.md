---
name: learn
description: Update local CLAUDE.md with strategic knowledge discovered during this session. Use when user says "learn", "save knowledge", "update claude.md", "capture learnings", or at end of significant work sessions.
allowed-tools: Read, Edit, AskUserQuestion
---

# Learn

## Activation Triggers

- "learn", "save knowledge", "update claude.md", "capture learnings"
- At end of significant work sessions
- Before finishing a session where architectural patterns were discovered

## Analysis Process

1. **Review Session History** — examine all files read and modified during this session
2. **Extract Strategic Knowledge** — filter out tactical details, focus on reusable patterns
3. **Categorize Findings:**
   - Project architecture and structure
   - Data flow patterns
   - External service integrations
   - Project-specific conventions
   - Key dependencies and their purposes
   - Testing strategies
   - Build and deployment processes
   - Operational knowledge (debugging, useful queries, log locations)

## What Qualifies for Local CLAUDE.md

**INCLUDE** — strategic discoveries from this session:
- Architectural patterns uncovered while working
- Project structure insights gained from navigation
- Conventions noticed across multiple files
- Integration patterns discovered
- Configuration approaches identified
- Testing strategies observed
- Build/deployment processes encountered
- Operational knowledge:
  - Database locations and connection details per environment
  - Useful queries discovered during debugging
  - Log locations and monitoring endpoints
  - Environment-specific quirks and gotchas

**EXCLUDE** — session-specific tactical work:
- The specific bug we fixed
- The particular feature we implemented
- Temporary workarounds
- One-off code changes
- TODO items we encountered

## Decision Criteria

Ask for each discovery:
- "Will this help understand the project in 6 months?"
- "Is this a pattern that appears multiple times?"
- "Does this represent a project-wide convention?"
- "Would knowing this speed up future development?"
- "Would this save debugging time in the future?"

## Workflow

### 1. Check Existing Local CLAUDE.md
Read current content to avoid duplication.

### 2. Early Exit if Nothing Found
If no new strategic knowledge was discovered:
- Report "no new strategic knowledge to capture"
- End the skill execution without asking further

### 3. Present New Knowledge
Format discovered knowledge for local CLAUDE.md:
```markdown
## [Section Name]
- Discovery 1
- Discovery 2
```


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
