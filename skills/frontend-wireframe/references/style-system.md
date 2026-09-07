# Wireframe style system

Use this with [assets/shell.html](../assets/shell.html). Neutrals below are substrate.
Resolve `--accent*` from [color system](color-system.md) before copying the shell. Do not
add frameworks, webfonts, or CDNs.

## Document state

```html
<html lang="zh-CN" data-theme="core" data-mode="dark" data-view="wireframe">
```

| Attribute | Values | Role |
|---|---|---|
| `data-view` | `wireframe` \| `clean` | Blueprint outlines vs presentable UI |
| `data-mode` | `dark` \| `light` | Canvas and ink |
| `data-theme` | `core` plus one optional alt | Accent only on the alt theme |

## Tokens

Keep the same names. Dark is a cold near-black, not navy. Light is diffuse gray/white, not
cream paper, unless project tokens say otherwise.

| Token | Dark | Light |
|---|---|---|
| `--bg-canvas` | `#060709` | `#F0F0F3` |
| `--bg-window` | `#0D0E12` | `#FFFFFF` |
| `--bg-card` | `rgba(255,255,255,.035)` | `rgba(0,0,0,.025)` |
| `--bg-inset` | `rgba(0,0,0,.35)` | `rgba(0,0,0,.03)` |
| `--ink-primary` | `#F4F4F6` | `#1C1D21` |
| `--ink-secondary` | `#92939B` | `#6E7079` |
| `--ink-tertiary` | `#5A5B64` | `#9B9DA7` |
| `--wire-line` | `rgba(255,255,255,.12)` | `rgba(0,0,0,.10)` |
| `--wire-line-strong` | `rgba(255,255,255,.28)` | `rgba(0,0,0,.25)` |
| `--wire-annotation` | resolved ink | resolved ink |
| `--accent` | white if one-ink-on-black, else resolved ink | resolved ink |
| `--accent-contrast` | readable on accent | readable on accent |
| `--dock-bg` | `rgba(20,21,26,.90)` | `rgba(255,255,255,.92)` |

Radius: 6 / 10 / 14 / 20 / 9999. Set the sans stack with **Source Han Sans first** for CJK
readability, then Latin/system fallbacks:

```css
--font-sans: "Source Han Sans SC", "Source Han Sans CN", "Noto Sans CJK SC", "Noto Sans SC",
  -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", "Helvetica Neue", sans-serif;
--font-mono: "SF Mono", "JetBrains Mono", Menlo, Monaco, Consolas, monospace;
```

Body ~13.5px, line-height 1.6, antialiased. Prefer Source Han Sans over a webfont CDN (none
allowed).

An alt theme overrides `--accent`, `--accent-contrast`, `--accent-soft`, and
`--wire-annotation` only.

## Deck chrome

Sticky `.control-dock`: brand chip + version badge, then segmented groups for view / theme /
mode, then `.nav-pills` to `#m00`… modules. Dock uses `backdrop-filter: blur(20px)`.

`.canvas`: max-width 1440px, padding 36px 24px 100px.

`.module-section` + `.section-header` (title + subtitle) + `.module-row` (frame column
`minmax(440px, auto)` | refine card). Stack to one column under 980px.

## Frames

| Surface | Class / size |
|---|---|
| Web SPA / web app | `.browser-window` 720px centered, address bar + per-route URL, 14px radius |
| Desktop app | `.mac-window` 440×560, 16px radius, traffic lights, optional segmented nav |
| Menubar | 24pt bar + `.popover` 240×auto, 10px radius |
| Phone | 390×844 column, 40px radius, 12px inset bezel |
| Overlay | 320–360pt floating card |
| Fullscreen | near-black stage, one focal object, two actions max |

A web SPA is a browser page, not a desktop app — render it as `.browser-window` (address bar,
route URL, bottom-corner radius on the body) and never as `.mac-window` with traffic lights.
Frames that are redlined must not clip the `data-dim` badge (see Annotation).

Product UI lives inside the frame. Deck chrome (dock, section titles, refine cards) stays
outside.

## Annotation

`.redline` + `data-dim="440 × 560 pt"` draws a dashed outline and a corner badge only when
`data-view="wireframe"`. Hide via:

```css
[data-view="clean"] .redline { outline: none; }
[data-view="clean"] .redline::after,
[data-view="clean"] .annot-badge { display: none; }
```

The `data-dim` badge anchors at `top:-8px`, so any redlined container that clips with
`overflow:hidden` will cut it off or overlap the chrome. For frames set `overflow:visible`,
add `margin-top` on the frame to park the badge (e.g. 16px), and put corner radius on the
frame's top/bottom children (`.browser-bar`, `.window-body`) instead of clipping. Never let
a badge sit on top of the browser bar or window title.

`.annot-badge` = module/spec chip. `.key-badge` = shortcut. `.refine-card` lists why, what
was deleted, and open tweaks. Put critique in the refine card, not as labels on the UI.

## Components

Use these inside frames. Do not invent a second button language.

- `.wire-card` — inset panel
- `.btn-primary` — 44px pill, accent fill, one per screen
- `.btn-secondary` — 34px, hairline border
- `.status-pill` — only if status is the screen's job
- `.segmented-control` / `.segmented-tab` — 2–5 peer destinations
- Inline SVG `<symbol>` sprite, `currentColor`, 12–14pt stroke, geometric. Replace generic
  timer/gear/chart icons when the product has a stronger metaphor.

## Script

Only toggle `data-view`, `data-theme`, `data-mode` and `.active` on the matching
`[data-*-btn]`. No routers, no component libraries, no analytics.

## Anti-slop

- No CDN, webfonts, Tailwind CDN, or image hosts
- No purple gradient, neon glass dashboard, or cream-serif landing default
- No lorem, fake avatars, or dummy charts unless the screen is a chart
- No second primary button on the same screen
- No production behavior (auth, payments, real data)
- Do not clone another product's metaphor (moons, craters, orbits) onto a new product
