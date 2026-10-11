---
name: frontend-demo-preview
description: Add or remove temporary frontend demo modes, with local data and preview behavior centralized in a removable Demo module.
---

# Frontend Demo Preview

Use this skill for temporary frontend previews that work without authentication, client-host APIs, or live backend data, and for removing their demo code before delivery.

## Core outcome

Render the real page and component tree with an explicit switch (usually `?demo=1`). Centralize the switch, fixtures, and preview functions in a project-local Demo module, then explicitly import it at the few integration points that need it. Those references make later removal discoverable. The demo path is for visual and interaction preview, not authorization simulation or production behavior.

## Choose the operation

- Before adding or changing a demo, read [references/add-demo.md](references/add-demo.md) for initialization, import-time effects, fixtures, and preview actions.
- Before removing a demo, read [references/remove-demo.md](references/remove-demo.md) for scoped deletion and cleanup of integration points.

## Reversibility and code boundaries

- Make each temporary behavior traceable to the Demo module. Avoid unmarked changes to production defaults, ownership rules, or component behavior merely to improve a preview; those changes survive deletion without a type error.
- Demo clicks use local behavior or clearly labeled unavailable results, never production writes.
- Preserve production request contracts and authorization. Keep the module within the project's ownership boundary; avoid changes to shared libraries for a single page.

## Verification and completion

After adding, verify that the demo uses local data and safe preview actions, while the page without the flag retains its normal initialization. After removal, verify that scoped demo references and behavior are gone and production paths remain intact. Run the repository's type check/lint commands and inspect the diff in either case. Reference search is also required for JavaScript or files outside the type check's coverage. Respect repository restrictions on starting a dev server and report code-level verification limits when runtime verification is unavailable.
