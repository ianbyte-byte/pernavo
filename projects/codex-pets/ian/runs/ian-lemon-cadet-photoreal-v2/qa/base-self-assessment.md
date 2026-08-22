# Base self-assessment

## Generation evidence

- r1 imagegen raw source (rejected): `/Users/chung/.codex/generated_images/019f9d06-bb08-7c61-aff7-8433e7d33ebd/exec-ac855a47-8090-4246-acab-7cbb2b315ef4.png`
- r2 imagegen raw source: `/Users/chung/.codex/generated_images/019f9d06-bb08-7c61-aff7-8433e7d33ebd/exec-f10ad1c1-d0d2-46b5-bff6-6ddbcf0f0a08.png` (copied to `sources/base-candidate-r2-raw.png`)
- r1 rejected raw backup: `sources/canonical-base-raw-rejected-r1.png`
- r1 rejected canonical backup: `sources/canonical-base-rejected-r1.png`
- Canonical output: `references/canonical-base.png`
- Output dimensions: `852 x 1846` pixels (`sips -g pixelWidth -g pixelHeight`)
- r2 raw SHA-256: `5c06b068a87945ab7bcd90b288848e85c8c1c6acdfc94313d6ea6e0440a2e8d4`
- r2 canonical SHA-256: `3c427fd4cb79168d9bd590269479bd8324d34447c635ae6417a67644762c9bef`

## Identity and visual checks

- r1 gate result is preserved: `qa/canonical-base-identity-qa.json` records `FAIL`, `2 FAIL / 1 PASS`, low same-person confidence, and animation unauthorized.
- For r2, the identity master was supplied first to imagegen and treated as the dominant face reference; frontal and three-quarter videos supplied supporting face geometry, while outfit references supplied copper twin-tails and Lemon Cadet clothing cues only.
- Visual self-check of r2 shows a fully human face with smaller horizontally longer almond eyes, lower eye axis, longer oval lower face, longer nose bridge/tip, Cupid's-bow upper lip, fuller lower lip and rounded jaw/chin; no doll-eye, short-face, pointed-chin or cartoon treatment was introduced. Independent gate remains pending; this is not a PASS claim.
- The generated subject is one complete centered head-to-toe human with attached ordinary twin ponytails, cream/pale-lemon sailor uniform, navy rosette with a simple embossed silver heart, cream boots, and no extra person, animal anatomy, props, text or scenery.
- The r2 raw imagegen background was not exact chroma blue. A single non-creative connected-background flood-fill normalized only connected blue background pixels to exact `(0, 0, 255)`; the untouched r2 raw image remains retained for audit.
- r2 canonical background corner samples after normalization are all `(0, 0, 255)`; exact-blue pixel count is `1,132,698` of `1,572,792` pixels. No face or outfit edits were performed during normalization.

## Residual risk

The sprite is a grounded photoreal generation rather than a biometric or pixel-identical reconstruction. At 192x208 display size, fine facial details such as the under-eye mole may be subtle. The r1 majority FAIL remains authoritative history; r2 requires the independent gate before any animation work is authorized.

## r3 full-body rebuild

- r2 canonical and raw were backed up before replacement as `sources/canonical-base-rejected-r2.png` and `sources/base-candidate-rejected-r2.png`.
- r3 raw source: `/Users/chung/.codex/generated_images/019f9d06-bb08-7c61-aff7-8433e7d33ebd/exec-60163891-bf1b-4163-9d17-e543c38b416c.png` (retained as `sources/base-candidate-r3-raw.png`).
- r3 canonical: `references/canonical-base.png`; dimensions `852 x 1846`; raw SHA-256 `a98c004e69bb203aa9a7ea24ae8ede2faa25d6b56e093ea696f6918f715beeb0`; canonical SHA-256 `4d01ef964b8a603726efee7f1780b2f5b6faa9116a99b2b073cb817eae87ae3a`.
- r3 uses the approved bust as the dominant face anchor and preserves the full-body Lemon Cadet outfit, ordinary copper-brown twin ponytails, boots and centered front pose. Visual self-check finds no animal anatomy, generic cartoon/toy treatment, extra people or props.
- The raw background was normalized only by a connected-background flood-fill to exact #0000FF; no face or outfit edits were made. Corner samples of the canonical are `(0, 0, 255)`.
- This remains a self-assessment only. `imagegen-jobs.json` is `qa_status=independent_gate_pending`; r1/r2 FAIL history and the 3/3 high-PASS bust evidence are retained, and no PASS is claimed for the full-body r3.
