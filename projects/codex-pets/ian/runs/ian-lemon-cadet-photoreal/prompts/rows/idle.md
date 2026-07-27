Create one horizontal animation strip for Codex pet `ian-lemon-cadet`, state `idle`.

Use the attached canonical base for identity. Use the attached layout guide only for slot count, spacing, centering, and padding; do not draw the guide.

Output exactly 6 full-body frames in one left-to-right row on flat pure blue #0000FF. Treat the row as 6 invisible equal-width slots: one centered complete pose per slot, evenly spaced, with no overlap, clipping, empty slots, labels, or borders.

Identity: same pet in every frame: Keep Ian fully human, age-appropriate and nonsexualized. Lock the face to the video references. Use long copper-auburn human twin ponytails with center-parted bangs, a modest cream-white sailor uniform with pale-lemon piping, structured square collar, short yellow waist bands, compact pleated skirt, navy fabric rosette with an original abstract silver-heart center and cream ankle boots. Ponytails are ordinary human hair, never animal ears or tails. One centered head-to-toe human with no scenery, props, text, logo, shadow or detached effects.. Preserve silhouette, face, proportions, markings, palette, material, style, and props.
Style: Photoreal sprite: one complete full-body real human, readable in a 192x208 cell, with natural facial geometry, natural human proportions, stable realistic materials, and crisp edges for chroma-key extraction. Style `auto`: Infer the most appropriate pet-safe style from the user request and reference images, then keep that exact style consistent across every row. User style notes: True-to-life photoreal miniature real human sprite; natural human anatomy and natural head-to-body proportions; realistic facial geometry, skin, individual hair strands, fabric weave, stitching, metal and footwear; maximum identity fidelity to the supplied face references; no illustration, anime, manga, cartoon, chibi, oversized head, toy, doll, figurine, sticker, painterly treatment, cel shading, plastic or wax..
Animation continuity: keep apparent pet scale and baseline stable within the row unless the state itself intentionally changes vertical position, such as `jumping`. Move the pose within the slot instead of redrawing the pet larger or smaller frame to frame.

State action: Calm low-distraction resting loop: subtle breathing, tiny blink, slight head/body bob, and only quiet persona-preserving motion.

State requirements:
- CRITICAL: idle is the low-distraction baseline state and the first frame is also used as the reduced-motion static pet.
- Use only subtle idle motion: gentle breathing, a tiny blink, a slight head or body bob, a very small material sway, or another quiet motion that fits the pet persona.
- Keep the pet essentially in the same pose, facing direction, silhouette, markings, palette, and prop state across all 6 frames.
- Idle variation must stay calm but still read as animation; do not repeat effectively identical copies across the loop.
- Do not show waving, walking, running, jumping, talking, working, reviewing, emotional reactions, large gestures, item interactions, or new props.
- Feet, base, body, or object anchor should remain planted or nearly planted.
- The first and last frames should be very close visually so the loop feels calm and does not pop.

Clean extraction: crisp opaque edges, safe padding, no scenery, text, guide marks, checkerboard, shadows, glows, motion blur, speed lines, dust, detached effects, stray pixels, or chroma-key colors inside the pet.
