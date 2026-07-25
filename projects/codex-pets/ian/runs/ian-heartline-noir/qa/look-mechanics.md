# Heartline Noir look mechanics

Heartline Noir is a fully human soft-vinyl sticker character. Her boots, hips, skirt hem, and lower torso stay registered to one stable baseline. Gaze starts with both complete eyes, eyelids, and eyebrows; the head and neck follow through a restrained anatomical turn, while the upper torso supplies only a small counterbalance. Facial spacing, skull volume, hand shape, asymmetric black-and-ivory stage outfit, silver heart ornament, and body proportions must not stretch or warp.

The copper-red braided bun stays attached to the scalp and follows the head as one stable hair mass. The long black ribbon remains tied to the bun and trails one step behind head motion with gentle inertia; it never becomes an ear, tail, wing, or detached appendage. The ivory shoulder accent and silver heart ornament remain on their original screen-relative garment sides and must not flip.

## Cardinal pose families

- `000 up`: pupils and highlights rise, upper eyelids open slightly, brows lift, chin rises, and the neck extends a little. The bun follows the skull and the attached ribbon settles behind it.
- `090 screen-right`: nose tip and both pupils move to the screen-right side of the head center. The head yaws right, screen-left cheek broadens, screen-right cheek compresses, and the ribbon follows without changing its attachment side.
- `180 down`: pupils lower, upper eyelids descend, brows soften, chin tucks, and the upper neck shortens slightly. The ribbon tips drift slightly forward while the lower body stays planted.
- `270 screen-left`: nose tip and both pupils move to the screen-left side of the head center. The head yaws left, screen-right cheek broadens, screen-left cheek compresses, and the asymmetric outfit remains unmirrored.

## Motion budget

Each 22.5-degree step advances the eyes first, then head and neck by a small even amount, followed by restrained shoulders and one-step-delayed ribbon motion. No adjacent step may change body scale, baseline, bun construction, ribbon attachment, silver heart position, shoulder accent side, facial proportions, or human anatomy. `157.5 -> 180` and `337.5 -> 000` must be as smooth as internal transitions. Whole-sprite rotation, pupil-only sliding, mirroring, affine tilt, and non-rigid facial warping are forbidden.
