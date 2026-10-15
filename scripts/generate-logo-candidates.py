#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pumpkin Spice Theme — logo candidates (code-drawn, reproducible).

Draws every candidate at 4x, downscales with LANCZOS, writes:
  logo/candidates/NN-name.png        256x256 preview per candidate
  logo/candidates/contact-light.png  3x2 contact sheet on a cream background
  logo/candidates/contact-dark.png   3x2 contact sheet on an espresso background
  logo/candidates/inline-strip.png   one-row strip of all candidates
  logo/logo.png                      128x128 official icon = SELECTED candidate

All colours are read from manifest.json. Change SELECTED and re-run to ship a
different candidate — never hand-copy PNGs.

Usage:
    py -3 scripts/generate-logo-candidates.py            # previews + SELECTED icon
    py -3 scripts/generate-logo-candidates.py --sheet     # only the sheets (default: all)
"""
import json
import math
import os
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
os.chdir(str(ROOT))                      # relative paths only (non-ASCII path safety)

SIZE = 128                               # official icon size
SS = 4                                   # supersampling factor
BIG = SIZE * SS * 4                      # 2048 drawing canvas (512 preview = /4)
PREVIEW = 256                            # per-candidate preview size
SELECTED = "01"                          # <- which candidate becomes logo/logo.png

CAND_DIR = Path("logo/candidates")
LOGO_OUT = Path("logo/logo.png")


def load_manifest():
    with open("manifest.json", "r", encoding="utf-8") as f:
        m = json.load(f)
    return m["theme"]["colors"], m["theme"]["properties"]


COLORS, PROPS = load_manifest()
ESPRESSO = tuple(COLORS["frame"])
CINNAMON = tuple(COLORS["toolbar"])
CREAM = tuple(COLORS["ntp_background"])
OAT = tuple(COLORS["button_background"])
PUMPKIN = tuple(PROPS["ntp_button_background"])
DEEP_PUMPKIN = tuple(PROPS["ntp_button_hover"])
INK = tuple(COLORS["tab_text"])


def layer():
    return Image.new("RGBA", (BIG, BIG), (0, 0, 0, 0))


def downsample(img, size):
    return img.resize((size, size), Image.LANCZOS)


def ellipse_mask(cx, cy, rx, ry):
    m = Image.new("L", (BIG, BIG), 0)
    ImageDraw.Draw(m).ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=255)
    return m


def clip(layer_img, mask):
    layer_img.putalpha(ImageChops.multiply(layer_img.split()[3], mask))
    return layer_img


def wavy(d, x0, x1, y0, y1, amp, color, width, phase=0.0, freq=1.5):
    pts = []
    n = 60
    for i in range(n + 1):
        t = i / n
        y = y0 + (y1 - y0) * t
        x = x0 + (x1 - x0) * t + amp * math.sin(2 * math.pi * freq * t + phase)
        pts.append((x, y))
    d.line(pts, fill=color, width=width, joint="curve")


def spiral(d, cx, cy, r0, r1, turns, color, width):
    pts = []
    n = 260
    for i in range(n + 1):
        t = i / n
        th = 2 * math.pi * turns * t
        r = r0 + (r1 - r0) * t
        pts.append((cx + r * math.cos(th), cy + r * math.sin(th) * 0.96))
    d.line(pts, fill=color, width=width, joint="curve")


def rotated_bar(angle_deg, cx, cy, w, h, radius, fill, inner=None):
    """Rounded bar rotated about its own centre; returns an RGBA layer."""
    lay = layer()
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2],
                        radius=radius, fill=fill + (255,))
    if inner:
        d.rounded_rectangle([cx - w * 0.18, cy - h * 0.40, cx + w * 0.18, cy + h * 0.40],
                            radius=radius * 0.6, fill=inner + (150,))
    return lay.rotate(angle_deg, resample=Image.BICUBIC, center=(cx, cy))


def star_polygon(cx, cy, r_out, r_in, points, rotate_deg=0.0):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rotate_deg + i * 180.0 / points)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


# ---------------------------------------------------------------- candidates
def cand_pumpkin():
    """01 ridged pumpkin — the current direction, refined."""
    img = layer()
    cx, cy, rx, ry = BIG * 0.50, BIG * 0.585, BIG * 0.375, BIG * 0.300
    mask = ellipse_mask(cx, cy, rx, ry)
    body = layer()
    ImageDraw.Draw(body).ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=PUMPKIN + (255,))

    ridges = layer()
    rd = ImageDraw.Draw(ridges)
    for k in (-0.56, -0.19, 0.19, 0.56):
        ex, ew = cx + k * rx, rx * 0.28
        rd.ellipse([ex - ew, cy - ry * 0.98, ex + ew, cy + ry * 0.98],
                   outline=DEEP_PUMPKIN + (240,), width=int(BIG * 0.017))
    body = Image.alpha_composite(body, clip(ridges, mask))

    sheen = layer()
    sd = ImageDraw.Draw(sheen)
    sd.ellipse([cx - rx * 0.74, cy - ry * 0.88, cx - rx * 0.04, cy - ry * 0.14], fill=CREAM + (92,))
    sd.ellipse([cx - rx * 0.50, cy - ry * 0.62, cx - rx * 0.16, cy - ry * 0.28], fill=CREAM + (76,))
    sheen = sheen.filter(ImageFilter.GaussianBlur(BIG * 0.006))
    body = Image.alpha_composite(body, clip(sheen, mask))

    shade = Image.new("RGBA", (BIG, BIG), DEEP_PUMPKIN + (255,))
    crescent = ImageChops.subtract(mask, ellipse_mask(cx, cy - BIG * 0.042, rx * 0.965, ry * 0.945))
    shade.putalpha(ImageChops.multiply(crescent.filter(ImageFilter.GaussianBlur(BIG * 0.005)),
                                       Image.new("L", (BIG, BIG), 125)))
    body = Image.alpha_composite(body, shade)

    stem = layer()
    sw = BIG * 0.050
    ImageDraw.Draw(stem).rounded_rectangle(
        [cx - sw * 0.5, cy - ry - BIG * 0.120, cx + sw * 0.5, cy - ry + BIG * 0.040],
        radius=sw * 0.45, fill=CINNAMON + (255,))
    body = Image.alpha_composite(body, stem.filter(ImageFilter.GaussianBlur(BIG * 0.0011)))
    return Image.alpha_composite(img, body)


def cand_badge():
    """02 pumpkin in an espresso badge — strongest at 32px."""
    img = layer()
    d = ImageDraw.Draw(img)
    d.ellipse([BIG * 0.075, BIG * 0.075, BIG * 0.925, BIG * 0.925], fill=ESPRESSO + (255,))

    cx, cy, rx, ry = BIG * 0.50, BIG * 0.565, BIG * 0.255, BIG * 0.205
    mask = ellipse_mask(cx, cy, rx, ry)
    body = layer()
    ImageDraw.Draw(body).ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=PUMPKIN + (255,))
    ridges = layer()
    rd = ImageDraw.Draw(ridges)
    for k in (-0.52, 0.0, 0.52):
        ex, ew = cx + k * rx, rx * 0.24
        rd.ellipse([ex - ew, cy - ry * 0.97, ex + ew, cy + ry * 0.97],
                   outline=DEEP_PUMPKIN + (250,), width=int(BIG * 0.015))
    body = Image.alpha_composite(body, clip(ridges, mask))
    stem = layer()
    sw = BIG * 0.044
    ImageDraw.Draw(stem).rounded_rectangle(
        [cx - sw * 0.5, cy - ry - BIG * 0.115, cx + sw * 0.5, cy - ry + BIG * 0.030],
        radius=sw * 0.45, fill=OAT + (255,))
    body = Image.alpha_composite(body, stem)
    return Image.alpha_composite(img, body)


def cand_latte():
    """03 mug with steam — the moodboard's coffee cup."""
    img = layer()
    d = ImageDraw.Draw(img)

    steam = layer()
    sd = ImageDraw.Draw(steam)
    for i, x0 in enumerate((BIG * 0.365, BIG * 0.50, BIG * 0.635)):
        wavy(sd, x0, x0, BIG * 0.20, BIG * 0.40, BIG * 0.030, CINNAMON + (215,),
             int(BIG * 0.022), phase=i * 0.9)
    steam = steam.filter(ImageFilter.GaussianBlur(BIG * 0.002))
    img = Image.alpha_composite(img, steam)

    body = layer()
    bd = ImageDraw.Draw(body)
    cup = [BIG * 0.285, BIG * 0.435, BIG * 0.715, BIG * 0.855]
    bd.rounded_rectangle(cup, radius=BIG * 0.075, fill=CREAM + (255,))
    bd.rounded_rectangle(cup, radius=BIG * 0.075, outline=ESPRESSO + (255,), width=int(BIG * 0.026))
    cup_mask = Image.new("L", (BIG, BIG), 0)
    ImageDraw.Draw(cup_mask).rounded_rectangle(cup, radius=BIG * 0.075, fill=255)
    band = layer()
    ImageDraw.Draw(band).rectangle([cup[0], BIG * 0.470, cup[2], BIG * 0.530], fill=CINNAMON + (255,))
    body = Image.alpha_composite(body, clip(band, cup_mask))
    bd = ImageDraw.Draw(body)
    bd.arc([BIG * 0.660, BIG * 0.520, BIG * 0.905, BIG * 0.760], start=-72, end=72,
           fill=ESPRESSO + (255,), width=int(BIG * 0.030))
    img = Image.alpha_composite(img, body)
    return img


