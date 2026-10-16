## Software Design

Design for ease of change (ETC): reduce what callers must know and keep
changes local (Locality).

Use intention-revealing names and clear control flow to make code read
as a coherent narrative. Apply Tell, Don't Ask to keep behavior with the
module that owns the relevant rules and state.

Apply KISS, YAGNI, information hiding, high cohesion, and low coupling to
build Deep Modules: useful behavior behind a simple, clear Interface,
with implementation complexity contained inside the module. The Interface
includes everything a caller must know to use the module correctly.

Introduce abstractions to hide actual complexity, centralize duplicated
knowledge, or isolate real variation. Apply the deletion test: if removing
a module removes complexity, question its value; if complexity spreads
back into callers, the module was earning its keep. Place Seams where
actual substitution or verification needs justify them.

Verify observable behavior through the Interface so tests can survive
internal refactoring. Use SOLID, DRY, and related principles to guide
trade-offs, judging each choice by whether it reduces the cost of
understanding and changing the software.
