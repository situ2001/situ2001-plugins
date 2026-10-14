# Resource use and observation cost

Use for process CPU, memory, GPU activity, and the cost of monitoring or reporting a workload.

## Attribute the process group

Record process identities and roles at collection time. Use available parent relationships, launch/session ownership, start times, or an authorized normal shutdown of the owned app to establish helper attribution. A shared executable name such as WebKit is insufficient to include every matching host process. Preserve unresolved roles instead of assigning them to a window by guesswork.

State whether the result covers the main process, helpers, waited-for child tools, or the whole host. Device-wide GPU activity does not attribute work to the target process.

## Account for CPU

For interval CPU cost, retain before/after user and system CPU counters and the wall interval. State whether 100% means one logical core or the entire machine; a short scan's CPU-time budget per second differs from its instantaneous utilization while running.

When a benchmark launches tools, collect its own CPU and children's CPU separately. On systems where child accounting includes terminated, reaped children, wait for the relevant children before taking the ending counters. Read the host API's accounting contract; live descendants and already reaped tools need different observation paths.

An external process timer can cross-check internal totals. Explain startup, sleeps, warmup, and output included in the external interval but excluded internally; compare within the tools' precision. Avoid subtracting estimates merely to make the totals match.

Include observed query failures and their cost in a scan benchmark. Preserve unavailable counts as unavailable. A default zero in an older recorder is not evidence of zero work or zero matches.

## Describe memory and activity windows

Preserve each metric's definition and timing:

| Measurement | Interpretation |
| --- | --- |
| Sampled RSS range/peak | Resident pages at sampled instants, potentially sharing pages with other processes |
| Physical footprint snapshot | The platform/tool's accounting at the recorded instant |
| Device allocations | Allocations within that API's coverage, rather than total host memory |
| CPU delta over interaction | Average over the actual interaction interval, including observed pauses |

Sequential end-of-run footprint snapshots are neither simultaneous peaks nor interval averages. On shared/unified-memory systems, overlapping categories cannot simply be added; group RSS can double-count shared pages. A short sample does not establish leak freedom or energy cost.

Record foreground application, window visibility, input/activity, and relevant gates. Background idle with polling disabled does not measure foreground idle with polling active. A mixed human interaction window describes that mixture; retain logs or markers of what actually occurred.

## Measure the observer

Locate collection, subprocess launch, statistics, hashes, serialization, copying, transport, and file writes relative to the timer. If timing excludes output hashing but a resource window includes it, label both boundaries.

For growing traces or datasets, invoke the real observation function against representative real-data sizes or prefixes and preserve those sizes. Report per-call cost and call frequency; a repeated full-trace scan can become expensive even when guest execution is unchanged. Treat this as a component measurement until an application run demonstrates the overall effect.

Keep profiling/sampling cost separate from baseline resource measurement when it perturbs the workload; use [profiling](profiling.md) for sample interpretation.
