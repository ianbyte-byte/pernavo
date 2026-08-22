# IAN photoreal Codex Pets final gate review

- recommendation: APPROVE
- blockers: none
- originalIntent: Deliver three YAML-defined, fully human photoreal IAN Codex Pets; bind the supplied images and videos to repository artifacts; produce and install valid v2 atlases; preserve rejected evidence without installing it.
- desiredOutcome: Three installed `person` pets whose repository and installed atlases are byte-identical, structurally valid 8x11/1536x2288 v2 assets, with three-reviewer PASS evidence and coherent repository documentation.
- userOutcomeReview: The requested three photoreal human pets are present, documented, bound to supplied media, validated, and installed. Contact sheets show human photographic figures rather than animal, cartoon, or abstract characters. No blocking mismatch was reproduced.

## Checked artifacts and reproduced evidence

- `projects/codex-pets/ian/ian-pets.yaml`: parses successfully; `character_policy: human_photoreal_only`; exactly three pets and three `photoreal_deliveries`; every delivery path exists; canonical and atlas SHA-256 fields match bytes.
- `projects/codex-pets/ian/references/SHA256SUMS`: all 46 entries pass when checked from the `references/` directory, including source images, both videos, selected frames, YAML/docs, final atlases, QA, and Lemon rejected-round evidence.
- All three `final/spritesheet-extended.webp`: 1536x2288; SHA-256 values match YAML, README, delivery-verification, and final QA.
- All three repository `final/validation-extended.json`: `ok: true`, v2, 8 columns, 11 rows, zero errors and warnings, zero transparent-RGB residue.
- Re-ran strict v2 atlas validation against all three installed `spritesheet.webp` files using the hatch-pet validator: all pass at 1536x2288, 8x11, zero errors/warnings and zero transparent-RGB residue.
- Installed atlases compare byte-for-byte equal to repository atlases; each install directory contains only `pet.json` and `spritesheet.webp`; installed manifests use `kind: person`, `spriteVersionNumber: 2`, and `spritesheetPath: spritesheet.webp`.
- `qa/final-visual-qa.json`: Azure PASS 3/3, Heartline PASS 3/3, Lemon round 2 PASS 3/3; human-photoreal, age-appropriate, identity, anatomy, state, structure, and cardinal-direction gates pass.
- `runs/ian-identity-master-v2/qa/final-cross-pet-qa.json`: PASS and install authorized for the exact three final atlas hashes.
- Lemon round 1: `qa/final-visual-round-1-failed/consensus.json` records `REJECTED_BEFORE_INSTALL`, rejected hash `dad7a6...`; round 2 final QA records the rejected hash as not installed; installed bytes match only round 2 hash `a9abfa...`; regenerated running-right component check passes.
- README and `delivery-verification.json`: current photoreal-v2 installed state and hashes agree; no claim that the legacy cartoon or rejected Lemon atlas is currently installed.
- Contact sheets visually inspected for all three pets: fully human, photoreal presentation; no animal anatomy, cartoon rendering, or abstract-only character.
- Unrelated Karina files remain modified in the worktree, but their timestamps predate the IAN delivery edits by about 16 hours and their diffs concern a separate Karina video/reference task. No evidence ties those pre-existing changes to this delivery.

## Direct remove-ai-slops / programming review

- Scope contains generated visual assets, JSON/YAML manifests, prompts, and prose; no new production Python/Rust/TypeScript/Go module is part of the IAN delivery.
- No deletion-only, tautological, implementation-mirroring, prompt-prose assertion, or excessive test suite was introduced. Validation evidence exercises machine-consumed atlas geometry, alpha/chroma constraints, hashes, manifest fields, and installed bytes.
- No unnecessary production extraction, parsing abstraction, normalization layer, dead helper, oversized source module, broad exception handler, or speculative compatibility code was found in scope.
- The separate code-review report/manual-QA-matrix/notepad inputs were not provided as named artifacts. This does not block because the required user-visible criteria were independently reproduced from the delivery files, deterministic validators, visual contact sheets, and installed bytes.

## Notes (non-blocking)

- P2 metadata hygiene: `projects/codex-pets/ian/runs/ian-lemon-cadet-photoreal-v2/final/spritesheet-extended.json` still contains `status: pre-despill-draft`, although the same file points to the accepted final WebP and its atlas geometry is correct. The field is not installed and is not referenced as the delivery status by YAML/README, so it does not violate a stated install criterion; update it later to avoid confusing future maintainers.

## Exact evidence gaps

- No standalone executor report, code-review report, or manual QA matrix path was supplied. Equivalent acceptance evidence exists in the three final visual QA files, cross-pet QA, deterministic validation JSON, SHA256SUMS, and installed artifact checks.
