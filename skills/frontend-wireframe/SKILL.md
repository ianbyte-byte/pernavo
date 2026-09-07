---
name: frontend-wireframe
description: >
  Produce a self-contained HTML wireframe deck for early product thinking, demos, and
  stakeholder review. Use when the user asks for 线稿, wireframe, UI blueprint, clickable
  mock, product demo pages, 设计稿, 全页面线稿, or a presentable multi-screen HTML prototype
  before implementation. Do not use for production frontend, visual-identity exploration,
  Figma/flow specs, or engineering reports.
---

# Frontend Wireframe

Own the presentable HTML deck that lets a human review structure, copy, and interaction
before anyone writes production UI. Do not implement the app, invent a visual identity for
its own sake, or turn the deck into a dashboard template.

## Line-art principle (default baseline)

A wireframe is **line art**: clear lines that establish outline, structure, and layout. It
does **not** carry large flat color areas, gradients, or complex shading by default. Treat
color as an *optional, opt-in* layer, never as the default skin:

- Default deck is near-monochrome: neutral substrate + ink + hairline rules. The only color
  is the annotation accent (redlines, badges) used to mark structure.
- Large color areas, gradients, complex lighting, or a full multi-hue palette appear **only
  when the client asks for them** — e.g. “商务蓝”, a brand palette, a themed demo.
- Even when color is requested, keep it an accent, not a full-bleed wash (see color system).
- If the brief is silent on color, ship line art. Do not fill the deck with a palette "to
  be safe" — that defeats the point of reviewing structure before visual decisions.

This is why the deck has a hard `data-view="wireframe"` (blueprint) vs `clean` (presentation)
toggle: the blueprint view is the honest line-art state; the clean view only removes the
annotation marks, it does not add decoration.

## Route away

| Request | Owner |
|---|---|
| Production page, component, or styling in the real app | `engineering-workflow` or a frontend Skill |
| Distinctive visual identity / anti-template art direction | `frontend-design` |
| Multi-screen flow spec, sitemap, or design brief without an HTML deck | product-design flow Skills |
| Formal findings report | `report-writer` |
| Diff / MR review | `change-review` |

If the user wants both a deck and later implementation, finish the deck first. Do not start
the production change in the same pass.

## Collect

Mark missing items unavailable; do not invent a product.

- Product name, audience, and the single job of this review
- Surfaces: web SPA, desktop window, menubar/popover, mobile, overlay, fullscreen
- Screens / states that must appear (happy path, empty, error, permission only if asked)
- Constraints: size, platform chrome, language
- Color system if the user named one; otherwise resolve from the project per
  [color system](references/color-system.md)
- Output path; default `docs/wireframes/<slug>-v<n>.html`

If the brief has no subject, name one concrete product and its audience before drawing.

## Design rules

Steal deck chrome, not a brand. The genre example is a single-file all-pages HTML deck with
a sticky control dock, device frames, dashed redlines, and a refine card beside each screen.
Do not copy lunar/moon, crater logos, or any other product metaphor unless this product is
that product.

1. One focus per screen. Delete status capsules, fake stats, stacked secondary CTAs, and
   decorative cards that steal the job of another module.
2. Whitespace first, structure first. Hairline rules, system type, small UI scale (11–13px).
3. One signature visual language derived from *this* product: 4–6 tokens and one metaphor
   that repeats. A second theme may change accent only.
4. Dual mode: dark = soft near-black canvas + gray ink (never pure `#000` — glare); light =
   diffuse gray canvas + white window. Chromatic accent is resolved, not assumed: user spec,
   then project `DESIGN.md`/CSS, then product inference, then the limited catalog. Once a
   palette is named ("商务蓝" = business blue), it is fixed — do not swap hues or repaint the
   background with it; an accent never becomes a full-bleed background. Stay to one plate (two
   only if the extra plate has a job). Do not default to `#007AFF`.
5. Readable, not fatiguing: text vs background ≥ 4.5:1 (WCAG AA), ≥ 3:1 for large text / UI.
   Desaturate semantic hues; set the sans stack with Source Han Sans first. Verify the ratio
   before shipping — never guess a tint.
6. Real copy in the product's language. No lorem. Name controls by what the user does.
7. Annotate decisions outside the UI: dimension badges, shortcut chips, refine cards. Keep
   `data-dim` badges clear of the frame chrome — frames that clip with `overflow:hidden` cut
   them off; use `overflow:visible` + `margin-top` to park them.
8. Match chrome to the surface: web app (SPA) uses a browser window with an address bar and
   per-route URL, not a macOS app window; macOS menubar 240pt popover; phone column; overlay;
   fullscreen. Do not put a desktop titlebar on a phone screen, and do not render a web SPA as
   a desktop app window.

Read [color system](references/color-system.md) then [style system](references/style-system.md)
before writing CSS. Copy [assets/shell.html](assets/shell.html) and replace product strings
and `--accent*`; do not regenerate the dock or toggle script from memory.

## Produce

1. Write a numbered IA: one module = one surface or one screen job.
2. Resolve the color recipe, then tokens and the signature metaphor. Reject
   purple-gradient / glass-dashboard / cream-serif defaults unless the brief asks for them.
3. Copy the shell. Keep it one HTML file: inline CSS and JS, inline SVG sprite, no CDN,
   no build, openable via `file://`.
4. For each module: device frame on the left, refine card on the right. Default
   `data-view="wireframe"` `data-mode="dark"`.
5. Wireframe view shows dashed outlines and `data-dim` badges; clean view hides them.
6. Theme and mode toggles only write `data-theme` / `data-mode` / `data-view` on `<html>`.
7. Cover empty/error/permission states only when the brief needs them, as extra modules,
   not as clutter inside the happy path.

## Output

Write the file. Then report:

```text
Path:
Modules (id · surface · job):
Color recipe (source · plates · hex):
Tokens and signature metaphor:
View / theme / mode defaults:
Not in this deck:
Color was fixed, not re-derived? (if a palette was named, confirm it was reused unchanged)
Open with: open <path>
```

Do not claim visual QA unless a browser screenshot was taken. Do not claim the production
app matches the deck.

## Resources

- [color system](references/color-system.md) — user/project/catalog priority and restraint
- [brand palettes](references/brand-palettes.md) — real products' color structure + DESIGN.md
  token schema, as anchors; not an identity to clone
- [style system](references/style-system.md) — tokens, dock, frames, annotation, anti-slop
- [shell](assets/shell.html) — copy this file; do not recreate the chrome