def cand_swirl():
    """04 spice swirl — abstract cinnamon-roll spiral, no objects."""
    img = layer()
    d = ImageDraw.Draw(img)
    spiral(d, BIG * 0.50, BIG * 0.50, BIG * 0.075, BIG * 0.385, 2.6, PUMPKIN + (255,),
           int(BIG * 0.075))
    d.ellipse([BIG * 0.50 - BIG * 0.070, BIG * 0.50 - BIG * 0.070,
               BIG * 0.50 + BIG * 0.070, BIG * 0.50 + BIG * 0.070], fill=CINNAMON + (255,))
    d.ellipse([BIG * 0.50 - BIG * 0.026, BIG * 0.50 - BIG * 0.026,
               BIG * 0.50 + BIG * 0.026, BIG * 0.50 + BIG * 0.026], fill=OAT + (255,))
    return img


def cand_cinnamon():
    """05 crossed cinnamon sticks + star anise."""
    img = layer()
    img = Image.alpha_composite(img, rotated_bar(34, BIG * 0.44, BIG * 0.60, BIG * 0.115,
                                                 BIG * 0.62, BIG * 0.055, CINNAMON, OAT))
    img = Image.alpha_composite(img, rotated_bar(-34, BIG * 0.56, BIG * 0.60, BIG * 0.115,
                                                 BIG * 0.62, BIG * 0.055, CINNAMON, OAT))
    d = ImageDraw.Draw(img)
    d.polygon(star_polygon(BIG * 0.50, BIG * 0.365, BIG * 0.175, BIG * 0.070, 8, 22), fill=ESPRESSO + (255,))
    d.ellipse([BIG * 0.50 - BIG * 0.040, BIG * 0.365 - BIG * 0.040,
               BIG * 0.50 + BIG * 0.040, BIG * 0.365 + BIG * 0.040], fill=PUMPKIN + (255,))
    d.ellipse([BIG * 0.50 - BIG * 0.015, BIG * 0.365 - BIG * 0.015,
               BIG * 0.50 + BIG * 0.015, BIG * 0.365 + BIG * 0.015], fill=ESPRESSO + (255,))
    return img


