## step 0: parse intent and gather context

before asking questions, understand what the user is working on:

1. **parse user's command arguments** to identify intent:
   - "add feature Z" / "implement W" → feature development
   - "fix bug" / "debug issue" → bug fix plan
   - "refactor X" / "improve Y" → refactoring plan
   - "migrate to Z" / "upgrade W" → migration plan
   - generic request → explore current work

2. **gather relevant context quickly** — use direct tool calls (Read, Glob, Grep). keep discovery under 30 seconds:

   **for feature development:**
   - glob for files matching the feature area (e.g., `**/*auth*`, `**/*cache*`)
   - read 1-3 most relevant files to understand existing patterns
   - check project structure with a quick `ls` of key directories

   **for bug fixing:**
   - grep for error messages or function names mentioned in the request
   - read the specific file(s) involved
   - check `git log --oneline -5` for recent changes

   **for refactoring/migration:**
   - glob for files matching the area being refactored
   - read 2-3 key files to understand current structure
   - grep for imports/references to identify dependencies

   **for generic/unclear requests:**
   - check `git status` and `git log --oneline -5`
   - read README.md or CLAUDE.md for project overview
   - `ls` the top-level directory structure

   **CRITICAL: do NOT read more than 5 files in this step. the goal is a quick scan, not exhaustive analysis. if more context is needed, ask the user in step 1.**

3. **synthesize findings** into a brief context summary (3-5 bullet points):
   - what the project is and primary language/framework
   - which files/areas are relevant to the request
   - key patterns or conventions observed
