---
name: linear-recall
description: Read Linear Requirement context and scoped work, including confirmed decisions not yet consolidated.
---

# Linear Recall

Read the shared [workflow](references/workflow.md). Recall is read-only.

1. Resolve the Requirement. On initial continuation, read its parent description and complete Handoff. Reuse context already read in this conversation; refresh when the question needs current state or changes are known. Read parent discussion when relevant, including intake not yet assigned to a sub-issue.
2. Scope discovery follows the shared focus and closure rules:
   - **Overview:** use `parentId` with `fields: ["id", "title", "status", "url"]` to discover sub-issues, then report open work as navigation, not a review of current decisions or progress.
   - **Selected Issue:** read it directly; leave siblings unopened unless needed.
   - **Topic:** use the lightweight index to find matching Issues, then read their descriptions.
3. Read scoped comments when continuing work or answering questions about current requirements, decisions, progress or results; `get_issue` omits discussion. A question about the recorded description alone needs no comments. Follow pagination as needed. Expand Issues, dependencies and sources only as needed within the shared focus boundary.
4. Combine the baseline with confirmed increments. Explain material conflicts and unresolved judgments, citing relevant records. Stop when the question is answered; a suggested next step is not execution authorization.
