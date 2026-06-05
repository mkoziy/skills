---
name: exec
description: "Execute plan tasks sequentially using subagents. Use when user says 'exec', 'execute plan', 'run plan', or wants to implement a plan file task by task with isolated subagents."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, AskUserQuestion, TaskCreate, TaskUpdate, EnterWorktree
---

# exec

Execute plan file tasks sequentially, each in an isolated subagent.

## Arguments

- `$ARGUMENTS` — path to plan file (optional; if omitted, ask user to pick from `docs/plans/`)

## File Resolution

ALWAYS use the resolve script to read prompt and agent files. NEVER construct the override chain manually:
```
bash ~/.claude/skills/planning/exec/scripts/resolve-file.sh prompts/task.md ~/.claude
bash ~/.claude/skills/planning/exec/scripts/resolve-file.sh agents/quality.txt ~/.claude
```
The script checks project overrides (`.claude/exec-plan/`), user overrides (`~/.claude/`), and bundled defaults automatically.

### Placeholder Substitution

After reading a prompt file, replace ALL placeholders with actual values before passing to a subagent. Subagents run in fresh contexts without env vars.

Always substitute: `PLAN_FILE_PATH`, `PROGRESS_FILE_PATH`, `DEFAULT_BRANCH`, `${CLAUDE_PLUGIN_ROOT}` → `~/.claude/skills/planning/exec`, `RESOLVE_SCRIPT` → `~/.claude/skills/planning/exec/scripts/resolve-file.sh`, `PLUGIN_DATA_DIR` → `~/.claude`, `USER_RULES` (resolved custom rules content or empty string), and phase-specific values (`FINDINGS_LIST`, `REVIEW_PHASE`, `DIFF_COMMAND`).

## Custom Rules Loading

Before starting execution, run:

```bash
bash ~/.claude/skills/planning/make/scripts/resolve-rules.sh planning-rules.md ~/.claude
```

If the output is non-empty, store it as the resolved custom rules. When substituting `USER_RULES` in task prompts, wrap the content: `"ADDITIONAL CUSTOM RULES:\n<content>"`. If empty, substitute empty string for `USER_RULES`.

## Process

### Step 1. Resolve plan file

If `$ARGUMENTS` contains a file path, use it. Otherwise, list `.md` files in `docs/plans/`, excluding `completed/`. If exactly one plan found, use it automatically. If multiple found, ask the user to pick one using AskUserQuestion.

Read the plan file. Count total Task sections (`### Task N:` or `### Iteration N:`) to know the scope.

Determine the default branch: `bash ~/.claude/skills/planning/exec/scripts/detect-branch.sh`

### Step 2. Ask about worktree isolation

First detect current branch state — run `git branch --show-current` and compare with the default branch. Two cases:

**Case A — currently on the default branch (master/main/trunk).** Step 4 will create a new feature branch. Ask the user where it should live. Invoke the **AskUserQuestion** tool with this payload:

```json
{
  "questions": [{
    "question": "Where should the feature branch be created?",
    "header": "Branch location",
    "options": [
      {"label": "Worktree (isolated)", "description": "Create the feature branch in a new isolated git worktree (under .claude/worktrees/). Main working directory stays on the default branch."},
      {"label": "In-place", "description": "Create the feature branch in this working directory. Main directory switches to the feature branch for the duration of the run."}
    ],
    "multiSelect": false
  }]
}
```

**Case B — currently on a feature branch.** Ask whether to move it to an isolated worktree or stay here:

```json
{
  "questions": [{
    "question": "You're already on a feature branch. Run the plan here, or in an isolated worktree?",
    "header": "Isolation",
    "options": [
      {"label": "Stay here", "description": "Run the plan in this working directory, on the existing feature branch."},
      {"label": "Move to worktree", "description": "Copy this branch into a new isolated git worktree (under .claude/worktrees/). Main directory stays untouched."}
    ],
    "multiSelect": false
  }]
}
```

In BOTH cases: invoke AskUserQuestion **now**, do not generate text first, do not skip, do not assume.

If user picks "Worktree (isolated)" or "Move to worktree", use the `EnterWorktree` tool before proceeding. All subsequent steps happen inside the worktree. At completion, report the worktree path and branch.

### Step 3. Create task list

ALWAYS create tasks using TaskCreate before starting any work. Create one task per plan Task section plus review phases:

For each `### Task N:` section in the plan:
- `TaskCreate(subject="Task N: <title>", description="<checkbox items>", activeForm="Executing task N...")`

Then add review tasks:
- `TaskCreate(subject="Review phase 1: comprehensive", description="5 parallel review agents + fixer", activeForm="Running review phase 1...")`
- `TaskCreate(subject="Review phase 2: code smells", description="smells agent + fixer", activeForm="Running smells review...")`
- `TaskCreate(subject="Review phase 3: codex external", description="adversarial codex/claude review loop", activeForm="Running codex review...")`
- `TaskCreate(subject="Review phase 4: critical only", description="2 review agents + fixer", activeForm="Running review phase 4...")`
- `TaskCreate(subject="Finalize", description="rebase, clean up commits, verify", activeForm="Finalizing...")`
- `TaskCreate(subject="Stats summary", description="aggregate token/duration/git stats from session log", activeForm="Summarizing stats...")`

