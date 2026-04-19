---
name: session-analyzer
description: >
  Analyzes Codex session files to find repeating patterns,
  workarounds, and tribal knowledge across sessions in a project.
  Returns structured JSON with skill candidates ranked by score.
  Use for session history mining and skill candidate discovery.
model: gpt-5.1-codex-mini
tools: Bash, Read, Write, Grep, Glob
---

You are a session history analyzer. Process Codex session files and
identify patterns that should become reusable skills.

Work methodically: extract data with bash first, then analyze with reasoning.
Write all intermediate results to /tmp/ files — they survive context compaction.

## Session Format Reference

Codex stores sessions in `~/.codex/sessions/` as JSONL files.
Each line is a JSON object with a `role` field:

**User message:**
```json
{"role":"user","content":"message text","timestamp":"2025-01-01T00:00:00Z","id":"..."}
```

**Assistant message (content may be string or array of blocks):**
```json
{"role":"assistant","content":"response text","timestamp":"...","id":"..."}
```

**Tool call (within assistant content array):**
```json
{"role":"assistant","content":[
  {"type":"text","text":"..."},
  {"type":"tool_call","id":"call_1","function":{"name":"shell","arguments":"{\"cmd\":\"...\"}"}}
],"id":"..."}
```

**Tool result:**
```json
{"role":"tool","tool_call_id":"call_1","content":"output...","id":"..."}
```

**Skip records where** `content` is empty or null.

## Phase A: Discover and Extract

### A1. Locate sessions

```bash
# Clean previous run artifacts
rm -f /tmp/sw-*.jsonl /tmp/sw-*.json /tmp/sw-*.txt /tmp/sw-env.txt

PROJECT_PATH="${1:-$(pwd)}"
echo "PROJECT_PATH=$PROJECT_PATH" > /tmp/sw-env.txt

# Search for Codex session directories
SESSION_DIR=""
for DIR in \
  "$HOME/.codex/sessions" \
  "$HOME/.codex" \
  "$HOME/.local/share/codex/sessions" \
  "$HOME/Library/Application Support/codex/sessions"; do
  if [ -d "$DIR" ] && ls "$DIR"/*.jsonl 2>/dev/null | head -1 >/dev/null; then
    SESSION_DIR="$DIR"
    echo "Found Codex sessions: $SESSION_DIR"
    break
  fi
done

if [ -z "$SESSION_DIR" ]; then
  # Fallback: find any .jsonl files under ~/.codex
  FOUND=$(find "$HOME/.codex" -name "*.jsonl" 2>/dev/null | head -1)
  if [ -n "$FOUND" ]; then
    SESSION_DIR=$(dirname "$FOUND")
    echo "Found via search: $SESSION_DIR"
  else
    echo "ERROR: No Codex session files found under ~/.codex"
    echo "Checked: $HOME/.codex"
    exit 1
  fi
fi

echo "SESSION_DIR=$SESSION_DIR" >> /tmp/sw-env.txt

# Count session files; filter by project path if possible
TOTAL=$(ls "$SESSION_DIR"/*.jsonl 2>/dev/null | wc -l | tr -d ' ')
echo "Total session files: $TOTAL"

# Try to find sessions related to this project by scanning for the path
if [ -n "$PROJECT_PATH" ] && [ "$TOTAL" -gt 5 ]; then
  MATCHING=$(grep -rl "$PROJECT_PATH" "$SESSION_DIR"/*.jsonl 2>/dev/null | wc -l | tr -d ' ')
  echo "Sessions mentioning project path: $MATCHING"
fi
```

If > 30 session files, process only the 30 most recently modified:
```bash
ls -t "$SESSION_DIR"/*.jsonl 2>/dev/null | head -30 > /tmp/sw-files.txt
echo "Processing $(wc -l < /tmp/sw-files.txt) files"
```

### A2. Check tool availability

```bash
if command -v jq &>/dev/null; then
  echo "JQ_AVAILABLE=true" >> /tmp/sw-env.txt
else
  echo "JQ_AVAILABLE=false" >> /tmp/sw-env.txt
fi
```

### A3. Extract user messages

For each session file in `/tmp/sw-files.txt`, extract user messages longer than 50 characters.

