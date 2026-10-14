# Scheduling and asynchronous pipelines

Use for event loops, emulators, workers, render pipelines, and other workloads whose progress crosses queues or clocks.

## Compare the same useful progress

For virtual-time workloads, fix guest input, initial state, clock policy, and a completion point such as a particular virtual timestamp or completed frame. Record virtual progress and host wall time separately. Changing the guest clock or skipping work changes the workload rather than measuring a scheduling improvement.

For a yield-mechanism comparison, hold execution-slice policy and workload constant; vary the host scheduling mechanism. Rotate comparable variants when compilation, caches, or host drift can affect them. A baseline → candidate → candidate → baseline order is one useful design, not a required run count.

Measure complementary outcomes:

| Outcome | Boundary |
| --- | --- |
| Progress cost | Wall time to the fixed virtual/work completion point |
| Longest observed stall | Maximum gap between specified progress or delivery events |
| Input response | Injected input to the corresponding useful state or visible result |
| Yield cost | Suspension to continuation, with count and covered interval |

Separate active execution, waiting after a yield, intentional clock waits, and downstream delivery where observable. A zero-delay timer is a request to the host scheduler; measure its actual continuation delay. Label message gaps as gaps unless the evidence establishes the cause of the stall.

Compare output identities or semantic checks at matched completion points. A faster wall-time slice may execute more instructions and therefore produce fewer slices; record slice counts rather than assuming equal counts imply equal work. Aggregate only events inside the named interval: boot-wide yield totals and a later interaction timer have different denominators.

## Correlate asynchronous stages

Carry a message sequence, frame identity, buffer generation, or explicit marker through the stages being compared. Reused buffer handles alone may not uniquely identify a frame. Establish clock domains before subtracting timestamps from different processes or devices.

Build an event path for the relevant identity, for example:

`input → work start/end → queue → acquire → submit → presented`

Record which identities are overwritten, dropped, or retained for final delivery. An acquired buffer may never be presented. Pairing each submit with the nearest timestamp can assign one frame's latency to another.

Report execution time, queue residence, submission, and observed presentation separately. High throughput or a stable frame rate can coexist with a long input-to-display delay. CPU submission, device completion, compositor presentation, and physical display are separate completion boundaries; claim the one actually observed.

## Check trace coverage

Inspect the trace's actual earliest/latest relevant events and its retained buffer window. A configured capture duration does not prove the earlier interaction survived a rolling buffer. Keep incomplete identities visible and exclude only the intervals that cannot be paired, with the reason recorded.

Finish with the correlated event records, clock/identity definitions, completion checks, and per-variant progress and responsiveness results. A component scheduling gain supports an end-to-end claim only after the useful result is measured there.
