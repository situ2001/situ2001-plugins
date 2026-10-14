# Data pipeline and generated-output checks

Use this reference for archive/package audits, parser and cross-table contracts, source-to-display provenance, time-zone behavior, and output cleanup. Pick the sections that match the uncertainty; a package inventory alone does not require a live-service or publishing test.

## Separate change detection from semantic correctness

For a package regression audit, inventory the entire archive member list before selecting known tables. Retain the original package identity and each member's path, byte length, and content hash, using the archive's actual member semantics. Report added, removed, and changed members against a frozen reviewed inventory. This detects changes outside currently parsed tables and distinguishes an unchanged member set from a changed container.

Verify that the audited bytes match the package manifest/version being reported. Keep the reviewed inventory independent of current parsing output. Update it as an explicit acceptance of inspected upstream changes; automatically writing the current inventory before comparison erases the regression signal.

Run semantic checks separately against decoded contents. A hash detects changed bytes, not a wrong field offset, units, encoding, record count, or omitted relationship. Associate semantic assertions with the tables and claims they cover so unchanged baseline hashes do not become a blanket correctness claim.

Derive cross-table relations from format documentation, original readers, or observed records that establish the contract. Equality, containment, uniqueness, and optional lookup are different relations. For example, a table containing a subset of station positions may legitimately be contained in the route table without being equal to it. Investigate mismatches before weakening assertions; record the evidence that justifies the corrected relation.

## Trace raw values to their meaning

For a disputed API or parser value, retain a minimal raw payload and its source context: endpoint/package/member identity, relevant request parameters, service date/time zone, and capture time when meaningful. Trace raw field → decoded value → normalized model → displayed or serialized value. Distinguish upstream absence, explicit zero, parse failure, derived values, and fixture substitutions according to the actual contract.

Use distinctive values to expose swapped fields or accidental joins, and preserve source identity through normalization where the product requires it. A plausible fixture can establish consumer behavior for that fixture; it cannot establish the current upstream response shape. Use current authorized upstream evidence when that shape is part of the question, or report the fixture-only boundary.

For overnight schedules or date-bearing records, distinguish service-day offsets, wall-clock values, and absolute instants. Derive the expected rollover from the domain contract; a repeated terminal time or missing departure may have different semantics from a normal intermediate stop. Preserve unknown values rather than coercing them into a convenient zero.

## Check time-zone invariants where required

Run the same fixture under differing process/browser time zones when the contract says its result is independent of the host zone. Hold the service date, source zone, input bytes, and clock instant fixed as needed to isolate host-zone dependence. Choose zones that expose the suspected day boundary or offset; include a daylight-saving transition only when that behavior matters to the contract.

Assert the contracted representation: for example, the same service-local date/time or the same absolute instant. Localized presentation may intentionally vary. Changing the clock, service date, and zone together leaves the cause of a difference unclear. Record the environment and the expected invariant instead of imposing universal UTC conversion.

## Verify removal as well as creation

For a generator or publisher, create the authorized content in an owned test workspace and inspect emitted files/routes/index entries. Then revoke, unpublish, remove, or exclude that same content using the supported workflow and run generation again over the previous output directory. A fresh empty output directory cannot reveal stale artifacts left by incremental rebuilds.

Check absence at the surfaces the contract exposes: page output, assets, search/feed/sitemap entries, or deployed responses when deployment is within scope. Retain a separate still-published item to detect over-broad cleanup. Record whether the check covers local generation, deployment, or cache invalidation; local absence alone leaves remote delivery unverified.

Preserve the frozen input/package, reviewed inventory, raw examples, semantic assertions, and replay command needed for the selected claim. State exactly which pipeline stages executed and which used saved data or fixtures.
