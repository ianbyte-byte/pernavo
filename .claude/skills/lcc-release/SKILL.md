---
name: lcc-release
description: Release prep workflow (notes, checklist, version bump guidance) using lcc-release-manager.
disable-model-invocation: true
---

Prepare a release without publishing.

## Steps

1) Draft release notes (lcc-release-manager)
- Delegate to `lcc-release-manager`.
- Require: version bump suggestion, release notes, and a checklist.

2) Update docs/changelog if needed (lcc-docs-writer)
- If documentation or changelog needs changes, delegate to `lcc-docs-writer`.

3) Final review (lcc-reviewer)
- Delegate to `lcc-reviewer` to ensure release notes and docs match the actual changes.
