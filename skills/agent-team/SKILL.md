---
name: agent-team
description: Orchestrate multi-agent delivery with GPT-6 Astra Medium direction and GPT-6.1 Sol High execution when explicitly invoked by the user.
---

# Agent Team

Give the user control over intent, constraints, and success criteria; give agents ownership of completing the work. The main agent is the **director**, responsible for direction, consequential decisions, and acceptance. Delegate concrete execution as fully as practical.

## Establish the director

Prefer **GPT-6 Astra Medium** for the director. The current agent directs the work and communicates with the user directly, without checking its model or requiring a model switch. Default to **GPT-6.1 Sol High** for Codex executors, including investigators and independent verifiers. Honor an explicitly requested agent CLI or model; Claude Code uses its configured model unless the user specifies one.

Use the user's explicitly chosen runtime. For `auto`, or when none is specified, choose Herdr when `HERDR_ENV=1` and the `herdr` CLI is available; otherwise choose Codex built-in collaboration. Report the selected runtime briefly. Read only the matching runtime guide: [Codex built-in](references/codex-builtin.md) or [Herdr](references/herdr.md). The guide supplies the launch, communication, wait, and cleanup mechanics; the workflow below is shared. Launch CLI executors with automatic approval review as described there. When the selected runtime cannot provide the required models, effort settings, or delegation, explain the limitation and ask the user to choose a supported arrangement before proceeding. Do not silently switch runtimes or claim a model switch. A role assignment grants no additional filesystem, external-action, or cross-chat permissions.

## Confirm the direction

Before implementation, read and apply [grilling-focused](../grilling-focused/SKILL.md), including its required `grilling` base. If the relative location is unavailable, find `grilling-focused` in the available skill catalog; report a missing dependency instead of inventing a replacement interview.

Carry forward already confirmed decisions. Build the focused design tree only from unresolved choices that need user judgment and could materially change the goal, scope, core approach, or acceptance criteria. Investigators establish facts; executors decide local, reversible implementation details. While direction is unresolved, discovery can supply evidence for decisions, but implementation waits for its scope to be confirmed.

Follow the focused/base interview's frontier and completion rules. Summarize the resulting direction and obtain confirmation before executing a newly agreed scope. An existing confirmation covering the current scope remains valid; unanswered questions and elapsed time are not confirmation.

## Delegate commitments

The director owns decomposition and shared interfaces. Delegate investigation, implementation, debugging, routine validation, and integration to executors by default. Executors decide reversible implementation details and complete their contract autonomously, including debugging and appropriate routine tests. Use findings to refine the plan and resolve dependencies; when work stalls, clarify the commitment, supply missing context, or reassign it.

Choose roles and concurrency to fit the work; a developer can investigate and test its own change. Add an independent verifier when behavioral uncertainty or the cost of a mistake justifies a separate perspective. A small task can use one executor while the main agent remains the director.

Run independent workstreams in parallel when dependencies, write ownership, and available agent slots allow it. Launch ready work before waiting for results; wait when dependent work or acceptance needs those results.

Before first dispatch or reassignment, read [delegation contract](references/delegation-contract.md). Each brief identifies:

- **Outcome and authority:** confirmed goal, acceptance criteria, settled decisions, and escalation boundaries.
- **Context and access:** source/artifact paths, applicable instructions, dependencies, and accessible resources.
- **Ownership and coordination:** write scope, shared interfaces, and peer addresses. Keep one active writer per shared file; serialize changes or explicitly transfer ownership. Agents share a workspace unless an isolated checkout is supplied.
- **Return contract:** usable deliverable, caller-facing semantics, return location, acceptance evidence, and unresolved gaps.

## Close defects with evidence

When choosing independent verification, read [independent verification](references/independent-verification.md). The verifier exercises behavior independently against confirmed criteria; developer claims are context, not proof. Connect verifier and developer directly for the reproduce → fix → recheck loop, then have the verifier return its verdict, traceable evidence, and remaining gaps to the director.

Escalate changes to the agreed goal, scope, shared/public interface, or authorization, and conflicting evidence requiring a decision. Include the failed commitment, evidence, consequence, and recommended next step. The director decides within its authority and returns to the user when judgment or permission is required. Runtime failures and uncertain implementation details belong in the executor's investigation loop.

Use completion notifications or runtime-appropriate agent waits. Investigate status when a dependency is blocked or intervention could help; avoid turning routine progress into repeated polling and summaries. Keep the user informed of meaningful findings, decisions, and remaining uncertainty.

## Accept and deliver

The director checks the key commitments against the delivered interface and acceptance evidence, including integration between workstreams. When a concrete discrepancy, missing evidence, or integration risk needs investigation or another check, delegate that follow-up and assess the returned evidence. Inspect source directly only when needed for a specific director-level decision; routine acceptance relies on the delivered evidence.

Complete the selected runtime guide's lifecycle requirements before final delivery or handoff.

Accept when the confirmed criteria are supported and material gaps are resolved or explicitly accepted by the user. Report what was delivered, how to use its interface or entry point, what the evidence establishes, and any remaining limits. Keep implementation logs and internal coordination out of the user's delivery summary.
