# skills

A flat collection of [Agent Skills](https://www.skills.sh/), installable with:

```bash
npx skills add mkoziy/skills
```

`npx skills` supports 70+ agents (Claude Code, Codex, Cursor, OpenCode, ...) — pass `-a <agent>` to target specific ones, or `-a '*'` for all of them.

Install a single skill:

```bash
npx skills add mkoziy/skills --skill critique
```

## Skills

| Skill | Description |
| --- | --- |
| [critique](skills/critique/SKILL.md) | Brutally honest critique of a plan, file, or prompt — exposes weak assumptions, logical gaps, and blind spots. |
| [brainstorm](skills/brainstorm/SKILL.md) | Turn ideas into designs through collaborative, one-question-at-a-time dialogue before implementation. |
| [exec](skills/exec/SKILL.md) | Execute a plan file's tasks sequentially, each in an isolated subagent, with review and finalize phases. |
| [git-review](skills/git-review/SKILL.md) | Interactive diff annotation review — edit the diff, get feedback addressed in a loop. |
| [pr](skills/pr/SKILL.md) | Comprehensive PR/issue review — architecture, tests, scope creep, drafts a review comment. |
| [writing-style](skills/writing-style/SKILL.md) | Direct, brief technical writing style for tickets, PR descriptions, and review comments. |
| [new](skills/new/SKILL.md) | Create a GitHub/GitLab/Gitea release with auto-versioning and generated release notes. |
| [last-tag](skills/last-tag/SKILL.md) | Show commits since the last tag in a formatted table. |
| [ask-codex](skills/ask-codex/SKILL.md) | Consult OpenAI Codex as a second opinion for investigation, debugging, or code review. |
| [dialectic](skills/dialectic/SKILL.md) | Prove and counter-prove a statement with parallel agents to eliminate confirmation bias. |
| [root-cause-investigator](skills/root-cause-investigator/SKILL.md) | Systematic 5-Why root cause analysis for bugs, failures, and regressions. |
| [learn](skills/learn/SKILL.md) | Capture strategic knowledge discovered during a session into CLAUDE.md. |
| [clarify](skills/clarify/SKILL.md) | Investigate and explain user confusion when expectations and reality diverge. |
| [wrong](skills/wrong/SKILL.md) | Reset and re-evaluate when the current approach has hit a dead end. |
| [md-copy](skills/md-copy/SKILL.md) | Format the final answer as markdown and copy it to the clipboard. |
| [txt-copy](skills/txt-copy/SKILL.md) | Copy generated text content to the clipboard. |

All skills except `critique` are ported from [umputun/cc-thingz](https://github.com/umputun/cc-thingz), flattened out of its per-plugin layout (`plugins/<plugin>/skills/<skill>/`) into the single-tier `skills/<skill>/` layout skills.sh expects, with plugin-only mechanics (`${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`) rewritten to resolve relative to each skill's own directory. Two plugin-only pieces didn't survive the port and aren't included:

- `skill-eval` — a `UserPromptSubmit` hook that forces skill evaluation before every response. Hooks aren't skills; there's no `SKILL.md` to write. Install it from cc-thingz's plugin marketplace if you want it.
- `planning`'s `make` command — a slash command + subagent + hook bundle for interactive plan authoring, not a standalone skill. `exec` (which runs an existing plan file) ported cleanly; `make` (which creates one) didn't.
