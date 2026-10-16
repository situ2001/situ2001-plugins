# Removing defensive tests

Use this guide when removing tests that enforce defensive behavior under review. Keep the audit within the requested scope.

## Triage by title

A full test run is an optional way to collect test titles and results when permitted by the active instructions. Use detailed runner output or test discovery to make the titles visible, and use them to identify retention and removal candidates.

Read a test's setup and assertions when its title does not establish what it protects or why it may be redundant. Resolve uncertain requirements through the relevant code, callers, contracts, and regression history.

## Decide what to retain

Retain tests that protect an explicit requirement, an established contract, a genuine trust boundary, or an observed regression. Defensive behavior at a boundary still needs a concrete rationale for the particular check being tested.

Remove tests whose only purpose is to enforce an unsupported guard, fallback, retry, limit, compatibility path, or repair of an impossible internal state. A test that expects such behavior does not itself establish a requirement for it.

Duplicate coverage and assertions tied only to implementation details can support removal when they add no distinct required behavior. A defensive-sounding title is a triage signal; judge the behavior it protects. Passing does not establish a test's value, and failure after simplification does not by itself justify deletion.

## Verify the result

After removing or updating the selected tests, choose verification that addresses the affected required behavior. A full run is available under the same authorization as above when useful for the audit; it is not required after every deletion. Report which defensive expectations were removed, why they lacked support, and which required behavior remains covered.
