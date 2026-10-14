# Native UI geometry and input

Use the real target app when the question depends on accessibility geometry, native windows, focus, or input routing. A focused host executable can establish an API mechanism; the target app decides whether that mechanism preserves its actual behavior.

## Capture geometry independently

For a popup that must avoid text, capture the target text bounds and read back the actual native popup frame after placement. Calculating an expected frame from the same inputs as the placement function only checks its arithmetic; it cannot reveal a wrong accessibility range or a window manager adjustment.

Retain enough identity to associate both observations with the same state: target build/executable, PID, window or element identity, selection/range, and capture order. Capture the intended source artifact, including whether the running app was rebuilt or merely reloaded. Read geometry after the relevant native layout completes; if text or window state changes between readings, repeat the paired observation.

Record the coordinate system of each rectangle: origin, axis direction, points versus pixels, display frame, and any window-local offset. Convert both into a common system before testing overlap or gap. Derive display offsets from the measured display configuration; a primary-screen height copied from an old run is fixture data.

Choose the accessibility range that represents the requirement. In a measured Apple Notes case, zero-length caret bounds were vertically above the actual text line. Resolving the containing line with `AXLineForIndex → AXRangeForLine → AXBoundsForRange` exposed the mismatch; the caret remained useful for horizontal alignment. Apply that method when line avoidance is the question and the target exposes those attributes. Missing range data leaves that geometry claim unresolved.

Save raw API results alongside the derived overlap assertion. A retained old placement that overlaps the measured line can provide a negative control. State whether a command captures a fresh UI state or only checks a saved measurement: rerunning assertions over a snapshot establishes the snapshot's geometry, not current application placement.

## Separate focus and input claims

Select the observations required by the user's claim rather than treating “focus worked” as one result.

| Claim | Useful evidence |
| --- | --- |
| Application activation changed | App activation state or notifications over the operation |
| Foreground application stayed the same | Frontmost app observations; event monitoring if transient changes matter |
| Window stacking stayed the same | Native window order before/after, plus continuous observation if required |
| Intended editor became first responder | Native responder identity or the target's available equivalent |
| Injected text reached the intended editor | Distinctive marker read back from that exact editor, checking other candidate windows too |
| Physical keyboard stayed with the user's app | A separate physical typing observation while the tested state is held |

Equal before/after foreground or stacking snapshots leave intermediate transitions unmeasured. Injected text reaching one window does not establish physical keyboard routing. A screenshot missing a blinking caret does not establish failed text input; read back the text or responder state where available, and label sparse visual observations accordingly.

## Isolate the mechanism, then check the app

For uncertain input APIs, an owned disposable app with two distinguishable windows/editors makes wrong-window delivery observable. Record their native state and text independently. Compare meaningful variations such as a cleared versus already-established text responder, event subtype, or ordering of click and focus operations, changing the disputed variable while retaining other conditions. Historical matrix sizes and marker strings are examples, not required parameters.

A fixture pass supports the fixture's controls and lifecycle. Repeat the relevant flow in the intended application before claiming app compatibility; carry forward unresolved fixture failures rather than hiding them behind a successful target screenshot. Respect the authorized interaction scope when a real app can send messages or change user content. Own the fixture and its restoration; target-app draft insertion and cleanup need the corresponding task authorization and fresh target state.

Report which claims were observed directly, which used snapshots, and which remain untested. Keep original failures visible when focus restoration or cleanup also fails.
