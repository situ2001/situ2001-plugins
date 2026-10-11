---
name: grilling-focused
description: Use grilling to ask only the key questions that could change a plan's direction, then summarize for user confirmation. Use when the user wants a focused interview about consequential decisions.
---

# Grilling Focused

Find and read the available `grilling` skill as the base methodology. If it is unavailable, report that this skill requires `grilling` and stop the interview.

Apply `grilling` to the user's current task with a scoped **design tree**: include only unresolved decisions that require the user's judgment and whose plausible answers would materially change the goal, deliverable scope, core approach, or acceptance criteria.

For each candidate question, identify which downstream decisions or work would change with the answer. This consequence determines whether it belongs in the tree, regardless of its depth. Resolve facts through investigation; leave local, easily reversible implementation decisions to agent judgment.

Apply the full base methodology to this scoped tree, including its dependency, frontier, recommendation, and completion rules.

Print every interview round and the final confirmation request directly in the response, using `grilling`'s chat question format. Include recommended answers and let the user reply in chat. Do not call question tools. Wait for the user's reply; an unanswered question is not confirmation.
