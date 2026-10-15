---
name: allow-breaking-change
description: Allow breaking changes in the current task without preserving compatibility with older code versions. Use only when explicitly invoked.
disable-model-invocation: true
---

# Allow Breaking Change

Treat this invocation as permission to make breaking changes within the current task. Change interfaces, data structures, and their callers together to implement the intended behavior directly.

Do not add or retain compatibility layers, version gates, legacy fallbacks, or parallel implementations solely to support older code versions. Update affected callers, tests, and documentation to the new contract instead of preserving the old path.

Keep validation required by the current behavior and its real boundaries. Handle existing persisted data according to the task's requirements; permission to break code compatibility does not itself decide how that data should be treated.

Keep the work scoped to the original task; this invocation does not request a repository-wide cleanup.
