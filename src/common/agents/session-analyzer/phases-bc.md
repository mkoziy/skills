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
