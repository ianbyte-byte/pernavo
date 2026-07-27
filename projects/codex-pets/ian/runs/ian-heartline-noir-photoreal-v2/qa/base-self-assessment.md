# Ian · Heartline Noir v2 — canonical base self-assessment

## Independent selection update

- Three isolated r2 reviewers selected the earlier r2 alternate by a `2 to 1` vote and passed it by `2 PASS to 1 REVISE`.
- The selected canonical is now `references/canonical-base.png`, copied from `sources/canonical-base-r2-initial-fail.png`; the historical filename is not the current decision.
- Selected canonical SHA-256: `89e35769b9d578937acd6232d17352624e322144b0bc391f078678836d119120` (`851 x 1848`).
- Selected raw copy: `sources/base-candidate-r2-selected.png`, SHA-256 `51c5a0d7fbf632dfc63b1727f752e7873595c9095c9e49be08953a805c0427d4`.
- The later copper-red candidate was rejected by candidate selection and retained as `sources/canonical-base-r2-current-rejected.png` and `sources/base-candidate-r2-current-rejected.png`.
- The authoritative r2 decision is `qa/canonical-base-identity-qa-r2.json`; this earlier author self-assessment is retained as generation history.

## Gate state before independent selection

- The prior independent identity gate remains unchanged and **FAIL** (`2 FAIL, 1 PASS`, low same-person confidence). See `qa/canonical-base-identity-qa.json`.
- This revision is a new whole-image imagegen candidate only. `qa_status` is intentionally `independent_gate_pending`; no PASS is asserted here and animation/YAML/install remain unauthorized.

## Revision 2 generation record

- Repair prompt: `prompts/base-identity-repair-r2.md`.
- Current raw imagegen source: `sources/base-candidate-r2-raw.png`.
- Current canonical output: `references/canonical-base.png`.
- Imagegen source path: `/Users/chung/.codex/generated_images/019f9d06-8ee1-7401-bf03-5a997caaadeb/exec-b9021b7a-994f-493e-ab5d-e32f56466288.png`.
- Raw SHA-256: `f87e8e40b1472c2316296ab0085cbafebdab9958bba498520a45921bc8937b0b`.
- Canonical SHA-256: `ee4ecfd3d5cda67c64878c7a8687c166ddbc508bdc7ab80f66bba340ea86a72a`.
- Both current files are RGB PNGs; raw/canonical dimensions are `853 × 1844` pixels.
- Rejected backups retained under `sources/`: r1 canonical/raw and the first r2 whole-image candidate (`*-initial-fail`).

## Visual checks before independent review

- **Whole-image edit:** The current candidate is a complete regenerated head-to-toe image; no face crop, paste, or Python subject synthesis was used.
- **Identity target:** The prompt gives the accepted identity master plus front/three-quarter video anchors priority and explicitly restores narrow horizontal almond eyes, low brow/eye axis, natural eye spacing, nose length/volume, nose-to-lip distance, longer lower face, broad rounded jaw/chin, Cupid's-bow/full lower lip, and viewer-left under-eye mole. Independent reviewers must decide whether these cues actually match.
- **Wardrobe and coverage:** Copper-red high braided bun, side bangs, narrow black ribbon, black short-sleeve top, full-shoulder ivory asymmetric panel, wide ivory belt, silver heart ornament, slightly longer neutral skirt, and black boots are present. The neckline and shoulders are covered; no sexualized pose or styling.
- **Human fidelity:** One centered, fully clothed human with photographic materials and natural anatomy is visible. Non-blocking review risks retained for QA include the long-legged miniature framing and whether the copper-red tone reads consistently at 192×208.
- **Chroma key:** Only green-dominant background pixels were rewritten as a non-creative key normalization. The canonical corners and keyed background are exact RGB `(0,255,0)`: `1,156,510 / 1,572,932` pixels. The raw gradient/noise source remains preserved.

## Next authorization boundary

Independent visual QA must re-evaluate same-person identity and style against the accepted master and videos. Until that gate records an explicit pass, do not generate animation rows, update the install manifest, or replace the installed pet.
