# Custom Rules for exec

Custom rules let you inject project-specific or personal conventions into the exec workflow. Rules are free-form markdown loaded at skill invocation time and applied as additional instructions alongside the skill's built-in behavior.

## File Locations

Two levels, checked in order (first-found-wins, never merged):

1. **Project-level**: `.claude/planning-rules.md` in the current working directory
2. **User-level**: `$CLAUDE_PLUGIN_DATA/planning-rules.md` — only available when this skill is installed via a Claude Code plugin marketplace; not set when installed standalone (e.g. via `npx skills add`), in which case only the project level applies

When both non-empty files exist, only the project-level file is used. Empty files are treated as absent and fall through to the next level.

## Resolution

`exec` runs `scripts/resolve-rules.sh planning-rules.md` via Bash at startup. It falls back to the `$CLAUDE_PLUGIN_DATA` env var for the user-level tier if set, otherwise skips straight to project-level / empty. Outputs the first file found (project, then user) or empty output if neither exists.

## Managing Rules

Ask exec to manage rules:

- **show rules** — displays current rules and which level they came from
- **add/update project rules** — writes to `.claude/planning-rules.md`
- **add/update user rules** — writes to `$CLAUDE_PLUGIN_DATA/planning-rules.md` (requires plugin marketplace install)
- **clear project rules** — deletes `.claude/planning-rules.md`
- **clear user rules** — deletes `$CLAUDE_PLUGIN_DATA/planning-rules.md` (requires plugin marketplace install)

## Example Content

```markdown
## testing conventions
- use table-driven tests with testify
- mock external dependencies with moq
- aim for 80% coverage minimum

## naming
- use camelCase for local variables
- keep function names under 30 characters

## plan structure preferences
- max 5 checkboxes per task
- always include rollback steps for migrations
```

## How Rules Apply

- **exec**: rules propagate to task subagents via the `USER_RULES` placeholder in task prompts

Rules supplement built-in instructions — they never replace them.