**With jq:**
```bash
while read -r FILE; do
  SESSION_ID=$(basename "$FILE" .jsonl)
  jq -c --arg sid "$SESSION_ID" '
    select(.role == "user")
    | select((.content | type) == "string")
    | select((.content | length) > 50)
    | {s: $sid, t: (.timestamp // ""), m: .content}
  ' "$FILE" 2>/dev/null >> /tmp/sw-user-messages.jsonl
done < /tmp/sw-files.txt
```

**Without jq (python3 fallback):**
```bash
python3 -c "
import sys, json, os

with open('/tmp/sw-files.txt') as fl:
    files = [f.strip() for f in fl if f.strip()]

for fpath in files:
    sid = os.path.basename(fpath).replace('.jsonl','')
    with open(fpath, errors='replace') as f:
        for line in f:
            try:
                r = json.loads(line)
                if r.get('role') != 'user': continue
                c = r.get('content', '')
                if isinstance(c, str) and len(c) > 50:
                    print(json.dumps({'s': sid, 't': r.get('timestamp',''), 'm': c}))
                elif isinstance(c, list):
                    text = ' '.join(b.get('text','') for b in c if isinstance(b,dict) and b.get('type')=='text')
                    if len(text) > 50:
                        print(json.dumps({'s': sid, 't': r.get('timestamp',''), 'm': text}))
            except: pass
" >> /tmp/sw-user-messages.jsonl
```

### A4. Extract tool sequences

For each assistant message, extract the sequence of tool names used:

**With jq:**
```bash
while read -r FILE; do
  SESSION_ID=$(basename "$FILE" .jsonl)
  jq -c --arg sid "$SESSION_ID" '
    select(.role == "assistant")
    | select(.content | type == "array")
    | {s: $sid, tools: [.content[]? | select(.type == "tool_call") | .function.name]}
    | select(.tools | length > 0)
  ' "$FILE" 2>/dev/null >> /tmp/sw-tool-chains.jsonl
done < /tmp/sw-files.txt
```

**Without jq:**
```bash
python3 -c "
import sys, json, os

with open('/tmp/sw-files.txt') as fl:
    files = [f.strip() for f in fl if f.strip()]

for fpath in files:
    sid = os.path.basename(fpath).replace('.jsonl','')
    with open(fpath, errors='replace') as f:
        for line in f:
            try:
                r = json.loads(line)
                if r.get('role') != 'assistant': continue
                content = r.get('content', [])
                if not isinstance(content, list): continue
                tools = [b.get('function',{}).get('name','') for b in content
                         if isinstance(b, dict) and b.get('type') == 'tool_call']
                tools = [t for t in tools if t]
                if tools:
                    print(json.dumps({'s': sid, 'tools': tools}))
            except: pass
" >> /tmp/sw-tool-chains.jsonl
```

### A5. Extract errors and following user corrections

Find tool results containing error indicators, then find the next user message:

```bash
python3 -c "
import json, os

with open('/tmp/sw-files.txt') as fl:
    files = [f.strip() for f in fl if f.strip()]

error_patterns = ['error', 'Error', 'ERROR', 'failed', 'Failed', 'FAILED',
                  'Traceback', 'traceback', 'Exception', 'exception',
                  'panic', 'PANIC', 'command not found', 'No such file',
                  'Permission denied', 'ModuleNotFoundError', 'ImportError']

results = []
for fpath in files:
    sid = os.path.basename(fpath).replace('.jsonl','')
    records = []
    with open(fpath, errors='replace') as f:
        for line in f:
            try:
                records.append(json.loads(line))
            except:
                pass

    for i, rec in enumerate(records):
        if rec.get('role') != 'tool': continue
        content = rec.get('content', '')
        if not isinstance(content, str): continue
        if not any(p in content for p in error_patterns): continue

        correction = None
        for j in range(i+1, min(i+5, len(records))):
            if records[j].get('role') == 'user':
                msg = records[j].get('content', '')
                if isinstance(msg, str) and len(msg) > 10:
                    correction = msg
                break

        if correction:
            results.append({
                's': sid,
                'error': content[:300],
                'correction': correction[:300],
                'tool_call_id': rec.get('tool_call_id', '')
            })

with open('/tmp/sw-error-corrections.json', 'w') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f'Found {len(results)} error\u2192correction pairs')
"
```

### A6. Write extraction summary

