# skills

A flat collection of [Agent Skills](https://www.skills.sh/), installable with:

```bash
npx skills add mkoziy/skills
```

Or a single skill:

```bash
npx skills add mkoziy/skills --skill critique
```

## Skills

| Skill | Description |
| --- | --- |
| [critique](skills/critique/SKILL.md) | Brutally honest critique of a plan, file, or prompt — exposes weak assumptions, logical gaps, and blind spots. |
| [ask-codex](skills/ask-codex/SKILL.md) | Consult OpenAI Codex as a second opinion for investigation, debugging, or code review. |
| [dialectic](skills/dialectic/SKILL.md) | Prove and counter-prove a statement with parallel agents to eliminate confirmation bias. |
| [root-cause-investigator](skills/root-cause-investigator/SKILL.md) | Systematic 5-Why root cause analysis for bugs, failures, and regressions. |

`ask-codex`, `dialectic`, and `root-cause-investigator` are ported from [umputun/cc-thingz](https://github.com/umputun/cc-thingz)'s `thinking-tools` plugin.

`cc-thingz` also ships a `skill-eval` plugin that forces skill evaluation before every response — it's a hook (`UserPromptSubmit`), not a skill, so it has no `SKILL.md` and isn't portable to this format. Install it directly from cc-thingz's plugin marketplace if you want it.
