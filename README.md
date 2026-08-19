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

`npx skills add` installs any of these into any of its 70+ supported harnesses, but installing a `SKILL.md` isn't the same as it *working* the same way everywhere: several skills call Claude Code-only mechanisms in their instructions — `Agent`/`Task` (subagents), `Skill` (invoke another skill), `EnterPlanMode`, `TaskCreate`/`TaskUpdate`/`TaskList`, `EnterWorktree`. Harnesses without an equivalent tool by that name won't be able to execute those steps. The **Portability** column below reflects that:

- 🟢 **Portable** — only uses universal tools (Bash, Read, Edit, Write, Grep, Glob). Should work anywhere `npx skills` installs it.
- 🟡 **Mostly portable** — uses `AskUserQuestion` for interactive prompts. Likely degrades gracefully to a plain-text question on harnesses without that exact tool, but untested outside Claude Code.
- 🔴 **Claude Code only** — depends on `Agent`/`Task`, `Skill`, `EnterPlanMode`, `TaskCreate`/`TaskUpdate`/`TaskList`, or `EnterWorktree`. Won't run as designed elsewhere.

| Skill | Description | Portability |
| --- | --- | --- |
| [critique](skills/critique/SKILL.md) | Brutally honest critique of a plan, file, or prompt — exposes weak assumptions, logical gaps, and blind spots. | 🟢 |
| [brainstorm](skills/brainstorm/SKILL.md) | Turn ideas into designs through collaborative, one-question-at-a-time dialogue before implementation. | 🔴 |
| [make](skills/make/SKILL.md) | Create a structured implementation plan in docs/plans/ with interactive context gathering, optional interactive/auto review. | 🔴 |
| [exec](skills/exec/SKILL.md) | Execute a plan file's tasks sequentially, each in an isolated subagent, with review and finalize phases. | 🔴 |
| [hermestrator-plan](skills/hermestrator-plan/SKILL.md) | Turn a GitHub issue into a plan on an agent/issue-&lt;N&gt; branch for [mkoziy/hermestrator](https://github.com/mkoziy/hermestrator)'s poller/worker pipeline to pick up. Chains make, an auto-review, and a critique subagent pass. | 🔴 |
| [grill-plan](skills/grill-plan/SKILL.md) | Chain grill-with-docs, brainstorm, and make — doc-grilled design and planning, interactively in the main thread. Requires the separately-installed `grill-with-docs` skill. | 🔴 |
| [git-review](skills/git-review/SKILL.md) | Interactive diff annotation review — edit the diff, get feedback addressed in a loop. | 🟢 |
| [pr](skills/pr/SKILL.md) | Comprehensive PR/issue review — architecture, tests, scope creep, drafts a review comment. | 🔴 |
| [writing-style](skills/writing-style/SKILL.md) | Direct, brief technical writing style for tickets, PR descriptions, and review comments. | 🟢 |
| [new](skills/new/SKILL.md) | Create a GitHub/GitLab/Gitea release with auto-versioning and generated release notes. | 🟡 |
| [last-tag](skills/last-tag/SKILL.md) | Show commits since the last tag in a formatted table. | 🟡 |
| [ask-codex](skills/ask-codex/SKILL.md) | Consult OpenAI Codex as a second opinion for investigation, debugging, or code review. | 🟢 |
| [dialectic](skills/dialectic/SKILL.md) | Prove and counter-prove a statement with parallel agents to eliminate confirmation bias. | 🔴 |
| [root-cause-investigator](skills/root-cause-investigator/SKILL.md) | Systematic 5-Why root cause analysis for bugs, failures, and regressions. | 🟢 |
| [learn](skills/learn/SKILL.md) | Capture strategic knowledge discovered during a session into CLAUDE.md. | 🟡 |
| [clarify](skills/clarify/SKILL.md) | Investigate and explain user confusion when expectations and reality diverge. | 🔴 |
| [wrong](skills/wrong/SKILL.md) | Reset and re-evaluate when the current approach has hit a dead end. | 🔴 |
| [md-copy](skills/md-copy/SKILL.md) | Format the final answer as markdown and copy it to the clipboard. | 🟢 |
| [txt-copy](skills/txt-copy/SKILL.md) | Copy generated text content to the clipboard. | 🟢 |
| [thermo-nuclear-code-quality-review](skills/thermo-nuclear-code-quality-review/SKILL.md) | Extremely strict maintainability review for abstraction quality, giant files, and spaghetti-condition growth. | 🟢 |

All skills except `critique` and `thermo-nuclear-code-quality-review` are ported from [umputun/cc-thingz](https://github.com/umputun/cc-thingz), flattened out of its per-plugin layout (`plugins/<plugin>/skills/<skill>/`) into the single-tier `skills/<skill>/` layout skills.sh expects, with plugin-only mechanics (`${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`) rewritten to resolve relative to each skill's own directory. `make` additionally had its `plan-review` custom subagent (`Task(subagent_type=plan-review)`, a Claude Code plugin-only mechanism skills.sh doesn't support) turned into a plain prompt file (`references/agents/plan-review.txt`) launched through a `general-purpose` subagent — the same pattern `exec`'s specialist reviewers already used.

One plugin-only piece didn't survive the port and isn't included:

- `skill-eval` — a `UserPromptSubmit` hook that forces skill evaluation before every response. Hooks aren't skills; there's no `SKILL.md` to write. Install it from cc-thingz's plugin marketplace if you want it.

These are copies, not a live reference to cc-thingz — that's a deliberate tradeoff for simpler install/reuse via `npx skills add` (a plugin dependency would defeat the point of this flat layout). The tradeoff is that they can drift from upstream: check [umputun/cc-thingz](https://github.com/umputun/cc-thingz) periodically for updates and re-port changes by hand.

`thermo-nuclear-code-quality-review` is ported from [cursor/plugins](https://github.com/cursor/plugins/blob/main/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md) (`cursor-team-kit`), unmodified since it has no plugin-only mechanics to rewrite. Same drift caveat as the cc-thingz copies applies: check upstream periodically for updates and re-port changes by hand.

`hermestrator-plan` and `grill-plan` are homegrown, not ported from cc-thingz. `hermestrator-plan` is a thin orchestrator over `make` and `critique` (both above), tightly coupled to how [mkoziy/hermestrator](https://github.com/mkoziy/hermestrator) expects its input (branch naming, plan location, labels). `grill-plan` chains `grill-with-docs` (a separate, globally-installed skill — not included here), `brainstorm`, and `make` in the main thread — subagents can't be used for the interactive phases since `AskUserQuestion` inside a subagent never reaches the user.
