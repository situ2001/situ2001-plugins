---
name: handoff-with-background
description: Create or update a handoff that preserves task background and current progress across sessions. Use when goals, sources, decisions, and open questions need to survive repeated handoffs.
---

# Handoff With Background

Write one Markdown handoff for a fresh agent, tailored to the next session's requested focus while retaining background that still affects decisions.

## Reconcile the context

Read the current conversation and the previous handoff, when available. Carry forward still-relevant background, update changed decisions, and record the outcome of resolved or superseded questions. Absence from recent discussion does not make a topic obsolete.

Reference existing artifacts by path or URL and reading location after verifying they contain the relevant background. Carry context found only in conversation or temporary handoffs into the new document; preserve links to primary inputs. Follow known sources to fill material gaps, and state what could not be checked.

Separate agreed requirements, historical proposals, observed implementation, and assumptions; record conflicts. Code establishes implementation state, while requirements and user decisions establish intent.

## Write the handoff

Keep enduring background distinguishable from the current snapshot. Cover what the task needs:

- **Purpose and sources:** the goal, task context, and primary inputs with their roles.
- **Decisions and open questions:** accepted scope, constraints, reasons and relevant rejected alternatives; unresolved or deferred matters and what would settle them.
- **Current progress:** completed and active work, blockers, evidence, and workspace or branch details needed to resume. Mark operational state as a snapshot to recheck.
- **Next steps:** concrete continuation points for the requested focus.
- **Suggested skills:** relevant available skills, paths when known, and why to invoke them; say if none apply.

Prune obsolete execution details and history that no longer helps continuation.

## Save and verify

Honor the user's destination or request to update an existing file. Otherwise save a uniquely named Markdown file in the OS temporary directory: `$TMPDIR`, else `/tmp`; `%TEMP%` on Windows.

Redact sensitive information while retaining paths needed to locate the work.

Before finishing, compare against the previous handoff: still-relevant background and unresolved items must remain in the document or a verified reference. Verify the saved file, then return a clickable absolute path and a brief description.
