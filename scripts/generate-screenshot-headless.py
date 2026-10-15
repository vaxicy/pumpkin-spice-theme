#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pumpkin Spice Theme — store screenshot #1 (browser mockup via headless Chromium).

1280x800 RGB. Theme-controlled surfaces read manifest.json; browser-owned
elements are literal hex calibrated from the user's real screenshot (1080x642).

Calibrated against the real browser (2026-10-16):
  frame #3A2A21 (manifest)      toolbar/bookmark bar #6B4A33 (manifest)
  NTP background #F4EEE2 (manifest)   omnibox pill #F7F2E7 (manifest, verified)
  Google single-colour logo  #CDB27C   shortcut circle #DAC69E   YouTube #FF0033
  Customize pill #202124 + white label
Layout targets are the real screenshot's own proportions (% of window height):
  logo glyph 31.3-42.1%  ·  search pill 47.2-52.8% (54.5% wide)
  shortcut circles 57.3-63.1%  ·  customize pill bottom 98.3%
"""
import json
import os
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
os.chdir(str(ROOT))                      # relative paths only (non-ASCII path safety)
MANIFEST = Path("manifest.json")
OUT = Path("store-assets/screenshots/en")
OUT.mkdir(parents=True, exist_ok=True)


def colors():
    d = json.loads(MANIFEST.read_text(encoding="utf-8"))
    c = d["theme"]["colors"]

    def rgb(k):
        return "rgb(%d,%d,%d)" % tuple(c[k])

    return {
        "frame":    rgb("frame"),
        "toolbar":  rgb("toolbar"),
        "omni":     rgb("omnibox_background"),
        "ntp_bg":   rgb("ntp_background"),
        "ink":      rgb("ntp_text"),
        "tab_text": rgb("tab_text"),
        # calibrated browser-owned literals
        "logo":     "#CDB27C",
        "circle":   "#DAC69E",
        "yt":       "#FF0033",
        "label":    "#4A3A2E",
        "custom":   "#202124",
        "chrome_ic": "#EFE6D8",
    }


C = colors()
NB = C["tab_text"]                        # cream ink on the dark chrome


def data_svg(body, w=16, h=16):
    return "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='%d' height='%d' viewBox='0 0 16 16'>%s</svg>" % (w, h, body)


BACK = data_svg("<path d='M7 2L2 7l5 5V8.5h7v-3H7z' fill='%23EFE6D8'/>")
FWD = data_svg("<path d='M9 2l5 5-5 5V8.5H2v-3h7z' fill='%23EFE6D8'/>")
RELOAD = data_svg("<path d='M8 2a6 6 0 1 0 5.7 4.2h-2.1A4 4 0 1 1 8 4v2l3-3-3-3z' fill='%23EFE6D8'/>")
HOME = data_svg("<path d='M8 1.5L1 7h2v7h4V9h2v5h4V7h2z' fill='%23EFE6D8'/>")
MIC = data_svg("<path d='M8 1.5A2.5 2.5 0 0 0 5.5 4v4a2.5 2.5 0 0 0 5 0V4A2.5 2.5 0 0 0 8 1.5zM13 8v.5a5 5 0 0 1-4 4.9V15H7v-1.6a5 5 0 0 1-4-4.9V8h1.5v.5a3.5 3.5 0 0 0 7 0V8H13z' fill='%234A3A2E'/>")
LENS = data_svg("<path d='M7 2a5 5 0 1 0 3 9l3.5 3.5 1-1L11 10a5 5 0 0 0-4-8zm0 1.6A3.4 3.4 0 1 1 7 10.4 3.4 3.4 0 0 1 7 3.6z' fill='%234A3A2E'/>")
GRID = data_svg("<g fill='%234A3A2E'><circle cx='4' cy='4' r='1.8'/><circle cx='9' cy='4' r='1.8'/><circle cx='14' cy='4' r='1.8'/><circle cx='4' cy='9' r='1.8'/><circle cx='9' cy='9' r='1.8'/><circle cx='14' cy='9' r='1.8'/><circle cx='4' cy='14' r='1.8'/><circle cx='9' cy='14' r='1.8'/><circle cx='14' cy='14' r='1.8'/></g>", 18, 18)
PUZZLE = data_svg("<path d='M6 1.5a1.8 1.8 0 0 1 1.8 1.8V4h2.4v2.4h.7a1.8 1.8 0 1 1 0 3.6h-.7V13H7.8v-1.1a1.8 1.8 0 1 0-3.6 0V13H1.5V9.9h1a1.8 1.8 0 1 0 0-3.6h-1V2.9h2.7v-.6A1.8 1.8 0 0 1 6 1.5z' fill='%23EFE6D8'/>")
FOLDER = data_svg("<path d='M1.5 3h5l1.5 2h6.5v8h-13z' fill='%23E0B070'/>", 14, 14)
STAR = data_svg("<path d='M8 1l2 4.6 5 .4-3.8 3.3 1.2 4.9L8 11.6 3.6 14.2l1.2-4.9L1 6l5-.4z' fill='%23E8C071'/>", 14, 14)
DOWN = data_svg("<path d='M8 1.5a4.6 4.6 0 0 0-4.6 4.6v3.2L1.6 12.5h12.8l-1.8-3.2V6.1A4.6 4.6 0 0 0 8 1.5zM6.2 13.7a1.8 1.8 0 0 0 3.6 0z' fill='%23EFE6D8'/>", 14, 14)
PENCIL = data_svg("<path d='M11.3 1.5l3.2 3.2-8.6 8.6-3.9.7.7-3.9z' fill='%238AB4F8'/>", 13, 13)

CWS = ("<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 20 20'>"
       "<path d='M10 10 L1.1 5.05 A9 9 0 0 1 9.3 1.02 Z' fill='#DC5549'/>"
       "<path d='M10 10 L9.3 1.02 A9 9 0 0 1 18.9 5.05 Z' fill='#F4B400'/>"
       "<path d='M10 10 L18.9 5.05 A9 9 0 0 1 18.9 14.95 Z' fill='#F4B400'/>"
       "<path d='M10 10 L18.9 14.95 A9 9 0 0 1 1.1 14.95 Z' fill='#0F9D58'/>"
       "<path d='M10 10 L1.1 14.95 A9 9 0 0 1 1.1 5.05 Z' fill='#0F9D58'/>"
       "<path d='M10 10 L1.1 5.05 A9 9 0 0 1 9.3 1.02 Z' fill='#DC5549'/>"
       "<circle cx='10' cy='10' r='4.1' fill='#FFFFFF'/>"
       "<circle cx='10' cy='10' r='3.0' fill='#4285F4'/></svg>")
YT = ("<svg xmlns='http://www.w3.org/2000/svg' width='22' height='16' viewBox='0 0 22 16'>"
      "<rect x='0' y='0' width='22' height='16' rx='4' fill='#FF0033'/>"
      "<path d='M8.6 4.4l6 3.6-6 3.6z' fill='#FFFFFF'/></svg>")

HTML = f"""
<!doctype html><html><head><meta charset="utf-8"><style>
* {{ margin:0; padding:0; box-sizing:border-box; font-family:'Segoe UI',Arial,sans-serif; }}
body {{ width:1280px; height:800px; background:{C['ntp_bg']}; overflow:hidden; }}
.tabstrip {{ height:44px; background:{C['frame']}; display:flex; align-items:flex-end;
             padding:0 0 0 10px; gap:2px; position:relative; }}
