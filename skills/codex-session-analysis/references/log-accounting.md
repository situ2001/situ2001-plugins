# Rollout accounting

## Inputs, sources, and identity

The extractor accepts plain `.jsonl` and `.jsonl.zst`. Compressed input streams through the installed `zstd` CLI; decompression failure fails extraction instead of returning a successful partial report. It retains parsed records for merging, so streaming decompression does not imply bounded total memory. Pass candidate files in one invocation: separate invocations cannot deduplicate each other's histories.

Use `--source root` for user or voice sessions, `--source subagent` for spawned agents, and `--source guardian` for approval reviews. Repeat the option to combine categories; omission or `--source all` includes everything. Unrecognized source metadata remains `unknown` and can be selected explicitly. A parent session ID or shared repository does not make guardian or delegated work a user turn. `user_text` comes from user response items; `delegated_text` contains inter-agent messages. Keyword filtering searches delegated text only for subagent records.

The first `session_meta` identifies the file's owning **thread** (`id`); its `session_id` can refer to the wider parent session. Preserve both IDs. Later inherited metadata must not replace that owner. Observed subagent logs expose `subagent_history_start_ordinal`: the extractor omits earlier inherited work rather than charging it to the child. Root forks can instead expose a `history_base` pointing to another file; the extractor reads supplied files only and does not recursively fetch that history or infer attribution from matching text.

Files with the same owning thread ID are merged by capture timestamp, using ordinal to break timestamp ties. Paginated resumes can reuse ordinals after their `history_base`; sorting merged files by ordinal alone can move a later start before an earlier abort. A single file keeps its recorded order. If merged records lack complete timestamps, input order is retained with a warning. Recorded turn IDs scope deduplication; call IDs, response IDs, and message IDs identify their corresponding records. Anonymous records match only when their captured contents and timestamps match within a known turn. Identical prompts in different turns remain separate. Conflicting payloads for an identity are retained with a warning for manual inspection. `files` lists provenance; `duplicate_records` counts removed work records, excluding metadata.

The extractor supports explicit task boundaries. Logs lacking them require manual inspection; a compaction summary or inherited final answer does not create a new measured turn. Missing source or boundary information is a limitation to report, rather than a reason to classify the log from its answer text.

## Event boundaries

Common JSONL records use `type` and `payload`. `session_meta` supplies cwd, IDs, source, and Git metadata. `turn_context` supplies model/effort and sometimes tier. `event_msg` payloads include `task_started`, `task_complete`, `turn_aborted`, and `token_count`. User and assistant messages and tool calls often appear as `response_item`. Modern logs also record `token_usage_record` with explicit thread, turn, and response IDs. Formats vary by client version.

Select the task bounded by its start and terminal event, matching turn IDs where available. Count repeated event/message representations once. A user message embedded in a response item is distinct from a quote in assistant output. Aborted or active tasks have no successful completion latency; keep their observed usage separate. The extractor retains `aborted` and `incomplete` status, terminal type, and abort reason; `--trace` includes recorded error payloads. An error event can precede recovery, so its presence alone does not redefine a completed task as failed. For older logs with no task boundaries, manually use user-message-to-final-message timing and explain that boundary rather than fabricating `duration_ms`.

Prefer `task_complete.duration_ms` for completed latency and `time_to_first_token_ms` for reported TTFT. If duration is absent, timestamp subtraction is an observed event interval, not an identical measurement. Final-message timestamps may represent message completion rather than its first token.

## Usage

Report per-run measurements before means or ratios. Keep effort differences visible.

When `token_usage_record` matches the owning thread and turn and supplies `turn_token_usage`, use that recorded turn meter directly. It is already cumulative within the turn: take its last value, rather than summing it or adding the adjacent `token_count` representation. Its per-response `usage.input_tokens` supplies the observed request context sizes. The extractor labels this `usage_basis: recorded_turn_token_usage` and preserves missing token fields as unknown. A truncated run still has partial usage even when its last meter is internally valid.

`token_count.info.total_token_usage` is cumulative and must not be summed across events. Subtract the last cumulative snapshot before the turn from the last within it. Fresh sessions whose first total equals their first `last_token_usage` can establish a zero baseline. With inherited context or a missing baseline, mark the delta unknown. Do not assume a later turn starts from zero.

Preserve available fields: `input_tokens`, `cached_input_tokens`, `cache_write_input_tokens`, `output_tokens`, `reasoning_output_tokens`, and `total_tokens`. Missing fields are unknown, not zero. Check for decreasing counters, repeated events, missing end snapshots, and total/input/output inconsistencies. If a reset or fork makes subtraction unreliable, split accounting intervals only with evidence; otherwise report unknown.

For compatible logs:

```text
uncached input = input - cached input
cache hit ratio = cached input / input
total = input + output
```

Reasoning output is a subset of output. Output includes generated tool calls and other generated content, not only the final answer. A zero reasoning field is not proof of absent reasoning. Image input is already represented in aggregated usage when the log includes it; do not also charge by image count without an explicit rate/metering model.

Cache-write overlap with input requires checking the producer's schema before applying a write surcharge. The simple uncached formula is sufficient for the observed zero-write cases, not a universal cache-write billing contract.

Use each event's `last_token_usage` to inspect per-request context sizes, not as an automatic alternative sum: duplicated snapshots may double-count requests. An incomplete set of snapshots makes the observed maximum a lower bound, not proof that long-context thresholds were never crossed.

## Tool traces

Count outer tool rounds separately from shell commands; parallel batches and tool discovery are not equivalent to one search each. For search comparisons, list each round's relative start time, key queries and scope, files read, visible results, and relevant truncation or failed attempts. Distinguish useful verification from repeated work using the question each read resolves. A skill announcement is not proof that its tool was used.

Match `function_call`/`custom_tool_call` with the corresponding output by `call_id`. Record the tool name and raw arguments/input as data. CUA or other shapes may need an adapter. Outer orchestration code can contain several shell invocations, loops, or parallel batches; static occurrences of `exec_command` do not reliably count actual commands.

Report both summed tool response latency and, when calls overlap, the union of intervals. Their sum can exceed elapsed task time. Tools returning a live process ID or `Script running` have yielded, not necessarily completed: label the duration as time to tool response and include subsequent waits when reconstructing process lifetime. Missing outputs mean incomplete timing. Result truncation estimates, including `original_token_count`, are not billed token usage. Attribute time outside tools to model processing, generation, communication, and other unseparated overhead, not exclusively reasoning.

The bundled extractor omits image bytes, hashes decoded data-URL image bytes, and emits trace text only with `--trace`. Hash equality establishes identical bytes, not equivalent cropping/rendering or model image processing. Non-data image URLs are references, not content identity. Unknown schemas should remain visible in warnings rather than be normalized into false precision.
