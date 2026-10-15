#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pumpkin Spice Theme — vector logo candidates (SVG rendered by headless Chromium).

Why the browser instead of PIL: the previous PIL set was flat and geometric.
Rendering real SVG gives true vector anti-aliasing, gradients and soft shadows,
which is what makes a 128px icon look designed rather than drawn.

Flow:
  1. one HTML page holds every candidate as an inline SVG in its own 512px cell
  2. Playwright screenshots each cell with omit_background=True  -> transparent PNG
  3. PIL composes the light/dark contact sheets, the inline strip and the
     official logo/logo.png from SELECTED

Colours come from manifest.json. Re-run with a different SELECTED; never hand-copy.
"""
import json
import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
os.chdir(str(ROOT))                      # relative paths only (non-ASCII path safety)

SIZE = 128
CELL = 512                               # rendered cell (2x of the 256 preview)
PREVIEW = 256
SELECTED = "06"
CAND_DIR = Path("logo/candidates")
LOGO_OUT = Path("logo/logo.png")

with open("manifest.json", "r", encoding="utf-8") as f:
    _m = json.load(f)
_C, _P = _m["theme"]["colors"], _m["theme"]["properties"]


def hx(rgb):
    return "#%02X%02X%02X" % tuple(rgb)


ESPRESSO = hx(_C["frame"])
CINNAMON = hx(_C["toolbar"])
CREAM = hx(_C["ntp_background"])
OAT = hx(_C["button_background"])
PUMPKIN = hx(_P["ntp_button_background"])
PUMPKIN_DEEP = hx(_P["ntp_button_hover"])
INK = hx(_C["tab_text"])
CREAM_DEEP = hx(_C["button_background_secondary"])

SC = 2                                   # svg user units -> rendered px (256 * 2)


def svg_open(body, defs=""):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
            'viewBox="0 0 256 256">%s%s</svg>' % (CELL, CELL, defs, body))


PUMPKIN_GRAD = """
<defs>
  <radialGradient id="pg1" cx="34%%" cy="26%%" r="86%%">
    <stop offset="0" stop-color="#F3AE66"/>
    <stop offset="0.5" stop-color="%s"/>
    <stop offset="1" stop-color="#AE6018"/>
  </radialGradient>
  <linearGradient id="lg1" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#8A6444"/>
    <stop offset="1" stop-color="%s"/>
  </linearGradient>
</defs>""" % (PUMPKIN, CINNAMON)

# ------------------------------------------------------------------ candidates
SVG_01 = svg_open(PUMPKIN_GRAD + """
<ellipse cx="128" cy="152" rx="95" ry="73" fill="url(#pg1)"/>
<g fill="none" stroke="#A65A1E" stroke-linecap="round">
  <path d="M128 82 C104 108 104 196 128 224" stroke-opacity=".38" stroke-width="4"/>
  <path d="M128 82 C152 108 152 196 128 224" stroke-opacity=".38" stroke-width="4"/>
  <path d="M128 80 C86 116 86 190 128 225" stroke-opacity=".22" stroke-width="4"/>
  <path d="M128 80 C170 116 170 190 128 225" stroke-opacity=".22" stroke-width="4"/>
</g>
<ellipse cx="128" cy="152" rx="95" ry="73" fill="none" stroke="#8E4E13" stroke-opacity=".45" stroke-width="3"/>
<ellipse cx="96" cy="120" rx="34" ry="24" fill="#FFFFFF" opacity=".20" transform="rotate(-18 96 120)"/>
<path d="M121 84 q-6 -22 7 -32 q7 10 5 32 z" fill="url(#lg1)"/>
<path d="M138 70 q30 -20 52 -8 q-16 26 -50 22 z" fill="#8A6444" opacity=".92"/>
<path d="M146 74 q18 -10 34 -6" stroke="#6B4A33" stroke-opacity=".55" stroke-width="2.5" fill="none" stroke-linecap="round"/>
""")

SVG_02 = svg_open("""
<defs>
  <radialGradient id="bg2" cx="40%%" cy="34%%" r="80%%">
    <stop offset="0" stop-color="#F3AE66"/>
    <stop offset="1" stop-color="#C4702A"/>
  </radialGradient>
