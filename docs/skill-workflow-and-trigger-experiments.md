# End-to-End Skill Workflow and Trigger Experiments

Use this guide to evaluate a Skill without confusing repository quality, installation, invocation,
and observed target behavior. It applies to an abstract change request and does not authorize an
external write, deployment, or production-data operation.

## Separate the evidence layers

| Layer | Question | Minimum evidence | Does not establish |
|-------|----------|------------------|-------------------|
| Static | Is the source well-formed and linked? | Validator, link check, corpus structure check | Installation or runtime use |
| Installed | Is the intended revision available to the test runtime? | Recorded target location and immutable revision identifier | That the runtime read it |
| Loaded | Did the runtime successfully read the target `SKILL.md`? | A targetable path plus successful reader command or matching frontmatter output | That the instructions were followed |
| Executed | Did the requested trial reach a completed terminal observation? | `turn.completed` or an equivalent documented terminal event | Correct routing or target behavior |
| Target-observed | Did the expected owner load without a prohibited owner? | Loaded-owner comparison against the case contract | Delivery, deployment, or production behavior |

Never turn one layer into another. A static check is not installation proof; a loaded file is not
execution proof; a completed turn is not a routing pass; a routing pass is not evidence of a
deployed target.

## Plan a workflow experiment

1. Define the requested outcome, allowed actions, and prohibited external effects. Keep read-only
   diagnosis separate from authorization to repair.
2. Select a fast, default, or deep lifecycle based on consequence, reversibility, active context,
   data/state ownership, recovery behavior, and target-environment uncertainty.
3. Write an abstract corpus with exactly one positive, negative, and collision case for each owner.
   A collision case may allow composition, but must name the expected and prohibited owners.
4. Run every trial in a fresh, recorded context. Keep input, installed revision, terminal event,
   command evidence, and result file together.
5. Evaluate static, installed, loaded, executed, and target-observed layers separately. Report the
   highest layer actually observed.
6. For implementation trials, trace active context and data/state lifecycle before editing; verify
   single-record and batch success, failure, and recovery behavior where relevant. Preserve the
   gap between local checks, target-environment observation, and deployment.

## Performance-specific trials

For hidden performance-risk work, keep review and measurement owners separate:

| Request | Owner | Minimum evidence |
|---|---|---|
| Find static amplification signals or establish runtime proof | `performance-work` | file/line, workload, target, revision, p50/p95/p99, resource signals, and cause artifact |
| Inspect SQL/ORM query shape or execute a test query | `data-work` | generated SQL, request query count, plan/runtime stats where authorized |
| Inspect browser loading, interaction, or layout stability | `performance-work` | field/lab distinction, LCP/INP/CLS p75, long-task/resource evidence |
| Validate a microbenchmark | `performance-work` | representative input, setup boundary, warmup, measurement, fork/iteration, variance and environment |

The performance evidence helper can create a secret-safe local inventory manifest:

```text
python3 skills/performance-work/scripts/performance_evidence.py inventory --target . --json
python3 skills/performance-work/scripts/performance_evidence.py validate <manifest.json>
```

This helper does not execute a workload or profiler. A trial that only reads source or a benchmark
configuration is `unverified`; it cannot be upgraded to `confirmed` without comparable runtime
observations. The source-backed rules and public URLs are collected in
[Hidden Performance Public Research](reference/hidden-performance-public-research.md).

## Summarize runtime observations

Use `scripts/summarize-skill-trigger-results.py` with a corpus, a directory of JSONL trial results,
the project Skill root, and an output path. It treats one result file as an **issued** trial.

```text
python3 scripts/summarize-skill-trigger-results.py \
  --corpus tests/skill-trigger-corpus.tsv \
  --results <results-directory> \
  --project-skill-root <project-skill-root> \
  --output <summary-path>
```

The summarizer recognizes a loaded Skill only when one reader command names a targetable `SKILL.md`
path and has successful read evidence: either that reader exits successfully or its output contains
the matching `name:` frontmatter. Any command containing a shell separator or multiple command
segments is rejected as aggregate evidence, even when its combined output has matching frontmatter
or its final exit status is zero. Path text, directory listings, and a successful command that read
another file are not load evidence.

Each issued trial is classified as follows:

| Observation | Meaning | Pass eligibility |
|-------------|---------|------------------|
| `completed` | A completed terminal event was observed | Eligible only after expected/prohibited owner checks |
| `timeout` | A timeout terminal event, timeout error, or exit status 124 was observed | Not eligible |
| `unobserved` | No completed or timeout observation is available | Not eligible |

`completed` and `execution_observed` describe trial completion only. `target_observed` means all
expected owners were loaded and no prohibited owner was loaded; an empty expected-owner set is a
negative control. `pass` additionally requires completion. Therefore a `turn.completed` event alone
never passes a case.

## Handle failures without upgrading evidence

- A failed check is evidence of a failed or incomplete trial, not a reason to relabel it as a
  timeout or success.
- A timeout is distinct from a missing observation. Record its available partial command evidence,
  but do not score it as completed.
- An unavailable installation or inaccessible target is an installed-layer gap. Do not infer a
  load from an instruction, a model statement, or a path mentioned in output.
- A local or isolated result must name the unobserved deployment, live runtime, and external-side
  effect boundaries. Do not repair, release, or operate those boundaries without separate authority.

## Report

Report the corpus revision, installed revision and location, issued count, counts by observation,
loaded expected/prohibited owners, completed-only pass rate, timeout count, unobserved count, and
the highest evidence layer per conclusion. Keep raw trial records available for audit.
