---
name: exec
description: "Execute plan tasks sequentially using subagents. Use when user says 'exec', 'execute plan', 'run plan', or wants to implement a plan file task by task with isolated subagents."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, AskUserQuestion
---

# exec

Execute plan file tasks sequentially, each in an isolated subagent.

## Arguments

- `$ARGUMENTS` — path to plan file (optional; if omitted, ask user to pick from `docs/plans/`)

## File Resolution

ALWAYS use the resolve script to read prompt and agent files. NEVER construct the override chain manually:
```
bash ~/.codex/skills/planning/exec/scripts/resolve-file.sh prompts/task.md ~/.codex
bash ~/.codex/skills/planning/exec/scripts/resolve-file.sh agents/quality.txt ~/.codex
```
The script checks project overrides (`.codex/exec-plan/`), user overrides (`~/.codex/`), and bundled defaults automatically.

### Placeholder Substitution

After reading a prompt file, replace ALL placeholders with actual values before passing to a subagent. Subagents run in fresh contexts without env vars.

Always substitute: `PLAN_FILE_PATH`, `PROGRESS_FILE_PATH`, `DEFAULT_BRANCH`, `${CLAUDE_PLUGIN_ROOT}` → `~/.codex/skills/planning/exec`, `RESOLVE_SCRIPT` → `~/.codex/skills/planning/exec/scripts/resolve-file.sh`, `PLUGIN_DATA_DIR` → `~/.codex`, `USER_RULES` (resolved custom rules content or empty string), and phase-specific values (`FINDINGS_LIST`, `REVIEW_PHASE`, `DIFF_COMMAND`).

## Custom Rules Loading

Before starting execution, run:

```bash
bash ~/.codex/skills/planning/make/scripts/resolve-rules.sh planning-rules.md ~/.codex
```

If the output is non-empty, store it as the resolved custom rules. When substituting `USER_RULES` in task prompts, wrap the content: `"ADDITIONAL CUSTOM RULES:\n<content>"`. If empty, substitute empty string for `USER_RULES`.

## Process

### Step 1. Resolve plan file

If `$ARGUMENTS` contains a file path, use it. Otherwise, list `.md` files in `docs/plans/`, excluding `completed/`. If exactly one plan found, use it automatically. If multiple found, ask the user to pick one using AskUserQuestion.

Read the plan file. Count total Task sections (`### Task N:` or `### Iteration N:`) to know the scope.

Determine the default branch: `bash ~/.codex/skills/planning/exec/scripts/detect-branch.sh`

Announce to user: "Executing plan: <plan-name> — N tasks found, branch: <branch>"

### Step 2. Create branch

**MANDATORY**: Run the script below. Do NOT create the branch manually — the script strips the date prefix from the plan filename:

```
bash ~/.codex/skills/planning/exec/scripts/create-branch.sh <plan-file-path>
```

Capture and use the branch name it outputs.

### Step 3. Initialize progress file

Initialize the progress file:
```
bash ~/.codex/skills/planning/exec/scripts/init-progress.sh /tmp/progress-<plan-name>.txt <plan-file-path> <branch-name>
```
(derive `<plan-name>` from the plan file stem). Report the full progress file path to the user.

IMPORTANT: Always use `~/.codex/skills/planning/exec/scripts/append-progress.sh` to write to the progress file. Never write directly.

### Step 4. Task loop

Repeat until no `[ ]` checkboxes remain in any Task section:

1. **Re-read the plan file** (subagent modifies it each iteration)
2. **Find the first Task section** (`### Task N:` or `### Iteration N:`) that still has `[ ]` checkboxes
3. **If none found** — all tasks complete, go to step 5
4. **Announce the task to the user** — output a visible summary:
   - Task number and title (from the `### Task N:` header)
   - List all `[ ]` checkbox items in that task section
5. **Spawn a subagent** using Agent tool with:
   - `mode: "bypassPermissions"`
   - `subagent_type: "general-purpose"`
   - The task prompt from `prompts/task.md`, resolved via:
     ```
     bash ~/.codex/skills/planning/exec/scripts/resolve-file.sh prompts/task.md ~/.codex
     ```
     with all placeholders substituted (see Placeholder Substitution above)
6. **After subagent returns**, re-read the plan file and check if that task's checkboxes are now `[x]`
   - If yes — task succeeded, continue loop
   - If no — **retry** with a fresh subagent up to 1 time. If all retries fail, stop and report failure to user
7. **Report to user**: "Task N completed" (one line).

CRITICAL: Spawn exactly ONE task subagent per iteration and WAIT for it to return before starting the next. NEVER batch-spawn multiple task subagents in a single message.

CRITICAL: Do NOT stop the loop based on subagent return text. The ONLY condition to stop is: no `[ ]` checkboxes remain. Always re-read the plan file to check.

