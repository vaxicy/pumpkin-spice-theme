#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the 128x128 logo for Pumpkin Spice Theme.

All colors are read from manifest.json (single source of truth).
Design: transparent background — a ridged pumpkin in the theme's pumpkin
orange with a cinnamon stem and a soft cream sheen, echoing the cozy
autumn moodboard (pumpkin, cinnamon, cream knit).

Rendered at 4x and downscaled with LANCZOS for smooth anti-aliased edges.
"""
import json
import os
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
os.chdir(str(ROOT))                      # relative paths only (non-ASCII path safety)

MANIFEST = Path("manifest.json")
OUT_DIR = Path("logo")
OUT = OUT_DIR / "logo.png"

SIZE = 128
SS = 4               # supersampling factor
BIG = SIZE * SS      # 512


def load_colors():
    with open(MANIFEST, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    return manifest["theme"]["colors"], manifest["theme"]["properties"]


def rgb(vals):
    return tuple(vals)


def body_mask(cx, cy, rx, ry):
    mask = Image.new("L", (BIG, BIG), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=255)
    return mask


def draw_pumpkin(pumpkin, ridge, stem_col, sheen):
    cx, cy = BIG * 0.50, BIG * 0.615
    rx, ry = BIG * 0.395, BIG * 0.305
    mask = body_mask(cx, cy, rx, ry)

    img = Image.new("RGBA", (BIG, BIG), (0, 0, 0, 0))
    body = Image.new("RGBA", (BIG, BIG), (0, 0, 0, 0))
    d = ImageDraw.Draw(body)
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=pumpkin + (255,))

    # ridges: tall thin ellipse outlines, clipped to the body
    ridges = Image.new("RGBA", (BIG, BIG), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ridges)
    for k in (-0.55, -0.19, 0.19, 0.55):
        ex = cx + k * rx
        ew = rx * 0.30
        rd.ellipse([ex - ew, cy - ry * 0.98, ex + ew, cy + ry * 0.98],
                   outline=ridge + (235,), width=int(BIG * 0.018))
    ridges.putalpha(ImageChops.multiply(ridges.split()[3], mask))
    body = Image.alpha_composite(body, ridges)

    # soft cream sheen on the upper left
    sheen_layer = Image.new("RGBA", (BIG, BIG), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sheen_layer)
    sd.ellipse([cx - rx * 0.72, cy - ry * 0.86, cx - rx * 0.02, cy - ry * 0.12],
               fill=sheen + (86,))
    sd.ellipse([cx - rx * 0.48, cy - ry * 0.66, cx - rx * 0.14, cy - ry * 0.30],
               fill=sheen + (70,))
    sheen_layer = sheen_layer.filter(ImageFilter.GaussianBlur(SS * 2.4))
    sheen_layer.putalpha(ImageChops.multiply(sheen_layer.split()[3], mask))
    body = Image.alpha_composite(body, sheen_layer)

    # bottom shading crescent for volume
    inner = body_mask(cx, cy - BIG * 0.045, rx * 0.965, ry * 0.945)
    crescent = ImageChops.subtract(mask, inner)
    crescent = crescent.filter(ImageFilter.GaussianBlur(SS * 2.0))
    shade = Image.new("RGBA", (BIG, BIG), ridge + (255,))
    shade.putalpha(ImageChops.multiply(crescent, Image.new("L", (BIG, BIG), 120)))
    body = Image.alpha_composite(body, shade)

    # cinnamon stem: slightly tapered rounded bar above the body
    stem = Image.new("RGBA", (BIG, BIG), (0, 0, 0, 0))
    st = ImageDraw.Draw(stem)
    sw = BIG * 0.052
    st.rounded_rectangle([cx - sw * 0.5, cy - ry - BIG * 0.125, cx + sw * 0.5, cy - ry + BIG * 0.045],
                         radius=sw * 0.45, fill=stem_col + (255,))
    stem = stem.filter(ImageFilter.GaussianBlur(SS * 0.45))
    body = Image.alpha_composite(body, stem)

    img = Image.alpha_composite(img, body)
    return img


def main():
    colors, props = load_colors()
    pumpkin = rgb(props["ntp_button_background"])     # pumpkin orange
    ridge = rgb(props["ntp_button_hover"])            # deeper pumpkin
    stem_col = rgb(colors["toolbar"])                 # cinnamon brown
    sheen = rgb(colors["ntp_background"])             # cream

    img = draw_pumpkin(pumpkin, ridge, stem_col, sheen)
    final = img.resize((SIZE, SIZE), Image.LANCZOS)
    os.makedirs(OUT_DIR, exist_ok=True)
    final.save(OUT)
    print("saved:", OUT, final.size, final.mode)


if __name__ == "__main__":
    main()