</defs>
<circle cx="128" cy="128" r="104" fill="%s"/>
<circle cx="128" cy="128" r="104" fill="none" stroke="%s" stroke-opacity=".35" stroke-width="3"/>
<g>
  <ellipse cx="128" cy="142" rx="66" ry="52" fill="url(#bg2)"/>
  <g fill="none" stroke="#A65A1E" stroke-linecap="round" stroke-opacity=".42" stroke-width="3.4">
    <path d="M128 92 C114 110 114 176 128 193"/>
    <path d="M128 92 C142 110 142 176 128 193"/>
  </g>
  <path d="M122 92 q-5 -18 6 -26 q6 8 4 26 z" fill="%s"/>
  <path d="M137 80 q22 -14 38 -5 q-12 19 -37 16 z" fill="%s" opacity=".9"/>
</g>
""" % (ESPRESSO, OAT, OAT, OAT))

SVG_03 = svg_open("""
<defs>
  <linearGradient id="mg3" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFFFFF"/>
    <stop offset="1" stop-color="%s"/>
  </linearGradient>
  <linearGradient id="sg3" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="%s" stop-opacity=".25"/>
    <stop offset="1" stop-color="%s" stop-opacity=".9"/>
  </linearGradient>
</defs>
<g fill="none" stroke="url(#sg3)" stroke-width="7" stroke-linecap="round">
  <path d="M96 96 q-14 -16 0 -30 q14 -14 0 -28"/>
  <path d="M128 92 q-14 -16 0 -30 q14 -14 0 -28"/>
  <path d="M160 96 q-14 -16 0 -30 q14 -14 0 -28"/>
</g>
<ellipse cx="128" cy="214" rx="76" ry="13" fill="%s" opacity=".85"/>
<path d="M74 132 h108 l-14 66 q-3 12 -16 12 h-48 q-13 0 -16 -12 z" fill="url(#mg3)" stroke="%s" stroke-width="6" stroke-linejoin="round"/>
<path d="M74 132 h108 l-3 14 h-102 z" fill="%s"/>
<path d="M182 140 q30 -4 30 26 q0 28 -34 30" fill="none" stroke="%s" stroke-width="9" stroke-linecap="round"/>
""" % (CREAM_DEEP, CINNAMON, CINNAMON, CINNAMON, ESPRESSO, CINNAMON, ESPRESSO))


def spiral_path(cx, cy, r0, r1, turns, steps=320):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        th = 2 * math.pi * turns * t
        r = r0 + (r1 - r0) * t
        pts.append("%.2f %.2f" % (cx + r * math.cos(th), cy + r * math.sin(th)))
    return "M" + " L".join(pts)


SVG_04 = svg_open("""
<defs>
  <linearGradient id="sw4" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#F3AE66"/>
    <stop offset="0.55" stop-color="%s"/>
    <stop offset="1" stop-color="#B0581A"/>
  </linearGradient>
</defs>
<path d="%s" fill="none" stroke="url(#sw4)" stroke-width="23" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="128" cy="128" r="26" fill="%s"/>
<circle cx="128" cy="128" r="11" fill="%s" opacity=".9"/>
""" % (PUMPKIN, spiral_path(128, 128, 34, 100, 2.35), CINNAMON, OAT))

SVG_05 = svg_open("""
<defs>
  <linearGradient id="cr5" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#8A6444"/>
    <stop offset="0.5" stop-color="%s"/>
    <stop offset="1" stop-color="#4A3122"/>
  </linearGradient>
  <linearGradient id="fi5" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#F0A85C"/>
    <stop offset="1" stop-color="%s"/>
  </linearGradient>
