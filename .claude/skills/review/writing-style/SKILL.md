---
name: writing-style
description: Technical communication style for GitHub/GitLab tickets, PR/MR descriptions, issue comments, code review comments, commit messages. Direct, brief, no AI-speak. NOT for README.md, public docs, or blog posts.
allowed-tools: Read
---

# Technical Communication Style Guide

## User Override Check

Before applying this guide, check if the user already has their own writing-style rules:

1. Check CLAUDE.md files (project-level and user-level) for writing style sections
2. Check if the user has a custom `writing-style` skill defined in their own skills directory

**If user-defined writing rules exist**: defer to those rules entirely. Do not apply this guide.

**If no user-defined rules exist**: apply this guide as the default.

---

**USE THIS STYLE FOR:**
- GitHub/GitLab issue comments
- PR/MR descriptions and comments
- Code review comments
- Commit messages
- Technical discussions in tickets
- Internal team communication

**NOT for:**
- README.md — public-facing documentation
- Official documentation — user guides, API docs, tutorials
- Public blog posts — articles, announcements
- Release notes (public-facing)
- Any publicly visible content intended for general audience

For exceptions: use proper English, complete sentences, proper capitalization, no abbreviations, professional tone.

# Core Principles

## Brevity and Directness

- Get straight to the point
- Skip filler phrases and unnecessary context
- Short responses are fine when they convey the full message
- No "I hope this helps" or "let me know if you have questions"

## Honest and Direct Feedback

- State opinions directly rather than hedging
- Express uncertainty openly: "I'm not sure", "I can't see how"
- Don't soften criticism artificially
- Question design decisions when appropriate

## Problem-Solution Structure

- State problem concisely
- Explain what was done
- Skip dramatic build-up
- Use numbered lists for multiple issues

## Technical Precision

- Include exact references: file paths, line numbers, commit hashes
- Use inline code with backticks for identifiers
- Code blocks with triple backticks for snippets
- Assume reader has technical context

# AI-Typical Language to Avoid

**Filler phrases (delete entirely):**
- "It's important to note that..."
- "It's worth mentioning..."
- "In order to..." — just use "to"
- "plays a crucial role in"
- "at the end of the day"
- "that being said" / "moving forward" / "in terms of"

**Overused AI words:**
- "comprehensive" → "full", "complete"
- "robust" → "solid", "reliable"
- "leverage" / "utilize" → "use"
- "facilitate" → "help", "enable"
- "optimal" → "best"
- "seamless" → skip it
- "streamline" → "simplify"

**Hedging phrases (be direct instead):**
- "I think maybe we could consider..." → state opinion directly
- "It would seem that..." → state the fact
- "Perhaps it might be worth..." → suggest directly

**Meta-commentary (delete):**
- "This approach works by..." → just describe what it does
- "The benefit of this is..." → state the benefit directly

**Never use:**
- "Thanks in advance" / "Hope this helps"
- "Let me know if you have any questions"
- "I appreciate your patience"
- Corporate speak or marketing language

# Code Review Comments

- Point out issues directly
- Suggest alternatives with code when possible
- Reference specific lines
- Don't restate what the PR does — the author knows what they built

Good examples:
```
LGTM
```
```
lgtm. one minor thing — `loadPatterns` could filter in a single pass instead of two, but not a blocker
```
```
couple issues:

1. test failure in `TestFoo` — looks like missing mock setup
2. linter complains about unused param on line 42

otherwise looks good
```
```
I don't get why we need the Factory pattern here — there's only one implementation. could simplify to just `NewNotifier()` directly?
```

# Markdown Formatting

- Inline code: `` `like this` ``
- Code blocks: ` ```language `
- Bold: `**text**` for emphasis
- Lists with `-` or `1.`