Update tasks as you go: `TaskUpdate(taskId, status="in_progress")` when starting, `TaskUpdate(taskId, status="completed")` when done.

### Step 4. Create branch

**MANDATORY**: Run the script below. Do NOT create the branch manually — the script strips the date prefix from the plan filename (e.g., `20260329-feature-name.md` → branch `feature-name`).

```
bash ~/.claude/skills/planning/exec/scripts/create-branch.sh <plan-file-path>
```

Capture and use the branch name it outputs.

### Step 5. Initialize progress file

Initialize the progress file:
```
bash ~/.claude/skills/planning/exec/scripts/init-progress.sh /tmp/progress-<plan-name>.txt <plan-file-path> <branch-name>
```
(derive `<plan-name>` from the plan file stem, e.g., `fix-issues.md` → `progress-fix-issues`). Report the full progress file path to the user.

IMPORTANT: Always use `~/.claude/skills/planning/exec/scripts/append-progress.sh` to write to the progress file after initialization. Never write directly.

### Step 6. Task loop

Repeat until no `[ ]` checkboxes remain in any Task section:

1. **Re-read the plan file** (subagent modifies it each iteration)
2. **Find the first Task section** (`### Task N:` or `### Iteration N:`) that still has `[ ]` checkboxes
3. **If none found** — all tasks complete, go to step 7
4. **Announce the task to the user** — before spawning the subagent, output a visible summary:
   - Task number and title (from the `### Task N:` header)
   - List all `[ ]` checkbox items in that task section
5. **Spawn a subagent** using Agent tool with:
   - `mode: "bypassPermissions"`
   - `subagent_type: "general-purpose"`
   - The task prompt from `prompts/task.md`, resolved via:
     ```
     bash ~/.claude/skills/planning/exec/scripts/resolve-file.sh prompts/task.md ~/.claude
     ```
     with all placeholders substituted (see Placeholder Substitution above)
6. **After subagent returns**, re-read the plan file and check if that task's checkboxes are now `[x]`
   - If yes — task succeeded, continue loop
   - If no — **retry** with a fresh subagent for the same task up to 1 time. If all retries fail, stop and report failure to user
7. **Report to user**: "Task N completed" (one line).

CRITICAL: Spawn exactly ONE task subagent per iteration and WAIT for it to return before starting the next. NEVER batch-spawn multiple task subagents in a single message. Plan tasks are ordered and interdependent.

CRITICAL: Do NOT stop the loop based on subagent return text. The ONLY condition to stop is: no `[ ]` checkboxes remain in any Task section. Always re-read the plan file to check.

CRITICAL: You are the ORCHESTRATOR. Never read code, debug errors, investigate diagnostics, or fix issues yourself. All code work happens inside subagents.

Maximum iterations safety limit: 50. If reached, stop and report to user.

### Step 7. Review phase 1 — comprehensive then critical re-check

Report to user: "--- Review phase 1: comprehensive ---"

Loop up to 5 times:

1. **Read review.md as a playbook (NOT as a subagent prompt)** — resolve via:
   ```
   bash ~/.claude/skills/planning/exec/scripts/resolve-file.sh prompts/review.md ~/.claude
   ```
   Substitute `DEFAULT_BRANCH`, `PLAN_FILE_PATH`, `PROGRESS_FILE_PATH`, `${CLAUDE_PLUGIN_ROOT}` → `~/.claude/skills/planning/exec`, `RESOLVE_SCRIPT` → `~/.claude/skills/planning/exec/scripts/resolve-file.sh`, `PLUGIN_DATA_DIR` → `~/.claude`, and `REVIEW_PHASE`. Then follow the playbook FROM THIS SESSION: launch the specified Agent tool calls in a single message for parallel execution.
   - **Iteration 1**: set `REVIEW_PHASE` to `comprehensive`. Launch 5 parallel review agents (quality, implementation, testing, simplification, documentation).
   - **Iteration 2+**: set `REVIEW_PHASE` to `critical`. Launch 2 parallel review agents (quality, implementation). Report: "--- Review phase 1: critical re-check (iteration N) ---"

2. **Collect findings** from ALL launched review agents. Pass the COMPLETE output (not a summary) to the fixer. Log to progress file:
   ```
   bash ~/.claude/skills/planning/exec/scripts/append-progress.sh <progress-file> "review phase 1: findings"
   echo "<findings>" | bash ~/.claude/skills/planning/exec/scripts/append-progress.sh <progress-file>
   ```

3. **If ALL agents reported zero issues** → report "Review phase 1: clean" and proceed to the next phase.

4. **Spawn a fixer agent** — resolve `prompts/fixer.md`:
   ```
   bash ~/.claude/skills/planning/exec/scripts/resolve-file.sh prompts/fixer.md ~/.claude
   ```
   Launch with `mode: "bypassPermissions"`, `subagent_type: "general-purpose"`. Pass the FULL unedited review output as FINDINGS_LIST.

