# Azure Navigator look mechanics

Azure Navigator is a fully human soft-vinyl character. Her boots, hips, skirt hem, and lower torso remain registered to one stable baseline. The gaze begins with coordinated rotation of both complete eye surfaces plus eyelid and eyebrow reshaping; the head and neck follow with a restrained anatomical turn, and the upper torso contributes only a small counterbalance. Facial spacing, skull volume, hand shape, sailor collar, bow, and denim pinafore never stretch or warp.

The sailor cap is worn on the head and follows it as a rigid attached prop without changing sides. Long copper hair stays attached at the scalp and follows one step behind the head with gentle inertia; it may partly occlude a shoulder but may not detach, teleport, or become an animal appendage. The blue bow remains fixed to the chest.

## Cardinal pose families

- `000 up`: pupils and eye highlights rise, upper eyelids open slightly, brows lift, chin rises and neck extends a little. More underside of the chin is visible; the cap follows the skull and hair settles behind the shoulders.
- `090 screen-right`: nose tip and both pupils cross to the screen-right side of the head center. The head yaws right, the screen-left cheek becomes broader, the screen-right cheek compresses toward partial profile, and hair/cap follow without flipping sides.
- `180 down`: pupils lower, upper eyelids descend, brows soften, chin tucks and the upper neck shortens slightly. Hair tips drift a little forward while boots and lower torso remain fixed.
- `270 screen-left`: nose tip and both pupils cross to the screen-left side of the head center. The head yaws left, the screen-right cheek becomes broader, the screen-left cheek compresses toward partial profile, and hair/cap follow without flipping sides.

## Motion budget

Each 22.5-degree step advances eyes first, then head/neck by a small even amount, with at most a subtle shoulder response and one-step-delayed hair motion. No adjacent step may change body scale, baseline, hat side, bow position, facial proportions, or hair attachment. `157.5 -> 180` and `337.5 -> 000` must be as smooth as every internal transition. Whole-sprite rotation, pupil-only sliding, affine tilt, and non-rigid facial warping are forbidden.
