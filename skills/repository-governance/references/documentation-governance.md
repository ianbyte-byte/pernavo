# Documentation governance and AI context safety

Use this reference when project documents may be stale, duplicated, contradictory, or exposed to an
AI agent as current guidance. The goal is not to make every document uniform. The goal is to keep
the active decision surface small, attributable, testable, and free of obsolete instructions.

## 1. Build the document inventory

Search at least these surfaces:

```text
AGENTS.md / CLAUDE.md / other host instructions
README files and contributing/security policies
docs/, runbooks, operations guides, ADRs, plans, reports, examples
Skill entrypoints and references
generated documentation and schemas
archive, deprecated, legacy, migration, and backup directories
CI/config files that publish, index, copy, or inject documentation
```

Record only fields that change a decision:

| Field | Meaning |
|---|---|
| path | Current repository path |
| class | normative, operational, reference, decision, generated, historical |
| status | active, draft, deprecated, superseded, archived |
| owner | Person/team/system accountable for correctness |
| scope | Product area, version, environment, or audience |
| source of truth | Code/config/system/document that can verify the important claims |
| revalidate when | Semantic trigger such as API/schema/command/owner/release change |
| AI exposure | Direct instruction, linked reference, indexed/searchable, or archive-only |
| conflicts | Other files that assert a different current state |

Do not require frontmatter on documents whose format or owner forbids it. A sidecar inventory is
acceptable. When metadata is embedded, prefer a compact block such as:

```yaml
status: active
owner: team-or-role
applies_to: component-or-version
last_verified: YYYY-MM-DD
revalidate_when: API, schema, command, owner, or release process changes
supersedes: path-or-none
```

`last_verified` is a signal, not proof. A semantic change can invalidate a document the next day.

## 2. Assign authority per claim

There is rarely one universal source of truth for the whole project. Map important claim types:

| Claim | Typical verification source |
|---|---|
| build/test command | package/build manifest, task runner, CI configuration, successful dry run |
| API/schema | source schema, generated spec, migration, target service |
| supported version | release manifest, compatibility matrix, maintained branches |
| ownership/approval | CODEOWNERS, team configuration, policy enforced by the host |
| runtime behavior | test or target-environment observation at a named revision |
| architectural decision | accepted ADR plus current implementation constraints |
| agent behavior | installed revision plus loaded/executed/target-observed evidence |

Documentation may describe desired state while code shows current state. Preserve that distinction.
When two active sources conflict, label the conflict and ask the responsible owner only if local
evidence cannot resolve which authority applies.

## 3. Detect harmful staleness

Prioritize documents that can change an agent's action:

- commands reference missing scripts, renamed packages, or unsupported flags;
- paths, module names, owners, environments, or versions no longer exist;
- active examples violate current security, data, testing, or output rules;
- README/instructions link to superseded plans or archived Skills as current guidance;
- several files define the same rule with different wording or exceptions;
- generated files were edited manually or no longer match their generator/source revision;
- completed plans and incident notes still use imperative language without historical status;
- an archive is included in agent indexes, Skill references, retrieval roots, or default searches;
- a document claims a deployment, installation, runtime load, or production result without evidence.

Use dates, Git history, broken links, and text similarity as discovery signals only. Confirm
staleness by checking the underlying claim and its authority.

## 4. Choose one disposition

| Condition | Action |
|---|---|
| Correct and authoritative | Keep active; repair metadata or links only if useful |
| Mostly correct with bounded drift | Update in place and verify affected claims |
| Duplicates a canonical source | Merge unique content, redirect inbound links, then retire |
| Needed only for history/audit | Archive with an explicit non-current banner |
| Generated from another source | Regenerate through the owning workflow; do not hand-edit |
| Unsafe, false, secret-bearing, or misleading with no retention need | Remove with authorization and a recoverable history/backup path |
| Authority cannot be established | Quarantine from active AI paths and mark `unknown` pending owner decision |

An archive banner should be unmistakable before any old instructions:

```markdown
> Status: archived; not current project guidance.
> Archived: YYYY-MM-DD. Reason: ...
> Current source: path/to/current-document.md
> Restore/history: commit, tag, or archive path
```

Do not leave a complete obsolete command immediately below a warning if an agent could still copy
it. Remove it from active docs; retain it only where historical evidence is actually required.

## 5. Control the AI-visible document graph

Trace from the files an agent loads first:

1. Root and directory-scoped instruction files.
2. README and documentation indexes linked from them.
3. Skill entrypoints and the references they route to.
4. Retrieval/search roots, generated indexes, memory, examples, and templates.
5. Archives or legacy paths reachable from any active node.

The desired graph has a small active core, explicit progressive disclosure, and one-way historical
links: archives may link to current sources, but current operational guidance should link to an
archive only when history is explicitly requested. If tooling supports ignore/exclusion rules for
retrieval or indexing, propose them as a separate authorized configuration change; a directory name
such as `archive` does not itself prove exclusion.

## 6. Verify a documentation change

Run checks proportional to impact:

- relative and external link resolution;
- referenced path, command, flag, environment, owner, and version existence;
- read-only/dry-run command smoke where safe and meaningful;
- active-to-archived link scan;
- duplicate/conflicting rule scan across active instructions and Skill references;
- generated-document provenance or regeneration check;
- one positive, negative, and collision trial when the change affects Skill/agent routing;
- review of the diff for accidental deletion of unique evidence or safety constraints.

Report exactly what was validated. A link check does not validate a command; a command smoke does
not prove production behavior; a moved archive is not excluded from AI retrieval until the host's
actual discovery behavior is observed.

## 7. Report

```markdown
## Documentation governance
- Scope / active revision:
- AI entrypoints and exposure graph:
### Canonical active sources
- Claim -> source -> owner -> revalidation trigger
### Stale, conflicting, or unowned documents
- Path -> evidence -> risk to agent decisions
### Disposition
- Update / merge / archive / quarantine / remove, with restore path
### Verification
- Links, commands, references, routing trials, and highest evidence layer
### Unknowns
- Unresolved authority, owner, runtime discovery, or target-environment gaps
```
