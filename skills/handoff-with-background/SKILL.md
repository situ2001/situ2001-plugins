---
name: handoff-with-background
description: Create or update a task handoff for the next session, preserving background and progress that affect continuation.
---

# Handoff With Background

Write one Markdown handoff for a fresh agent, tailored to the next session's requested focus while retaining background that still affects decisions.

## Reconcile the context

Read the current conversation and the previous handoff, when available. Reassess what the next session needs to understand the goal, respect active constraints, make sound decisions, and continue the work. Preserve background and decision rationale that serve those needs, even when they are not used in the immediate next step. Absence from recent discussion does not make a topic obsolete.

Merge, rewrite, or omit inherited material according to that relevance. An unresolved question does not automatically need to be carried forward. Completed operation logs, temporary investigation details, and unrelated research can be omitted when they no longer affect continuation. Omitted material needs no separate archive or reference solely to preserve history.

Reference existing artifacts by path or URL and reading location after verifying they contain the relevant background. Carry needed context found only in conversation or temporary handoffs into the new document; preserve links to relevant primary inputs. Follow known sources to fill material gaps, and state what could not be checked.

Separate agreed requirements, historical proposals, observed implementation, and assumptions; record conflicts. Code establishes implementation state, while requirements and user decisions establish intent.

## Write the handoff

Keep enduring background distinguishable from the current snapshot. Cover what the task needs:

- **Purpose and sources:** the goal, task context, and primary inputs with their roles.
- **Decisions and open questions:** accepted scope, constraints, reasons and relevant rejected alternatives; unresolved or deferred matters that affect continuation and what would settle them.
- **Current progress:** completed and active work, blockers, evidence, and workspace or branch details needed to resume. Mark operational state as a snapshot to recheck.
- **Next steps:** concrete continuation points for the requested focus.
- **Suggested skills:** relevant available skills, paths when known, and why to invoke them; say if none apply.

## Save and verify

Honor the user's destination or request to update an existing file. Otherwise save a uniquely named Markdown file in the OS temporary directory: `$TMPDIR`, else `/tmp`; `%TEMP%` on Windows.

Redact sensitive information while retaining paths needed to locate the work.

Before finishing, compare against the previous handoff to check that a fresh agent can continue the next session's work with the needed background, decisions, and constraints. Verify the saved file, then return a clickable absolute path and a brief description.
