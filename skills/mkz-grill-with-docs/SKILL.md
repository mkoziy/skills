---
name: mkz-grill-with-docs
description: Stress-test a plan or design through an interview and capture the resulting ADRs and glossary. Use when the user asks to grill a design and document the decisions.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, AskUserQuestion, Agent
---

# Grill with Docs

This skill composes two required skills:

1. Invoke `mkz-grilling` with the user's request. Complete its design-tree interview.
2. Invoke `domain-modeling` with the settled design. Capture its ADRs and glossary before returning.

`domain-modeling` is an external dependency and must be installed. If it is unavailable, stop and report the missing dependency; do not replace it with an improvised documentation workflow.

Return the decisions and paths to the docs created in this session to the calling workflow.
