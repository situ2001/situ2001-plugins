# Original binary differential checks

Use original executable code as a compatibility baseline when recovering firmware/library semantics or comparing an emulator or HLE implementation. Original-code agreement establishes the selected behavior under the supplied state and boundary substitutions; it does not establish hardware fidelity or correctness of the original product.

## Build the evidence chain

Follow the links needed for the disputed interface:

1. Identify the application wrapper or caller and the interface number it selects.
2. Locate the dispatch entry and its actual target in the original binary.
3. Inspect the implementation and relevant callers to recover argument layout, signedness, return convention, and memory effects.
4. Execute the unmodified original path with controlled inputs and record its effects.
5. Run the candidate implementation with equivalent inputs/state and compare the relevant observations.

Keep addresses and evidence for each link. Register snapshots can contain stale values; use caller/callee data flow before inferring argument count. A symbol name or a dispatch branch alone is insufficient evidence of ABI semantics.

Record original image/code hashes, extraction identity, load and relocation addresses, endianness, ISA/runtime, and entry/return locations. Preserve the initial registers, stack, mapped memory, structures, and global state needed to repeat the case. Establish calling-convention details from the original path rather than assuming a host function signature.

## Control the boundary without answering the question for it

Keep the original function and relevant callees unmodified. List intercepted helpers, MMIO accesses, or host services with their supplied inputs/results and the behavior those replacements exclude. For example, executing an original file-position routine with fixed drive-validity helpers can establish its offset/position rules while leaving real filesystem coordination untested.

Observe return registers or error codes, relevant memory regions and flags, output pixels or buffers, and consequential calls/events. Compare effects with equivalent initial state, including reset state between runs. A matching return code can hide a wrong file position, omitted memory write, or missing event.

When GPU helpers are intercepted, original control-flow execution may establish frame selection, geometry, or blend endpoints while leaving pixel conversion unverified. Compare actual pixel buffers only when that execution path produces them; a presented screenshot does not by itself establish intermediate GPU behavior or physical display output.

Keep unknown behavior explicit. An unimplemented instruction, device transition, or unknown register read is an unresolved execution boundary. Supply success/completion values only when supported by the device contract or measured original behavior; otherwise stop and preserve the diagnostic. Failures from invented completion values cannot explain the original device.

## Preserve complete replay inputs

A syscall or allocation trace may reproduce one subsystem without reproducing the application history that created it. Record external inputs needed for the intended replay: touch/key actions and coordinates, virtual-clock advances, message delivery, resource contents, random/RTC state, and host completions as applicable. Preserve capture order and identify omitted inputs.

If an old trace lacks touch events, label a successful allocation replay as an allocation check. A newly recorded interaction can exercise a similar flow but cannot be called exact replay of the missing history. Use the actual user journey when the reported failure depends on reaching a particular state.

## Report coverage by the claim it supports

| Evidence | Supported claim |
| --- | --- |
| Wrapper/interface inventory | Interfaces discovered in the inspected corpus |
| Dispatcher contains a branch | A routing path exists |
| Original application reaches startup/queue | That entry path ran under the tested environment |
| Original/candidate comparison of selected cases | Agreement for those inputs, states, and observed effects |
| Application interaction through the intended runtime | The recorded flow worked through the exercised integrations |

Keep these results separate. Inventory totals, handlers present, or startup counts do not establish every parameter, blocking behavior, device mode, or application feature. Report differences and unsupported modes next to the relevant interface, together with commands and artifacts for the controlled original-code cases.
