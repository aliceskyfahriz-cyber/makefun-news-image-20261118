#!/usr/bin/env python3
"""
News-image generator for the make.fun daily news-image bounty
"news-image-20261118" - "Sum up 18 November's world news in one image".

Draws a 1600x900 PNG news infographic from scratch using only Pillow
shapes, lines, fills, gradients and text. No photographs, no logos,
no pasted images, no network access, no API keys.

Run:  python3 generate.py   (writes output.png next to this file)
"""

from PIL import Image, ImageDraw, ImageFont
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output.png")

W, H = 1600, 900

# ---- palette ------------------------------------------------------------
BG_TOP = (13, 21, 38)        # deep navy
BG_BOT = (10, 16, 30)
PANEL = (22, 35, 61)          # card navy
PANEL_LINE = (48, 68, 104)
HERO_PANEL = (24, 40, 70)
INK = (240, 244, 252)         # near-white
MUTED = (159, 176, 204)       # grey-blue
AMBER = (242, 183, 5)         # accent gold
TEAL = (45, 212, 191)
RED = (248, 113, 113)
BLUE = (96, 165, 250)
GREEN = (74, 222, 128)
PURPLE = (192, 132, 252)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, text, fnt, fill, max_w, leading):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def rounded(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


# ---- story data (verified 18 Nov 2026 UTC, 2+ sources each) ------------
HERO = {
    "rank": "01",
    "tag": "SUMMIT  ·  SHENZHEN",
    "headline": "APEC opens in Shenzhen as Xi urges free and open trade",
    "summary": ("China's Xi Jinping opened the APEC summit calling for an end to "
                "trade and investment barriers and wider market access for foreign "
                "business - a day before the first-ever Trump-Xi-Putin trilateral "
                "meeting on nuclear arms."),
    "sources": "Reuters  ·  Bloomberg",
}

STORIES = [
    {
        "rank": "02",
        "tag": "GULF  ·  US-IRAN",
        "headline": "Bahrain and Kuwait intercept Iranian air attacks",
        "summary": ("Bahrain's air defences shot down Iranian aerial attacks early "
                    "Wednesday and Kuwait's army answered drone raids, a day after "
                    "US jets struck a missile site on Iran's Qeshm Island."),
        "sources": "Reuters  ·  Virgin Radio Dubai",
        "icon": "radar",
        "accent": RED,
    },
    {
        "rank": "03",
        "tag": "DIPLOMACY  ·  MANILA",
        "headline": "Trump holds state visit with Marcos in Manila",
        "summary": ("The US president received military honours at Malacanang and "
                    "held talks on trade and South China Sea security, before "
                    "flying to Shenzhen for APEC."),
        "sources": "GMA News  ·  Office of the President of the Philippines",
        "icon": "flags",
        "accent": BLUE,
    },
    {
        "rank": "04",
        "tag": "SPACE  ·  MILESTONE",
        "headline": "Voyager 1 reaches one light-day from Earth",
        "summary": ("At 10:16 UTC the 49-year-old probe became the first human-made "
                    "object one light-day away - 25.9 billion km out - so a radio "
                    "signal now takes 24 hours to reach it."),
        "sources": "NASA  ·  USA Today",
        "icon": "probe",
        "accent": TEAL,
    },
    {
        "rank": "05",
        "tag": "CULTURE  ·  FILM",
        "headline": "Bezos says he helped pick Pattinson as Bond",
        "summary": ("Amazon's Jeff Bezos said he was heavily involved in choosing "
                    "Robert Pattinson, 40, as the next 007 for the 26th Bond film, "
                    "directed by Denis Villeneuve."),
        "sources": "Reuters  ·  Finwire",
        "icon": "clapper",
        "accent": PURPLE,
    },
]


# ---- icons (shapes only) -------------------------------------------------
def icon_globe(d, cx, cy, r, col):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=5)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=None)
    d.ellipse([cx - int(r * 0.45), cy - r, cx + int(r * 0.45), cy + r],
              outline=col, width=4)
    d.line([cx - r, cy, cx + r, cy], fill=col, width=4)
    d.arc([cx - r, cy - int(r * 0.55), cx + r, cy + int(r * 0.55)],
          start=200, end=340, fill=col, width=4)
    d.arc([cx - r, cy - int(r * 0.55), cx + r, cy + int(r * 0.55)],
          start=20, end=160, fill=col, width=4)
    # skyline bars under the globe
    base = cy + r + 14
    for i, h in enumerate([26, 44, 34, 52, 30]):
        x0 = cx - 62 + i * 26
        d.rectangle([x0, base - h, x0 + 18, base], fill=col)


