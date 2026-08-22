# Canonical full-body base self-assessment

## Candidate and source evidence

- Accepted output: `references/canonical-base.png`
- Final r2 imagegen source: `sources/base-candidate-r2-raw.png`
- r1 rejected backups: `sources/canonical-base-rejected-r1.png`, `sources/base-candidate-raw-rejected-r1.png`
- Accepted output dimensions: 866 x 1817 PNG, RGB, non-interlaced.
- Accepted output SHA256: `c511bc17b5edef9c520d5dff467d137634ec75ce4c579224c2157ca7228001e8`.
- Raw r2 imagegen source SHA256: `1db6983065150cc916a69811a8be4077cfd2cc29f2416d514a46471c59ed2c41`.
- `references/canonical-base.png` is the raw r2 candidate with only non-creative chroma-key normalization applied; no face or outfit synthesis was done after imagegen.
- Generation used the identity master and frontal/three-quarter video frames as face authorities; the rejected r1 canonical supplied full-body composition and outfit continuity.
- One full-image identity-repair edit was performed for r2; no animation rows were generated.

## Visual checks

- Human: one fully visible real human from sailor cap to boot soles; no animal, abstract shape, second person, or detached object.
- Composition: centered, straight-on, relaxed natural standing pose, head-to-toe visible with margin; no crop or multi-panel strip.
- Identity repair self-check: eye apertures are visibly smaller and horizontally longer with a flatter brow-eye axis; nose bridge and nose-to-lip spacing are longer with a fuller rounded tip; lower face and chin are less shortened and less pointed; cupid's bow, fuller lower lip, and viewer-left under-eye mole remain visible. No round doll eyes or generic-idol retouching observed.
- Hair and outfit: copper-auburn long hair, tilted navy sailor cap, navy-and-white collar, sky-blue bow, silver heart ornament, dark-denim pinafore with stitching, and compact navy ankle boots.
- Keying: background is a flat pure green-screen plate with sampled corner and edge pixels exactly RGB `(0,255,0)` / `#00FF00`; no gradient, scenery, horizon, cast/contact shadow, halo, glow, or checkerboard. The normalization only replaces green-screen pixels and leaves the human/outfit geometry intact.
- Style: photographic skin/hair/fabric/metal/boot detail; no anime, cartoon, chibi, doll, toy, figurine, plastic/wax, painterly, cel-shaded, or 3D-render treatment.

## Residual risk

The canonical base is a generated photoreal reconstruction, not biometric or pixel-identical evidence. The compact full-body framing necessarily reduces facial detail relative to the identity master, and the stage outfit introduces copper hair and cap framing that can change perceived face shape. Minor face, hair-strand, fabric, and anti-aliased edge differences may still appear when this base is downsampled into a 192x208 sprite cell. The previous independent gate was `2 REVISE, 1 PASS`; this self-assessment does not overwrite that decision. Independent QA must rerun the same identity gate before any row generation is authorized.
