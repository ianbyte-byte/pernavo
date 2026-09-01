# Shared agent guidance

This file contains reusable guidance distilled from repository learning notes.

## Avoid unrequested compatibility

Do not add backward-compatibility layers, legacy fallbacks, dual-write, field aliases, or silent
mitigations unless a real caller, shipped contract, or explicit user request requires them. Do not
preserve obsolete paths in code that has never been deployed. Removing an existing shipped contract
requires evidence and a human decision; this rule does not authorize that.

This preference applies to greenfield or explicitly unconsumed code. It does not authorize deleting
an existing supported API, message, library, data, or configuration contract. Treat unconfirmed
dispatch, reflection, and configuration entry points as unconfirmed until evidence resolves them.