CRITICAL: You are the ORCHESTRATOR. Never read code, debug errors, investigate diagnostics, or fix issues yourself. All code work happens inside subagents.

Maximum iterations safety limit: 50. If reached, stop and report to user.

### Step 5. Review phase 1 — comprehensive then critical re-check

Report to user: "--- Review phase 1: comprehensive ---"

Loop up to 5 times:

1. **Read review.md as a playbook (NOT as a subagent prompt)** — resolve via:
   ```
   bash ~/.codex/skills/planning/exec/scripts/resolve-file.sh prompts/review.md ~/.codex
   ```
   Substitute `DEFAULT_BRANCH`, `PLAN_FILE_PATH`, `PROGRESS_FILE_PATH`, `${CLAUDE_PLUGIN_ROOT}` → `~/.codex/skills/planning/exec`, `RESOLVE_SCRIPT` → `~/.codex/skills/planning/exec/scripts/resolve-file.sh`, `PLUGIN_DATA_DIR` → `~/.codex`, and `REVIEW_PHASE`. Then follow the playbook FROM THIS SESSION: launch the specified parallel Agent calls in a single message.
   - **Iteration 1**: set `REVIEW_PHASE` to `comprehensive`. Launch 5 parallel review agents (quality, implementation, testing, simplification, documentation).
   - **Iteration 2+**: set `REVIEW_PHASE` to `critical`. Launch 2 parallel review agents. Report: "--- Review phase 1: critical re-check (iteration N) ---"

2. **Collect findings** from ALL launched review agents. Pass COMPLETE output to fixer. Log to progress file:
   ```
   bash ~/.codex/skills/planning/exec/scripts/append-progress.sh <progress-file> "review phase 1: findings"
   echo "<findings>" | bash ~/.codex/skills/planning/exec/scripts/append-progress.sh <progress-file>
   ```

3. **If ALL agents reported zero issues** → report "Review phase 1: clean" and proceed.

4. **Spawn a fixer agent** — resolve `prompts/fixer.md`:
   ```
   bash ~/.codex/skills/planning/exec/scripts/resolve-file.sh prompts/fixer.md ~/.codex
   ```
   Launch with `mode: "bypassPermissions"`, `subagent_type: "general-purpose"`. Pass the FULL unedited review output as FINDINGS_LIST.

5. **After fixer returns** → show "FIXES:" section to the user. Loop back to step 1.

If 5 iterations reached with issues still found, report "Review phase 1: max iterations reached, moving on" and continue.

### Step 6. Review phase 2 — code smells

Report to user: "--- Review phase 2: code smells analysis ---"

Run once:

1. **Spawn a smells agent** — resolve `agents/smells.txt`:
   ```
   bash ~/.codex/skills/planning/exec/scripts/resolve-file.sh agents/smells.txt ~/.codex
   ```
   Launch with `mode: "bypassPermissions"`, `subagent_type: "general-purpose"`.

2. **Collect findings** — report compact list to user. Log to progress file.

3. **If no issues found** → report "Smells analysis: clean" and proceed.

4. **Spawn a fixer agent** — resolve `prompts/fixer.md`. Pass FULL smells output as FINDINGS_LIST.

5. **After fixer returns** → report fixes. Proceed.

### Step 7. Review phase 3 — critical only

Report to user: "--- Review phase 3: critical/major only (single pass) ---"

Same structure as step 5 but with `REVIEW_PHASE` set to `critical`. Resolve `prompts/review.md` and follow its playbook — launch 2 parallel review agents (quality, implementation) focusing on critical/major issues only. Same fixer flow.

### Step 8. Completion

When all phases are done:
- Log completion: `bash ~/.codex/skills/planning/exec/scripts/append-progress.sh <progress-file> "completed"`
- Report final line: "All N tasks completed, reviews passed"
- Do NOT move the plan file or push — just report completion

## Key rules

- Each subagent gets a fresh context — no accumulated state from previous tasks
- Parent session only tracks: task number, success/failure, retry count
- Plan file is the single source of truth for progress — always re-read it
- No signals — just checkboxes in the plan for task progress
- Maintain progress file (`/tmp/progress-<plan-name>.txt`)
- Do not modify the plan file yourself — only subagents modify it
- Do not implement or fix code yourself — only subagents implement and fix
- If a subagent fails or leaves broken code, re-run the loop — do NOT investigate or fix it yourself
- NEVER dismiss findings as "pre-existing", "not from changes", or "architectural" — ALL findings are actionable
- NEVER summarize or filter agent findings — pass the full output to the fixer agent verbatim
- All prompt and agent files MUST be resolved through the resolve script before use
- All `subagent_type` values must be `general-purpose` — agent files provide the specialized prompt
- After reading a prompt file, substitute all placeholders before passing to subagent
