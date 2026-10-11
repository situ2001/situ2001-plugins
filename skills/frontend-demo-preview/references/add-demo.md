# Add a demo

1. Locate bootstrap and effects in the page, its imports, hooks, and child components: requests, login, bridge setup, timers, analytics, and media. Account for effects that run during module import; a guard added after importing App cannot undo them.
2. Create a module such as `demo.ts`, exposing a named `Demo` object with the switch, typed data or fixture factories, and preview functions. Prefer a plain module; use a class when simulation needs state, reset, or disposal. Keep module import inert apart from reading the switch; create fixtures and resources when the demo branch runs.
3. Import `Demo` explicitly where needed. Prefer namespaced uses such as `Demo.enabled`, `Demo.getReportData()`, and `Demo.previewShare(image)` over copied flags, globals, or hidden registration. Put temporary logic in small, clearly removable branches near initialization and action boundaries.
4. Inject data through the existing state boundary: an apply-data function, store seed, provider, or component props. Keep fixtures and preview implementations in the Demo module; any necessary demo-only prop/action should have an explicit demo name and a traceable call site. For layout previews, skip live initialization. For workflow previews, provide local service behavior with finite, resettable response sequences.
5. Gate production integrations before they execute, including nested effects and login error paths. Handle client-only guards before the action as well as the action itself. Keep sharing previews in the Demo module, for example a dismissible layer showing the generated PNG, with cleanup for temporary listeners, timers, and DOM.

Prefer branches that leave the production path intact and can be deleted together:

```ts
import { Demo } from "./demo";

async function initPage() {
  if (Demo.enabled) {
    applyReportData(Demo.getReportData());
    return;
  }
  // Existing production initialization follows.
}
```

For this temporary workflow, a Demo module and a few explicit imports are the default. Reuse established preview infrastructure when appropriate; introduce a permanent dependency-injection architecture or separate build only when the requested scope benefits from it.

## Fixtures

- Use named, typed fixtures for relevant populated, empty, loading, long-text, or failure scenarios. Prefer existing response/state/props types over `any` or unchecked assertions. Keep times, random choices, and assets repeatable where screenshots need stability.
- Keep secrets, real user data, access tokens, and production identifiers out of fixtures.
