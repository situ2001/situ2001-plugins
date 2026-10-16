---
name: de-defend
description: Audit speculative code defenses and inferred properties, or consolidate repetitive and easily outdated Markdown. Use for de-defend reviews, overengineering audits, stalled debugging with a plausible self-imposed restriction, or Markdown cleanup.
---

# De-Defend

Requirements create constraints. Evidence creates defensive code. Imagination does not.

Use the user-specified scope. Otherwise, start with the current diff and directly involved code or documents. Follow document references and duplicated facts as needed to resolve repetition and inconsistent claims within that task. Review an entire workspace when explicitly requested. Preserve the requested behavior; this audit does not add features.

For Markdown cleanup, read [references/consolidating-markdown.md](references/consolidating-markdown.md) and follow its workflow. For code, follow the audit below. When both are involved, apply each workflow to its part of the change.

## Establish the target

Before editing, identify the required behavior, the failure or audit target, and an observable result that would show the task is complete. Treat an unknown cause as a hypothesis to test. For a review without a known failure, the result can be a supported decision to keep or simplify each mechanism in scope, with affected behavior verified.

## Trace each defense to its source

Inspect relevant guards, validation, empty-state checks, catches, default recovery, retries, timeouts, fallbacks, feature or version checks, limits, wrappers, and abstractions. For each nontrivial mechanism, find its concrete source:

- an explicit task or product requirement;
- a documented platform or API contract;
- a real security or trust boundary;
- an observed failure, regression, or failing test;
- an established project convention whose rationale applies here.

Treat a mechanism without such support as speculative. Existing code is not itself evidence that a restriction is required.

Inspect newly added properties in types, schemas, persisted data, and API or UI models that infer or evaluate information, such as scores, grades, ambiguity flags, and confidence values. Trace each to an explicit requirement or established contract. If neither calls for the property, remove it and the computation and consumers added solely to support it. Possible future ranking, filtering, or explanation is not a requirement.

Preserve checks and resource limits backed by real contracts, security needs, reliability needs, or operational constraints at genuine trust boundaries. A boundary's existence alone does not justify every guard or fallback within it.

When the task involves removing defensive tests, read [references/removing-defensive-tests.md](references/removing-defensive-tests.md) for title-based triage and retention criteria.

## Simplify the path

When debugging, first test whether an existing guard, validation rule, fallback, compatibility branch, or self-imposed limit causes the failure. Prefer removing an unsupported restriction and restoring the direct intended path over layering a workaround around it. Expose the real error when catch-and-continue behavior hides a bug.

For internal states guaranteed by types, caller contracts, framework semantics, or validated transitions, trust the invariant or fail fast when its violation is a programming error. Remove silent defaults and speculative repair logic for impossible states. Remove compatibility branches for unsupported environments and abstractions kept only for possible future use; keep an abstraction that gives immediate clarity or removes real duplication.

Do not add a new guard, retry, fallback, limit, compatibility path, abstraction, or inferred property without its required source. Falsify the current debugging hypothesis before adding more machinery.

## Verify and report

After each coherent simplification, run the narrowest relevant check or reproduction. Verify the required behavior and any boundary or error behavior affected by the edit. Review the final diff and justify every remaining new defensive mechanism and inferred property; remove those without support.

Report briefly what was removed and why, which required defenses and inferred properties were preserved and why, and how the required behavior was verified. If the audit finds no speculative addition in scope, say so and give the evidence.
