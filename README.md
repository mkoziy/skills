# skills

A flat collection of [Agent Skills](https://www.skills.sh/), installable with:

```bash
npx skills add mkoziy/skills
```

`npx skills` supports 70+ agents (Claude Code, Codex, Cursor, OpenCode, ...) — pass `-a <agent>` to target specific ones, or `-a '*'` for all of them.

Install a single skill:

```bash
npx skills add mkoziy/skills --skill mkz-critique
```

## Skills

`npx skills add` installs any of these into any of its 70+ supported harnesses, but installing a `SKILL.md` isn't the same as it *working* the same way everywhere: several skills call Claude Code-only mechanisms in their instructions — `Agent`/`Task` (subagents), `Skill` (invoke another skill), `EnterPlanMode`, `TaskCreate`/`TaskUpdate`/`TaskList`, `EnterWorktree`. Harnesses without an equivalent tool by that name won't be able to execute those steps. The **Portability** column below reflects that:

- 🟢 **Portable** — only uses universal tools (Bash, Read, Edit, Write, Grep, Glob). Should work anywhere `npx skills` installs it.
- 🟡 **Mostly portable** — uses `AskUserQuestion` for interactive prompts. Likely degrades gracefully to a plain-text question on harnesses without that exact tool, but untested outside Claude Code.
- 🔴 **Claude Code only** — depends on `Agent`/`Task`, `Skill`, `EnterPlanMode`, `TaskCreate`/`TaskUpdate`/`TaskList`, or `EnterWorktree`. Won't run as designed elsewhere.

| Skill | Description | Portability |
| --- | --- | --- |
| [mkz-critique](skills/mkz-critique/SKILL.md) | Brutally honest critique of a plan, file, or prompt — exposes weak assumptions, logical gaps, and blind spots. | 🟢 |
| [mkz-brainstorm](skills/mkz-brainstorm/SKILL.md) | Turn ideas into designs through collaborative, one-question-at-a-time dialogue before implementation. | 🔴 |
| [mkz-make](skills/mkz-make/SKILL.md) | Create a structured implementation plan in docs/plans/ with interactive context gathering, optional interactive/auto review. | 🔴 |
| [mkz-exec](skills/mkz-exec/SKILL.md) | Execute a plan file's tasks sequentially, each in an isolated subagent, with review and finalize phases. | 🔴 |
| [mkz-hermestrator-plan](skills/mkz-hermestrator-plan/SKILL.md) | Turn a GitHub issue into a plan on an agent/issue-&lt;N&gt; branch for [mkoziy/hermestrator](https://github.com/mkoziy/hermestrator)'s poller/worker pipeline to pick up. Chains make, an auto-review, and a critique subagent pass. | 🔴 |
| [mkz-factory-goal](skills/mkz-factory-goal/SKILL.md) | Grill a product idea (via mkz-grilling) into one `goal`-labeled GitHub issue, or adopt an existing issue as a goal in place, in a fixed What/Why/Success criteria/Non-goals/Notes format — the software factory's planner and auditor agents consume it. `disable-model-invocation: true`. | 🔴 |
| [mkz-grill-plan](skills/mkz-grill-plan/SKILL.md) | Chain grill-with-docs, grill-brainstorm, and make — doc-grilled design and planning, interactively in the main thread. | 🔴 |
| [mkz-grill-with-docs](skills/mkz-grill-with-docs/SKILL.md) | Stress-test a plan or design through an interview, critique the settled decisions in a fresh subagent, and capture the resulting ADRs and glossary. | 🔴 |
| [mkz-grilling](skills/mkz-grilling/SKILL.md) | Grill the user relentlessly about a plan, decision, or idea through a one-round-at-a-time design-tree interview. | 🔴 |
| [mkz-grill-brainstorm](skills/mkz-grill-brainstorm/SKILL.md) | grill-plan's own copy of brainstorm — auto-picks the recommended approach instead of asking, skips brainstorm's next-steps menu. `disable-model-invocation: true`: only grill-plan calls it by name, never triggers on its own. | 🔴 |
| [mkz-git-review](skills/mkz-git-review/SKILL.md) | Interactive diff annotation review — edit the diff, get feedback addressed in a loop. | 🟢 |
| [mkz-pr](skills/mkz-pr/SKILL.md) | Comprehensive PR/issue review — architecture, tests, scope creep, drafts a review comment. | 🔴 |
| [mkz-writing-style](skills/mkz-writing-style/SKILL.md) | Direct, brief technical writing style for tickets, PR descriptions, and review comments. | 🟢 |
| [mkz-new](skills/mkz-new/SKILL.md) | Create a GitHub/GitLab/Gitea release with auto-versioning and generated release notes. | 🟡 |
| [mkz-last-tag](skills/mkz-last-tag/SKILL.md) | Show commits since the last tag in a formatted table. | 🟡 |
| [mkz-ask-codex](skills/mkz-ask-codex/SKILL.md) | Consult OpenAI Codex as a second opinion for investigation, debugging, or code review. | 🟢 |
| [mkz-dialectic](skills/mkz-dialectic/SKILL.md) | Prove and counter-prove a statement with parallel agents to eliminate confirmation bias. | 🔴 |
| [mkz-diagnosing-bugs](skills/mkz-diagnosing-bugs/SKILL.md) | Diagnosis loop for hard bugs and performance regressions. | 🟢 |
| [mkz-learn](skills/mkz-learn/SKILL.md) | Capture strategic knowledge discovered during a session into CLAUDE.md. | 🟡 |
| [mkz-clarify](skills/mkz-clarify/SKILL.md) | Investigate and explain user confusion when expectations and reality diverge. | 🔴 |
| [mkz-wrong](skills/mkz-wrong/SKILL.md) | Reset and re-evaluate when the current approach has hit a dead end. | 🔴 |
| [mkz-backlog](skills/mkz-backlog/SKILL.md) | Read, work, and maintain a repo's deferred-work items in docs/backlog/, one file per item. | 🟡 |
| [mkz-retro](skills/mkz-retro/SKILL.md) | Conduct a retrospective on a coding session, suggesting environment/process improvements. | 🔴 |
| [mkz-md-copy](skills/mkz-md-copy/SKILL.md) | Format the final answer as markdown and copy it to the clipboard. | 🟢 |
| [mkz-txt-copy](skills/mkz-txt-copy/SKILL.md) | Copy generated text content to the clipboard. | 🟢 |
| [mkz-thermo-nuclear-code-quality-review](skills/mkz-thermo-nuclear-code-quality-review/SKILL.md) | Extremely strict maintainability review for abstraction quality, giant files, and spaghetti-condition growth. | 🟢 |
| [mkz-writing-for-agents](skills/mkz-writing-for-agents/SKILL.md) | Writing documents for agents — use when creating/editing skills or modifying AGENTS.md/CLAUDE.md. | 🟢 |

All skills except `mkz-critique` and `mkz-thermo-nuclear-code-quality-review` are ported from [umputun/cc-thingz](https://github.com/umputun/cc-thingz), flattened out of its per-plugin layout (`plugins/<plugin>/skills/<skill>/`) into the single-tier `skills/<skill>/` layout skills.sh expects, with plugin-only mechanics (`${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`) rewritten to resolve relative to each skill's own directory. `mkz-make` additionally had its `plan-review` custom subagent (`Task(subagent_type=plan-review)`, a Claude Code plugin-only mechanism skills.sh doesn't support) turned into a plain prompt file (`references/agents/plan-review.txt`) launched through a `general-purpose` subagent — the same pattern `mkz-exec`'s specialist reviewers already used.

One plugin-only piece didn't survive the port and isn't included:

- `skill-eval` — a `UserPromptSubmit` hook that forces skill evaluation before every response. Hooks aren't skills; there's no `SKILL.md` to write. Install it from cc-thingz's plugin marketplace if you want it.

These are copies, not a live reference to cc-thingz — that's a deliberate tradeoff for simpler install/reuse via `npx skills add` (a plugin dependency would defeat the point of this flat layout). The tradeoff is that they can drift from upstream: check [umputun/cc-thingz](https://github.com/umputun/cc-thingz) periodically for updates and re-port changes by hand.

`mkz-thermo-nuclear-code-quality-review` is ported from [cursor/plugins](https://github.com/cursor/plugins/blob/main/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md) (`cursor-team-kit`), unmodified since it has no plugin-only mechanics to rewrite. Same drift caveat as the cc-thingz copies applies: check upstream periodically for updates and re-port changes by hand.

`mkz-hermestrator-plan`, `mkz-grill-plan`, `mkz-factory-goal`, `mkz-backlog`, and `mkz-retro` are homegrown, not ported from cc-thingz. `mkz-hermestrator-plan` is a thin orchestrator over `mkz-make` and `mkz-critique` (both above), tightly coupled to how [mkoziy/hermestrator](https://github.com/mkoziy/hermestrator) expects its input (branch naming, plan location, labels). `mkz-grill-plan` chains `mkz-grill-with-docs`, `mkz-grill-brainstorm` (a `disable-model-invocation` fork of `mkz-brainstorm`, kept in sync by hand), and `mkz-make` in the main thread — subagents can't be used for the interactive phases since `AskUserQuestion` inside a subagent never reaches the user. `mkz-grill-with-docs` itself depends on `domain-modeling`, a separate, globally-installed skill not included here — it stops and reports the missing dependency rather than improvising if that's absent.
