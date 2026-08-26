# Retired Skill Source

These 24 fine-grained Skill directories were removed from the default `skills/` discovery root on
2026-08-26. Their source, references, scripts, agent metadata, and SkillOpt fixtures are preserved
for targeted recovery and historical comparison.

They are not an active compatibility layer: do not add this directory as a Skill root unless a
specific legacy workflow is being restored. To recover one entry, copy or move only its named
directory back under `skills/`, update the README/install list and three trigger cases, then run
`./scripts/validate-skills.sh`.

Consolidation rationale and usage evidence: [skill-system-optimization-20260826.md](../../docs/skill-system-optimization-20260826.md).
