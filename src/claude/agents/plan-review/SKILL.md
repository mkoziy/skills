---
name: plan-review
description: "Use this agent PROACTIVELY after creating implementation plans with /planning:make to review plan quality before execution. Reviews plans in docs/plans/ for completeness, correctness, and adherence to project conventions. If plan file is unclear from context, asks user which plan to review. <example>Context: User just created a plan with /planning:make. user: \"Let's review this plan before we start\" assistant: \"I'll use the plan-review agent to verify the plan solves the problem correctly and follows conventions.\" <commentary>Plan was just created, review ensures quality before implementation begins.</commentary></example> <example>Context: User wants to validate an existing plan. user: \"Check the feature-x plan for over-engineering\" assistant: \"Let me use the plan-review agent to analyze the plan for unnecessary complexity.\" <commentary>Specific review focus requested, agent will emphasize over-engineering detection.</commentary></example> <example>Context: User mentions a plan without specifying which one. user: \"Review my plan\" assistant: \"I'll use the plan-review agent. It will identify available plans and ask which one to review.\" <commentary>When plan is ambiguous, agent asks for clarification.</commentary></example>"
model: claude-opus-4-7
color: cyan
tools: Read, Glob, Grep, Bash
---

{{ include "common/agents/plan-review/SKILL.md" }}
