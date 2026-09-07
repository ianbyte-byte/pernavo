# Brand palette reference library

Source of the catalog: [DESIGN.md — Real Brands](https://designmd.app/brands) (the public CSS of
real products extracted into DESIGN.md), plus the [DESIGN.md token schema](https://designmd.app/what-is-design-md).

Use this as a **lexicon of how mature products structure color**, and as a palette anchor when a
project already uses one of these brands or when a product's domain maps to one of these archetypes.
Do **not** clone a brand as this product's identity and do not re-skin a wireframe deck as Nubank
or Atlassian. A brand is grammar, not a template.

## DESIGN.md color token schema

An agent reads a repo-root `DESIGN.md` top-to-bottom. YAML holds values, prose holds rules.
Recommended semantic color keys:

```yaml
name: <product>
colors:
  primary:     # the dominant / most important action
  secondary:   # a supporting action, if the system needs two
  tertiary:    # a third role, only if genuinely used
  neutral:     # grayscale base
  surface:     # card / window background
  on-surface:  # text on surface
  error:       # semantic failure — never a decorative accent
```

`colors.<token>` accepts any CSS color. `primary` is required when a palette exists; the rest are
recommended. Keep semantic names (so error red is never used as an accent) and limit `primary` to
the single most important action.

## Catalog

| Brand | Primary | Role colors | Structure note |
|---|---|---|---|
| 99 | `#FFDD00` | CTA `#FC4C02` | Two-plate: yellow dominance + orange CTA |
| Atlassian | `#1868DB` | neutral-dominant | **Restrained saturation**, four-plane elevation |
| Clerk | `#6C47FF` | | Developer-tool purple, single accent |
| Embraer | `#0E1C59` | corporate blue `#0067B1` | Navy dominant, one supporting blue |
| Flame (Santander) | `#EC0000` | named red ramps, sky `#DEEDF2` | Ramps + reserved accent |
| Globo | `#FF0000` | | Dark/light switch, single chrome color |
| GOL | `#FF7020` | | Warm orange, aviation booking |
| Boticário Flora | `#006B3F` | golden accents | Deep green + gold, sustainability |
| iFood Pomodoro | `#EA1D2C` | | Vibrant red, card discovery |
| Loggi ELKE | `#0055FF` | cyan gradients, navy surface | Blue lockup with dark neutral surfaces |
| Magalu | `#0086FF` | | Product-card architecture |
| Mercado Livre | `#FFE600` + `#3483FA` | | **Dual identity**: header vs actions |
| Mintlify | `#0C8C5E` light / `#18E299` dark | | Theme-switch, warm off-white |
| Mondrian (Claro) | `#D52B1E` + `#ADAFAF` | | Two-tone red + gray |
| Nubank Marketing | `#820AD1` | pure black ink | Purple **reserved for CTAs**, **zero shadows** |
| Nubank NuDS | `#820AD1` | | OLED dark mode, oblong shapes |
| Nuvemshop Nimbus | `#0059D5` | | Accessibility-first |
| Nuxt | `#00DC82` | | Electric green, single accent |
| olist | `#043FBE` | 6 per-product themes | Complexity-progressive radius |
| PicPay | `#21C25E` | | Green, mobile-first |
| Pulso (RD Saúde) | Raia `#006F83` / Drogasil `#B6202F` | | **Real multi-brand switch** |
| RD Station Tangram | `#1D63FF` | | Dashboard metrics |
| Resend | black canvas | | Dark minimal |
| Stone | `#00A868` | | Green, hardware language |
| TOTVS PO UI | purple accent | | Enterprise |
| Vercel Geist | black/white | | Monochrome |
| VoltAgent | `#00D992` | | Neon, AI platform |
| VTEX | pink/rose accent | | Commerce |
| Wellhub Yoga | multi-brand | | Corporate wellness |

## Archetypes to anchor on (not to copy)

Match the product's domain and restraint to a structure, then pick your own anchor values.

- **One ink on neutral** — Vercel Geist, Resend. Product is monochrome / reads as a tool: use one
  chromatic accent max, or zero.
- **Reserved single accent** — Nubank, Clerk, Nuxt, VoltAgent. One strong plate held for CTAs and
  links; everything else neutral. Best for a **decision instrument** like Finance.
- **Dual identity (two roles)** — Mercado Livre, Pulso. Header/surface in one hue, actions in a
  second. Only when real structure has two jobs.
- **Dual mode theme-switch** — Mintlify, Globo. A light and a dark value of the same hue; default
  light unless the product is terminal/night.
- **Ramps + reserved accent** — Santander. Build a lightness ramp of the primary and reserve an
  accent for calls-to-action; adds hierarchy without a rainbow.

## Restraint rules (unchanged)

- At most two chromatic plates; dominant neutral ~70–85%, accent ~15–30%.
- Use the second plate only if it has a job (alt theme, or one reserved CTA/role), never decoration.
- Text vs background ≥ 4.5:1 (WCAG AA). Semantic red/amber = state, not brand accent.
- Do not introduce a color token you never reference.

## Work the deck

1. Read a repo `DESIGN.md` first; use its `colors.primary` as `--accent` if the product follows it.
2. If the project already ships a Real Brand (a repo that is actually e.g. `olist`), follow it.
3. Otherwise anchor on the product's domain archetype (a finance decision tool → *reserved single
   accent*), pick one hex from the catalog family you like, and record the source in the recipe.
4. Name the choice `user` / `DESIGN.md` / `css` / `inferred` / `catalog` in `Color recipe`.

Built-in agent skills that read DESIGN.md live at
[designmd.app/skills](https://designmd.app/skills).