def icon_radar(d, cx, cy, r, col):
    for rr, w in ((r, 4), (int(r * 0.66), 3), (int(r * 0.33), 3)):
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=col, width=w)
    d.line([cx, cy, cx + int(r * 0.8), cy - int(r * 0.8)], fill=col, width=5)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=col)
    # incoming dots
    for dx, dy in ((-r - 18, -r + 6), (-r - 6, r - 14), (r + 14, r - 4)):
        d.ellipse([cx + dx - 5, cy + dy - 5, cx + dx + 5, cy + dy + 5],
                  outline=col, width=3)


def icon_flags(d, cx, cy, s, col):
    # two abstract pennant flags on poles (no national flag designs)
    # kept inside a ~100px tile centred on (cx, cy)
    d.line([cx - 26, cy - s, cx - 26, cy + s], fill=col, width=5)
    d.line([cx + 18, cy - s, cx + 18, cy + s], fill=col, width=5)
    d.polygon([(cx - 26, cy - s), (cx + 2, cy - s + 11), (cx - 26, cy - s + 24)],
              fill=col)
    d.polygon([(cx + 18, cy - s), (cx + 46, cy - s + 11), (cx + 18, cy - s + 24)],
              fill=AMBER)


def icon_probe(d, cx, cy, s, col):
    # spacecraft: triangular body, round window, dish, dotted path, stars
    d.polygon([(cx, cy - s), (cx + s, cy + s // 2), (cx - s, cy + s // 2)],
              outline=col, width=5)
    d.ellipse([cx - 12, cy - 14, cx + 12, cy + 10], outline=col, width=4)
    d.line([cx - s - 6, cy + s // 2 + 14, cx + s + 6, cy + s // 2 + 14],
           fill=col, width=4)
    # short dotted trail, kept inside the tile
    for dx, dy in ((-36, 30), (-24, 36), (-12, 40)):
        d.ellipse([cx + dx - 3, cy + dy - 3, cx + dx + 3, cy + dy + 3],
                  fill=MUTED)
    for sx, sy in ((cx + 42, cy - 38), (cx - 40, cy - 18),
                   (cx + 40, cy + 40)):
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=AMBER)


def icon_clapper(d, cx, cy, s, col):
    # film clapperboard
    d.rounded_rectangle([cx - s, cy - s // 2, cx + s, cy + s], radius=8,
                        outline=col, width=5)
    d.line([cx - s, cy - 6, cx + s, cy - 6], fill=col, width=4)
    for i in range(4):
        x0 = cx - s + 8 + i * (2 * s - 16) // 4
        d.line([x0, cy - s // 2 - 16, x0 + 16, cy - 6], fill=AMBER, width=6)
    d.line([cx - s, cy - s // 2 - 16, cx + s, cy - s // 2 - 16], fill=col, width=4)
    d.ellipse([cx - 14, cy + 18, cx + 14, cy + 46], outline=col, width=4)


ICONS = {"radar": icon_radar, "flags": icon_flags,
         "probe": icon_probe, "clapper": icon_clapper}


# ---- build ----------------------------------------------------------------
def build():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    # vertical gradient background
    for y in range(H):
        t = y / H
        col = tuple(int(BG_TOP[i] + (BG_BOT[i] - BG_TOP[i]) * t) for i in range(3))
        d.line([(0, y), (W, y)], fill=col)
    # faint world-map-ish dotted band (decorative dots, shapes only)
    for gx in range(60, W - 40, 46):
        for gy in (128, 150):
            d.ellipse([gx, gy, gx + 3, gy + 3], fill=(30, 46, 78))

    # ---- header ---------------------------------------------------------
    d.text((48, 34), "THE WORLD IN ONE DAY", font=font(46, bold=True), fill=INK)
    d.text((48, 92), "WEDNESDAY  ·  18 NOVEMBER 2026",
           font=font(21, bold=True), fill=AMBER)
    d.text((W - 48, 44), "GLOBAL EDITION", font=font(20, bold=True),
           fill=MUTED, anchor="ra")
    d.text((W - 48, 76), "5 stories  ·  all first published 18 Nov 2026 (UTC)",
           font=font(16), fill=MUTED, anchor="ra")
    d.line([(48, 128), (W - 48, 128)], fill=AMBER, width=3)

    # ---- hero story -----------------------------------------------------
    hx, hy, hw, hh = 48, 152, 1504, 268
    rounded(d, [hx, hy, hx + hw, hy + hh], 18, fill=HERO_PANEL,
            outline=PANEL_LINE, width=2)
    # left icon tile
    ix, iy, iw, ih = hx + 24, hy + 24, 220, 220
    rounded(d, [ix, iy, ix + iw, iy + ih], 14, fill=(16, 28, 52))
    icon_globe(d, ix + iw // 2, iy + 92, 58, AMBER)
    d.text((ix + iw // 2, iy + ih - 26), "APEC · SHENZHEN",
           font=font(15, bold=True), fill=AMBER, anchor="ma")
    tx = hx + 272
    d.text((tx, hy + 26), "01  ·  SUMMIT", font=font(17, bold=True), fill=AMBER)
    y = draw_text_block(d, tx, hy + 56, HERO["headline"], font(31, bold=True),
                        INK, 1180, 40)
    y = draw_text_block(d, tx, y + 10, HERO["summary"], font(19),
                        (205, 216, 235), 1180, 27)
    d.text((tx, hy + hh - 34), "Sources:  " + HERO["sources"],
           font=font(15), fill=MUTED)

    # ---- grid of 4 stories ----------------------------------------------
    gx0, gy0 = 48, 444
    cw, ch, gap = 742, 168, 20
    for i, s in enumerate(STORIES):
        x = gx0 + (i % 2) * (cw + gap)
        y = gy0 + (i // 2) * (ch + gap)
        rounded(d, [x, y, x + cw, y + ch], 16, fill=PANEL,
                outline=PANEL_LINE, width=2)
        d.line([(x, y + 4), (x, y + ch - 4)], fill=s["accent"], width=5)
        # icon tile
        ix, iy = x + 20, y + 20
        rounded(d, [ix, iy, ix + 108, iy + 108], 12, fill=(16, 28, 52))
        fn = ICONS[s["icon"]]
        if s["icon"] == "radar":
            fn(d, ix + 54, iy + 54, 34, s["accent"])
        elif s["icon"] == "flags":
            fn(d, ix + 54, iy + 54, 34, s["accent"])
        elif s["icon"] == "probe":
            fn(d, ix + 54, iy + 50, 30, s["accent"])
        else:
            fn(d, ix + 54, iy + 54, 34, s["accent"])
        tx = x + 148
        d.text((tx, y + 16), f"{s['rank']}  ·  {s['tag']}",
               font=font(14, bold=True), fill=s["accent"])
        yy = draw_text_block(d, tx, y + 40, s["headline"], font(20, bold=True),
                             INK, 574, 25)
        draw_text_block(d, tx, yy + 4, s["summary"], font(14),
                        (205, 216, 235), 574, 19)
        d.text((tx, y + ch - 26), "Sources:  " + s["sources"],
               font=font(12), fill=MUTED)

    # ---- footer ---------------------------------------------------------
    d.line([(48, 832), (W - 48, 832)], fill=PANEL_LINE, width=2)
    d.text((48, 848),
           "Sources: Reuters · Bloomberg · Virgin Radio Dubai · GMA News · "
           "Office of the President of the Philippines · NASA · USA Today · Finwire",
           font=font(14), fill=MUTED)
    d.text((48, 872),
           "Every story was first published on 18 November 2026 (UTC). "
           "All graphics are drawn from shapes, lines and text only - no photographs.",
           font=font(14), fill=MUTED)

    img.save(OUT, "PNG")
    return OUT


if __name__ == "__main__":
    path = build()
    print("wrote", path, os.path.getsize(path), "bytes")
