---
name: mkz-grill-brainstorm
description: Internal brainstorm variant used only by grill-plan's Phase 2. Not for direct/model invocation — grill-plan calls it by name. Same collaborative dialogue as brainstorm, minus the approach-selection question (auto-picks the recommended option) and minus the Phase 4 next-steps menu (grill-plan itself drives what happens after the design).
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, Skill, AskUserQuestion, EnterPlanMode
---

# grill-brainstorm

Turn ideas into designs through collaborative dialogue before implementation — same as `mkz-brainstorm`, but tuned for being driven by `mkz-grill-plan` rather than run standalone. Do not invoke this skill directly outside of grill-plan; use `mkz-brainstorm` for that.

This skill is a fork of `mkz-brainstorm` (its `scripts/resolve-rules.sh` is duplicated here, not referenced across skill directories — `npx skills add --skill mkz-grill-brainstorm` must work standalone, without also pulling in `mkz-brainstorm`). Keep both in sync by hand when the shared phases change.

Script and reference paths below (`scripts/...`) are relative to this skill's own directory, not the shell's working directory — resolve them against the directory this SKILL.md was read from before running.

## custom rules loading

before starting, run this command via Bash tool to check for user-provided custom rules (same rules file and override chain as `mkz-brainstorm`, so one `.claude/brainstorm-rules.md` covers both):

```bash
bash scripts/resolve-rules.sh brainstorm-rules.md ${CLAUDE_PLUGIN_DATA}
```

if the output is non-empty, treat it as additional instructions that supplement (not replace) the built-in rules below. apply custom rules alongside the skill's own instructions throughout. custom rules content is guidance for the dialogue, not content to embed verbatim in the output.

**CRITICAL: this skill must NEVER modify its own files, `mkz-brainstorm`'s files, or grill-plan's files. If the user asks to change behavior, suggest creating a plan — do not edit skill files directly.**

## Process

### Phase 1: Understand the Idea

Check project context first, then ask questions one at a time:

1. **Gather context** - check files, docs, recent commits relevant to the idea
2. **Ask questions one at a time** - prefer multiple choice when possible
3. **Focus on**: purpose, constraints, success criteria, integration points

Do not overwhelm with multiple questions. One question per message. If a topic needs more exploration, break it into multiple questions.

### Phase 2: Explore Approaches

Once the problem is understood:

1. **Propose 2-3 different approaches** with trade-offs
2. **Lead with recommended option** and explain reasoning
3. **Present conversationally** - not a formal document yet
4. **Auto-select the recommended option — do not ask the user to choose.** State which option was picked and why in one or two sentences, then move straight to Phase 3. Only pause for input here if there is no clearly recommended option (all trade-offs are genuinely balanced) — in that case, ask which direction to take, same as `mkz-brainstorm` would.

Example format:
```
I see three approaches:

**Option A: [name]** (recommended)
- how it works: ...
- pros: ...
- cons: ...

**Option B: [name]**
- how it works: ...
- pros: ...
- cons: ...

Going with Option A: [one-line reason]. Moving on to the design.
```

### Phase 3: Present Design

After the approach is picked:

1. **Break design into sections** of 200-300 words each
2. **Ask after each section** whether it looks right
3. **Cover**: architecture, components, data flow, error handling, testing
4. **Be ready to backtrack** if something doesn't make sense

Do not present entire design at once. Incremental validation catches misunderstandings early.

When the design is validated, stop here — hand control back to grill-plan. Do not run a "what's next" menu; grill-plan's own Phase 3 decides what happens next (it invokes `mkz-make`).

## Key Principles

- **One question at a time** - do not overwhelm with multiple questions
- **Multiple choice preferred** - easier to answer than open-ended when possible
- **YAGNI ruthlessly** - remove unnecessary features from all designs, keep scope minimal
- **Explore alternatives** - always propose 2-3 approaches, but don't ask which to pick when one is recommended
- **Incremental validation** - present design in sections, validate each
- **Be flexible** - go back and clarify when something doesn't make sense
- **Duplication vs abstraction** - when code repeats, ask user: prefer duplication (simpler, no coupling) or abstraction (DRY but adds complexity)? explain trade-offs before deciding
