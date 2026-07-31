# Code review: Phase 1 agentctl

## Scope and evidence inspected

- Goal/contract supplied for the Phase 1 read-only Python 3.9 CLI.
- Uncommitted files: `README.md`, `harness/**`, `scripts/agentctl*.py`, and `tests/test_agentctl_cli.py`.
- `git status --short`, tracked diff, full contents of untracked implementation/test/harness files, and existing validation-script convention.
- Independently ran `python3 -m unittest tests/test_agentctl_cli.py` (12 tests passed), `./scripts/validate-skills.sh` (12 skills / 36 trigger cases passed), `python3 -m py_compile` on all four modules, and `git diff --check` (clean).

The repository has no ulw-loop plan (`omo ulw-loop status --json` returned `ULW_LOOP_PLAN_MISSING`), so this report uses the required fallback path.

## Skill-perspective check

Ran the available `omo:remove-ai-slops` and `omo:programming` skills, including the Python reference before judging test relevance and maintainability.

- `remove-ai-slops`: **violated** by the source-AST “read-only” test below. It is a brittle, implementation-shaped test that creates false confidence instead of proving the user-visible security property. No deletion-only or prose/prompt tests were found. Production modules are all below the 250 pure-LOC threshold (61, 33, 148, and 108 respectively).
- `programming`: no additional blocking structural violation identified. The code is stdlib-only as required, has explicit frozen models, avoids `Any`/`object` annotations, and uses Python-3.9-compatible syntax. The test weakness conflicts with its requirement for behavior-focused tests rather than implementation mirrors.

## Findings

### CRITICAL

None.

### HIGH

1. **Canonical JSON is accepted with duplicate object members and non-finite numeric tokens, so a purportedly canonical security-sensitive record can be silently reinterpreted.** [agentctl_data.py:49](/Users/chung/Developer/Code/loongclaude/scripts/agentctl_data.py:49)–[59](/Users/chung/Developer/Code/loongclaude/scripts/agentctl_data.py:59) and [agentctl_data.py:165](/Users/chung/Developer/Code/loongclaude/scripts/agentctl_data.py:165)–[168](/Users/chung/Developer/Code/loongclaude/scripts/agentctl_data.py:168) call Python’s permissive `json.loads` without an `object_pairs_hook` or `parse_constant` rejection. Duplicate JSON keys are collapsed last-wins rather than being fatal; e.g., a JSONL object with both `"sensitivity":"sensitive"` and a later `"sensitivity":"normal"` is accepted and may expose its `text` in a default search. `NaN`, `Infinity`, and `-Infinity` are also accepted despite not being JSON, and `NaN` route predicates cannot exact-match deterministically. This violates the canonical-data and default-sensitive-exclusion boundary. The tests never exercise either input class. Require strict duplicate-key and non-finite-token rejection for config, event, and each JSONL record, with regression coverage.

### MEDIUM

1. **The test that claims to prove the implementation “cannot execute processes, sockets, or write files” does not establish that guarantee.** [test_agentctl_cli.py:236](/Users/chung/Developer/Code/loongclaude/tests/test_agentctl_cli.py:236)–[259](/Users/chung/Developer/Code/loongclaude/tests/test_agentctl_cli.py:259) only bans two imports and a small, spellings-based set of attribute calls. It misses standard-library execution paths such as `os.system`/`os.exec*`, `ctypes`, and network clients; it also misses writes via `Path.touch`, `Path.chmod`, `os.open`, keyword `mode="w"`, or indirect aliases. Passing it says little about the advertised no-hook/no-network/no-write property and will require frequent changes for harmless refactors. Replace or narrow it to observable CLI/data behavior plus a deliberately complete, maintainable policy check if static enforcement is a release requirement.

2. **Deep but syntactically valid malformed JSON can escape the documented exit-1 envelope.** [agentctl_data.py:56](/Users/chung/Developer/Code/loongclaude/scripts/agentctl_data.py:56)–[59](/Users/chung/Developer/Code/loongclaude/scripts/agentctl_data.py:59) and [agentctl_data.py:165](/Users/chung/Developer/Code/loongclaude/scripts/agentctl_data.py:165)–[168](/Users/chung/Developer/Code/loongclaude/scripts/agentctl_data.py:165) only translate `JSONDecodeError`. CPython can raise `RecursionError` while decoding sufficiently nested JSON (including a sub-64KiB JSONL line); `main` catches only `DataError` at [agentctl.py:69](/Users/chung/Developer/Code/loongclaude/scripts/agentctl.py:69)–[72](/Users/chung/Developer/Code/loongclaude/scripts/agentctl.py:72). That produces a traceback/exit 1 by accident rather than the stable JSON data-error output the contract promises. Convert decoder recursion failures (and other expected boundary input exceptions) to `DataError`, then add a process-level regression test for the stable envelope.

