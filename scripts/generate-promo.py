#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pumpkin Spice Theme — promo tiles (440x280 + 1400x560), all English.

Colours are read from manifest.json. Each canvas has its own geometry and font
scale; the layout is redrawn from scratch every run, with bounds assertions so
overflow fails loudly at generation time.
"""
import json
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
os.chdir(str(ROOT))                      # relative paths only (non-ASCII path safety)

OUT_DIR = "store-assets/promo"


def rgb(vals):
    return tuple(vals)


def font(size, bold=False):
    for name in (("segoeuib.ttf", "seguisb.ttf") if bold else ("segoeui.ttf", "segoeuisl.ttf")):
        p = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def text_w(d, s, f):
    return d.textbbox((0, 0), s, font=f)[2]


def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def bg_gradient(size, top, bottom):
    w, h = size
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        d.line([(0, y), (w, y)], fill=lerp(top, bottom, y / max(1, h - 1)))
    return img


def draw_chip(d, x, y, h, label, f, fill, txt, pad=18):
    w = text_w(d, label, f) + pad * 2
    d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=fill)
    d.text((x + pad, y + (h - f.size) // 2 - 3), label, font=f, fill=txt)
    return w


def compose(size, geom, colors):
    W, H = size
    M = geom["margin"]
    RIGHT = W - M

    img = bg_gradient(size, rgb(colors["ntp_background"]), rgb(colors["button_background"]))
    d = ImageDraw.Draw(img)

    ink = rgb(colors["ntp_text"])
    sub = lerp(ink, rgb(colors["ntp_background"]), 0.34)
    chip_bg = rgb(colors["ntp_header"])
    cta_bg = rgb(colors["frame"])
    cta_txt = rgb(colors["tab_text"])

    bar_colors = [rgb(colors["ntp_background"]), rgb(colors["button_background_secondary"]),
                  rgb(colors["button_background"]), rgb(colors["ntp_link"]),
                  rgb(colors["toolbar"]), rgb(colors["frame"])]
    bw, bgap = geom["bar_w"], geom["bar_gap"]
    bars_w = bw * len(bar_colors) + bgap * (len(bar_colors) - 1)
    bx, by = RIGHT - bars_w, geom["bar_y"]
    for i, col in enumerate(bar_colors):
        x0 = bx + i * (bw + bgap)
        d.rounded_rectangle([x0, by, x0 + bw, by + geom["bar_h"]], radius=bw // 3,
                            fill=col, outline=lerp(col, ink, 0.22), width=2)
    assert bx + bars_w <= RIGHT, "palette bars overflow the right margin"

    lsize = geom["logo"]
    logo = Image.open("logo/logo.png").convert("RGBA").resize((lsize, lsize), Image.LANCZOS)
    img.paste(logo, (M, geom["logo_y"]), logo)

    f_title, f_sub = font(geom["title_size"], True), font(geom["sub_size"])
    tx = M + (lsize + geom["logo_gap"] if geom["title_beside_logo"] else 0)
    ty = geom["title_y"] if geom["title_beside_logo"] else geom["logo_y"] + lsize + geom["logo_gap"]
    d.text((tx, ty), geom["title"], font=f_title, fill=ink)
    sub_y = ty + geom["title_size"] + geom["title_sub_gap"]
    d.text((tx if geom["title_beside_logo"] else M, sub_y), geom["subtitle"], font=f_sub, fill=sub)
    assert geom["title_sub_gap"] >= 8, "title/subtitle gap too tight"

    f_chip = font(geom["chip_size"])
    cx, cy = (tx if geom["title_beside_logo"] else M), sub_y + geom["sub_size"] + geom["chip_gap"]
    for label in geom["chips"]:
        w = draw_chip(d, cx, cy, geom["chip_h"], label, f_chip, chip_bg, ink)
        cx += w + geom["chip_gap_x"]
    assert cx - geom["chip_gap_x"] <= bx - 24, "chips collide with the palette bars"

    f_cta = font(geom["cta_size"], True)
    btn_w, btn_h = geom["cta_w"], geom["cta_h"]
    btn_x = M
    btn_y = geom["cta_y"] if geom["cta_beside"] else cy + geom["chip_h"] + geom["cta_gap"]
    d.rounded_rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + btn_h], radius=btn_h // 2, fill=cta_bg)
    tw = text_w(d, geom["cta"], f_cta)
    d.text((btn_x + (btn_w - tw) // 2, btn_y + (btn_h - f_cta.size) // 2 - 3),
           geom["cta"], font=f_cta, fill=cta_txt)
    assert btn_y + btn_h <= H - 12, "CTA button too close to the canvas bottom"
    assert btn_x + btn_w <= RIGHT, "CTA button overflows the right margin"
    assert btn_x + btn_w <= bx - 20, "CTA button collides with the palette bars"
    return img, {"btn": (btn_x, btn_y, btn_w, btn_h), "bars": (bx, by, bars_w, geom["bar_h"])}


LARGE = {
    "margin": 70,
    "logo": 104, "logo_y": 82, "logo_gap": 26, "title_beside_logo": True,
    "title": "Pumpkin Spice", "title_size": 58, "title_y": 98,
    "title_sub_gap": 14, "subtitle": "A cosy autumn Chrome theme", "sub_size": 21,
    "chips": ["Solid colors", "Warm earth palette", "Easy on the eyes"],
    "chip_size": 15, "chip_h": 34, "chip_gap": 34, "chip_gap_x": 12,
    "cta": "Try It Now", "cta_size": 20, "cta_w": 210, "cta_h": 54,
    "cta_y": 366, "cta_beside": True,
    "bar_w": 46, "bar_gap": 10, "bar_h": 300, "bar_y": 130,
}

SMALL = {
    "margin": 28,
    "logo": 46, "logo_y": 22, "logo_gap": 10, "title_beside_logo": False,
    "title": "Pumpkin Spice", "title_size": 26, "title_y": 0,
    "title_sub_gap": 8, "subtitle": "A cosy autumn Chrome theme", "sub_size": 12,
    "chips": ["Solid colors", "Warm earth palette"],
    "chip_size": 10, "chip_h": 22, "chip_gap": 12, "chip_gap_x": 8,
    "cta": "Try It Now", "cta_size": 13, "cta_w": 118, "cta_h": 36,
    "cta_y": 0, "cta_gap": 16, "cta_beside": False,
    "bar_w": 20, "bar_gap": 5, "bar_h": 120, "bar_y": 68,
}


def main():
    with open("manifest.json", "r", encoding="utf-8") as f:
        c = json.load(f)["theme"]["colors"]
    os.makedirs(OUT_DIR, exist_ok=True)
    for size, geom in (((1400, 560), LARGE), ((440, 280), SMALL)):
        img, boxes = compose(size, geom, c)
        out = "%s/%dx%d.png" % (OUT_DIR, size[0], size[1])
        img.save(out)
        print("saved:", out, img.size, img.mode, "cta:", boxes["btn"], "bars:", boxes["bars"])


if __name__ == "__main__":
    main()
