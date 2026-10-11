# Shader migration checks

Read this when choosing shader stages, moving precision-sensitive geometry, or implementing a path through WebGPU/runtime bindings. Select the relevant guidance for the project's actual GLSL or WGSL backend.

## Expansion and reuse

Sketch the old and proposed data flows in concrete units: source events/samples, CPU-generated records, bytes uploaded, shader invocations, and output consumers. For example, one burst event can drive a ring and many particles directly in a vertex shader. Keeping the event on GPU while its appearance changes can avoid uploading expanded geometry each frame.

Estimate repeated work at its actual shader stage. An instanced quad with six vertices can execute its geometry formula six times. An expensive fragment expression scales with covered samples, overlapping layers, and antialiasing. Moving a CPU calculation into a shader can increase total executions. Consider compute-generated data when multiple vertices or passes reuse substantial work; include dispatch and storage costs in the comparison.

Cache static geometry before choosing a CPU/GPU migration. A caption cache must account for every input that changes its geometry or clipping. A history ring can upload appended immutable samples while advancing its head, but this relies on the scene's actual append/prune/reset contract. Mutable inputs need an explicit mutation/invalidation path.

## Numerical and drawing contracts

Read the source shader language/version, precision declarations, buffer layouts, and matrix conventions. In GLSL, honor the target API and its actual precision guarantees. In WebGPU/WGSL, account for shader floating-point semantics rather than assuming JS double arithmetic carries through an upload.

Inspect discontinuities: rounding, floor, pixel snapping, threshold branches, clip edges, and cancellation in large absolute timestamps. Small arithmetic differences near these boundaries can become a whole-pixel or behavioral difference. Options include retaining a few precise CPU scalars, using a validated integer representation, or using a relative origin that preserves the required range. Choose from the actual failure or contract; these are not mandatory transforms.

Match storage/uniform layout, colors, blend order, primitive expansion for antialiasing, and coordinate origins. Buffer padding and binding sizes follow the real API/shader layout. Treat baseline output as the oracle; avoid changing the expected image or loosening tolerance merely to accept a migration.

Pause, reset, and seek should update the time/history that shaders consume. Independent image checks for frozen frames can catch temporal drift that a tolerant baseline comparison misses.

## Completion and observation

Inspect the application's bridge before adding features: storage buffers, instancing, compute, and timestamp queries may not all be exposed even when the backend supports them. Extend that bridge only when the requested experiment requires it.

For WebGPU, GPU submission and completion are separate boundaries. A timer around `renderer.render()` measures that call's elapsed time, including any bridge or synchronous waiting; `queue.onSubmittedWorkDone()` around a batch establishes completed batch elapsed time. Pure GPU time needs suitable device timestamps. Apply the corresponding API-specific instrumentation for a GLSL renderer.

Keep validation readback outside the timed window unless the application normally consumes those results. A successful readback establishes offscreen output. A successful present call, surface presentation, and physical scanout are separate observations.

When window timing is involved, record the actual paced frame rate. A 120 Hz fixed input sequence presented at 60 frames/s takes twice its simulated duration in wall time. Compare the same amount of work at comparable pacing, and keep offscreen throughput separate from normal-window CPU and memory costs.

## Experience that motivates these checks

The 2026-10-08 `webgpu-runtime` experiments used the real baseline renderer, real Metal work, and GPU readback. Their conclusions apply to those inputs and hardware:

- NYAN's initial f32 migration changed half-grid snapping at selected song times. Keeping a few double-precision CPU projections while moving bulk animation produced exact images in the tested cases. Bulk GPU placement and a small CPU precision boundary worked together.
- COMET kept charge/burst events on CPU and expanded stars, trail, particles, pitch markers, and an energy bar on GPU. Tests allowed a declared one-step RGBA8 difference between implementations, while requiring exact pause stability. That observed tolerance is an example, not a default for other renderers.
- Upload bytes decreased substantially, but upload-call counts increased. Normal-window CPU savings were smaller than unpaced offscreen savings, and unpaced peak RSS increased.
- Native window pacing varied, and two window processes stopped producing frames and were manually interrupted. The runtime had an occlusion pause path, but the particular cause remained unconfirmed. Completed comparable runs supported a limited conclusion; interrupted runs were retained.

When that repository is available, inspect `benchmarks/intonation-nyan/README.md` and `benchmarks/intonation-comet/README.md` with their raw JSON results. The skill works without that checkout; avoid using its old measurements as predictions for a new workload.

For current API semantics, consult the [WebGPU programming model](https://www.w3.org/TR/webgpu/#programming-model), [WGSL floating-point accuracy](https://gpuweb.github.io/gpuweb/wgsl/#floating-point-accuracy), or the project's target [Khronos OpenGL specifications](https://registry.khronos.org/OpenGL/specs/). These establish contracts, not performance guarantees.
