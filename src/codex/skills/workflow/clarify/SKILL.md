---
name: clarify
description: Handle confusion and misalignment. Use when user appears confused, frustrated, or shows misalignment between expectations and reality. Triggers on "I don't understand", "confused", "wait, shouldn't it...", "why is this happening", contradictory statements, or frustration signals.
allowed-tools: Read, Glob, Grep, Bash
---

# Clarify

Handle user confusion by verifying intent, explaining actual behavior, and determining if there's a real issue.

**Primary goal**: Clarify and explain, not fix. Most confusion stems from misunderstanding, not bugs.

{{ include "common/skills/workflow/clarify/_body.md" }}

## Phase 5: Plan the Fix (for real issues)

If Phase 4 identified a real issue (category F):

### Step 1: Summarize and Assess Scope

Explain to user what fixing this involves:

| Scope | Meaning |
|-------|---------|
| **Trivial** | Single file, no side effects |
| **Localized** | Few files, contained to one component |
| **Moderate** | Multiple components, requires testing |
| **Significant** | Cross-cutting concern, affects multiple subsystems |
| **Architectural** | Fundamental design change |

### Step 2: Present Options

When multiple approaches exist, list 2-4 options with trade-off descriptions and wait for user's choice.

### Step 3: Create a Plan

After user confirms an approach, describe the implementation plan clearly before touching any code.

## Response Format

```
## Understanding Your Confusion

**What you expected**: [user's expectation]
**What actually happens**: [actual behavior]

## Why This Happens

[Explanation with evidence — code references, config, docs]

## Assessment

[Category: Not an issue / Documentation issue / Real issue / Configuration issue]
```

## Guidelines

- Users are experienced developers — trust their instincts
- About half of confusion cases are real issues
- Never dismiss confusion as "user error" — investigate first
- Always back explanations with evidence from the actual codebase
