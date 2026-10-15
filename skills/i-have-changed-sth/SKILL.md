---
name: i-have-changed-sth
description: Refresh understanding after the user has manually changed code, then continue the original task from the current files. Use only when explicitly invoked.
disable-model-invocation: true
---

# I Have Changed Sth

The user has manually changed code since your last view. Treat the current files as the baseline and refresh your understanding before continuing work that depends on them.

Use the user's pointers and the repository's current status to locate relevant changes. Read the related staged and unstaged diffs, relevant new files, and affected source. Reconcile your plan and assumptions with what is now present on disk.

Continue the original task from that state. This notification alone is not a request to revert or correct the user's edits, or to perform a comprehensive review. If continuing the task requires changing the intent of their edits, resolve that conflict with the user first.

Briefly acknowledge the changes you observed and any effect on the ongoing task.
