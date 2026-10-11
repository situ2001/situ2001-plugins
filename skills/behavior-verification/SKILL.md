---
name: behavior-verification
description: Verify a concrete behavioral uncertainty against actual source with a focused executable check, from individual functions and stateful components to service or application flows. Useful when a test harness is missing or the full app cannot run; not an automatic requirement for every edit.
---

# Behavior Verification

Turn a concrete uncertainty into an executable check whose result can contradict the implementation. Choose the smallest environment that preserves the behavior under investigation. If source reading and existing checks settle the question, finish without another script; a reversible cosmetic edit alone does not justify a custom harness.

## Establish the verification contract

Before writing code, record a compact contract:

- **Source:** exact revision or staged/working-tree state and the entry to execute.
- **Trigger:** initial state, input/action, and relevant completion order.
- **Oracle:** expected observable result and its independent basis (requirement, protocol, reported failure, or established behavior).
- **Boundary:** dependencies kept real, substitutions, and what those substitutions cannot prove.
- **Discriminator:** the plausible defect that would make this check fail.

Keep this proportional: one sentence can suffice. Without an independent oracle, label the check as characterization and report observations; a plausible implementation is not its own specification. Verification stays within the requested scope; finding a defect does not itself authorize modifying the implementation.

Load the requested source state and keep relevant collaborators consistent with it. Record revisions or preserve snapshots; disclose mixed states. Verify that the executed file or deployed artifact contains the intended changes, rather than inferring that from its path.

## Choose the environment and references

Inspect available scripts, dependencies, runtime versions, and repository instructions. Prefer an existing focused test. Missing infrastructure can justify a temporary harness within the authorized scope. Respect local limits on servers and host applications; keep required type/lint checks separate.

Choose directly from the question; running every level is unnecessary.

| Question | Smallest useful environment | Evidence boundary |
| --- | --- | --- |
| Transformation, validation, serialization, calculations | Actual function in its supported runtime | Outputs and effects for supplied inputs |
| State transitions, lifecycle, concurrency, retries | Actual stateful module with a compatible runner | Observed transitions and controlled completion orders |
| Framework behavior and event handling | Real framework with its supported test environment | Only the lifecycle and event semantics it implements |
| Native source in an iOS/macOS app | Focused macOS executable compiling original source where feasible | Real macOS APIs; device-only behavior remains untested |
| Layout, device behavior, platform APIs | Relevant browser, device, or host | Tested platform and configuration |
| Persistence, transactions, process or service coordination | Relevant real integration environment | Exercised systems' guarantees |
| User journey across application boundaries | Runnable application and relevant services | Integrations actually exercised |

Read [Check design](references/check-design.md) when designing or adjusting cases, fixtures, assertions, observation windows, or negative controls, or evaluating an existing harness. It also covers delivery paths and failure triage. Read [Temporary harness](references/temporary-harness.md) when creating, relocating, or retaining a one-off check, installing scratch dependencies, or managing its resources.

Read only the relevant execution recipe:

- [Node / TypeScript](references/node-typescript.md): direct loading is impractical and temporary transpilation or `vm` is needed.
- [React behavior](references/react-behavior.md): hooks, effects, component interactions, asynchronous transitions, or native component substitutes.
- [Browser flows](references/browser-flows.md): Playwright/browser setup, request fixtures, browser assertions, and E2E boundaries.
- [Native source on a compatible host](references/native-host.md): focused local compile-and-run checks for iOS/macOS source, replacing only unavailable boundaries.

For other languages, apply the same method using their native runtime and assertion tools.

## Run actual behavior

Invoke actual source through its exported function, component, or real application entry, retaining the relevant dependencies and call path. Prefer whole modules. Rewriting the algorithm tests the rewrite. Disclose fragment extraction and any bypassed wiring; verify and disclose scratch source edits. Replace only named boundaries outside the behavior under investigation and make unexpected imports or calls fail visibly.

Run the check and inspect output and exit status. Await asynchronous assertions, bound waits, and propagate failures to a nonzero exit. Control completion order or timers when relevant instead of relying on arbitrary sleeps. Classify failures before changing the harness, and explain any assertion change using contract or runtime evidence. Weakening an unexplained failing assertion does not resolve it.

For a fix, prefer the same check against isolated original and fixed source: original fails for the reported reason, fixed passes. If original source is unavailable and a false pass remains plausible, use a relevant scratch mutation to challenge the assertion; follow Check design for negative-control mechanics.

Stop when the question is answered and applicable repository checks are complete. If a harness starts recreating a framework, large module graph, or production integration, use an existing integration environment or report the unresolved boundary. Keep production source, manifests, and lockfiles unchanged solely for harness convenience.

## Report and finish

Report briefly:

- Actual source behavior executed, decisive cases and outcomes, including a negative control when used.
- Dependencies or environment objects replaced.
- Material behavior still unverified and the command/artifact needed to repeat the check.

Label evidence precisely: component callback, DOM interaction, browser integration with mocked services, or E2E through listed real systems. Static rendering cannot establish hydration or interaction; browser fixtures cannot establish backend behavior; replacement native views cannot establish native rendering or bridge correctness. A pass supports the selected cases, not every aspect of the change.

Conclude only when selected cases ran against intended source, assertions support the contract, failures and unexpected diagnostics are explained, and owned resources are cleaned up. Timeouts, skipped cases, swallowed exceptions, and harness import failures remain unresolved evidence. Report a concrete limit when the required runtime is unavailable. Add cases only to distinguish another material failure mechanism; broad coverage claims require broader evidence.
