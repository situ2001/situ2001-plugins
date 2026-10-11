# Remove a demo

1. Establish the requested scope, including the actual diff base when one is supplied. Identify the Demo module, its imports, supporting assets, and demo-only props/actions; preserve pre-existing demos outside that scope.
2. Delete the scoped Demo module, then remove its imports. Deleting only the module may report an unresolved import without identifying every use; removing the imports exposes remaining `Demo` identifiers to type checking.
3. Run the repository's type check and use reference search to locate remaining integration points. Remove complete demo branches, supporting props/actions, and unused assets. For mixed conditions, retain the production terms: `Demo.enabled || isShareView` becomes `isShareView`. Do not silence cleanup errors with `any`, ignore comments, or replacement stubs.
4. Inspect the diff for changes that type errors cannot detect: altered defaults, inline fixtures, magic query flags, skipped effects, and preview DOM/styles. Type errors are a cleanup aid, not a complete inventory or proof of restored behavior.
