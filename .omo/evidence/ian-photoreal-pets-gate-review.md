# IAN Photoreal Codex Pets Final Gate Review

- recommendation: REJECT
- originalIntent: Deliver three fully human, photoreal, age-appropriate IAN Codex Pets bound to repository artifacts, with strong recognizable visual likeness at 192x208, stable identity across 88 cells, readable states and directions, and no blocking anatomy, transparency, edge, animal, cartoon, abstract, text, or other-person defects.
- desiredOutcome: Azure Navigator, Heartline Noir, and Lemon Cadet are all independently shippable and depict the same recognizable person across their complete v2 atlases.
- userOutcomeReview: Azure Navigator and Heartline Noir meet the visible delivery gate. Lemon Cadet does not yet meet the all-cells anatomy/edge criterion because two running-right cells contain visible detached human fragments.

## Blockers

1. violatedCriterion: ANATOMY_EDGES_ALL_88
   evidencePointer: `projects/codex-pets/ian/runs/ian-lemon-cadet-photoreal-v2/final/spritesheet-extended.webp`, row 1 column 1 and row 1 column 2.
   observation: r1c1 contains a detached forearm/hand at the left edge; r1c2 contains a detached white boot/lower-leg fragment at the lower-left edge. Both are visibly separate from the main figure in their 192x208 cells.

## User-visible verdicts

- ian-azure-navigator: PASS. Photoreal human, age-appropriate, recognizable IAN-like facial geometry, stable identity and outfit, readable state families, correct opposed movement directions, coherent 16-direction loop, no blocking visible anatomy/edge defect.
- ian-heartline-noir: PASS. Photoreal human, age-appropriate, strongest identity consistency of the three, readable state families, correct opposed movement directions, coherent 16-direction loop, no blocking visible anatomy/edge defect.
- ian-lemon-cadet: REVISE. Identity/style/state/direction gates otherwise pass; repair the complete grounded running-right row or at minimum its source generation so r1c1 and r1c2 no longer contain detached body fragments, then rerun final despill, atlas validation, and final visual QA.
- crossPetSamePerson: PASS with hairstyle and costume variation; face shape, eye spacing, nose/mouth relationships, and overall age presentation remain mutually consistent.

## Checked artifact paths

- `projects/codex-pets/ian/references/video-frames/ian-video-02-t01.25.jpg`
- `projects/codex-pets/ian/runs/ian-identity-master-v2/references/identity-master.png`
- `projects/codex-pets/ian/runs/ian-azure-navigator-photoreal-v2/references/canonical-base.png`
- `projects/codex-pets/ian/runs/ian-heartline-noir-photoreal-v2/references/canonical-base.png`
- `projects/codex-pets/ian/runs/ian-lemon-cadet-photoreal-v2/references/canonical-base.png`
- all three `qa/contact-sheet-extended.png`
- all three `qa/look-directions.png`
- all three `final/spritesheet-extended.webp`
- all three `final/validation-extended.json`
- all three `qa/chroma-despill-extended.json`
- all three `qa/direction-blind-validation-r2.pre-despill.json`
- all three `qa/direction-visual-arbitration-r2.pre-despill.json`

## Evidence notes and gaps

- All three final atlas validators report v2, 1536x2288, 8x11, 88 cells, RGBA, zero chroma fringe, zero opaque chroma-key pixels, zero transparent RGB residue, and no validator warnings/errors.
- All three despill reports report `ok: true` and `alpha_preserved: true`.
- Blind direction hard cardinals pass for all three; review-only warnings are covered by explicit visual arbitration and direct inspection of the labeled loops.
- The automated atlas validator does not detect detached connected components. Its green result therefore does not invalidate the Lemon visual blocker.
- Direct anti-slop/false-confidence pass: no production-code or test diff is in this visual-only review scope. The material false-confidence risk is reliance on validation JSON that omits component-connectivity semantics; direct cell inspection caught the defect.
- No separate executor code-review report or manual-QA matrix was supplied to this reviewer. Direct inspection of every required artifact category was sufficient to decide the stated gate; these missing reports are notes, not independent blockers.
