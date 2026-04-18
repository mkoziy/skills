---
name: haiku-shell-routing
description: Route simple shell, repository inspection, and project test work to the haiku-shell subagent. Use when the task is mostly grep, find, ls, git status, git log, git diff, file lookup, test execution, or command-output summarization and does not require edits or deep reasoning.
allowed-tools: Task, Read, Grep, Glob
---

# Haiku Shell Routing

Use this skill to keep trivial command-heavy work cheap.

## When to Use

Activate this skill when the user asks for:
- `grep`, `rg`, `find`, `ls`, `tree`
- `git status`, `git log`, `git diff`, `git show`
- locating files or symbols
- reading a few files and summarizing them
- running tests or linters in a project
- bootstrapping dependencies only as needed to run tests
- lightweight repo inspection without edits

## Workflow

1. Decide whether the task is read-only and command-centric.
2. Treat project test execution as eligible cheap work, including setup commands required to run those tests.
3. If yes, delegate the work to the `haiku-shell` subagent immediately.
4. Ask the subagent for raw findings, exact commands, and concise failures, not broad analysis.
5. Summarize the result for the user or continue with higher-level work in the main agent.

## Do Not Use

Do not use this skill when the task requires:
- file edits
- multi-step debugging
- architecture decisions
- test fixes after initial diagnosis
- refactors
- ambiguous work where command output alone is insufficient

## Important Limitation

This is a routing hint, not a hard per-tool switch. It improves the chance that cheap shell work goes through a Haiku-backed subagent, but it cannot force every internal tool call onto Haiku.
