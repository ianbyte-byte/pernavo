Create one horizontal animation strip for Codex pet `ian-azure-navigator`, state `idle`.

Use the attached canonical base for identity. Use the attached layout guide only for slot count, spacing, centering, and padding; do not draw the guide.

Output exactly 6 full-body frames in one left-to-right row on flat pure green #00FF00. Treat the row as 6 invisible equal-width slots: one centered complete pose per slot, evenly spaced, with no overlap, clipping, empty slots, labels, or borders.

Identity: same pet in every frame: Create a compact full-body human Codex Pet inspired by the public stage persona and supplied visual references of Hearts2Hearts member IAN. This is a stylized, age-appropriate, nonsexualized teenage human idol avatar, not a photoreal portrait. She has warm copper-auburn waist-length human hair, a softly rounded face, bright dark eyes, subtle rosy cheeks, two clearly formed human hands with five fingers each, and two human legs in compact navy ankle boots. Outfit: navy-and-white sailor uniform with broad sailor collar, sky-blue satin bow, one small original silver heart ornament, structured dark-denim pinafore, and a small navy sailor cap tilted slightly to one side. Use a polished soft-vinyl 3D collectible figure style with an oversized expressive head, compact body, clean shapes, smooth material and details readable inside a 192x208 sprite cell. Personality: emotionally perceptive, people-loving, positive, playful and fan-minded; varied readable expressions should move from a trace of pre-camera nervousness into focused enjoyment and confident warmth. She must remain fully human. No animal ears, tail, paws, muzzle, whiskers, wings, horns, mascot animal, plush animal, copied character, readable logo, text, handheld prop, floating decoration, scenery, floor or shadow.. Preserve silhouette, face, proportions, markings, palette, material, style, and props.
Style: Pet-safe sprite: compact full-body mascot, readable in a 192x208 cell, clear silhouette, simple face, stable palette/materials, and crisp edges for chroma-key extraction. Style `3d-toy`: Stylized 3D toy mascot with smooth rounded forms, simple materials, clear silhouette, and no photoreal complexity. User style notes: Premium soft-vinyl 3D toy; navy, white, sky blue, dark denim, silver and copper-auburn palette; compact human silhouette; long hair, sailor cap, wide collar and bow are the identity anchors; modest age-appropriate styling; all accessories physically attached..
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
