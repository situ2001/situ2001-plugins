---
name: optimize-glsl-and-webgpu
description: 当你要考虑逻辑是放在 shader 做还是在 WebGPU API 做的时候，可以参考这个。
---

# Optimize GLSL and WebGPU

Choose a rendering boundary from actual data flow, then establish whether a change preserves behavior and improves the user's target workload. Follow a discussion-only request with source-backed recommendations; implement and measure when requested. Keep the user's chosen platform and output contract.

## Locate the cost and ownership

Trace a real frame through state updates, geometry generation, allocations, uploads, draw/dispatch, and presentation. Identify which API and shader language the project actually uses: GLSL and WebGPU/WGSL require different integration paths. Check runtime bindings as well as the underlying graphics API; a native feature may be absent from a JS bridge.

For each candidate, identify input size and lifetime, independent work, where results are consumed, required precision, and any CPU/GPU synchronization. Distinguish a source-backed mechanism from a measured bottleneck. Without profiling, describe expected benefits as hypotheses.

Use these starting points, adjusting for the actual workload:

| Work | Starting choice | Evidence that can change it |
|---|---|---|
| Static or infrequently changing geometry/text | Cache and upload when changed | Invalidation frequency, memory cost, actual rebuilding cost |
| Many independent transforms, interpolations, particles, or color calculations consumed by drawing | GPU candidate | Upload volume, shader work, GPU headroom, and measured frame cost |
| Few ordered events, lifecycle changes, or host-consumed decisions | CPU candidate | A sufficiently large parallel workload with results kept on GPU |
| Precision-sensitive projection, pixel snapping, or thresholds | Preserve the established numerical behavior | Validated GPU representation or a user-authorized visual tolerance |
| Results immediately needed by CPU | Include readback and waiting in the comparison | Batch size or computation savings sufficient to cover that boundary |

A compact event or sample expanded into many visible elements is a useful GPU candidate. Reducing CPU work can increase GPU work or memory; evaluate the resource the user wants to improve rather than maximizing the amount of shader code. Business state and event history can run on GPU when their ownership and consumer justify it; their names alone do not determine placement.

Finish the investigation with a concrete proposed boundary, its expected mechanism, and the unresolved measurements. A discussion request can end here.

## Implement the boundary

Choose the smallest change that tests the proposed mechanism. Preserve an independently executable baseline or an existing faithful oracle before replacing the path.

Prefer persistent data and compact updates where they remove observed rebuilding or transfer costs. Invalidate caches according to the source's mutation contract; immutable sample identities, mutable objects, and newly allocated arrays need different handling. Reuse existing render passes or draws when suitable.

Choose vertex/fragment/compute placement from consumption and reuse. Account for invocation count and the cost of additional passes; a CPU loop alone does not justify adding compute.

Keep host events, pause/seek/reset, clipping, blend order, and output lifetime consistent across the boundary. Preserve established precision where a cheaper partial migration meets the goal. For shader arithmetic, geometry expansion, or WebGPU bridges, read [shader-paths.md](references/shader-paths.md).

## Establish behavior and benefit

Use a focused check against actual source and the real rendering backend. For help choosing the check, consult [behavior-verification](../behavior-verification/SKILL.md). Compare baseline and candidate images or another independent output contract; shader compilation alone establishes neither visual equivalence nor presentation.

Define the comparison contract before interpreting results: exact pixels where required, or a justified visual tolerance where permitted. Keep temporal checks separate from cross-renderer tolerance; a frozen frame may require exact stability even when two implementations differ slightly. Exercise boundary cases relevant to the migrated data, such as pause/seek, clipping, resizing, history wrap, and changing captions. Report coverage rather than claiming equivalence for all inputs.

Measure the requested workload with [benchmark-workload](../benchmark-workload/SKILL.md). Include actual host/bridge/upload/submission work and any new synchronization. If measuring offscreen throughput, also use the application's normal pacing when conclusions concern presented rendering. Hold input sequence, output size, frame count, and presentation rate comparable; a fixed input clock may advance differently from wall time.

Keep these observations distinct:

- Render-call elapsed time, OS process CPU time, GPU execution timestamps, batch completion, and display latency answer different questions.
- Upload bytes and upload calls expose different costs. A smaller upload can retain substantial bridge overhead.
- Peak RSS and GPU allocations may overlap on unified memory; report their tool-defined scopes.
- Missing GPU timestamps or an unavailable target remain explicit gaps. Infer no FPS, power, or latency improvement from CPU savings alone.

Retain failed or interrupted runs and exclude them explicitly from performance summaries. If native pacing changes or the frame loop stalls, preserve that evidence and limit the conclusion to successful comparable runs. Repeat measurement only when it resolves a material uncertainty.

Deliver the implemented boundary, behavior evidence, matched before/after measurements with variability, repeat commands, and material tradeoffs. For a proposal without measurements, state what the source establishes and what the experiment would need to establish. Keep a migration only when its behavior and measured tradeoffs meet the user's goal, or report the unresolved adoption decision.
