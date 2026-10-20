---
name: mkz-grilling
description: Grill the user about a plan, decision, or idea. Use when they want to stress-test their thinking or use “grill” trigger phrases.
allowed-tools: Read, Glob, Grep, Bash, Agent, AskUserQuestion
---

# Grilling

Interview the user until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are settled: questions you can ask now without guessing at answers you have not heard. Ask the entire frontier in one round; number each question and give the recommended answer. Then wait for the user's answers before the next round.

Format a round like this:

```
❓ **Q1** — **<question title>**: <question body, including choices when useful>

➡️ <your recommended answer>

---

❓ **Q2** — **<question title>**: <question body, including choices when useful>

➡️ <your recommended answer>
```

Word each question so “yes” accepts the recommendation.

Each round reshapes the tree: settled decisions push the frontier outward and unblock their dependents. Recompute the frontier before the next round. A question whose answer depends on another open question belongs in a later round.

Finding facts is your job, never the user's. When a frontier question needs a fact from the environment, investigate it. Do not ask the user for information you can obtain yourself. Decisions remain theirs: present the relevant choices and wait for their answer.

The session ends when the frontier is empty: every branch has been visited and nothing material is silently assumed. Do not act on the result until the user confirms the shared understanding.
