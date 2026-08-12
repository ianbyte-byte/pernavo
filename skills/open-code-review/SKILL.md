---
name: open-code-review
description: >
  Run Alibaba's Open Code Review agent through the `ocr` CLI for focused,
  line-level review of Git changes or full-file scans. Use when the user
  explicitly asks for Open Code Review, OCR, the `ocr` command, or the
  Open Code Review integration; support workspace, commit, branch, preview,
  JSON/agent output, custom rules, and requested fixes. Do not trigger for a
  generic code-review request unless the user selects this tool; use
  `review-mr` for the repository's normal multi-reviewer diff report.
---

# Open Code Review

Use the [Open Code Review](https://github.com/alibaba/open-code-review) CLI as
a focused review pipeline around an LLM. It separates file and rule selection
from model reasoning and returns structured, line-oriented comments. This skill
owns OCR invocation and interpretation; it does not replace independent
behavior verification, deployment evidence, or the repository's `review-mr`
report.

## Preconditions

Before a real review, inspect the target repository and run:

```bash
git --version
node --version
command -v ocr || true
ocr version
ocr llm test
```

Open Code Review documents Git 2.41+ and Node.js 18+ as prerequisites. If the
CLI is absent and the user asked to run OCR, install it as the standard setup
step:

```bash
npm install -g @alibaba-group/open-code-review
```

Never invent, print, commit, or hardcode an API key. If `ocr llm test` fails,
stop before reviewing and ask the user to configure a provider:

```bash
ocr config provider       # interactive provider, key, and model setup
ocr config model          # change the selected model later
ocr llm test              # verify the endpoint
```

For non-interactive setup, use `ocr config set` or the documented `OCR_LLM_*`
environment variables without exposing their values. Delegation mode can use
the host agent's model and does not require a separate OCR endpoint; do not
silently switch modes unless requested.

## Select the review mode

Identify the intended scope and, when useful, derive a short requirement or
business-context string for `--background`. Never include credentials or
unrelated private data in it.

| User intent | OCR invocation |
| --- | --- |
| Current staged, unstaged, and untracked changes | `ocr review --audience agent --background "<context>"` |
| A branch range | `ocr review --audience agent --background "<context>" --from <base> --to <head>` |
| One commit | `ocr review --audience agent --background "<context>" --commit <sha>` |
| Preview scope without an LLM call | `ocr review --preview` (add scope flags when needed) |
| Whole files or an unfamiliar/non-Git tree | `ocr scan --audience agent [--path <path>]` |

`--from`/`--to`, `--commit`, and workspace mode are mutually exclusive. Use
`--repo <path>` when the current directory is not the repository root. For
large or rate-limited reviews, tune concurrency, timeout, or OCR token/tool
limits only when there is a concrete reason.

Always use `--audience agent` for machine-facing output. For automation or
subsequent processing, additionally use JSON and preserve the complete output:

```bash
ocr review --format json --audience agent --background "<context>" > /tmp/ocr-review.json
```

The JSON result distinguishes `success`, `completed_with_warnings`,
`completed_with_errors`, and `skipped`; it includes reviewed-file summaries,
comments, warnings, and sometimes a resumable `session_id`. Exit code 0 means
the run completed, including zero comments; exit code 1 means a fatal error.
Preserve and report warnings separately from findings.

For interrupted branch or commit reviews, inspect sessions and resume only
with the exact same target:

```bash
ocr session list
ocr review --from <base> --to <head> --resume <session-id>
ocr review --commit <sha> --resume <session-id>
```

Workspace reviews cannot be resumed, and `--preview` cannot be combined with
`--resume`.

## Interpret and report results

Read the complete OCR output and map each comment to its `path` and line range.
If both line numbers are zero, inspect the referenced file and locate the code
before reporting or fixing it. Classify comments using repository evidence:

- **High**: obvious correctness bug, security issue, data-loss risk, broken
  contract, or a well-founded defect with a precise repair.
- **Medium**: credible but context-dependent correctness, performance,
  maintainability, or test concern.
- **Low**: weakly supported suggestion, nit, or likely false positive; do not
  inflate it into a defect.

Report files reviewed, fatal errors, and warnings, then group actionable
findings by priority:

```markdown
## Code Review Results

**Files reviewed**: N
**Issues found**: X high priority / Y medium priority

### High Priority

- **`path/to/file:line`** — concise defect and impact
  > Recommendation: smallest safe correction

### Medium Priority

- **`path/to/file:line`** — concern and evidence
  > Recommendation: follow-up or test
```

If there are no actionable findings, say so with the file count. Do not claim
OCR proves the code is correct, deployed, or accepted in a live environment.
For a conventional repository MR review, route to
[review-mr](../review-mr/SKILL.md); for completed-change behavior evidence,
route to [verify-change-evidence](../verify-change-evidence/SKILL.md).

## Fixing findings

Review alone does not authorize code changes. Apply fixes only when the user
explicitly asks to review and fix. Then:

1. Fix high-confidence High and Medium findings only; preserve unrelated dirty
   work and avoid speculative refactors.
2. Re-read changed code and inspect the final diff.
3. Run focused author checks for the changed surface.
4. Report fixes, remaining uncertainty, and checks actually run.

Do not commit, push, deploy, or claim independent verification unless separately
requested and evidenced.

## Rules and safeguards

OCR resolves custom rules in this order: `--rule <path>`,
`<repo>/.opencodereview/rule.json`, `~/.opencodereview/rule.json`, then built-in
rules. Use `ocr rules check <path>` to inspect the selected rule. Do not modify
rules merely to make a review pass. Bare workspace review includes untracked
files; use preview or selective staging when scope must be explicit. Large
diffs can hit token limits, and OCR comments remain model output requiring
human judgment.

Official references:

- [Quickstart](https://open-codereview.ai/docs/quickstart)
- [CLI reference](https://open-codereview.ai/docs/cli-reference)
- [Agent Skill integration](https://open-codereview.ai/docs/agent-skill)
- [NPM package](https://www.npmjs.com/package/@alibaba-group/open-code-review)
