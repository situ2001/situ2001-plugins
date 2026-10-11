# Delegation contract

Read before first dispatch or reassignment. Describe outcomes and constraints rather than prescribing a sequence of edits. Carry forward confirmed decisions and supply enough context for a fresh agent to complete its assignment.

## Brief

- **Outcome and authority:** confirmed intent, constraints, acceptance criteria, and settled decisions. Identify what the executor can decide and what requires escalation.
- **Context and access:** relevant source/artifact paths, applicable instructions or skills, current state, dependencies, and available tools/resources. Supply essential content when a reference is inaccessible; omit unrelated conversation history.
- **Ownership and coordination:** files or modules the executor may write, shared interface commitments, dependent work, and peer agent IDs. Respect the entrypoint's single-writer rule. Agents share a workspace unless an isolated checkout is actually supplied.
- **Return contract:** usable deliverable, caller-relevant interface and semantics, acceptance evidence or unresolved gaps, and where to return results. Explain how to reach collaborators using runtime tool addresses.

Wire peers together using returned live agent IDs; send missing IDs once those agents exist. Further delegation needs a concrete benefit and must respect available slots and ownership agreements.

## Handoff

Developers return the implemented interface and semantics callers need: relevant invariants, lifecycle, failure behavior, and integration instructions. Include paths or symbols and meaningful validation results. Explain any change to a promised interface before dependent work relies on it.

When reassigning, supply the current deliverable, relevant findings, unresolved commitment, and transferred write ownership so the new executor can continue from the actual state.