def cand_pie():
    """06 pumpkin pie slice with a cream dollop."""
    img = layer()
    apex = (BIG * 0.50, BIG * 0.820)
    r_out = BIG * 0.400
    a0, a1 = 215.0, 325.0
    pts = [apex]
    for i in range(41):
        a = math.radians(a0 + (a1 - a0) * i / 40)
        pts.append((apex[0] + r_out * math.cos(a), apex[1] + r_out * math.sin(a)))
    d = ImageDraw.Draw(img)
    d.polygon(pts, fill=PUMPKIN + (255,))
    d.line(pts[1:], fill=DEEP_PUMPKIN + (255,), width=int(BIG * 0.018), joint="curve")

    crust = layer()
    cd = ImageDraw.Draw(crust)
    rr = r_out * 0.94
    cd.arc([apex[0] - rr, apex[1] - rr, apex[0] + rr, apex[1] + rr],
           start=a0, end=a1, fill=CINNAMON + (255,), width=int(BIG * 0.090))
    img = Image.alpha_composite(img, crust)

    dollop = layer()
    dd = ImageDraw.Draw(dollop)
    pad = BIG * 0.008
    for dx, dy in ((0.0, 0.045), (-0.045, 0.030), (0.045, 0.030), (0.0, 0.005)):
        dd.ellipse([BIG * (0.50 + dx) - BIG * 0.058 + pad, BIG * (0.655 + dy) - BIG * 0.058 + pad,
                    BIG * (0.50 + dx) + BIG * 0.058 - pad, BIG * (0.655 + dy) + BIG * 0.058 - pad],
                   fill=CREAM + (255,))
    img = Image.alpha_composite(img, dollop)
    d = ImageDraw.Draw(img)
    for dx, dy in ((-0.030, -0.020), (0.026, -0.032), (-0.006, -0.048)):
        d.ellipse([BIG * (0.50 + dx) - BIG * 0.009, BIG * (0.645 + dy) - BIG * 0.009,
                   BIG * (0.50 + dx) + BIG * 0.009, BIG * (0.645 + dy) + BIG * 0.009],
                  fill=CINNAMON + (235,))
    return img


