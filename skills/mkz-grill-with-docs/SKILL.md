---
name: mkz-grill-with-docs
description: Stress-test a plan or design through an interview and capture the resulting ADRs and glossary. Use when the user asks to grill a design and document the decisions.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, AskUserQuestion, Agent
---

# Grill with Docs

This skill composes two required skills:

1. Invoke `mkz-grilling` with the user's request. Complete its design-tree interview.
2. Critique the settled decisions before persisting them. Spawn a fresh-context subagent running `mkz-critique` on the decisions and the evidence each rests on, and have it verify every factual claim (root cause, "X causes Y", "field Z carries the defect") against the code and data. Bring confirmed findings back to the user as a grilling round. This step is done when every claim behind a decision is either verified or explicitly labelled a hypothesis.
3. Invoke `domain-modeling` with the critiqued design. Capture its ADRs and glossary before returning.

`domain-modeling` is an external dependency and must be installed. If it is unavailable, stop and report the missing dependency; do not replace it with an improvised documentation workflow.

Return the decisions and paths to the docs created in this session to the calling workflow.
