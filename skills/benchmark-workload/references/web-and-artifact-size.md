# Web delivery and artifact size

Use for page assets, transfer/readiness comparisons, or native libraries and application packages.

## Route and interaction scope

Start from the requested route's emitted entry points. Follow static imports and count reached files once. Record dynamic imports by the interaction or lifecycle that triggers them: opening search, mounting a chart, or navigating to another route. An all-dynamic inventory is a potential reachability total, while a particular visit may trigger only part of it.

A large emitted lazy chunk remains lazy until its trigger occurs. Conversely, a chart imported dynamically on mount may be fetched during the initial visit, so a static-only total can understate that visit. Verify requests through the intended user flow when reporting delivery cost.

Keep these quantities separate:

- Raw emitted file bytes and the files included in the inventory.
- Locally compressed bytes, including compressor/settings and whether files are compressed independently.
- Observed network transfer, including encoding, caching, runtime requests, and external resources.
- Page readiness or interaction latency, with the completion event and browser/throttling configuration.

An inventory of JS omits HTML, CSS, fonts, images, headers, and runtime search/data requests unless included explicitly. Use request/resource evidence to find the cost dominating the page in question. A large JS reduction may leave text rendering, font delivery, CSS, or other work dominant. Measure readiness separately rather than projecting it from byte savings.

For a migration, list the functional changes alongside the runtime swap. Compare matching route and interaction behavior before attributing the whole difference to a framework. Use profiles, request timing, or a controlled follow-up to identify the mechanism behind a measured loading change.

## Native libraries and packages

Build a variant table that records platform/architecture, backend/features, toolchain, optimization profile, stripping, linking, exported entry points, and artifact identity. Keep raw, stripped, and compressed sizes in distinct columns with exact byte counts; label unit conversions.

State the packaged scope: one architecture's library, universal binary, app/APK, external bootstrap/resources, or install footprint. A gzip estimate for a library does not measure an APK increment or installed size. Record system dependencies versus libraries that must be distributed.

Verify retained functionality. A minimal probe needs reachable entry points that actually exercise the intended engine/GPU/host path, so dead-code elimination does not silently reduce its scope. When variants differ in bridge, audio, lifecycle, or backend support, report those differences beside the size delta; the delta cannot be attributed solely to the swapped component.

For target platforms available to execute, load the exact measured artifact and run a representative operation through those entry points. Preserve output checks and artifact hashes. Successful compilation, export checks, alignment, and dependencies establish static properties; record unavailable target runtime validation separately. Exclude artifacts that fail to load from claims about working deliverables while retaining their failure records.

Size-oriented compiler options can change runtime semantics or performance. Describe concrete tradeoffs, such as aborting instead of unwinding, and benchmark performance independently when the question requires it.
