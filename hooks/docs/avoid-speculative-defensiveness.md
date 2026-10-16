## Avoid Speculative Defensiveness and Inferred Properties

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
