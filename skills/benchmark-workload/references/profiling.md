# Profiling and injected probes

Use to explain measured costs or select a concrete optimization target. Keep normal-configuration timing and diagnostic runs identifiable throughout collection and reporting.

## Establish what was observed

Measure the normal workload without profiler/debugger instrumentation, then collect profiles in separate comparable runs. Profiling can alter compilation tiers, optimization, scheduling, and timing. If symbols or dynamic code require debugger access, collect them after timing/sampling when possible, and record the lifecycle. Profile-run latency describes the instrumented configuration.

Verify an injected probe in the actual execution context: read a probe-owned counter, marker, or recorded invocation from the target worker/process. Successful script delivery alone does not show that the hook ran after the relevant globals existed or intercepted the path in use. Preserve ineffective injections and their diagnostics as invalid measurements, then measure with a verified probe.

Record the actual execution backend. Headless WebGL/WebGPU may use a software renderer; a requested GPU provider or enabled feature is weaker evidence than the active adapter/renderer and exercised path. Label software-rendered results accordingly.

## Interpret sample weights

Retain the profile's process/thread/worker scope, interval, sample count, and elapsed coverage. Make the denominator explicit when reporting percentages: all samples, non-idle samples, or a selected subtree.

- **Self time** attributes samples to the frame itself; **inclusive time** includes descendants. Inclusive categories can overlap and cannot be added as independent costs.
- **Idle or blocked stacks** describe where a sampled thread waited. Their weight is neither whole-process idle time nor evidence that the waiting function consumed that CPU time.
- **Worker samples** omit main-thread painting, helper processes, device execution, and other work outside that profile. Use appropriate separate observations for those costs.
- **Sample weights** estimate time within the sampled scope. They are not automatically operating-system CPU seconds, especially when the instrument samples waits.

## Resolve hotspots to real work

Use the code identity, loaded base, module bytes, symbols, or source map that belongs to the measured artifact. For JIT blocks, preserve the mapping from generated code to original addresses/functions; partial mappings cover only the blocks actually resolved. Account for helper descendants once when grouping samples.

A hotspot fraction identifies a candidate, not a promised speedup. The replacement may preserve only part of that work, move cost elsewhere, or change output. Verify a candidate's useful result and measure the normal workload again before claiming its end-to-end benefit. Likewise, a framework migration that also changes libraries or features establishes the combined change unless a controlled comparison separates the cause.

Retain raw profiles, mapping inputs, normal timing records, and failed/invalid diagnostic attempts with their exclusion reasons. This lets another run reproduce both the timing result and its narrower attribution.
