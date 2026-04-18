---
name: session-analyzer
description: >
  Analyzes Claude Code session JSONL files to find repeating patterns,
  workarounds, and tribal knowledge across sessions in a project.
  Returns structured JSON with skill candidates ranked by score.
  Use for session history mining and skill candidate discovery.
model: haiku
disable-model-invocation: true
tools: Bash, Read, Write, Grep, Glob
---

{{ include "common/skills/skill-workshop/SKILL.md" }}