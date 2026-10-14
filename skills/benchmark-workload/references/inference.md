# Inference and generated output

Use for backend selection, model stages, startup/cache comparisons, and end-to-end generation such as TTS.

## Align the measured operation

Preserve model/weights identity, input tensors or their hashes, preprocessing, precision, thread configuration, and the actual execution provider/device. Compare an individual stage on the same input before selecting its backend; an encoder's GPU advantage need not apply to an autoregressive loop or the complete pipeline.

Trace the application's real stage boundaries. Include or exclude decode, resampling, tokenization, reference preparation, synthesis, encoding, transport, file output, and validation explicitly. Two similarly named stages may cover different work. Keep the component result and full-pipeline result distinct.

For generation, inspect effective implementation settings as well as configuration: sampling/greedy rules, repetition penalties, EOS, text splitting, speed, and limits that already belong to the workload. A Top-1 setting alone does not establish equivalent generation rules. Preserve remaining differences with the result.

## Separate lifecycle phases

Record loading/session creation, first execution, reused-session execution, and full output readiness separately. Describe which caches survive each reset: another call, page reload, worker recreation, model session rebuild, or process relaunch. Fresh processes may still use warm OS file caches.

Use comparable reset boundaries across variants. Service-ready time and first synthesis including initialization are different operations; present them independently unless their boundaries are aligned. Preserve warmup runs as a separate phase rather than silently treating them as unsuccessful measurements.

## Observe device completion and output

For asynchronous backends, use the API's completion contract and synchronize or read back where required by the chosen boundary. Record whether the timer includes a CPU-readable result, device-only completion, or merely submission. Include the relevant device synchronization when measuring an otherwise asynchronous stage.

Check outputs with evidence appropriate to the operation: token count/hash, tensor values, deterministic intermediate hashes, or semantic equivalence when exact equality is not expected. For audio, retain duration, sample rate/channels, decodable nonempty samples, and artifact identity. Hash matches establish identity, not perceptual quality; audio validity alone does not establish equal quality.

Keep correctness checks outside a performance timer when that matches the question, and say whether resource sampling still includes them. Preserve failed, empty, interrupted, and invalid-controller runs separately, including whether a useful output was ever completed.

## Compare varying generation lengths

Report total latency together with generated token count or audio duration. When useful, add throughput or real-time factor (`elapsed / output audio duration`), naming included silence or postprocessing. Different output lengths mean a total-time ratio is not an equal-output compute ratio. A normalized measure also retains generation/quality differences and does not erase them.

Pair stage timing with end-to-end timing before explaining a speedup. A backend that is faster on one fixed tensor can incur session creation, transfers, messaging, or different generation behavior in the application. Keep the conclusion within the measured stages, lifecycle, outputs, and backend configuration.
