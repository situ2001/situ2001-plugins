# Measurement boundaries

Read the sections matching the workload and metrics; multiple sections may apply.

## Web delivery

Distinguish raw build size, compressed artifact size, and actual transferred bytes. Capture the requested page's requests, encoding, and cache conditions; a bundle inventory alone does not measure network transfer or page readiness.

## Inference

Separate loading from inference, identify the actual CPU/GPU backend, and wait for device completion when execution is asynchronous. Check the resulting output. For generated audio, output duration and elapsed inference time can support a real-time-factor comparison when useful.

## Resource use

Retain the tool's CPU normalization and memory definition, such as RSS or device allocation. On shared or unified-memory systems, overlapping memory categories cannot simply be added. System GPU activity does not by itself attribute work to the target process.
