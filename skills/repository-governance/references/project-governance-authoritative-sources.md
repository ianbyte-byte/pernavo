# Project governance: authoritative sources

Research snapshot: 2026-09-01. These sources are decision support for the Skill; they are not a
claim that this repository complies with any standard.

## User-supplied experience report

- Tencent Cloud Developer Community, [删掉80%的Skill，Agent反而更听话了](https://developer.cloud.tencent.com/article/2712930).
  This is the motivating secondary source: it recommends layered instructions, deduplication,
  positive wording, structured formats, external references, consistency checks, and limits on
  automated append-only repair. Treat its numeric adherence claims and causal explanations as
  unverified until reproduced against the project's models, corpus, and runtime.

## Instruction and context design

- Liu et al., *Lost in the Middle: How Language Models Use Long Contexts* (TACL 2023),
  [arXiv:2307.03172](https://arxiv.org/abs/2307.03172). The authors report that relevant
  information is often used best at the beginning or end of long contexts and performance can
  degrade when it is in the middle. Governance implication: keep entrypoint rules short, ordered,
  and test position/length sensitivity instead of assuming repetition improves compliance.

## Secure development and supply chain

- NIST, *SP 800-218 Secure Software Development Framework (SSDF) Version 1.1*,
  [publication page](https://csrc.nist.gov/pubs/sp/800/218/final). SSDF organizes practices for
  preparing the organization, protecting software, producing well-secured software, and responding
  to vulnerabilities. Governance implication: name owners, protect source and credentials, retain
  evidence, and make vulnerability/rollback handling explicit.
- SLSA, *Specification v1.2*, [specification](https://slsa.dev/spec/v1.2/). SLSA defines
  incrementally stronger supply-chain guarantees and provenance/attestation concepts across source,
  build, and verification tracks. Governance implication: record immutable revisions and provenance
  for generated or installed Skills and other artifacts; do not treat a URL or filename as proof.
- OpenSSF, [Scorecard](https://scorecard.dev/). Scorecard provides automated checks for repository
  supply-chain security practices and publishes its checks and methodology. Governance implication:
  use automated checks as signals in a baseline, not as a substitute for owner judgment or runtime
  evidence.

## Ownership, review, and change control

- GitHub Docs, [About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners).
  CODEOWNERS maps paths to responsible people/teams and can be coupled with required review; the
  file must be valid, available on the base branch, and owned itself for stronger protection.
  Governance implication: make ownership discoverable and protect the ownership policy.
- GitHub Docs, [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).
  Branch protection can require reviews, status checks, and other merge conditions. Governance
  implication: distinguish a local check from an enforced merge/release gate and record which one
  actually ran.

## Configuration and operational risk

- The Twelve-Factor App, [Config](https://12factor.net/config). Deploy-varying configuration,
  including credentials and resource handles, should be separated from code and environment-specific
  values should not be committed. Governance implication: audit config ownership and secret boundaries;
  never place credentials in Skills, examples, reports, or repository history.
- Google SRE, [Embracing risk](https://sre.google/sre-book/embracing-risk/) and
  [Error-budget policy](https://sre.google/workbook/error-budget-policy/). SRE frames reliability
  as an explicit risk tradeoff and uses error budgets to guide change decisions. Governance
  implication: define a measurable signal and a human/release gate for customer-impacting changes;
  do not infer production safety from static evidence.

## Applying the sources

Use these sources to justify a control, then tailor it to project risk:

1. State the local threat or failure mode.
2. Choose the smallest applicable control and its owner.
3. Define the observable signal, revision, and rollback path.
4. Run the cheapest evidence layer that can answer the question; label higher layers unverified.
5. Review or retire the control when it creates duplication, contradiction, or no useful signal.
