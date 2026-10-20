# Matt Pocock skills — adoption note

Checked 2026-10-20 against [`mattpocock/skills` at `5beb35b`](https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2), Matt Pocock's public upstream. It is MIT-licensed; adapted copies may be shipped with the license notice. Its README now lists native Codex plugin and `skills.sh` installation. This repository should retain its flat `skills/<name>/` layout, not adopt plugin packaging. [Source](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/README.md)

## Take these

1. **Replace `mkz-root-cause-investigator` with adapted `diagnosing-bugs`.** It is substantially stronger than the existing generic 5-Whys: first build a tight, red-capable, deterministic loop; then minimise, rank falsifiable hypotheses, probe, fix, and prove the original repro is gone. Bring `scripts/hitl-loop.template.sh` too. Strip the `GLOSSARY.md` assumption unless domain docs are adopted. [Source](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/diagnosing-bugs/SKILL.md)

2. **Add adapted `writing-for-agents`.** It fills the maintainer gap: strong trigger wording, context/cognitive-load trade-offs, completion criteria, progressive disclosure, and pruning stale/no-op instructions. Import its required sibling `SKILL-MECHANICS.md`, then replace its generic “Skill tool” wording for each harness. Best fit: this repo is itself a skills collection. [Skill](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/productivity/writing-for-agents/SKILL.md), [reference](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/productivity/writing-for-agents/SKILL-MECHANICS.md)

3. **Add adapted `retro`.** A useful post-session review: navigation pointers, automated checks, coding standards, steering-file pruning, tool economy, and missing information access. Rewrite its Skill-tool invocation and retain primary-source session inspection. [Source](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/retro/SKILL.md)

## Defer / do not duplicate

| Upstream | Decision |
| --- | --- |
| `tdd` | Good later addition: public seams, agreed seams, vertical red→green. Must import `tests.md`/`mocking.md` and either `codebase-design` or remove the call. [Source](https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/tdd) |
| `code-review` | Do not add another review router: overlaps `mkz-pr`, `mkz-git-review`, `mkz-thermo-nuclear-code-quality-review`. Borrow its `git diff <fixed>...HEAD` validation and explicit “no spec available” outcome instead. Requires parallel agents plus issue/spec discovery. [Source](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/code-review/SKILL.md) |
| `prototype` | Useful, but only if this repo deliberately expands into implementation skills. It is a package (`LOGIC.md`, `UI.md`); its throwaway-branch requirement is too prescriptive universally. [Source](https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/prototype) |
| `domain-modeling` + `codebase-design` | Defer as a pair. They require the glossary/ADR architecture and supporting references; one alone makes terminology few local skills use. [Domain](https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/domain-modeling), [design](https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/codebase-design) |
| `handoff` | Portable and sensible but low priority: platform session continuity already covers much of it. Add only if users routinely switch sessions/agents. [Source](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/productivity/handoff/SKILL.md) |
| `setup-matt-pocock-skills`, `triage`, `to-spec`, `to-tickets`, `implement`, `implement-spec`, `wayfinder` | Do not cherry-pick: a coupled tracker workflow using `docs/agents/*`, tracker CLI commands/labels, Skill-tool chaining, subagents, and worktrees. It conflicts with `mkz-make`, `mkz-exec`, `mkz-backlog`, and `mkz-hermestrator-plan`. [Setup](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/setup-matt-pocock-skills/SKILL.md), [implement-spec](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/implement-spec/SKILL.md) |
| `research`, `grilling`, `pr`, and misc niche skills | Already installed in this Codex environment, or too narrow/tool-specific to duplicate. `research` contains only the primary-source/background-agent rule without a repo-specific addition. [Promoted skill manifest](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/.claude-plugin/plugin.json) |

## Adaptation rules

- Preserve every sibling file named by a Markdown link; several upstream skills are packages, not a lone `SKILL.md`.
- Replace `Skill tool` instructions with a target-harness mechanism, or inline the required discipline. Do not retain invisible dependencies.
- Keep subagent/worktree operations only where explicitly harness-bound. Preserve a single-agent core.
- Do not import tracker/domain setup without its full dependency graph: it writes repo configuration and may create GitHub/GitLab labels. [Source](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/setup-matt-pocock-skills/SKILL.md)

The upstream tree has engineering, productivity, misc, and explicitly `in-progress` directories; only its promoted subset is in the plugin manifest. Treat `in-progress` as experiments. [Tree](https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills), [manifest](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/.claude-plugin/plugin.json)
