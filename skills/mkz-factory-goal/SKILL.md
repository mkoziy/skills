---
name: mkz-factory-goal
description: Turn a product conversation into one `goal`-labeled GitHub issue for the software factory's planner and auditor agents.
argument-hint: [repo owner/name] [what you want built]
allowed-tools: Read, Bash, Skill, AskUserQuestion
disable-model-invocation: true
---

# factory-goal

Product-discovery front door of the software factory. Output is exactly one GitHub issue labeled `goal`. A planner agent parses it into a plan and sub-issues; an auditor agent later checks delivered work against its Success criteria. The body format is a **contract**: keep the headings, order, and rules below verbatim.

Scope is **product**: what, why, for whom, how we know it's done. Implementation, architecture, and task breakdown belong to the planner. This skill ends at the created issue: plans, branches, ADRs, and code come later, from other agents.

1. **Resolve the repo.** The repo the user names, else the cwd's GitHub remote (`gh repo view --json nameWithOwner`). Run `gh auth status`; if either fails, tell the user and stop.
2. **Grill.** Invoke the `mkz-grilling` skill (Skill tool) with `$ARGUMENTS`, scoped to product questions: what, the problem behind it, for whom, checkable done-outcomes, explicit non-goals, the user's constraints and ideas. Ask only questions whose answer changes the outcome. Done when every template section below can be filled without guessing.
3. **Dedupe.** `gh issue list --repo <repo> --label goal --state open`. If an open goal covers the same outcome, propose adding the new material as a comment on it instead; on yes, `gh issue comment` and report its URL.
4. **Draft and confirm.** Write the body to a temp file using the template. Show the title and full body; revise until the user confirms.
5. **Create.** `gh label create goal --repo <repo>` if `gh label list` lacks it, then `gh issue create --repo <repo> --label goal --title "<short outcome-phrased title>" --body-file <tmpfile>`. Report the URL.

## Template

Exact headings, this order:

```markdown
## What
<what we are building, 2-5 sentences, user-facing terms>

## Why
<problem / motivation>

## Success criteria
1. <checkable outcome>
2. ...

## Non-goals
- ...

## Notes
<user's ideas, constraints, references; "-" if none>
```

**Success criteria** are numbered, each independently verifiable by an agent reading the repo, PR, or running app: an observable behaviour, or a command plus its expected result. Quality words ("fast", "robust", "nice") carry a measurable threshold. Implementation details belong in Notes as ideas, never as criteria.