### LOW

None.

## Residual risk after fixes

- Physical-path validation resolves the path before later opening it. On an adversarial concurrently mutable filesystem, a symlink can be swapped between those operations (TOCTOU). This is not counted as a blocker for a local Phase 1 inspector, but a future stronger confidentiality boundary should use descriptor-based/no-follow opening where supported.
- The only automated CLI tests invoke `agentctl.main` in-process; the independently observed real-process smoke tests are not preserved as reproducible test evidence in the repository.

## Decision

- `codeQualityStatus`: **BLOCK**
- `recommendation`: **REQUEST_CHANGES**
- `blockers`:
  1. Reject duplicate keys and non-standard numeric constants at every canonical JSON boundary, with regressions that cover default sensitive filtering and routing semantics.
  2. Ensure deeply nested malformed JSON produces the documented JSON error envelope and stable exit code rather than an uncaught exception.

---

## Re-review after fixes (current verdict; supersedes findings above)

### Evidence re-inspected

- Full current contents of `scripts/agentctl_json.py`, `scripts/agentctl_data.py`, `scripts/agentctl.py`, both test modules, README, and untracked harness files; `git status --short` and `git diff --check`.
- Independently ran `python3 -m unittest discover -s tests -p 'test_agentctl*.py'`: **15 tests passed**.
- Independently ran `doctor --config /dev/null --json`: JSON envelope `{valid:false,error.code:"invalid_json"}`, exit **1**; and the example `doctor` command: exit **0**.
- Ran `py_compile` for the implementation modules successfully. A direct two-file unittest invocation is import-path-sensitive because `test_agentctl_strict_json.py` imports its shared base from the sibling test module; normal discovery is green.

### Prior blockers

1. **Resolved.** [agentctl_json.py:36](/Users/chung/Developer/Code/loongclaude/scripts/agentctl_json.py:36)–[52](/Users/chung/Developer/Code/loongclaude/scripts/agentctl_json.py:52) installs a duplicate-key object hook and rejects constants and overflowed floats. [test_agentctl_strict_json.py:12](/Users/chung/Developer/Code/loongclaude/tests/test_agentctl_strict_json.py:12)–[55](/Users/chung/Developer/Code/loongclaude/tests/test_agentctl_strict_json.py:55) exercises config, event, and JSONL boundaries, including the sensitive-record case.
2. **Resolved.** Decoder recursion is translated to `DataError` at [agentctl_json.py:49](/Users/chung/Developer/Code/loongclaude/scripts/agentctl_json.py:49)–[50](/Users/chung/Developer/Code/loongclaude/scripts/agentctl_json.py:50); the real-process test asserts exit 1, JSON-only stdout, and no stderr at [test_agentctl_strict_json.py:57](/Users/chung/Developer/Code/loongclaude/tests/test_agentctl_strict_json.py:57)–[75](/Users/chung/Developer/Code/loongclaude/tests/test_agentctl_strict_json.py:75).
3. **Resolved.** The brittle AST policy test has been replaced with an observable no-mutation test over config, event, and memory inputs at [test_agentctl_cli.py:240](/Users/chung/Developer/Code/loongclaude/tests/test_agentctl_cli.py:240)–[253](/Users/chung/Developer/Code/loongclaude/tests/test_agentctl_cli.py:253). This complies with the remove-ai-slops and programming test-relevance perspectives; no deletion-only, prompt/prose, tautological, or implementation-mirroring test remains.
4. **Resolved.** File opening and path-resolution expected errors are translated to `DataError` at [agentctl_data.py:49](/Users/chung/Developer/Code/loongclaude/scripts/agentctl_data.py:49)–[56](/Users/chung/Developer/Code/loongclaude/scripts/agentctl_data.py:56) and [agentctl_data.py:68](/Users/chung/Developer/Code/loongclaude/scripts/agentctl_data.py:68)–[93](/Users/chung/Developer/Code/loongclaude/scripts/agentctl_data.py:93). The `/dev/null` process check confirmed the envelope.

### Current findings

#### CRITICAL

None.

#### HIGH

None.

#### MEDIUM

None.

#### LOW

None.

### Non-blocking residual risks

- The resolve-then-open physical-path check has a conventional symlink TOCTOU window on a concurrently attacker-controlled filesystem; descriptor/no-follow traversal would be needed for a stronger future confidentiality boundary.
- `tests/test_agentctl_strict_json.py` relies on unittest discovery (or `tests` on `sys.path`) because it imports a sibling test module. This does not affect the documented discovery suite, but makes arbitrary direct-file invocation less convenient.

### Re-review decision

- `codeQualityStatus`: **CLEAR**
- `recommendation`: **APPROVE**
- `blockers`: none.
