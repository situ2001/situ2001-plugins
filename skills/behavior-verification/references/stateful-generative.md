# Stateful generative checks and failure reduction

Use generated sequences when the uncertainty depends on operation history, replicas, undo/redo, reopening, or asynchronous delivery. Keep the existing production executor and dependencies real; generation is a way to select histories, not a second implementation of the system.

## Make a failing history replayable

A seed identifies a generation run only with its generator, dependencies, and initial state. Preserve the resolved operation trace as well as the seed. Record the relevant source revision/dirty state, executable or WASM identity, dependency versions or hashes, generation configuration, and initial snapshot. Capture identity allocation and nondeterministic inputs that affect the failure.

For replicated or asynchronous systems, preserve the causal schedule: which replica performs each operation; when updates/checkpoints are captured; and which captured message is delivered to which receiver and in what order. Regenerating a message at delivery time can silently replace a historical update with a newer one. Either retain the actual bytes and their dependencies, or record capture commands and regenerate bytes from replayed state at those exact points.

Represent created objects symbolically when their runtime IDs change during replay, and bind each creation result to later references. Preserve explicit reopening/writer identities when they affect merge behavior. A trace that references a removed object, message, or checkpoint is an invalid replay candidate, not a reproduced product failure.

Use one executor for generation, replay, and shrinking where practical. Verify the recorded trace reproduces the original failure before attempting reduction; a fresh generated run with the same seed alone is weaker evidence. Preserve the earliest failure and diagnostics before teardown or poisoned state can produce secondary exceptions.

## Choose independent properties

Separate properties that need different evidence:

- **Structural validity:** parentage, reachability, ordering, selection validity, or other domain constraints justified by the model.
- **Convergence:** replicas reach the same observable state after the declared delivery schedule settles.
- **Identity:** the intended objects, characters, cursors, or containers retain their identities through edits and history operations.
- **Operation semantics:** the result matches an independent model or a specific user action's contract.

Convergence can coexist with lost user edits. For example, applying a stale full-text view after importing a remote update can delete that update and still converge. Repeated text can also produce equal final strings while retaining different character identities. Assert IDs/cursors or specific range-edit intent when those are the claim; string equality cannot substitute for them.

A single-writer reference model can supply a strong oracle for local operations. Concurrent runs may establish structural invariants and convergence while leaving concurrent user intentions unspecified. State that boundary instead of inventing a merge policy to turn observations into expected results.

## Shrink the same failure

Group failures by their mechanism before counting defects. Keep a failure signature sufficient to distinguish the original assertion or panic from setup, missing dependencies, and later cleanup errors; category, stage, and decisive diagnostic often suffice. A large number of failing seeds can expose one underlying bug.

Reduce commands, data, replicas, and scheduling only while the candidate remains valid and reproduces that signature. Preserve necessary initialization, ID mappings, capture points, and delivery dependencies. Report invalid candidates separately. A smaller trace that now fails because a referenced object was never created is not a successful reduction.

Replay the minimized case in fresh state to check repeatability. If failure enters a bottom dependency, build a focused case against that dependency using the same relevant state and operations. This distinguishes adapter semantics from dependency behavior without replacing the dependency with a model. Keep the original application trace as evidence of how the fault was reached.

After a fix, rerun the preserved original and minimized traces plus the relevant saved exploration plan. Retain failing configurations when expanding exploration; replacing them with new passing seeds loses regression evidence. Where replay/minimization correctness is uncertain, challenge it with a targeted behavioral fault and verify that the reduced case still detects that fault rather than an invalid-trace error.

Finish with replay commands, source/artifact identities, failure groups, minimized traces, and the exact properties checked. Treat test-process time or step budgets as recorded experiment configuration, not product restrictions or proof that longer histories are safe.