5. **After fixer returns** → show the "FIXES:" section to the user. Loop back to step 1.

If 5 iterations reached with issues still found, report "Review phase 1: max iterations reached, moving on" and continue.

### Step 8. Review phase 2 — code smells

Report to user: "--- Review phase 2: code smells analysis ---"

Run once (no loop):

1. **Spawn a smells agent** — resolve `agents/smells.txt`:
   ```
   bash ~/.claude/skills/planning/exec/scripts/resolve-file.sh agents/smells.txt ~/.claude
   ```
   Launch one Agent tool call with `mode: "bypassPermissions"`, `subagent_type: "general-purpose"`.

2. **Collect findings** — report to user with a compact list. Log to progress file.

3. **If no issues found** → report "Smells analysis: clean" and proceed.

4. **Spawn a fixer agent** — resolve `prompts/fixer.md`. Pass the FULL smells output as FINDINGS_LIST.

5. **After fixer returns** → report fixes to user. Proceed.

### Step 9. Review phase 3 — codex external review

Report to user: "--- Review phase 3: codex external review ---"

Adversarial loop: codex reviews the code, fixer evaluates and fixes, codex re-reviews. The loop exits early once an iteration produces no `CRITICAL` or `MAJOR` findings.

Determine external review command:
- Check if codex is available: `which codex`
- If not available, report "External review: skipped (codex not available)" and proceed to step 10

Loop up to 10 times:

1. **Resolve the codex prompt**:
   ```
   bash ~/.claude/skills/planning/exec/scripts/resolve-file.sh prompts/codex-review.md ~/.claude
   ```
   Replace `DIFF_COMMAND`: iteration 1 = `git diff DEFAULT_BRANCH...HEAD`, subsequent = `git diff`. Also replace `PLAN_FILE_PATH` and `PROGRESS_FILE_PATH`.

2. **Run codex**:
   ```
   bash ~/.claude/skills/planning/exec/scripts/run-codex.sh "<resolved prompt>"
   ```
   with `run_in_background: true`. Wait for notification — do NOT poll or sleep.

3. **Check codex output** — if "NO ISSUES FOUND" or equivalent, phase is done. Proceed to step 10.

4. **Classify severity** — scan for `CRITICAL` or `MAJOR` markers. Set `has_blocking = true` if either present, otherwise `has_blocking = false`.

5. **Report codex findings** to user — show a compact list (one line per finding).

6. **Spawn a fixer agent** — resolve `prompts/fixer.md`, pass codex output as FINDINGS_LIST.

7. **Report fixer results** to user. Log to progress file.

8. **Decide whether to loop**:
   - If `has_blocking` is false → report "Codex review: only minor findings — fixes applied, stopping loop" and proceed to step 10.
   - Otherwise → loop back to step 1.

If 10 iterations reached, report "Codex review: max iterations reached, moving on" and continue.

### Step 10. Review phase 4 — critical only

Report to user: "--- Review phase 4: critical/major only (single pass) ---"

Same structure as step 7 but with `REVIEW_PHASE` set to `critical`. Resolve `prompts/review.md` and follow its playbook FROM THIS MAIN SESSION — launch 2 parallel review agents (quality, implementation) focusing on critical/major issues only. Same fixer flow.

### Step 11. Finalize

Check if this is a git repo: `bash ~/.claude/skills/planning/exec/scripts/detect-vcs.sh`. If `hg`, skip this step.

After all reviews pass, rebase and clean up commits.

Report to user: "--- Finalize: rebase and clean up commits ---"

Spawn one Agent tool call with `mode: "bypassPermissions"`, `subagent_type: "general-purpose"`, and the prompt from `prompts/finalizer.md` resolved via:
```
bash ~/.claude/skills/planning/exec/scripts/resolve-file.sh prompts/finalizer.md ~/.claude
```
Replace `DEFAULT_BRANCH`, `PLAN_FILE_PATH`, `PROGRESS_FILE_PATH`, and `${CLAUDE_PLUGIN_ROOT}` → `~/.claude/skills/planning/exec`.

This is best-effort — if rebase fails, report the issue but don't block completion.

### Step 12. Stats summary

Spawn one Agent tool call with `mode: "bypassPermissions"`, `subagent_type: "general-purpose"`, and the prompt from `prompts/stats.md` resolved via:
```
bash ~/.claude/skills/planning/exec/scripts/resolve-file.sh prompts/stats.md ~/.claude
```
Replace `DEFAULT_BRANCH` and `PROGRESS_FILE_PATH`.

Show the stats agent's full markdown output to the user verbatim.

This step is best-effort — if the stats agent fails, report the failure but do not block completion.

### Step 13. Completion

When stats summary is done (or skipped on failure):
- Log completion: `bash ~/.claude/skills/planning/exec/scripts/append-progress.sh <progress-file> "completed"`
- Report final line: "All N tasks completed, reviews passed, branch finalized"
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
