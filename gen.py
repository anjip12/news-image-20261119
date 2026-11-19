"""Draw the front page for Thursday 19 November 2026.

A single 1024x1024 newspaper page: masthead, one lead story, four
smaller stories in two rows, a ticker of two more items, and a source
line. Every picture is drawn with shapes; no photographs are used.
Run: python3 gen.py  ->  writes entry.png next to this file.
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024
HERE = os.path.dirname(os.path.abspath(__file__))

PAPER = (246, 239, 224)
INK = (20, 20, 26)
NAVY = (20, 38, 74)
GOLD = (232, 184, 75)
CARD = (255, 252, 244)
RULE = (180, 168, 140)
MUTED = (90, 84, 72)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def serif_b(size):
    return font("DejaVuSerif-Bold.ttf", size)


def sans_b(size):
    return font("DejaVuSans-Bold.ttf", size)


def sans(size):
    return font("DejaVuSans.ttf", size)


def sans_i(size):
    path = os.path.join(FONT_DIR, "DejaVuSans-Oblique.ttf")
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return font("DejaVuSans.ttf", size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, color, max_w, leading=22):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def kicker(draw, x, y, text, color):
    draw.text((x, y), text, font=sans_b(13), fill=color)
    return y + 20


def headline(draw, x, y, text, max_w, size=27):
    fnt = sans_b(size)
    yy = y
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, yy), line, font=fnt, fill=INK)
        yy += size + 6
    return yy


def card(draw, x, y, w, h):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=CARD, outline=RULE, width=2)


def band(draw, x, y, w, h, top, bottom):
    for i in range(h):
        t = i / max(1, h - 1)
        col = tuple(int(top[c] + (bottom[c] - top[c]) * t) for c in range(3))
        draw.line([(x, y + i), (x + w, y + i)], fill=col)


def skyline(draw, x, base, w, color, seed):
    rng = random.Random(seed)
    cx = x
    while cx < x + w - 18:
        bw = rng.randint(22, 46)
        bh = rng.randint(28, 78)
        draw.rectangle([cx, base - bh, cx + bw, base], fill=color)
        if rng.random() < 0.4:
            draw.rectangle([cx + bw // 3, base - bh - 12, cx + 2 * bw // 3,
                            base - bh], fill=color)
        cx += bw + 4


def palm(draw, x, base, s, color):
    draw.line([(x, base), (x + 4 * s, base - 34 * s)], fill=color,
              width=max(2, 3 * s))
    top = (x + 4 * s, base - 34 * s)
    for ang in (-70, -35, 0, 35, 70):
        rad = math.radians(ang - 90)
        ex = top[0] + int(20 * s * math.cos(rad))
        ey = top[1] + int(20 * s * math.sin(rad))
        draw.line([top, (ex, ey)], fill=color, width=max(2, 2 * s))


def draw_lead_art(draw, x, y, w, h):
    band(draw, x, y, w, h, (255, 122, 89), (94, 42, 110))
    sun_x, sun_y = x + w - 110, y + 62
    draw.ellipse([sun_x - 34, sun_y - 34, sun_x + 34, sun_y + 34],
                 fill=(255, 214, 130))
    skyline(draw, x + 8, y + h - 46, w - 16, (46, 22, 66), 19)
    draw.rectangle([x, y + h - 46, x + w, y + h], fill=(30, 16, 48))
    draw.polygon([(x, y + h), (x + w, y + h - 34), (x + w, y + h),
                  (x, y + h)], fill=(52, 28, 72))
    draw.line([(x + 30, y + h - 8), (x + w - 30, y + h - 30)],
              fill=(255, 214, 130), width=3)
    draw.rectangle([x + w // 2 - 46, y + h - 30, x + w // 2 + 46, y + h - 16],
                   fill=(16, 10, 28))
    draw.rectangle([x + w // 2 - 34, y + h - 40, x + w // 2 + 34, y + h - 30],
                   fill=(16, 10, 28))
    draw.ellipse([x + w // 2 - 38, y + h - 12, x + w // 2 - 28, y + h - 2],
                 fill=(10, 8, 18))
    draw.ellipse([x + w // 2 + 28, y + h - 12, x + w // 2 + 38, y + h - 2],
                 fill=(10, 8, 18))
    palm(draw, x + 26, y + h - 44, 1, (24, 12, 40))
    palm(draw, x + w - 58, y + h - 44, 1, (24, 12, 40))
    draw.text((x + 16, y + 12), "VI", font=serif_b(64), fill=(255, 92, 168))


def draw_flags(draw, x, y, w, h):
    third = w // 3
    draw.rectangle([x, y, x + third - 6, y + h], fill=(178, 34, 52))
    for i in range(5):
        yy = y + i * (h // 5)
        draw.rectangle([x, yy, x + third - 6, yy + h // 10],
                       fill=(255, 255, 255))
    draw.rectangle([x, y, x + 34, y + h // 2], fill=(30, 48, 110))
    draw.text((x + 8, y + 6), "*", font=sans_b(16), fill=(255, 255, 255))
    draw.rectangle([x + third, y, x + 2 * third - 6, y + h],
                   fill=(222, 41, 16))
    for sx, sy in ((10, 10), (30, 22), (16, 34)):
        draw.text((x + third + sx, y + sy), "*", font=sans_b(15),
                  fill=(255, 222, 0))
    draw.rectangle([x + 2 * third, y, x + w, y + h // 3],
                   fill=(255, 255, 255))
    draw.rectangle([x + 2 * third, y + h // 3, x + w, y + 2 * h // 3],
                   fill=(0, 57, 166))
    draw.rectangle([x + 2 * third, y + 2 * h // 3, x + w, y + h],
                   fill=(213, 0, 50))
    draw.rectangle([x, y, x + w, y + h], outline=(120, 110, 90), width=2)
    draw.rectangle([x, y + h - 4, x + w, y + h], fill=(120, 90, 40))


def draw_gulf(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(126, 178, 196))
    draw.polygon([(x, y), (x + w * 0.42, y), (x + w * 0.30, y + h),
                  (x, y + h)], fill=(226, 205, 160))
    draw.polygon([(x + w * 0.72, y), (x + w, y), (x + w, y + h),
                  (x + w * 0.82, y + h)], fill=(214, 190, 148))
    draw.line([(x + w * 0.42, y), (x + w * 0.30, y + h)], fill=(60, 90, 120),
              width=3)
    spots = [("Qeshm", 0.48, 0.62), ("Bahrain", 0.60, 0.38),
             ("Kuwait", 0.66, 0.16)]
    for name, fx, fy in spots:
        px, py = x + int(w * fx), y + int(h * fy)
        draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=(178, 34, 52),
                     outline=(255, 255, 255), width=2)
        draw.text((px + 9, py - 8), name, font=sans_b(12), fill=(20, 30, 44))
    draw.text((x + 8, y + h - 20), "STRAIT OF HORMUZ", font=sans_b(11),
              fill=(20, 50, 70))


def draw_cyclone(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(58, 110, 158))
    draw.polygon([(x, y + h), (x + w * 0.30, y + h), (x + w * 0.22, y),
                  (x, y)], fill=(226, 205, 160))
    cx, cy = x + int(w * 0.68), y + int(h * 0.55)
    for r in (44, 33, 22, 12):
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300,
                 fill=(255, 255, 255), width=5)
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(255, 214, 130))
    draw.text((x + w * 0.34, y + 8), "BAY OF BENGAL", font=sans_b(11),
              fill=(255, 255, 255))
    draw.text((x + w - 118, y + 8), "LANDFALL 20 NOV", font=sans_b(11),
              fill=(255, 255, 255))


def draw_voyager(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(10, 12, 30))
    rng = random.Random(7)
    for _ in range(46):
        sx = x + rng.randint(4, w - 4)
        sy = y + rng.randint(4, h - 4)
        r = rng.choice([1, 1, 2])
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255))
    for i in range(0, 120, 16):
        px = x + 16 + i
        py = y + h - 14 - int(0.35 * i)
        draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(150, 150, 180))
    cx, cy = x + int(w * 0.52), y + int(h * 0.58)
    draw.line([(cx, cy), (cx + 52, cy - 34)], fill=(200, 170, 90), width=5)
    draw.ellipse([cx + 38, cy - 58, cx + 78, cy - 18], outline=(232, 184, 75),
                 width=4)
    draw.line([(cx + 58, cy - 38), (cx + 58, cy - 58)], fill=(232, 184, 75),
              width=3)
    draw.rectangle([cx - 26, cy - 8, cx + 6, cy + 14], fill=(200, 170, 90),
                   outline=(120, 90, 30), width=2)
    draw.text((x + 10, y + 8), "1 LIGHT-DAY", font=sans_b(16),
              fill=(232, 184, 75))
    draw.text((x + 10, y + 30), "16bn MILES", font=sans_b(13),
              fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 122], fill=GOLD)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=serif_b(52))
    d.text(((W - tw) / 2, 12), title, font=serif_b(52), fill=(255, 255, 255))
    date = "THURSDAY  19  NOVEMBER  2026"
    dw = d.textlength(date, font=sans_b(28))
    d.text(((W - dw) / 2, 72), date, font=sans_b(28), fill=GOLD)

    stand = "Five stories that defined the day \u2014 from Vice City to interstellar space."
    sw = d.textlength(stand, font=sans_i(19))
    d.text(((W - sw) / 2, 130), stand, font=sans_i(19), fill=MUTED)

    # Lead story: GTA VI
    card(d, 24, 158, 976, 238)
    draw_lead_art(d, 40, 172, 560, 210)
    tx = 624
    yy = kicker(d, tx, 172, "CULTURE  \u00b7  GAMES", (178, 34, 52))
    yy = headline(d, tx, yy, "VICE CITY OPENS ITS GATES", 352, size=30)
    yy = para(d, tx, yy + 4,
              "Grand Theft Auto VI rolls out worldwide at midnight local "
              "time, New Zealand first \u2014 13 years after GTA V.",
              sans(17), INK, 352, leading=22)
    para(d, tx, yy + 6,
         "Metacritic 99 \u00b7 ~16m copies pre-sold \u00b7 $79.99 \u00b7 PS5 & "
         "Xbox Series X|S", sans_b(14), MUTED, 352, leading=19)

    # Row two
    card(d, 24, 408, 482, 232)
    draw_flags(d, 40, 422, 450, 88)
    yy = kicker(d, 40, 518, "DIPLOMACY  \u00b7  SHENZHEN", (20, 38, 74))
    yy = headline(d, 40, yy, "THREE LEADERS, ONE TABLE", 450, size=24)
    para(d, 40, yy + 2,
         "Trump, Xi and Putin meet today \u2014 the first trilateral of the "
         "three presidents \u2014 at the APEC summit. On the table: nuclear "
         "arms, AI, trade, Iran.", sans(15), INK, 450, leading=20)

    card(d, 518, 408, 482, 232)
    draw_gulf(d, 534, 422, 450, 88)
    yy = kicker(d, 534, 518, "THE GULF", (178, 34, 52))
    yy = headline(d, 534, yy, "GULF EXCHANGES WIDEN", 450, size=24)
    para(d, 534, yy + 2,
         "US jets hit a missile site on Qeshm Island; Iran's drones reach "
         "Kuwait and Bahrain. Defences report interceptions; no casualties "
         "reported.", sans(15), INK, 450, leading=20)

    # Row three
    card(d, 24, 652, 482, 232)
    draw_cyclone(d, 40, 666, 450, 88)
    yy = kicker(d, 40, 762, "WEATHER  \u00b7  INDIA", (20, 90, 120))
    yy = headline(d, 40, yy, "CYCLONE AKVAN BEARS DOWN", 450, size=24)
    para(d, 40, yy + 2,
         "Strengthening over the Bay of Bengal, Akvan is due to cross the "
         "Andhra Pradesh coast between Machilipatnam and Puri on 20 Nov.",
         sans(15), INK, 450, leading=20)

    card(d, 518, 652, 482, 232)
    draw_voyager(d, 534, 666, 450, 88)
    yy = kicker(d, 534, 762, "SPACE", (120, 90, 30))
    yy = headline(d, 534, yy, "VOYAGER, A DAY OF LIGHT AWAY", 450, size=24)
    para(d, 534, yy + 2,
         "NASA briefs today on Voyager 1, now about 16 billion miles out "
         "\u2014 a radio signal takes a full day to reach it. Launched 1977.",
         sans(15), INK, 450, leading=20)

    # Ticker
    d.rectangle([24, 896, 1000, 962], fill=NAVY)
    d.text((40, 904), "ALSO TODAY", font=sans_b(14), fill=GOLD)
    d.text((40, 926),
           "House Democrats nominate Hakeem Jeffries for Speaker, 251\u201311; "
           "full House vote 3 Jan.",
           font=sans(15), fill=(255, 255, 255))
    d.text((40, 946),
           "EU proposes a \u20ac45bn Ukraine loan, to be repaid after Russia "
           "pays reparations.",
           font=sans(15), fill=(255, 255, 255))

    # Footer
    d.line([(24, 978), (1000, 978)], fill=RULE, width=2)
    d.text((24, 988), "Sources: Reuters  \u00b7  AP  \u00b7  NASA  \u00b7  The Hindu  "
           "\u00b7  APSDMA  \u2014  19 November 2026",
           font=sans(14), fill=MUTED)
    d.text((700, 988), "Drawn by program \u2014 no photographs",
           font=sans(14), fill=MUTED)

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
