# Skills Builder

This repo builds skill and agent markdown files from `src/` into agent-specific folders for Claude and Codex, and deploys them to `~/.claude` and `~/.codex`.

## Layout

```
src/
  common/          # shared source (included via {{ include "..." }})
    skills/
    agents/
  claude/          # Claude-specific source
    skills/
    agents/
  codex/           # Codex-specific source
    skills/
    agents/
scripts/
  build.py         # expands includes, writes to .claude/ and .codex/
  deploy.sh        # copies built output to ~/.claude and ~/.codex
tests/
  test_build.py    # minimal build smoke test
```

## Agent Targeting

Only files under `src/claude` or `src/codex` are built. `src/common` is include-only — nothing is generated directly from it.

## Includes

Skill files can reuse shared content from anywhere under `src/` with:

```md
{{ include "common/skills/exec-simple/SKILL.md" }}
```

Include paths are resolved from `src/`.

## Build

Expand all includes and write generated files:

```bash
python3 scripts/build.py
```

The script scans `src/claude` and `src/codex`, expands `{{ include "..." }}` directives, and writes output into `.claude/` and `.codex/`, removing stale skill/agent directories first.

## Deploy

Copy built output to `~/.claude` and `~/.codex`:

```bash
bash scripts/deploy.sh
```

This copies each skill/agent subdirectory from `.claude/` and `.codex/` into the corresponding directories under `~`.

## Test

```bash
python3 -m unittest tests.test_build -v
```

## Notes

- Edit files under `src/`, not the generated output in `.claude/` or `.codex/`.
- Includes resolve from `src/`, so cross-agent includes work.
- Run `build.py` then `deploy.sh` to push changes to the live agent configs.
