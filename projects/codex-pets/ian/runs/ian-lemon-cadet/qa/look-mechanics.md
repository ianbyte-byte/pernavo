# Lemon Cadet look mechanics

Lemon Cadet is a fully human painterly sticker character. Her boots, hips, skirt hem, and lower torso remain registered to one stable baseline. Gaze begins with coordinated motion of both complete eyes, eyelids, and eyebrows; the head and neck follow with a restrained anatomical turn, while the upper torso contributes only a subtle counterbalance. Facial spacing, skull volume, hand shape, cream-and-lemon sailor outfit, navy rosette, and body proportions never stretch or warp.

Both copper twin ponytails are ordinary human hair fixed at two stable scalp ties. They follow the head with one-step-delayed inertia and may sway gently, but never behave as animal ears, tails, tentacles, or detached props. The navy rosette stays attached to its original chest side and must not flip or wander.

## Cardinal pose families

- `000 up`: pupils and highlights rise, upper eyelids open slightly, brows lift, chin rises, and the neck extends a little. Hair ties remain fixed and ponytail lengths settle behind the shoulders.
- `090 screen-right`: nose tip and both pupils cross to the screen-right side of the head center. The head yaws right, screen-left cheek broadens, screen-right cheek compresses, and ponytails follow without changing attachment points.
- `180 down`: pupils lower, upper eyelids descend, brows soften, chin tucks, and the upper neck shortens slightly. Ponytail tips drift a little forward while the lower body stays planted.
- `270 screen-left`: nose tip and both pupils cross to the screen-left side of the head center. The head yaws left, screen-right cheek broadens, screen-left cheek compresses, and the navy rosette remains on its original garment side.

## Motion budget

Each 22.5-degree step advances eyes first, then head and neck by a small even amount, with minimal shoulder response and one-step-delayed ponytail motion. No adjacent step may change body scale, baseline, hair-tie positions, ponytail count, rosette side, facial proportions, or human anatomy. `157.5 -> 180` and `337.5 -> 000` must be as smooth as internal transitions. Whole-sprite rotation, pupil-only sliding, mirroring, affine tilt, and non-rigid facial warping are forbidden.
