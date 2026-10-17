## Avoid Speculative Defensiveness and Inferred Properties

Defensive code is easy to add, but every extra branch adds behavior
to understand, verify, and maintain. Take on that cost only for a
concrete need supported by the sources below.

Do not add guards, fallbacks, retries, compatibility paths,
version checks, arbitrary limits, or recovery logic merely
because a failure is theoretically imaginable.

Trust established internal invariants and framework contracts.
Use assertions or fail-fast behavior when an invariant violation
would indicate a programming error; do not silently recover from it.

Defensive handling is justified when there is a concrete source:
- an external or untrusted boundary;
- an explicit requirement;
- a documented platform/API behavior;
- an observed failure or regression.

Do not invent restrictions such as maximum page counts, step counts,
file sizes, supported versions, or timeouts without such a source.

Add inferred or evaluative properties, such as scores, grades,
ambiguity flags, or confidence values, only when an explicit task
requirement or established contract calls for them. A possible future
use is not a requirement.

When debugging, first check whether an existing guard, fallback,
validation rule, or self-imposed restriction is causing the failure
before adding another layer around it.

## Keep Verification Proportionate

Tests are easy to generate, but their assertions create expectations
that future changes must maintain. Protect required behavior,
established contracts, and observed regressions; a passing test does
not establish that the defensive behavior it enforces is necessary.

Writing or running unit tests and focused local checks is optional.
For simple changes that can be assessed reliably by inspection,
it is fine to skip them. When verification would help, choose the
smallest check that addresses a concrete uncertainty in the change.

Create or run smoke tests, end-to-end checks, or full integration
suites only when the user explicitly requests them. A general request
to implement, fix, test, or verify a change is not such a request.

Once the relevant checks pass, stop. Repeat or broaden verification
only when new changes, failures, or unresolved concerns justify it,
within the scope allowed above.

## Keep Documentation Worth Maintaining

Documentation is easy to generate but costly to keep accurate.
Before creating or expanding it, identify its reader and lasting use.
Prefer references to maintained documents, code, configuration, or
lookup commands over copying information readily available there,
especially details that change with the implementation.

Keep one-off progress, change summaries, and verification results in
the response unless a persistent record is requested or required by
the project's workflow.

Honor requested documentation and established project responsibilities.
Preserve useful operating instructions, non-obvious decisions and
conventions, and historical evidence. Judge inline detail by the
reader's need and lookup cost.

## Only include Context Where It Helps

Background and rationale are optional, not a required part of every output.
Include them when they help the intended reader understand, use, or maintain
the result. Describe the result in its final form; avoid carrying incidental
prompts, rejected alternatives, or correction history into names, comments,
documentation, or other deliverables. Preserve context that explains a lasting
constraint or a non-obvious decision.

Do not turn a one-off correction into a lasting label, disclaimer, or explanation
in the final result. These remnants create maintenance debt: future readers must
reconstruct irrelevant history, and later changes may mistake an incidental
correction for a lasting requirement.

**Code example:** After being asked to remove a fallback, name the resulting
function `loadConfig`, rather than `loadConfigWithoutFallback`, and omit comments
or explanations such as “fallback removed as requested” or “a fallback is
unnecessary here.” Explain the failure behavior only where callers need to
understand it.

**Documentation example:** A user describes a past outage and asks for a reusable
deployment checklist. Present the steps operators need to follow. Include a lesson
from the outage when it changes a step or explains a necessary precaution; keep
the incident narrative in the incident report.
