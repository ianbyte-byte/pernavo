# Pernavo release code review

## Scope and verdict

- Goal reviewed: rebrand the repository to Pernavo, publish 14 responsibility-split Skills, a read-only harness, and the AI installation guide; the public repository and raw guide must be usable.
- Reviewed scope: README.md, AI_INSTALL.md, scripts/validate-skills.sh, docs/reference/*.md, modified/new Skill content, tests/skill-trigger-corpus.tsv, harness/**, scripts/agentctl*.py, and tests/test_agentctl*.py. `.omo/**`, `output/**`, and historic audit docs were excluded except for this required review artifact.
- **codeQualityStatus: BLOCK**
- **recommendation: REQUEST_CHANGES**

## Evidence independently inspected

- `git diff --check` passed.
- `./scripts/validate-skills.sh` passed: 14 Skill frontmatters, links, README entries, trigger triplets, and Skills CLI listing; corpus size 42.
- `python3 -m unittest discover -s tests -p 'test_agentctl*.py' -v` passed: 15 tests.
- `python3 -m compileall -q scripts/agentctl*.py` passed. Ruff and basedpyright are not installed, so no lint/type-check result is available.
- Verified installed `skills` CLI 1.5.21 help against the install-guide commands. The documented `add`, `ls`, `update`, and targeted `remove` syntaxes are supported.
- Live release check on 2026-07-31: `https://github.com/tuloong/pernavo` returned HTTP 404 and the declared raw `AI_INSTALL.md` URL returned HTTP 404 (14-byte `404: Not Found`). The configured `origin` remains `https://github.com/tuloong/loongclaude.git`.

## Findings

### CRITICAL

None.

### HIGH

1. **The advertised canonical repository and AI-install entrypoint do not exist yet, so the release goal is not met.** [README.md:5](/Users/chung/Developer/Code/loongclaude/README.md:5), [README.md:18](/Users/chung/Developer/Code/loongclaude/README.md:18), [AI_INSTALL.md:5](/Users/chung/Developer/Code/loongclaude/AI_INSTALL.md:5), and [AI_INSTALL.md:8](/Users/chung/Developer/Code/loongclaude/AI_INSTALL.md:8) direct users and agents to `tuloong/pernavo`; both live URLs returned 404. `origin` still names `tuloong/loongclaude.git`. The guide correctly tells an agent to stop on this condition, but that makes the advertised installation path unusable. Create/rename and publish the target repository, push this exact content to `main`, then independently fetch the raw file and list the remote package before approval.

### MEDIUM

1. **A local absolute path remains in a publicly scoped reference document.** [docs/reference/ai-assisted-code-reading-and-verification.md:3](/Users/chung/Developer/Code/loongclaude/docs/reference/ai-assisted-code-reading-and-verification.md:3) embeds `/Users/chung/Downloads/`. It is outside this diff, but inside the explicit `docs/reference/*.md` release-review scope. It is not a credential, yet it leaks workstation/user layout and is not portable. Remove or replace it with a repository-relative/redacted provenance note before treating the rebranded repository as clean public release material.

### LOW

1. **Legacy validator compatibility is silent.** [scripts/validate-skills.sh:22](/Users/chung/Developer/Code/loongclaude/scripts/validate-skills.sh:22)-[25](/Users/chung/Developer/Code/loongclaude/scripts/validate-skills.sh:25) accepts `LOONGCLAUDE_SKILL_VALIDATOR` without reporting that a deprecated name supplied the validator. This is an acceptable migration fallback, and no old repository URL is used outside documented migration handling, but a deprecation notice would make source provenance clearer.

## Skill-perspective check

- **Ran:** `omo:programming` (including its Python rules) and `omo:remove-ai-slops` before judging harness/test maintainability.
- **Programming perspective:** no blocker found in the read-only harness. It has typed public functions, strict JSON parsing at the input boundary, explicit static/runtime limits, no network/process/hook invocation, and behavior-focused tests. The repository has no available Ruff/basedpyright executable, so that part remains unverified.
- **Remove-AI-slops perspective:** no deletion-only or tautological test was found. The trigger corpus is checked only for structural triplets and known Skill tokens; it is not represented as runtime-trigger proof, and the guide expressly requires observable host loading events. The harness adds only functionality needed for its stated JSON/JSONL inspection boundary; no needless parsing/normalization or unneeded abstraction was identified.
- Therefore, the diff does not violate either skill perspective in a way that adds a finding.

## Responsibility, safety, and scope assessment

- The declared 14 names match README, AI_INSTALL, filesystem discovery, validator output, and the 42-row (positive/negative/collision) corpus.
- The newly split lifecycle Skills have compatible explicit boundaries: controller chooses risk path; discovery investigates; planner plans; production skill implements; verifier observes behavior; reviewer reports diff findings. The broader engineering-system skill routes rather than claiming those leaf responsibilities.
- The install guide correctly requires explicit target/scope authorization, stops on conflict, uses a current-user Codex default, blocks broad `--all`, defines snapshot-based rollback, and separates installed/loaded/executed proof.
- Harness documentation and code agree that Phase 1 is read-only and cannot establish hooks, authentication, model, tool, or runtime availability. It constrains memory to the physical config directory and defaults sensitive records out of search; `--include-sensitive` is an explicit local opt-in.
- No credential-like secret was found in the reviewed changed/new surfaces. The only local absolute-path finding is above.

## Blockers before approval

1. Make `https://github.com/tuloong/pernavo` and `https://raw.githubusercontent.com/tuloong/pernavo/refs/heads/main/AI_INSTALL.md` return the intended published repository and guide; verify their contents after push/rename.
2. Resolve or explicitly accept the local workstation path in `docs/reference/ai-assisted-code-reading-and-verification.md` for this public release.
