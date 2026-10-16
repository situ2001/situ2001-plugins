---
name: grilling-focused
description: Use grilling to ask only the key questions that could change a plan's direction, then summarize for user confirmation. Use when the user wants a focused interview about consequential decisions.
---

# Grilling Focused

Find and read the available `grilling` skill as the base methodology. If it is unavailable, report that this skill requires `grilling` and stop the interview.

Before building the design tree, use the request and existing context to understand the problem the user wants to solve, their desired outcome, and their stated constraints. Distinguish a proposed approach from the outcome it serves while preserving the user's explicit choices. Open the interview with a brief statement of this understanding, making any uncertain interpretation visible. Ask for intent clarification only when plausible interpretations would change the direction of the work.

Use this understanding to select questions and ground recommendations. When the user corrects it, revise the design tree and recommendations accordingly.

Apply `grilling` to the user's current task with a scoped **design tree**: include only unresolved decisions that require the user's judgment and whose plausible answers would materially change the goal, deliverable scope, core approach, or acceptance criteria.

For each candidate question, identify which downstream decisions or work would change with the answer. This consequence determines whether it belongs in the tree, regardless of its depth. Resolve facts through investigation; leave local, easily reversible implementation decisions to agent judgment.

Apply the full base methodology to this scoped tree, including its dependency, frontier, recommendation, and completion rules.

Print every interview round and the final confirmation request directly in the response, using `grilling`'s chat question format. Include recommended answers and let the user reply in chat. Do not call question tools. Wait for the user's reply; an unanswered question is not confirmation.