</defs>
<path d="M128 208 L40 108 A104 104 0 0 1 216 108 Z" fill="url(#fi5)"/>
<path d="M44 104 A104 104 0 0 1 212 104" fill="none" stroke="url(#cr5)" stroke-width="30" stroke-linecap="round"/>
<path d="M60 132 A92 92 0 0 1 196 132" fill="none" stroke="#8E4E13" stroke-opacity=".18" stroke-width="10"/>
<g>
  <ellipse cx="120" cy="146" rx="30" ry="21" fill="%s"/>
  <ellipse cx="140" cy="138" rx="22" ry="17" fill="%s"/>
  <ellipse cx="130" cy="128" rx="15" ry="12" fill="%s"/>
</g>
<g fill="#6B4A33" opacity=".85">
  <circle cx="112" cy="128" r="3.2"/><circle cx="131" cy="118" r="3.2"/><circle cx="148" cy="130" r="3.2"/>
</g>
""" % (CINNAMON, PUMPKIN, CREAM, CREAM, CREAM))


def leaf(angle, base, scale, fill, vein):
    """Leaf sprouting from `base`, pointing along `angle` (SVG rotation degrees)."""
    return ('<g transform="translate(%d %d) rotate(%d) scale(%.3f)">'
            '<path d="M0 0 C 24 -32 72 -32 98 0 C 72 32 24 32 0 0 Z" fill="%s"/>'
            '<path d="M6 0 H92" stroke="%s" stroke-opacity=".5" stroke-width="3.2" fill="none" stroke-linecap="round"/>'
            '<path d="M28 -7 L42 -19 M28 7 L42 19 M54 -9 L68 -20 M54 9 L68 20" stroke="%s" '
            'stroke-opacity=".35" stroke-width="2.6" fill="none" stroke-linecap="round"/></g>'
            % (base[0], base[1], angle, scale, fill, vein, vein))


SVG_06 = svg_open("""
<defs>
  <linearGradient id="lf6" x1="0" y1="0" x2="0.6" y2="1">
    <stop offset="0" stop-color="#F5B672"/>
    <stop offset="1" stop-color="%s"/>
  </linearGradient>
