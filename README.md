<p align="center">
  <img src="logo/logo.png" width="128" alt="Pumpkin Spice Theme logo">
</p>

<h1 align="center">Pumpkin Spice Theme</h1>

<p align="center">
  A cozy autumn Chrome theme in espresso, cinnamon, cream and pumpkin tones — the warm colours of a spiced latte on a knitted blanket.
</p>

Pumpkin Spice pairs a deep espresso frame with a cinnamon-brown toolbar, then opens onto a soft cream New Tab Page warmed by oat and pumpkin accents. Espresso ink keeps every tab, bookmark, and icon crisp against the pale surfaces, links take a burnt-pumpkin tone, and a single-row shortcut layout with a color-matched Google logo keeps the page clean.

## Design Concept

Pumpkin Spice is built from a classic autumn moodboard palette: espresso brown, cream, oat, pumpkin orange, and cinnamon. The dark browns carry the browser chrome and the pale creams carry the page, so the theme has strong contrast without ever feeling cold — the orange stays as a single warm accent rather than competing for attention.

| Color | Hex | RGB | Role |
|---|---|---|---|
| Espresso | `#3A2A21` | 58, 42, 33 | Frame |
| Cinnamon | `#6B4A33` | 107, 74, 51 | Toolbar |
| Cream | `#F4EEE2` | 244, 238, 226 | New Tab background |
| Oat | `#E9D2A8` | 233, 210, 168 | New Tab header / buttons |
| Light Oat | `#F0E3C8` | 240, 227, 200 | Secondary buttons |
| Pumpkin | `#DF8A3B` | 223, 138, 59 | Logo accent / New Tab buttons |
| Deep Pumpkin | `#A0521B` | 160, 82, 27 | New Tab links |
| Cream Ink | `#F5EFE2` | 245, 239, 226 | Tab, bookmark, and toolbar text |

## Features

- Pure color, no wallpaper — fast and distraction-free
- Warm earth palette: espresso, cinnamon, cream, oat and pumpkin in one family
- Dark browser chrome over a light page — strong contrast, cosy feel
- Tab text, bookmark text, toolbar icons: all share the same cream ink
- Single-row shortcut row and a color-matched Google logo for a clean New Tab Page
- No configuration needed — install and enjoy

## Installation

### Load Unpacked (Development)

1. Download or clone this repository.
2. Open `chrome://extensions` in Chrome.
3. Enable "Developer mode" in the top right.
4. Click "Load unpacked" and select this folder (`pumpkin-spice-theme`).
5. The theme is now active.

### Web Store Packaging

```
chrome://extensions → Pack extension → select this folder → pumpkin-spice-theme.zip
```

Upload the resulting `.zip` to the Chrome Web Store developer dashboard.

## Files

| File | Purpose |
|---|---|
| `manifest.json` | Theme definition (single-file, inlined `theme` field) |
| `logo/logo.png` | 128×128 store icon (transparent background) |
| `scripts/generate-logo.py` | Regenerate the logo from `manifest.json` colors |
| `LICENSE` | Non-Commercial License (English / 中文) |

## License

Pumpkin Spice Theme is released under the Non-Commercial License. See `LICENSE` for full text (English / 中文).
