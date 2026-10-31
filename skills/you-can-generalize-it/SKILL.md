---
name: you-can-generalize-it
description: Generalize logic unnecessarily coupled to particular data or scenarios within the current task's required scope. Use only when explicitly invoked.
disable-model-invocation: true
---

# You Can Generalize It

Use the current task's requirements to determine which inputs and scenarios the
logic must support. Inspect the relevant implementation and callers to find
assumptions that tie its behavior to a particular example, dataset, or scenario.

Derive the shared rule or mechanism from the required cases. Separate variable
data and scenario-specific policy from that mechanism where they actually vary.
Replace example-specific branches with logic that follows the shared rule;
renaming a hardcoded value or adding more special cases does not establish that
the logic is general. Preserve valid domain rules and explicit task constraints.

Keep the solution as general as the current task requires. Introduce parameters
or abstractions when they represent required variation and simplify the affected
code. Keep changes local and update affected callers as needed.

Follow the current task's authorization: implement the correction when edits are
authorized; during discussion or review, explain the coupling and proposed
correction. Ask when the required scope of generality is unclear and the answer
would materially change the solution.

When verification helps, use a focused check covering representative required
variations, including a case that differs from the original example. Report what
was generalized and any required cases that remain unsupported.