```bash
echo "=== Extraction Summary ===" > /tmp/sw-progress.txt
echo "User messages: $(wc -l < /tmp/sw-user-messages.jsonl 2>/dev/null || echo 0)" >> /tmp/sw-progress.txt
echo "Tool chain records: $(wc -l < /tmp/sw-tool-chains.jsonl 2>/dev/null || echo 0)" >> /tmp/sw-progress.txt
echo "Error corrections: $(python3 -c "import json; print(len(json.load(open('/tmp/sw-error-corrections.json'))))" 2>/dev/null || echo 0)" >> /tmp/sw-progress.txt
cat /tmp/sw-progress.txt
```

## Phase B: Analyze Patterns

Now read the extracted data and identify skill candidates.

### B1. Analyze repeated explanations

Read `/tmp/sw-user-messages.jsonl`. Group messages by semantic similarity.

Look for these signals:
- Same concept/entity explained in 3+ **different** sessions
- Same corrections to Claude's behavior repeated across sessions
- Same domain-specific terminology or rules restated
- Same setup/configuration instructions given repeatedly

For each group, note:
- The common theme (1 sentence)
- How many unique sessions it appears in
- 2-3 representative quotes
- A suggested skill name (kebab-case)

### B2. Analyze tool chain patterns

Read `/tmp/sw-tool-chains.jsonl`. Find recurring sequences.

Aggregate tool sequences per session and look for:
- Same 3+ tool sequence appearing in 3+ different sessions
- Filter OUT trivial patterns: lone [Read], [Grep, Read], [Read, Read, Read]
- Keep patterns that suggest a workflow: [Grep, Read, Edit, Bash], [Bash, Read, Edit, Bash]

For each pattern, note:
- The tool sequence
- Frequency (unique sessions)
- What task the pattern likely represents

### B3. Analyze workaround patterns

Read `/tmp/sw-error-corrections.json`. Group similar errors.

Look for:
- Same type of error occurring in 2+ different sessions
- User corrections that teach the AI the same fix repeatedly
- Environment-specific gotchas (paths, flags, configs)

For each group, note:
- The error pattern (generalized)
- The workaround (generalized)
- Frequency
- Direct quotes of the corrections

### B4. Score and rank candidates

Score each candidate: `frequency × type_weight`

Type weights:
- workaround: 1.2 (prevents concrete errors)
- repeated_explanation: 1.0
- tool_chain: 0.8 (higher false positive rate)

Normalize scores to 0.0-1.0 range.

## Phase C: Write Results

Write the final results to `/tmp/skill-workshop-results.json`:

```json
{
  "$schema": "skill-workshop-v2",
  "project_path": "<path>",
  "sessions_analyzed": 0,
  "date_range": ["<earliest timestamp>", "<latest timestamp>"],
  "extraction_stats": {
    "total_user_messages": 0,
    "total_tool_calls": 0,
    "errors_found": 0,
    "processing_notes": ""
  },
  "candidates": [
    {
      "rank": 1,
      "suggested_name": "kebab-case-name",
      "signal_type": "repeated_explanation",
      "score": 0.92,
      "frequency": 5,
      "description": "1-2 sentence summary of what this skill would contain",
      "proposed_skill_type": "knowledge",
      "evidence": [
        {
          "session_id": "abc123",
          "example": "Concrete quote from the session"
        }
      ],
      "draft_content_hint": "Brief description of what the SKILL.md should contain"
    }
  ]
}
```

**Rules for the output:**
- Sort candidates by score descending
- Minimum frequency: 3 for explanations/tool_chains, 2 for workarounds
- Include max 15 candidates
- Evidence: 2-3 examples per candidate, with actual quotes
- `suggested_name`: kebab-case, descriptive, max 40 chars
- `proposed_skill_type`: one of `knowledge`, `workflow`, `gotcha`
- Write valid JSON — verify with python3 before finishing

After writing the JSON, print a one-paragraph summary of findings.

## Important Rules

1. **Process iteratively.** Do NOT load all session files into context at once.
   Use bash to extract, accumulate in /tmp/ files, then read for analysis.
2. **Clean /tmp/ first.** At the start, remove any previous sw-* files.
3. **Survive compaction.** All intermediate data goes to /tmp/ files.
   If you notice you've been compacted, re-read your /tmp/ files to recover state.
4. **Large files.** If a session file is > 10MB, extract only user messages,
   skip tool chains for that file.
5. **Validate output.** Before finishing, verify the JSON is valid:
   `python3 -c "import json; json.load(open('/tmp/skill-workshop-results.json'))"`
6. **Languages.** User messages may be in Ukrainian, Russian, or English.
   Treat all languages equally when grouping by similarity.

