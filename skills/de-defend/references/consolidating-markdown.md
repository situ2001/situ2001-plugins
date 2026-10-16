# Consolidating Markdown

Reduce the places that must change when a fact changes. Judge content by its purpose and maintenance cost, rather than repeated wording alone.

## Establish the document's purpose

Identify the reader's task and whether the document provides current guidance, a decision's rationale, or a historical record. Read related sources before treating apparent duplication or conflicting claims as a cleanup target. Different versions, backends, environments, or validation stages can legitimately have different results.

## Choose where facts are maintained

For repeated facts, find the existing place responsible for maintaining them. Prefer a useful local summary with a reference over copying its explanation. Make the reference say what the reader will find and when to consult it; preserve instructions needed for independently used entry points and agent documents.

Treat implementation inventories, command options, configuration defaults, exact test counts, measured results, and completion lists as candidates for drift. Use maintained code, configuration, command help, or structured evidence as the source where appropriate. Keep selected details inline when they help the reader act or interpret a result; easy lookup is a reason to reference a source, not to reproduce its contents.

## Consolidate content

- Merge repeated explanations into the maintained location and update other occurrences to concise references. Repetition can be useful when separate contexts each need an instruction or consequential warning; keep that local information.
- Delete explanations that add no useful action, understanding, or evidence, including repeated assurances and residue from earlier editing conversations. Preserve necessary prerequisites, limitations, uncertainty, and rationale.
- Verify apparently stale claims against the relevant implementation or evidence. Replace duplicated current-status snapshots with a maintained status and evidence link. State the applicable version, backend, patch, or stage when it changes the conclusion. Report unresolved discrepancies rather than choosing the newest-looking statement as truth.
- Preserve dated research, measurements, and decision records as historical evidence. Clarify their historical role and point to current guidance when needed; a later implementation does not invalidate what an earlier experiment observed.
- Move or merge sections and whole documents when their useful content belongs together. Delete a redundant document once its unique information has a suitable home and its references are updated. Prefer existing destinations over creating another summary that repeats them.

For example, if a skill reference says game execution is unfinished but a project report records successful execution in an isolated copy, point the skill to the maintained implementation and evidence. Preserve the distinction between that validation and changes to the production world. A topic-specific report can link to overall validation results instead of repeating unrelated project-wide test counts.

## Verify and report

Check incoming references when moving or deleting content, update affected links and anchors, and confirm that readers can still reach the maintained information. Check changed factual claims against their sources. Completion means redundant maintenance points are removed while required instructions, distinct evidence, and historical context remain accessible.

Report what was consolidated or removed, where the maintained information lives, and any unresolved factual discrepancy. Scale the report to the change; an additional cleanup report document is unnecessary unless requested.
