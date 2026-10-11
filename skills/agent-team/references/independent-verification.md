# Independent verification

Read when choosing an independent verifier. A separate verifier is warranted by behavioral uncertainty or the cost of a mistake; it is not required for every executor.

## Acceptance evidence

Give the verifier the confirmed acceptance criteria, executable resources, and delivered interface. Have it exercise behavior independently and return an acceptance verdict with traceable evidence and remaining gaps. Developer claims are context, not proof.

Evidence identifies the artifact or revision checked, the check or reproduction, and its result. Keep raw logs available by reference when useful.

## Defect loop

Connect verifier and developer directly using the selected runtime's messaging tools:

1. The verifier sends reproducible defects within the agreed contract to the developer.
2. The developer fixes them and returns the changed behavior and evidence.
3. The verifier checks affected acceptance criteria and reports completion or an unresolved blocker to the director.

Keep routine corrections between peers. Escalate consequential changes and conflicting evidence under the entrypoint's escalation rules; the director retains final acceptance, including integration between workstreams.
