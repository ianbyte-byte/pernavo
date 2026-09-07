# Color system

Color is an **opt-in layer** for a wireframe, not the default skin. The default deck is
line art: neutral substrate + ink + hairline rules, with color reserved for the annotation
accent (redlines/badges) that marks structure. Only reach for a real palette when the client
names one (“商务蓝”), brings a brand/`DESIGN.md`, or asks for a themed demo; otherwise keep it
near-monochrome and let the review focus on structure. See SKILL.md "Line-art principle".

Resolve `--accent` (and optional alt) before filling the shell. Neutrals (canvas, window,
ink, hairlines) are substrate, not extra hues. Keep chromatic area small — it is an accent,
not a full-bleed wash.

Grammar comes from [mono-color-skill](https://github.com/yanliudesign/mono-color-skill)
and [DESIGN.md](https://designmd.app/what-is-design-md). The
[brand palette library](brand-palettes.md) gives real products' color structure as anchors —
use it to ground a choice, never to clone a brand as this product's identity.

## Priority

Use the first source that actually exists. Do not ask unless a named choice would change
the deck.

1. **User.** Hex, named ink, “只用黑白”, or an explicit pair. User choices win unless they
   demand a rainbow or unreadable type. Once a palette is named (e.g. “商务蓝” = business
   blue), treat it as fixed: never silently swap it for another hue, and never repaint the
   background with it. Business blue is an ACCENT, not a full-bleed background. Do not
   “improve” a user-named palette unprompted — a palette change is a user decision.
2. **Project.** Repo-root `DESIGN.md` `colors` (prefer `primary`); then CSS/token files,
   logo, or existing UI. If colors exist, require one primary. Do not invent a second
   accent the file does not use. ([schema + keys](brand-palettes.md#designmd-color-token-schema))
3. **Product / archetype.** Infer one plate from the subject and match a *structure* —
   one-ink-on-neutral, reserved single accent, dual identity, theme-switch, or ramp+accent —
   from the [archetypes](brand-palettes.md#archetypes-to-anchor-on-not-to-copy). Map
   everyday color words onto the catalog below instead of picking a random hex.
4. **Catalog fallback.** One-ink Charcoal `#30343A` on dark decks; two-ink Cobalt
   `#2148B8` + Terracotta `#C65F38` only when an alt theme is needed. Do not default to
   system blue `#007AFF` as brand identity.

Record the source in the output recipe (`user` / `DESIGN.md` / `css` / `inferred` /
`catalog`).

## Restraint

- At most two chromatic plates. Dominant neutrals ~70–85% of the frame; accent ~15–30%
  and only where it has a job (primary button, key state, annotation).
- One-ink when the user says monochrome / 黑白 / one named color, or the product is
  grayscale by nature.
- Second plate is an alt theme or one reserved CTA role — never decoration, charts-for-
  charts, or a third “success/warning/info” rainbow.
- Primary fill on the single most important action per screen. Semantic red is error, not
  accent.
- Text vs background ≥ 4.5:1 (WCAG AA) for body; ≥ 3:1 for large text (≥18pt or 14pt bold)
  and non-text UI. Verify with a ratio calculator before shipping — never guess a tint.
- Anti-fatigue, not max contrast: avoid pure black `#000` background (glare/halation) — use a
  soft dark like `#1B1B1E`–`#222426`. Avoid near-white-on-white tints. Desaturate semantic
  hues (critical/tight) to cut vibration. Light canvas is diffuse gray/white, not cream paper.
- Do not add unused color tokens.

## Catalog

Map loose words to these inks. Prefer a listed pair over an improvised duo.

| Word | Ink | Hex |
|---|---|---|
| blue / 蓝 | Cobalt | `#2148B8` |
| royal | Royal Blue | `#2058D4` |
| green / 绿 | Botanical Green | `#008A4B` |
| mint | Mint Green | `#5EB783` |
| orange / 橙 | Terracotta Orange | `#C65F38` |
| red / 红 | Signal Red | `#C83232` |
| purple / 紫 | Aubergine | `#63365F` |
| black / 黑 / charcoal | Charcoal | `#30343A` |

Known pairs: Cobalt + Terracotta, Charcoal + Signal Red, Botanical Green + Oxblood
`#8F3434`, Ultramarine `#263E99` + Safety Orange `#E55D2B`, Cyan `#159DDA` + Brick Red
`#B64032`, Mint + Warm Charcoal `#302D2E`.

Substrate (not inks): Neutral White `#FAFAF7`, Cool Gray `#E9E9E5`, Pale Beige `#F5F1E8`.
Wireframe light mode uses Cool Gray canvas + white window unless project tokens override.

## Apply

Write `--accent`, `--accent-contrast`, `--accent-soft`, `--wire-annotation`. Dark mode may
keep a white accent when the brief is monochrome-on-black; otherwise use the resolved ink.
Alt theme changes those four tokens only.

Use the [brand palette library](brand-palettes.md) for structure and anchor hexes; it is a
reference, not a source of identity. Do not re-skin the product as a library brand.
