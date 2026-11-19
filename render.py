#!/usr/bin/env python3
"""Draw entry.png for the make.fun news-image-20261119 bounty.

A 1024x1024 infographic that sums up Thursday 19 November 2026:
a date header and six story panels. Each panel carries a flat icon
built from Pillow primitives, a short headline and one factual line.
No photos, no downloaded assets, no network access.

Deterministic by construction: fixed layout, fixed fonts, no random
numbers, so running it again writes the same PNG bytes.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

SIZE = 1024

FONT_DIR = "/usr/share/fonts/truetype/noto"
F_BLACK = os.path.join(FONT_DIR, "NotoSans-Black.ttf")
F_BOLD = os.path.join(FONT_DIR, "NotoSans-Bold.ttf")
F_REG = os.path.join(FONT_DIR, "NotoSans-Regular.ttf")

INK = (19, 27, 46)
HEADER_BG = (24, 33, 56)
ACCENT = (232, 93, 63)
CARD = (246, 244, 239)
HEAD_TXT = (20, 32, 52)
SUB_TXT = (70, 82, 100)
WHITE = (255, 255, 255)
STEEL = (88, 98, 114)


def load(path, size):
    return ImageFont.truetype(path, size)


def lines_for(draw, text, fnt, width):
    """Greedy word wrap into lines no wider than width pixels."""
    out, line = [], ""
    for word in text.split():
        test = word if not line else line + " " + word
        if draw.textlength(test, font=fnt) <= width:
            line = test
        else:
            if line:
                out.append(line)
            line = word
    if line:
        out.append(line)
    return out


def best_font(draw, text, path, big, small, width, max_lines):
    """Biggest size from big down to small that wraps into max_lines."""
    for size in range(big, small - 1, -2):
        fnt = load(path, size)
        if len(lines_for(draw, text, fnt, width)) <= max_lines:
            return fnt
    return load(path, small)


# ------------------------------------------------------------ icons
# Each icon is drawn centred on (cx, cy) and stays inside ~110x110 px.

def _flag_us(d, x, y):
    for i in range(5):
        d.rectangle([x, y + i * 5, x + 30, y + i * 5 + 4],
                    fill=(200, 40, 50) if i % 2 == 0 else WHITE)
    d.rectangle([x, y, x + 13, y + 12], fill=(50, 70, 150))


def _flag_cn(d, x, y):
    d.rectangle([x, y, x + 30, y + 24], fill=(214, 36, 36))
    d.ellipse([x + 4, y + 4, x + 12, y + 12], fill=(255, 214, 0))


def _flag_ru(d, x, y):
    d.rectangle([x, y, x + 30, y + 8], fill=WHITE)
    d.rectangle([x, y + 8, x + 30, y + 16], fill=(40, 90, 180))
    d.rectangle([x, y + 16, x + 30, y + 24], fill=(210, 40, 40))


def draw_summit(d, cx, cy, col):
    """Three small table flags (US, China, Russia) on one round table."""
    d.ellipse([cx - 48, cy + 14, cx + 48, cy + 44], fill=(150, 104, 62),
              outline=(96, 64, 36), width=3)
    for i, fn in enumerate((_flag_us, _flag_cn, _flag_ru)):
        px = cx - 34 + i * 34
        d.line([(px, cy - 30), (px, cy + 28)], fill=STEEL, width=3)
        fn(d, px + 1, cy - 30)
        d.rectangle([px - 5, cy + 26, px + 5, cy + 30], fill=STEEL)
    # outline frames so the white bands read on light backgrounds
    for i in range(3):
        px = cx - 34 + i * 34
        d.rectangle([px + 1, cy - 30, px + 31, cy - 6], outline=INK, width=1)


def draw_scales(d, cx, cy, col):
    """Scales of justice: a post, a beam and two hanging pans."""
    d.rectangle([cx - 3, cy - 40, cx + 3, cy + 34], fill=col)
    d.rounded_rectangle([cx - 26, cy + 34, cx + 26, cy + 44], radius=4,
                        fill=col)
    d.ellipse([cx - 7, cy - 48, cx + 7, cy - 34], fill=col)
    d.line([(cx - 44, cy - 32), (cx + 44, cy - 32)], fill=col, width=5)
    for sx in (-40, 40):
        px = cx + sx
        d.line([(px, cy - 32), (px - 16, cy + 4)], fill=col, width=2)
        d.line([(px, cy - 32), (px + 16, cy + 4)], fill=col, width=2)
        d.chord([px - 20, cy - 8, px + 20, cy + 16], start=0, end=180,
                fill=col)


def draw_barrel(d, cx, cy, col):
    """An oil barrel with a warning triangle on its side."""
    d.rounded_rectangle([cx - 32, cy - 44, cx + 32, cy + 44], radius=10,
                        fill=col, outline=INK, width=2)
    for yy in (-26, 26):
        d.line([(cx - 32, cy + yy), (cx + 32, cy + yy)], fill=INK, width=3)
    tri = [(cx, cy - 18), (cx + 20, cy + 16), (cx - 20, cy + 16)]
    d.polygon(tri, fill=(255, 205, 40), outline=INK)
    d.rectangle([cx - 2, cy - 8, cx + 2, cy + 5], fill=INK)
    d.rectangle([cx - 2, cy + 8, cx + 2, cy + 12], fill=INK)


def draw_fire_house(d, cx, cy, col):
    """A small house with flames rising from it."""
    d.rectangle([cx - 34, cy - 4, cx + 34, cy + 44], fill=(222, 214, 200),
                outline=INK, width=2)
    d.polygon([(cx - 42, cy - 2), (cx, cy - 34), (cx + 42, cy - 2)],
              fill=(120, 60, 40), outline=INK)
    d.rectangle([cx - 9, cy + 18, cx + 9, cy + 44], fill=(90, 70, 55))
    d.rectangle([cx + 16, cy + 8, cx + 28, cy + 20], fill=(255, 190, 60))
    # flames
    d.polygon([(cx - 26, cy - 14), (cx - 16, cy - 52), (cx - 8, cy - 26),
               (cx + 2, cy - 58), (cx + 12, cy - 24), (cx + 22, cy - 46),
               (cx + 28, cy - 12)], fill=(240, 110, 30))
    d.polygon([(cx - 14, cy - 16), (cx - 6, cy - 38), (cx + 2, cy - 22),
               (cx + 10, cy - 40), (cx + 16, cy - 14)], fill=(255, 205, 50))


def draw_storm(d, cx, cy, col):
    """A cyclone: two curved arms around an eye."""
    for k in (0, 1):
        pts = []
        for i in range(0, 61):
            t = i / 60.0
            ang = k * math.pi + t * 1.6 * math.pi
            r = 12 + 34 * t
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        d.line(pts, fill=col, width=11, joint="curve")
    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=col)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=WHITE)


def draw_globe(d, cx, cy, col):
    """The Earth with a rising thermometer beside it."""
    d.ellipse([cx - 40, cy - 34, cx + 28, cy + 34], fill=(60, 140, 200),
              outline=INK, width=2)
    d.polygon([(cx - 26, cy - 18), (cx - 6, cy - 24), (cx + 2, cy - 8),
               (cx - 10, cy + 4), (cx - 24, cy - 2)], fill=(70, 160, 90))
    d.polygon([(cx - 4, cy + 10), (cx + 14, cy + 6), (cx + 16, cy + 22),
               (cx + 2, cy + 26)], fill=(70, 160, 90))
    # thermometer
    tx = cx + 40
    d.rounded_rectangle([tx - 7, cy - 44, tx + 7, cy + 26], radius=7,
                        fill=WHITE, outline=INK, width=2)
    d.rectangle([tx - 3, cy - 26, tx + 3, cy + 28], fill=(215, 45, 40))
    d.ellipse([tx - 12, cy + 22, tx + 12, cy + 46], fill=(215, 45, 40),
              outline=INK, width=2)


# ------------------------------------------------------------ stories

STORIES = [
    dict(
        head="TRUMP, XI, PUTIN MEET",
        sub="First three-way summit, in Shenzhen; no breakthrough",
        bg=(232, 238, 248), icon=draw_summit, col=(46, 90, 160),
    ),
    dict(
        head="WORLD COURT ON ROHINGYA",
        sub="ICJ finds Myanmar forces killed about 10,000 in 2017",
        bg=(240, 234, 226), icon=draw_scales, col=(120, 84, 48),
    ),
    dict(
        head="IEA: HORMUZ SHOCK",
        sub="'Largest threat to energy security in history'",
        bg=(250, 238, 222), icon=draw_barrel, col=(40, 50, 64),
    ),
    dict(
        head="BANGLADESH LOCKDOWN",
        sub="Yunus family home set ablaze; police say 2 killed",
        bg=(252, 232, 226), icon=draw_fire_house, col=(200, 70, 40),
    ),
    dict(
        head="CYCLONE AKVAN NEARS",
        sub="India's Odisha evacuates over 80,000 people",
        bg=(228, 240, 246), icon=draw_storm, col=(36, 110, 150),
    ),
    dict(
        head="COP31 DEAL ELUSIVE",
        sub="Antalya climate talks enter final stretch",
        bg=(232, 244, 232), icon=draw_globe, col=(60, 130, 80),
    ),
]


def render():
    img = Image.new("RGB", (SIZE, SIZE), WHITE)
    d = ImageDraw.Draw(img)

    # header band
    d.rectangle([0, 0, SIZE, 152], fill=HEADER_BG)
    d.text((SIZE // 2, 20), "WORLD NEWS", font=load(F_BLACK, 44),
           fill=ACCENT, anchor="ma")
    d.text((SIZE // 2, 70), "19 NOVEMBER 2026", font=load(F_BLACK, 62),
           fill=WHITE, anchor="ma")
    d.rectangle([0, 152, SIZE, 158], fill=ACCENT)
    d.text((SIZE // 2, 1012), "THURSDAY  ·  SIX STORIES THAT SHAPED THE DAY",
           font=load(F_BOLD, 15), fill=STEEL, anchor="ms")

    # 2 x 3 grid
    top, bottom, side, gap = 174, 990, 16, 14
    cw = (SIZE - 2 * side - gap) // 2
    ch = (bottom - top - 2 * gap) // 3
    strip = 118

    for n, s in enumerate(STORIES):
        x = side + (n % 2) * (cw + gap)
        y = top + (n // 2) * (ch + gap)
        d.rounded_rectangle([x, y, x + cw, y + ch], radius=12, fill=CARD)
        d.rounded_rectangle([x, y, x + strip, y + ch], radius=12, fill=s["bg"])
        d.rectangle([x + strip - 12, y, x + strip, y + ch], fill=s["bg"])
        s["icon"](d, x + strip // 2, y + ch // 2, s["col"])

        tx = x + strip + 16
        tw = cw - strip - 30
        fh = best_font(d, s["head"], F_BOLD, 38, 24, tw, 2)
        fs = best_font(d, s["sub"], F_REG, 26, 18, tw, 3)
        hl = lines_for(d, s["head"], fh, tw)
        sl = lines_for(d, s["sub"], fs, tw)
        block = len(hl) * (fh.size + 4) + 10 + len(sl) * (fs.size + 5)
        cy = y + max(18, (ch - block) // 2 - 4)
        for ln in hl:
            d.text((tx, cy), ln, font=fh, fill=HEAD_TXT)
            cy += fh.size + 4
        cy += 10
        for ln in sl:
            d.text((tx, cy), ln, font=fs, fill=SUB_TXT)
            cy += fs.size + 5

    img.save(OUT, format="PNG", optimize=False)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    render()
