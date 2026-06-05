---
name: learn
description: Update local CLAUDE.md with strategic knowledge discovered during this session. Use when user says "learn", "save knowledge", "update claude.md", "capture learnings", or at end of significant work sessions.
allowed-tools: Read, Edit
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

Present discovered knowledge and ask: "Which items to save? List them by number, or 'all', or 'none'."

Wait for response, then save only the selected items to local CLAUDE.md.

## Important Guidelines

- Only capture genuinely new discoveries from this session
- Don't duplicate existing local or global CLAUDE.md content
- Focus on patterns observed, not specific code written
- Keep descriptions concise and actionable
- If no knowledge found, exit early without asking
