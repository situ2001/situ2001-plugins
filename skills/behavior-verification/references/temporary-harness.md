# Temporary harness lifecycle

Read this when creating, relocating, or retaining a one-off check, installing scratch dependencies, or managing its resources. Prefer an existing focused test when available.

## Build within the task's scope

Use a uniquely named temporary directory or an inline command. Prefer installed tools; a small version-compatible dependency isolated in scratch space is reasonable when permitted and necessary. Record temporary dependencies and their versions. Keep the check focused rather than turning it into a framework migration.

Write readable setup/action/assertion/cleanup blocks with case names and diagnostic assertions. Another agent should be able to locate a failure without reconstructing compressed code. Preserve useful source snapshots deliberately and avoid overwriting unrelated artifacts. Identify whether rerunning uses frozen source or rereads current Git state.

## Run from the final location

Execute the documented command from the final artifact location: moving a saved script can change dependency resolution. Record the source revision or working-tree state, inputs, command, and environment requirements sufficiently to repeat the check. For source-loading mechanics, use the relevant runtime recipe linked from SKILL.md.

Move a recurring regression into the repository's established test structure when that fits the task.

## Release owned resources

Clean up owned processes, browser contexts, listeners, timers, and fixture state even after failed assertions. Restore replaced globals or loader hooks as the relevant runtime requires. Retain useful failure evidence and deliberate snapshots. Keep cleanup failures visible without erasing the original assertion failure; inspect exit status after cleanup, not merely an earlier printed result.
