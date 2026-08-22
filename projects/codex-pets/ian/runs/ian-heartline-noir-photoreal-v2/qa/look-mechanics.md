# Ian look mechanics

Ian remains planted through the look loop: boots, skirt hem, belt, and torso scale share one baseline. Her gaze leads with natural almond-eye movement, subtle eyelid and eyebrow changes, then a restrained neck/head turn and a small upper-torso follow-through. The bun and narrow black ribbon lag very slightly with the head; the belt and silver heart stay worn and body-locked.

- `000` up: eyes lift, eyelids open slightly, chin lifts a little; frontal face remains readable.
- `090` screen-right: pupils, nose bridge, chin, and head turn toward the viewer's right; the screen-left side of her face becomes slightly more visible.
- `180` down: eyes lower, lids soften, chin tucks slightly; torso remains planted.
- `270` screen-left: the inverse right-facing pose, with head, nose, and gaze toward the viewer's left and the screen-right cheek becoming slightly more visible.

Every 22.5-degree step is an even interpolation of those eye, head, neck, and shoulder motions. No whole-sprite rotation, face warping, prop swapping, or replacement eye construction is allowed. The `157.5 -> 180` and `337.5 -> 000` transitions must be the same small motion budget as the other adjacent pairs.
