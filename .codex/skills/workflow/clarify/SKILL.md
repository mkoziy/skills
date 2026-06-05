---
name: clarify
description: Handle confusion and misalignment. Use when user appears confused, frustrated, or shows misalignment between expectations and reality. Triggers on "I don't understand", "confused", "wait, shouldn't it...", "why is this happening", contradictory statements, or frustration signals.
allowed-tools: Read, Glob, Grep, Bash
---

# Clarify

Handle user confusion by verifying intent, explaining actual behavior, and determining if there's a real issue.

**Primary goal**: Clarify and explain, not fix. Most confusion stems from misunderstanding, not bugs.

## Activation Triggers

- "confused", "I'm confused", "this is confusing"
- "I don't understand", "doesn't make sense"
- "wait, shouldn't it...", "but I thought..."
- "why is this happening", "I expected X but got Y"
- Frustration signals, contradictory statements
- Questions that reveal misconceptions about system behavior

## Important Context

Users often:
- **Work on multiple projects in parallel** — may confuse behaviors between them
- **Forget how things were implemented** — especially after time away
- **Have outdated mental models** — based on old versions or different projects

But also:
- **Users are experienced developers** — their instincts are often correct
- **Real bugs exist** — about half of confusion cases point to actual issues

**Do not assume either way. Investigate before concluding.**

## Phase 1: Identify the Confusion

1. Extract the core question — what specifically is the user asking about?
2. Identify the expectation — what did the user expect?
3. Identify the reality — what is actually happening?
4. Locate the gap — where is the misalignment?
5. Consider context mixing — could the user be thinking of a different project?

Categories of confusion:
- **Memory gap** — user forgot how it works, needs a reminder
- **Project mixing** — user confused this with another project
- **Outdated mental model** — understanding based on old behavior
- **Architectural** — misunderstanding system design or data flow
- **Behavioral** — expecting different runtime behavior
- **Configuration** — settings not producing expected results
- **Implementation** — code doesn't work as assumed

## Phase 2: Investigate

Before explaining, gather evidence:

1. Read relevant code — understand actual implementation
2. Check configuration — verify settings and their effects
3. Trace the flow — follow execution path if behavioral confusion

Do not guess or assume. Investigate the actual system state.

## Phase 3: Explain

1. **Acknowledge the confusion** — confusion is normal
2. **State the expectation** — "You expected X to do Y"
3. **State the reality** — "Actually, X does Z because..."
4. **Explain why** — reasoning/design decision behind the behavior
5. **Show evidence** — point to specific code, config, or docs

Tone: gentle, not condescending. If user mixed up projects, clarify without judgment.

## Phase 4: Assess

**Start with the most common cases first:**

**A) Memory gap** — user forgot how it works → gentle reminder with code references

**B) Project mixing** — thinking of a different project → clarify without judgment

**C) Outdated understanding** — system changed or model never matched → explain current behavior

**D) Documentation issue** — system works but docs are misleading → suggest updating docs

**E) Configuration issue** — can do what user expects but isn't configured → suggest config changes

**F) Real issue** — user's expectation is reasonable AND system genuinely doesn't meet it → **proceed to Phase 5**


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
