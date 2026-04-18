---
name: skill-workshop
description: >
  Analyze Codex CLI session history to discover skill candidates.
  Finds repeating explanations, tool chains, and workaround patterns
  across project sessions. Use when user wants to find what should
  become a skill, mine session history, or extract tribal knowledge.
allowed-tools: Bash, Read, Write, Grep, Glob
model: gpt-5.1-codex-mini
---

{{ include "common/skills/skill-workshop/SKILL.md" }}