</defs>
<path d="M128 204 V230" stroke="%s" stroke-width="7" stroke-linecap="round" fill="none"/>
%s
%s
%s
""" % (PUMPKIN, CINNAMON,
       leaf(-142, (128, 206), 0.98, PUMPKIN_DEEP, "#8E4E13"),
       leaf(-90, (128, 206), 1.12, "url(#lf6)", CINNAMON),
       leaf(-38, (128, 206), 0.98, OAT, "#8A6444")))

CANDIDATES = [
    ("01", "pumpkin-gradient", "Gradient pumpkin with leaf — polished classic", SVG_01),
    ("02", "pumpkin-badge", "Pumpkin in an espresso badge — best at 32px", SVG_02),
    ("03", "latte-cup", "Cup, saucer and steam — warm, product-like", SVG_03),
    ("04", "spice-swirl", "Gradient cinnamon-roll swirl — cleanest mark", SVG_04),
    ("05", "pie-slice", "Pumpkin pie with cream — most on-name", SVG_05),
    ("06", "leaf-trio", "Three autumn leaves — calm and botanical", SVG_06),
]


def font(size, bold=False):
    for name in (("segoeuib.ttf", "seguisb.ttf") if bold else ("segoeui.ttf", "segoeuisl.ttf")):
        p = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def render_cells():
    cells = "".join(
        '<div id="cell%s" style="width:%dpx;height:%dpx">%s</div>' % (num, CELL, CELL, svg)
        for num, _n, _d, svg in CANDIDATES)
    html = ('<!doctype html><html><head><meta charset="utf-8"><style>'
            'html,body{margin:0;padding:0;background:transparent}'
            '#grid{display:flex;flex-wrap:wrap;width:%dpx}'
            'div[id^=cell]{display:block}'
            '</style></head><body><div id="grid">%s</div></body></html>' % (CELL * 3, cells))
    out = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": CELL * 3, "height": CELL * 2})
        pg.set_content(html)
        for num, name, _d, _svg in CANDIDATES:
            path = CAND_DIR / ("%s-%s.png" % (num, name))
            pg.locator("#cell" + num).screenshot(path=str(path), omit_background=True)
            img = Image.open(path).convert("RGBA")
            img = img.resize((PREVIEW, PREVIEW), Image.LANCZOS)
            img.save(path)
            bbox = img.split()[3].getbbox()
            assert bbox, "candidate %s rendered empty" % name
            assert bbox[0] > 8 and bbox[1] > 8 and bbox[2] < PREVIEW - 8 and bbox[3] < PREVIEW - 8, \
                "candidate %s touches the canvas edge: %s" % (name, bbox)
            out[num] = img
            print("candidate %s %s -> alpha bbox %s" % (num, name, bbox))
        b.close()
    return out


def contact_sheet(rendered, bg, txt, sub, path, title):
    cols, rows = 3, 2
    cw, ch = 384, 374
    gap, margin = 28, 40
    W = margin * 2 + cols * cw + (cols - 1) * gap
    H = margin * 2 + 34 + rows * ch + (rows - 1) * gap
    sheet = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(sheet)
    f_title, f_name, f_desc, f_file = font(24, True), font(21, True), font(15), font(14)
    d.text((margin, margin), title, font=f_title, fill=txt)
    y0 = margin + 34
    for i, (num, name, desc, _svg) in enumerate(CANDIDATES):
        r, c = divmod(i, cols)
        x = margin + c * (cw + gap)
        y = y0 + r * (ch + gap)
        big = rendered[num].resize((220, 220), Image.LANCZOS)
        sheet.paste(big, (x + (cw - 220) // 2, y + 14), big)
        d.text((x + 18, y + 250), "%s · %s" % (num, name), font=f_name, fill=txt)
        d.text((x + 18, y + 280), desc, font=f_desc, fill=sub)
        thumb = rendered[num].resize((32, 32), Image.LANCZOS)
        sheet.paste(thumb, (x + 18, y + 330), thumb)
        d.text((x + 60, y + 339), "%s.png  256x256" % name, font=f_file, fill=sub)
        assert y + 300 <= y + 322, "text block collides with the thumbnail row"
    sheet.save(path)
    print("saved:", path, sheet.size)


def inline_strip(rendered, path):
    n, cell, gap, margin = len(CANDIDATES), 108, 22, 30
    W = margin * 2 + n * cell + (n - 1) * gap
    H = margin * 2 + cell + 30
    strip = Image.new("RGB", (W, H), (247, 243, 236))
    d = ImageDraw.Draw(strip)
    f = font(15, True)
    for i, (num, _n, _d, _s) in enumerate(CANDIDATES):
        x = margin + i * (cell + gap)
        img = rendered[num].resize((cell, cell), Image.LANCZOS)
        strip.paste(img, (x, margin), img)
        d.text((x + cell // 2 - 8, margin + cell + 8), num, font=f, fill=(58, 42, 33))
    strip.save(path)
    print("saved:", path, strip.size)


def main():
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    rendered = render_cells()
    contact_sheet(rendered, (247, 243, 236), (58, 42, 33), (122, 96, 72),
                  CAND_DIR / "contact-light.png", "Pumpkin Spice — vector logo candidates (light)")
    contact_sheet(rendered, (36, 26, 19), (245, 239, 226), (196, 170, 142),
                  CAND_DIR / "contact-dark.png", "Pumpkin Spice — vector logo candidates (dark)")
    inline_strip(rendered, CAND_DIR / "inline-strip.png")
    sel = [c for c in CANDIDATES if c[0] == SELECTED][0]
    icon = rendered[sel[0]].resize((SIZE, SIZE), Image.LANCZOS)
    icon.save(LOGO_OUT)
    print("official icon from SELECTED=%s (%s):" % (sel[0], sel[1]), LOGO_OUT, icon.size)


if __name__ == "__main__":
    main()
