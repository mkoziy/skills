# `npx skills`: portable `SKILL.md` for Claude Code, Codex, Pi

Checked 2026-10-20 against [`vercel-labs/skills` `a80e4c9`](https://github.com/vercel-labs/skills/tree/a80e4c9d12d607631249d4d7d059f835d4b2f13a) and the current first-party docs.

## What `npx skills` actually does

It is an installer/discovery CLI, **not** a portability runtime. It copies or symlinks the same directory; it does not translate frontmatter or Claude-only instructions. Its source discovery expects a `SKILL.md` directory, requires `name` and `description`, and walks `skills/<name>/` (up to two category levels). [CLI authoring/discovery](https://github.com/vercel-labs/skills/blob/a80e4c9d12d607631249d4d7d059f835d4b2f13a/docs/creating-skills.md)

For the three targets, project installs split as follows:

| Harness | Project location used by `skills` | Native shared location |
|---|---|---|
| Claude Code | `.claude/skills/` | no shared `.agents` location |
| Codex | `.agents/skills/` | `.agents/skills/` |
| Pi | `.agents/skills/` | `.agents/skills/` |

The CLI’s current source makes Codex and Pi "universal" because both use `.agents/skills`; Claude gets a symlink to that canonical copy during `experimental_sync`, but ordinary `add` still targets its native location. [Agent paths](https://github.com/vercel-labs/skills/blob/a80e4c9d12d607631249d4d7d059f835d4b2f13a/docs/agents.md), [`agents.ts`](https://github.com/vercel-labs/skills/blob/a80e4c9d12d607631249d4d7d059f835d4b2f13a/src/agents.ts), [sync behavior](https://github.com/vercel-labs/skills/blob/a80e4c9d12d607631249d4d7d059f835d4b2f13a/docs/commands.md#skills-experimental_sync)

## Portable contract

Use only this frontmatter unless an explicitly harness-specific feature is intended:

```yaml
---
name: mkz-example
description: Does X. Use when Y.
license: MIT # only when applicable
compatibility: Requires git and jq # only when real
metadata: # optional string-to-string values
  author: mkoziy
---
```

- `name`: directory name exactly; lowercase letters/numbers/hyphens, 1–64 chars; no repeated/edge hyphens.
- `description`: concise routing text: capability + concrete trigger words + boundary. Put the main trigger first.
- Keep the body direct and short. All three advertise name/description first and load the body only after selection; Codex can truncate/omit long descriptions when the skill inventory exceeds its context budget.
- Bundle `scripts/`, `references/`, and `assets/`; link to files with paths relative to the skill directory. Do not depend on the current working directory.

This is the Agent Skills base spec, including the name/parent-directory match. [Specification](https://agentskills.io/specification) Codex explicitly recommends front-loading trigger words and exposes `$skill-name`/`/skills`; Pi documents the same description-routing and relative-path rule. [Codex](https://learn.chatgpt.com/docs/build-skills), [Pi `a731ba8`](https://github.com/badlogic/pi-mono/blob/a731ba8b80ac56662b4ca7f09102f94447862d8c/packages/coding-agent/docs/skills.md)

## Do not treat these as portable

- Claude-only frontmatter: `context: fork`, `agent`, `background`, `hooks`, `model`, `effort`, `arguments`, `when_to_use`, `user-invocable`, `disallowed-tools`, and Claude dynamic `!\`command\`` injection. Other harnesses may silently ignore fields.
- `allowed-tools` is experimental and tool names differ: omit it in cross-harness skills.
- `disable-model-invocation: true` is documented by Claude and Pi, but not in the base spec nor Codex’s skill-authoring docs. Use it only when manual-only behavior matters more than Codex parity; otherwise leave it out.
- Claude tool names and control flow (`Skill`, `Agent`, `Task`, `AskUserQuestion`, `EnterPlanMode`, hooks, plugin env vars) are not a shared API. `npx skills` will install them faithfully; the other agents simply cannot execute the promise. Tiny portability joke: copying a spellbook does not grant mana.

Claude’s extras and their semantics are documented here: [frontmatter](https://code.claude.com/docs/en/skills#frontmatter-reference), [invocation](https://code.claude.com/docs/en/skills#control-who-invokes-a-skill). The `skills` compatibility matrix likewise marks only basic skills as universally safe; `context: fork` is Claude-only. [Matrix](https://github.com/vercel-labs/skills/blob/a80e4c9d12d607631249d4d7d059f835d4b2f13a/docs/agents.md#compatibility)

## Cross-skill invocation

There is **no portable skill-to-skill invocation primitive**. Claude has its `Skill` tool; Codex documents `$name` as prompt-level explicit invocation; Pi documents `/skill:name` as a user command. None is an interoperable API a `SKILL.md` can call.

Therefore a wrapper must either:

1. be self-contained (best), or
2. state a normal instruction: “If `mkz-x` is installed, read its `SKILL.md` and follow it before continuing.” This is best-effort model behavior, not a dependency guarantee.

Do not make completion depend on option 2. If two skills need the same process, put that process in a bundled reference/script or duplicate a small stable section; ship any cross-skill dependency as one package only when the workflow can verify its files exist.

## Recommendation for this repo

Keep the `mkz-*` flat `skills/<name>/` layout and valid matching names. Rework every skill claimed as portable to: ordinary Markdown steps + universal filesystem/shell operations + local relative files. Mark Claude orchestration skills as Claude-only in their `compatibility` text or split their reusable core from the Claude wrapper. Do not promise that named MKZ skills can launch each other in all three harnesses.
