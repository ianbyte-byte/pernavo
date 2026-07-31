# Agentctl Phase 1 format

`agentctl` reads versioned JSON configuration and canonical JSONL memory. It never writes a file, invokes a hook, starts a process, opens a socket, or calls a tool.

The config accepts exactly `schema_version`, `memory`, and `routes`. Version 1 `memory` accepts a confined config-relative `path` and declared `scopes`. A route has `id`, bounded integer `priority`, scalar exact-match `when` fields, and `requires` capability names. Equal-priority matches are reported as conflicts.

Each newline-terminated JSONL record accepts `id`, `text`, `scope`, `sensitivity`, and optional `supersedes`. The only sensitivities are `normal` and `sensitive`; sensitive records are excluded unless `--include-sensitive` is given. A record named by another record's `supersedes` field is obsolete and excluded from default search results. Malformed records, duplicate ids, unknown supersession targets, cycles, blank lines, overlong lines, and a missing final newline are fatal.

`MEMORY.md` is not an input or projection target in Phase 1. It may become a human-readable projection in a later phase, but JSONL remains canonical here.