CANDIDATES = [
    ("01", "pumpkin-ridged", "Ridged pumpkin — the current direction, crisper ridges", cand_pumpkin),
    ("02", "pumpkin-badge", "Pumpkin inside an espresso badge — boldest at 32px", cand_badge),
    ("03", "latte-steam", "Mug with rising steam — straight from the moodboard", cand_latte),
    ("04", "spice-swirl", "Cinnamon-roll swirl — fully abstract, most modern", cand_swirl),
    ("05", "cinnamon-star", "Crossed cinnamon sticks + star anise — most 'spice'", cand_cinnamon),
    ("06", "pie-slice", "Pumpkin pie slice with cream — warmest, most playful", cand_pie),
]


def font(size, bold=False):
    for name in (("segoeuib.ttf", "seguisb.ttf") if bold else ("segoeui.ttf", "segoeuisl.ttf")):
        p = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def assert_bounds(img, name):
    bbox = img.split()[3].getbbox()
    assert bbox, "candidate %s rendered empty" % name
    lo, hi = BIG * 0.055, BIG * 0.945
    assert bbox[0] >= lo and bbox[1] >= lo and bbox[2] <= hi and bbox[3] <= hi, \
        "candidate %s exceeds the safe margin: %s" % (name, bbox)
    return bbox


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
    for i, (num, name, desc, _) in enumerate(CANDIDATES):
        r, c = divmod(i, cols)
        x = margin + c * (cw + gap)
        y = y0 + r * (ch + gap)
        img = rendered[num]
        big = img.resize((220, 220), Image.LANCZOS)
        sheet.paste(big, (x + (cw - 220) // 2, y + 14), big)
        d.text((x + 18, y + 250), "%s · %s" % (num, name), font=f_name, fill=txt)
        d.text((x + 18, y + 280), desc, font=f_desc, fill=sub)
        thumb = img.resize((32, 32), Image.LANCZOS)
        sheet.paste(thumb, (x + 18, y + 330), thumb)
        d.text((x + 60, y + 339), "%s.png  256x256" % name, font=f_file, fill=sub)
        assert y + 280 + 20 <= y + 330 - 8, "text block collides with the 32px thumbnail row"
        assert x + cw <= W - margin + 1, "cell overflows the sheet"
    sheet.save(path)
    print("saved:", path, sheet.size)


def inline_strip(rendered, path):
    n, cell, gap, margin = len(CANDIDATES), 108, 22, 30
    W = margin * 2 + n * cell + (n - 1) * gap
    H = margin * 2 + cell + 30
    strip = Image.new("RGB", (W, H), (247, 243, 236))
    d = ImageDraw.Draw(strip)
    f = font(15, True)
    for i, (num, _name, _desc, _fn) in enumerate(CANDIDATES):
        x = margin + i * (cell + gap)
        img = rendered[num].resize((cell, cell), Image.LANCZOS)
        strip.paste(img, (x, margin), img)
        d.text((x + cell // 2 - 8, margin + cell + 8), num, font=f, fill=(58, 42, 33))
    strip.save(path)
    print("saved:", path, strip.size)


def main():
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    rendered = {}
    for num, name, _desc, fn in CANDIDATES:
        img = fn()
        bbox = assert_bounds(img, name)
        small = downsample(img, PREVIEW)
        small.save(CAND_DIR / ("%s-%s.png" % (num, name)))
        rendered[num] = small
        print("candidate %s %s -> alpha bbox %s" % (num, name, bbox))

    contact_sheet(rendered, (247, 243, 236), (58, 42, 33), (122, 96, 72),
                  CAND_DIR / "contact-light.png", "Pumpkin Spice — logo candidates (light)")
    contact_sheet(rendered, (36, 26, 19), (245, 239, 226), (196, 170, 142),
                  CAND_DIR / "contact-dark.png", "Pumpkin Spice — logo candidates (dark)")
    inline_strip(rendered, CAND_DIR / "inline-strip.png")

    sel = [c for c in CANDIDATES if c[0] == SELECTED][0]
    sel_img = downsample(sel[3](), SIZE)
    sel_img.save(LOGO_OUT)
    print("official icon from SELECTED=%s (%s):" % (sel[0], sel[1]), LOGO_OUT, sel_img.size)


if __name__ == "__main__":
    main()