.tab {{ flex:0 0 auto; height:28px; display:flex; align-items:center; gap:7px;
        padding:0 13px; border-radius:8px 8px 0 0; font-size:11.5px; color:{NB}; opacity:.75; }}
.tab.active {{ height:34px; background:{C['toolbar']}; color:{NB}; opacity:1; font-weight:600; }}
.tab .fav {{ width:11px; height:11px; border-radius:3px; background:#8A6A50; }}
.wctl {{ position:absolute; right:10px; top:3px; display:flex; gap:15px; color:{NB}; font-size:12px; }}
.toolbar {{ height:48px; background:{C['toolbar']}; display:flex; align-items:center;
            padding:0 10px; gap:6px; }}
.tbtn {{ width:27px; height:27px; border-radius:50%; display:flex; align-items:center; justify-content:center; }}
.tbtn img {{ width:15px; height:15px; }}
.omnibox {{ flex:1; height:32px; margin:0 8px; background:{C['omni']}; border-radius:16px;
            display:flex; align-items:center; padding:0 6px 0 13px; gap:8px;
            color:{C['label']}; font-size:12px; }}
.ob-right {{ margin-left:auto; display:flex; align-items:center; gap:6px; }}
.ob-ico {{ width:25px; height:25px; display:flex; align-items:center; justify-content:center; }}
.ob-ico img {{ width:14px; height:14px; }}
.avatar {{ width:25px; height:25px; border-radius:50%; background:#8A4A22; color:#F7F2E7;
           font-size:11px; font-weight:600; display:flex; align-items:center; justify-content:center; }}
.bm {{ height:28px; background:{C['toolbar']}; display:flex; align-items:center; gap:20px; padding:0 14px; }}
.bm a {{ display:flex; align-items:center; gap:6px; font-size:11px; color:{NB}; opacity:.9; text-decoration:none; }}
.bm img {{ width:13px; height:13px; }}
.ntp {{ position:relative; height:680px; background:{C['ntp_bg']}; }}
.nav {{ position:absolute; top:38px; right:46px; display:flex; align-items:center; gap:20px;
        font-size:12px; color:{C['label']}; }}
.nav img {{ width:16px; height:16px; display:block; }}
.logo {{ position:absolute; top:101px; left:0; right:0; text-align:center; font-size:84px;
         font-weight:500; letter-spacing:-2px; color:{C['logo']};
         font-family:'Product Sans','Segoe UI',Arial,sans-serif; }}
.search {{ position:absolute; top:258px; left:50%; transform:translateX(-50%); width:700px;
           height:45px; background:#FFFFFF; border-radius:23px; display:flex; align-items:center;
           padding:0 20px; gap:12px; font-size:14px; color:{C['label']};
           box-shadow:0 1px 6px rgba(0,0,0,0.12); }}
.search img {{ width:15px; height:15px; }}
.shortcuts {{ position:absolute; top:338px; left:0; right:0; display:flex; justify-content:center; gap:10px; }}
.sc {{ width:96px; display:flex; flex-direction:column; align-items:center; gap:12px; }}
.circ {{ width:47px; height:47px; border-radius:50%; background:{C['circle']};
         display:flex; align-items:center; justify-content:center; }}
.circ svg {{ display:block; }}
.plus {{ color:{C['label']}; font-size:22px; font-weight:600; line-height:1; }}
.sclabel {{ font-size:12px; color:{C['label']}; }}
.customize {{ position:absolute; right:15px; bottom:14px; height:30px; padding:0 15px;
              background:{C['custom']}; color:#fff; font-size:11.5px; border-radius:15px;
              display:flex; align-items:center; gap:8px; }}
.customize img {{ width:13px; height:13px; display:block; }}
</style></head><body>
<div class="tabstrip">
  <div class="tab"><span class="fav"></span>Color Palette</div>
  <div class="tab"><span class="fav"></span>Theme Bake</div>
  <div class="tab"><span class="fav"></span>CrowdCity</div>
  <div class="tab active">New Tab</div>
  <div class="wctl"><span>&#8722;</span><span>&#9633;</span><span>&#10005;</span></div>
</div>
<div class="toolbar">
  <div class="tbtn"><img src="{BACK}"></div>
  <div class="tbtn"><img src="{FWD}"></div>
  <div class="tbtn"><img src="{RELOAD}"></div>
  <div class="tbtn"><img src="{HOME}"></div>
  <div class="omnibox">
    <span>Search Google or type a URL</span>
    <div class="ob-right">
      <div class="ob-ico"><img src="{MIC}"></div>
      <div class="ob-ico"><img src="{LENS}"></div>
    </div>
  </div>
  <div class="tbtn"><img src="{PUZZLE}"></div>
  <div class="avatar">A</div>
</div>
<div class="bm">
  <a href="#"><img src="{FOLDER}">Folders</a>
  <a href="#"><img src="{STAR}">Favorites</a>
  <a href="#"><img src="{DOWN}">Downloads</a>
  <a href="#">Dev</a>
</div>
<div class="ntp">
  <div class="nav"><span>Images</span><img src="{GRID}"></div>
  <div class="logo">Google</div>
  <div class="search"><img src="{LENS}"><span>Search Google or type a URL</span></div>
  <div class="shortcuts">
    <div class="sc"><div class="circ">{YT}</div><div class="sclabel">YouTube</div></div>
    <div class="sc"><div class="circ">{CWS}</div><div class="sclabel">Web Store</div></div>
    <div class="sc"><div class="circ"><span class="plus">+</span></div><div class="sclabel">Add shortcut</div></div>
  </div>
  <div class="customize"><img src="{PENCIL}">Customize Chrome</div>
</div>
</body></html>
"""


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1280, "height": 800})
        pg.set_content(HTML)
        out = OUT / "screenshot-1-browser.png"
        pg.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": 1280, "height": 800})
        from PIL import Image
        im = Image.open(out).convert("RGB")
        im.save(out, "PNG")
        b.close()
        print("screenshot:", out, im.size, im.mode)


if __name__ == "__main__":
    main()
