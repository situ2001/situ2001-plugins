# Linear Requirement workflow

## Ownership

- **Parent Issue:** overall goal, scope and an explicit link to the designated Handoff. Other Documents are supporting sources.
- **Handoff:** shared navigation and project-wide constraints with necessary rationale. Link code entry points, requirements, designs, conversation records, transcripts and resources, explaining what each contains and when to read it. State consequential shared constraints directly. Keep task-specific sources and specifications with their Issue; discover work through `list_issues`, not a duplicate directory. Reference maintained repository and skill guidance, retaining project-specific exceptions.
- **Sub-issue:** an independently trackable outcome. Its description holds consolidated objectives, scope and acceptance criteria. Give a local contract one primary record and reference it from related Issues; affecting several tasks does not make it a global constraint.
- **Comments:** incoming material, discussion, confirmations, progress and evidence. Append by default; edit existing comments only when requested. Use parent discussion for intake whose task ownership is unresolved.

Resolve targets from the request or conversation. For a selected sub-issue, read its Requirement parent. Search when necessary; clarify meaningful ambiguity before writing. Keep Requirements separate; an absent match does not authorize creating one.

## Ticket scope

An execution Issue is a vertical slice: one narrow but complete behavior that can be demonstrated or verified independently across the layers it needs. Describe the outcome and acceptance criteria, not a layer-by-layer implementation list. Keep implementation steps in the Issue's checklist. Declare a blocking edge only when another Issue must finish before this one can start.

## Incremental context

Select the appropriate skill from the user's request; naming the skill is optional. Ordinary chat alone does not authorize Linear writeback. Triage routes increments, creates necessary sub-issues and organizes relationships. Existing descriptions and Handoff remain unchanged unless their edit is explicitly requested; routine consolidation waits for the user to request Digest or describe the consolidation they want.

Descriptions and Handoff are baselines. Explicit confirmations in comments apply before Digest; proposals and linked sources do not become decisions merely by being recorded. Distinguish agreed intent, observed implementation and unresolved interpretation. Digest consolidates confirmed changes into their owning records, keeping comments as history.

Keep local evidence local when requested. Record a base directory for relative paths and useful provenance: source identity, speakers/timestamps, commits and observation dates. Current source establishes current implementation; historical checks establish only what they checked.

## Focus and closure

Use the team's statuses to identify closed Issues. Default discovery, progress summaries and follow-up to open Issues. Read a closed Issue only when the user explicitly selects it or current open work needs its historical contract or evidence; reading it does not resume tracking.

Closure ends attention to that work. Historical TODOs, unresolved questions or missing verification evidence in a closed Issue do not become reminders, active gaps or replacement Issues. Resuming that work requires an explicit user request.

## Authorization and Review

Triage, Digest, Issue creation and assignment do not authorize implementation or merge; direct user instructions can authorize work. Triage preserves status unless separately instructed. On delivery, record results, actual checks and unfinished work in a comment and request Review. The human decides Done. Query team statuses when the intended status's availability is unknown; without a Review state, request Review in a comment and retain the actual status.

## Writes

Use the connected Linear MCP and its current schemas and Markdown conventions.

Read current targets and relevant discussion before editing. Before creating an Issue, check for matching work; reuse discovery results that already cover the relevant scope. Update only intended fields, preserving unrelated data and human edits. Prefer exact-anchor patches for local changes; reread and reconcile after conflicts or before broad rewrites.

For moved content, confirm destination records before shortening the source. Verify saved content and associations from the write response when it provides sufficient evidence; read the records when it does not. Report partial completion on failure; check an uncertain create before retrying it. Multi-record writes are not a transaction.

## Write Clearly

Apply these principles, adapted from ASD-STE100 Simplified Technical
English, in chat replies, documentation, and code comments. Adapt them
to the language being used, including Chinese.

- Use the same term for the same concept or object throughout a text.
- Use familiar words in general prose and established technical terms
  for domain concepts.
- Prefer direct verbs. State the action instead of wrapping it in
  abstract nouns or unnecessary introductory phrases.
- Make the actor explicit when known and relevant. Prefer active voice
  when it makes responsibility clearer.
- Give each sentence one main topic. Keep necessary conditions and
  causal relationships clear, and connect related explanations.
- In procedures, put conditions readers must know before the actions
  they govern. Present sequential actions in a clear order.

Preserve meaning, necessary detail, and natural flow when simplifying
language. Preserve exact wording in quotations, code identifiers, and
required formats.

