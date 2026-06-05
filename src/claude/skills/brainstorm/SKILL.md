---
name: brainstorm
description: Use before any creative work or significant changes. Activates on "brainstorm", "let's brainstorm", "deep analysis", "analyze this feature", "think through", "help me design", "explore options for", or when user asks for thorough analysis of changes, features, or architectural decisions. Guides collaborative dialogue to turn ideas into designs through one-at-a-time questions, approach exploration, and incremental validation.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, Skill, AskUserQuestion, EnterPlanMode
---

# Brainstorm

Turn ideas into designs through collaborative dialogue before implementation.

## Custom Rules Loading

Before starting, run this command via Bash tool to check for user-provided custom rules:

```bash
bash ~/.claude/skills/brainstorm/scripts/resolve-rules.sh brainstorm-rules.md ~/.claude
```

If the output is non-empty, treat it as additional instructions that supplement (not replace) the built-in rules below. Apply custom rules alongside the skill's own instructions throughout the brainstorm process — they may influence design preferences, naming conventions, technology choices, or other aspects of the brainstorm session. Custom rules content is guidance for the brainstorm dialogue, not content to embed verbatim in the output.

### Rules Management

When the user asks to add, show, or clear custom brainstorm rules, handle these operations:

- **show rules**: run `bash ~/.claude/skills/brainstorm/scripts/resolve-rules.sh brainstorm-rules.md ~/.claude` and display the output. If the output is empty, tell the user no custom rules are configured at either level. Otherwise, to determine the source, check if `.claude/brainstorm-rules.md` exists and is non-empty (project-level) — if not, the output came from user-level (`~/.claude/brainstorm-rules.md`). Tell the user which level it came from.
- **add/update project rules**: write content to `.claude/brainstorm-rules.md` in the current working directory.
- **add/update user rules**: write content to `~/.claude/brainstorm-rules.md`.
- **clear project rules**: delete `.claude/brainstorm-rules.md`.
- **clear user rules**: delete `~/.claude/brainstorm-rules.md`.

Project-level rules (`.claude/brainstorm-rules.md`) take precedence over user-level rules (`~/.claude/brainstorm-rules.md`). When both non-empty files exist, only project-level rules are loaded. Empty files are treated as absent and fall through to the next level. See `~/.claude/skills/brainstorm/references/custom-rules.md` for full documentation on the rules mechanism.

**CRITICAL: this skill must NEVER modify its own files (skills, scripts, references). The ONLY files it may create or modify for rules management are `.claude/brainstorm-rules.md` and `~/.claude/brainstorm-rules.md`. If the user asks to change the skill's behavior, suggest creating a plan — do not edit skill files directly.**

{{ include "common/skills/brainstorm/_body.md" }}
