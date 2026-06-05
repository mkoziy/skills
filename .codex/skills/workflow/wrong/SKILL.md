---
name: wrong
description: Reset and re-evaluate when current approach isn't working. Use when user says "wrong", "this isn't working", "wrong approach", "start over", "try again", "bad direction", or current solution path has hit a dead end.
allowed-tools: Read, Grep, Glob, Bash
---

# Wrong — Reset and Re-evaluate

## Activation Triggers

- "wrong", "this isn't working", "wrong approach"
- "start over", "try again", "bad direction"
- Current solution path hit a dead end and needs a fresh perspective

## Workflow

### Step 1: Re-analyze the Core Problem

State the problem in clear, simple terms. What exactly are we trying to solve?

### Step 2: Identify Missing Context

Determine what additional information is needed about:
- The existing codebase and its patterns
- Performance requirements or constraints
- Integration points with other systems
- Expected usage patterns or scale
- Any domain-specific requirements not yet mentioned

Read relevant files to understand the codebase context before proposing alternatives.

### Step 3: Propose Fresh Approaches

Suggest 2-3 alternative solutions that:
- Follow project best practices and idioms
- Match the existing code's style and architecture patterns
- Are maintainable and testable
- Solve the exact problem without over-engineering
- Don't use shortcuts or hacks

### Step 4: Explain Trade-offs

For each proposed approach:
- Why this approach fits the problem
- Main benefits and drawbacks
- How it integrates with the existing codebase

### Step 5: Recommend the Best Path Forward

Which approach is most appropriate and why? Ask clarifying questions if needed before proceeding.

## Requirements

- Solution must be production-ready, not a proof of concept
- Code should be idiomatic and follow established patterns
- Include comprehensive tests with edge cases
- No placeholders — complete, runnable code

