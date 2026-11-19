"""Draw the front page for Thursday 19 November 2026 -- v2 redesign.

A single dense 1024x1024 newspaper front page built to be read at
thumbnail size: a rich Vice City sunset lead panel with stat chips,
then four saturated story panels (Shenzhen trilateral, Gulf exchanges,
Cyclone Akvan, Voyager 1), a navy ticker and a source line. Every
picture is drawn with shapes; no photographs are used.
Run: python3 gen.py  ->  writes entry.png next to this file.
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

PAPER = (246, 239, 224)
CARD = (253, 250, 242)
INK = (18, 20, 30)
NAVY = (13, 27, 62)
GOLD = (238, 190, 80)
BORDER = (24, 32, 66)
MUTED = (92, 86, 74)
PINK = (198, 30, 92)


def _f(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def serif_b(size):
    return _f("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return _f("DejaVuSerif.ttf", size)


def sans_b(size):
    return _f("DejaVuSans-Bold.ttf", size)


def sans(size):
    return _f("DejaVuSans.ttf", size)


def centered(d, cx, y, text, fnt, fill):
    w = d.textlength(text, font=fnt)
    d.text((cx - w / 2, y), text, font=fnt, fill=fill)


def wrap(d, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, fnt, color, max_w, leading):
    lines = wrap(d, text, fnt, max_w)
    for line in lines:
        d.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y - leading + fnt.size


def fit_headline(img, d, x, y, text, max_w):
    """One-line headline, largest size that fits; if even 29px is too
    wide, render at 29px and squeeze horizontally to fit (height and
    weight stay full, so it still reads as a headline)."""
    for size in (31, 30, 29):
        fnt = sans_b(size)
        if d.textlength(text, font=fnt) <= max_w:
            d.text((x, y), text, font=fnt, fill=INK)
            return
    fnt = sans_b(29)
    w = int(d.textlength(text, font=fnt)) + 4
    layer = Image.new("RGBA", (w, 44), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.text((2, 4), text, font=fnt, fill=INK + (255,))
    layer = layer.resize((max_w, 44), Image.LANCZOS)
    img.paste(layer, (x, y - 2), layer)


def gradient(size, stops):
    w, h = size
    col = Image.new("RGB", (1, h))
    for yy in range(h):
        t = yy / max(1, h - 1)
        for i in range(len(stops) - 1):
            t0, c0 = stops[i]
            t1, c1 = stops[i + 1]
            if t0 <= t <= t1:
                u = 0.0 if t1 == t0 else (t - t0) / (t1 - t0)
                col.putpixel((0, yy), tuple(
                    int(c0[k] + (c1[k] - c0[k]) * u) for k in range(3)))
                break
    return col.resize((w, h))


def dashed_line(d, p0, p1, fill, width=3, dash=9, gap=6):
    x0, y0 = p0
    x1, y1 = p1
    dist = math.hypot(x1 - x0, y1 - y0)
    if dist == 0:
        return
    ux, uy = (x1 - x0) / dist, (y1 - y0) / dist
    t = 0.0
    while t < dist:
        t2 = min(dist, t + dash)
        d.line([(x0 + ux * t, y0 + uy * t), (x0 + ux * t2, y0 + uy * t2)],
               fill=fill, width=width)
        t += dash + gap


def dashed_arc(d, p0, p1, p2, fill, width=3, dash=7, gap=5):
    pts = []
    for i in range(61):
        t = i / 60
        pts.append(((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0]
                    + t ** 2 * p2[0],
                    (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1]
                    + t ** 2 * p2[1]))
    pen, acc = True, 0.0
    for i in range(1, len(pts)):
        seg = math.hypot(pts[i][0] - pts[i - 1][0],
                         pts[i][1] - pts[i - 1][1])
        if pen:
            d.line([pts[i - 1], pts[i]], fill=fill, width=width)
        acc += seg
        if acc >= (dash if pen else gap):
            pen, acc = not pen, 0.0


def star(d, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = math.radians(-90 + i * 36)
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def halo_text(d, x, y, text, fnt, fill):
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        d.text((x + dx, y + dy), text, font=fnt, fill=(18, 28, 40))
    d.text((x, y), text, font=fnt, fill=fill)


def palm(d, x, y, s, color):
    pts = []
    for i in range(13):
        t = i / 12
        pts.append((x + 18 * s * t * t, y - 66 * s * t))
    d.line(pts, fill=color, width=max(2, int(6 * s)))
    tx, ty = pts[-1]
    for dx, up, droop in ((-40, 16, 30), (-26, 24, 26), (-8, 28, 22),
                          (12, 26, 24), (30, 20, 28), (42, 12, 30)):
        curve = []
        for i in range(9):
            t = i / 8
            curve.append((tx + dx * s * t,
                          ty - up * s * t + droop * s * t * t))
        d.line(curve, fill=color, width=max(2, int(3 * s)))
    d.ellipse([tx - 4 * s, ty - 2 * s, tx + 2 * s, ty + 4 * s],
              fill=color)
    d.ellipse([tx + 1 * s, ty - 1 * s, tx + 6 * s, ty + 4 * s],
              fill=color)


def lead_art():
    img = gradient((968, 156), [(0.0, (255, 94, 58)),
                                 (0.45, (240, 80, 120)),
                                 (0.75, (140, 60, 140)),
                                 (1.0, (70, 32, 100))])
    d = ImageDraw.Draw(img)
    # Sun with a soft ring.
    d.ellipse([692, 24, 768, 100], outline=(255, 190, 110), width=3)
    d.ellipse([700, 32, 760, 92], fill=(255, 216, 130))
    # Back skyline.
    rng = random.Random(5)
    x = -6
    while x < 968:
        bw = rng.randint(30, 62)
        bh = rng.randint(30, 70)
        d.rectangle([x, 118 - bh, x + bw, 118], fill=(88, 40, 110))
        x += bw + rng.randint(2, 8)
    # Front skyline with lit windows.
    rng = random.Random(9)
    x = -4
    while x < 968:
        bw = rng.randint(34, 66)
        bh = rng.randint(20, 55)
        d.rectangle([x, 126 - bh, x + bw, 126], fill=(34, 16, 54))
        for _ in range(rng.randint(1, 4)):
            wx = x + rng.randint(4, max(5, bw - 8))
            wy = 126 - bh + rng.randint(4, max(5, bh - 10))
            d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 200, 90))
        x += bw + rng.randint(2, 7)
    # Neon VI.
    d.text((33, 13), "VI", font=serif_b(104), fill=(196, 26, 116))
    d.text((30, 10), "VI", font=serif_b(104), fill=(255, 64, 160))
    # Palm silhouettes.
    palm(d, 215, 130, 1.1, (24, 10, 38))
    palm(d, 872, 132, 1.25, (24, 10, 38))
    palm(d, 640, 133, 0.9, (24, 10, 38))
    # Causeway.
    d.rectangle([0, 126, 968, 156], fill=(22, 10, 36))
    d.line([(0, 126), (968, 126)], fill=(255, 190, 90), width=2)
    dashed_line(d, (0, 144), (968, 144), (255, 220, 150), width=2,
                dash=16, gap=12)
    # Sports car, side profile facing right, lit against the road.
    d.polygon([(420, 140), (428, 128), (470, 124), (500, 112),
               (545, 110), (575, 122), (592, 128), (594, 140)],
              fill=(56, 26, 96))
    d.polygon([(478, 123), (502, 114), (540, 113), (560, 122)],
              fill=(120, 60, 150))
    d.line([(470, 124), (500, 112), (545, 110)], fill=(170, 110, 200),
           width=2)
    d.ellipse([448, 133, 467, 149], fill=(8, 8, 14))
    d.ellipse([547, 133, 566, 149], fill=(8, 8, 14))
    d.ellipse([455, 139, 460, 144], fill=(130, 130, 150))
    d.ellipse([554, 139, 559, 144], fill=(130, 130, 150))
    d.rectangle([419, 128, 427, 133], fill=(255, 60, 70))
    d.ellipse([585, 127, 596, 134], fill=(255, 240, 180))
    d.polygon([(594, 128), (636, 125), (636, 134), (594, 133)],
              fill=(255, 226, 160))
    d.line([(424, 142), (590, 142)], fill=(255, 64, 160), width=2)
    for rx in range(432, 590, 14):
        d.line([(rx, 145), (rx, 151)], fill=(120, 60, 110), width=2)
    return img


def flags_art():
    img = Image.new("RGB", (464, 110), (250, 246, 235))
    d = ImageDraw.Draw(img)
    fw, fh, fy = 144, 78, 4
    # USA: proper stripes, blue canton, dot-grid stars.
    x = 6
    d.rectangle([x, fy, x + fw, fy + fh], fill=(245, 245, 245))
    sh = fh / 13
    for i in range(13):
        if i % 2 == 0:
            d.rectangle([x, fy + i * sh, x + fw, fy + (i + 1) * sh],
                        fill=(178, 34, 52))
    d.rectangle([x, fy, x + 58, fy + 7 * sh], fill=(30, 45, 110))
    for r in range(4):
        for c in range(5):
            sx = x + 8 + c * 11
            sy = fy + 6 + r * 10
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2],
                      fill=(255, 255, 255))
    # China: one large star, four small.
    x = 160
    d.rectangle([x, fy, x + fw, fy + fh], fill=(215, 35, 25))
    star(d, x + 27, fy + 24, 13, (255, 222, 0))
    for sy in (12, 27, 42, 57):
        star(d, x + 52, fy + sy, 5, (255, 222, 0))
    # Russia: white, blue, red thirds.
    x = 314
    d.rectangle([x, fy, x + fw, fy + 26], fill=(245, 245, 245))
    d.rectangle([x, fy + 26, x + fw, fy + 52], fill=(0, 57, 166))
    d.rectangle([x, fy + 52, x + fw, fy + fh], fill=(213, 0, 50))
    for fx in (6, 160, 314):
        d.rectangle([fx, fy, fx + fw, fy + fh], outline=(110, 100, 80),
                    width=1)
    for fx, label in ((6, "USA"), (160, "CHINA"), (314, "RUSSIA")):
        centered(d, fx + fw / 2, 87, label, sans_b(16), INK)
    return img


def gulf_art():
    img = Image.new("RGB", (464, 110), (43, 102, 138))
    d = ImageDraw.Draw(img)
    land = (224, 203, 152)
    d.polygon([(96, 0), (464, 0), (464, 36), (340, 24), (250, 8),
               (180, 14), (140, 6)], fill=land)
    d.polygon([(0, 52), (80, 46), (160, 68), (200, 110), (0, 110)],
              fill=land)
    d.ellipse([286, 21, 306, 31], fill=(206, 182, 128))
    # Dashed drone trajectories out of Iran.
    dashed_arc(d, (308, 18), (215, 0), (110, 20), (255, 80, 60),
               width=3)
    dashed_arc(d, (308, 18), (292, 58), (213, 60), (255, 80, 60),
               width=3)
    # Qeshm starburst.
    pts = []
    for i in range(16):
        ang = math.radians(i * 22.5)
        rr = 13 if i % 2 == 0 else 6
        pts.append((296 + rr * math.cos(ang), 26 + rr * math.sin(ang)))
    d.polygon(pts, fill=(255, 138, 0), outline=(200, 60, 0))
    halo_text(d, 316, 13, "US STRIKE", sans_b(13), (255, 205, 80))
    halo_text(d, 262, 46, "Qeshm", sans_b(11), (255, 255, 255))
    # Bahrain and Kuwait dots.
    for px, py in ((208, 60), (104, 20)):
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=(200, 30, 40),
                  outline=(255, 255, 255), width=2)
    halo_text(d, 219, 54, "Bahrain", sans_b(12), (255, 255, 255))
    halo_text(d, 115, 14, "Kuwait", sans_b(12), (255, 255, 255))
    d.text((255, 92), "STRAIT OF HORMUZ", font=sans_b(12),
           fill=(175, 220, 240))
    return img


def cyclone_art():
    img = gradient((464, 110), [(0.0, (36, 98, 158)),
                                (1.0, (16, 56, 102))])
    d = ImageDraw.Draw(img)
    # Andhra coast on the right.
    d.polygon([(398, 0), (464, 0), (464, 110), (410, 110), (394, 66),
               (402, 26)], fill=(226, 205, 154))
    d.text((416, 90), "INDIA", font=sans_b(11), fill=(90, 70, 40))
    # Spiral storm: shadow pass, then white rotating bands.
    cx, cy = 166, 55
    for r, a0 in ((52, -50), (43, 50), (34, 140), (25, 230)):
        d.arc([cx - r + 4, cy - r + 5, cx + r + 4, cy + r + 5],
              start=a0, end=a0 + 190, fill=(110, 160, 200), width=9)
    for r, a0 in ((52, -50), (43, 50), (34, 140), (25, 230)):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=a0,
              end=a0 + 190, fill=(255, 255, 255), width=9)
    d.arc([cx - 16, cy - 16, cx + 16, cy + 16], start=300, end=470,
          fill=(255, 255, 255), width=6)
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(16, 56, 102),
              outline=(255, 255, 255), width=3)
    # Landfall arrow toward the coast.
    dashed_line(d, (224, 55), (380, 55), (235, 60, 45), width=4,
                dash=10, gap=7)
    d.polygon([(388, 55), (368, 45), (368, 65)], fill=(235, 60, 45))
    # Red landfall chip.
    d.rounded_rectangle([238, 6, 452, 32], radius=6, fill=(198, 32, 32))
    centered(d, 345, 12, "LANDFALL 20 NOV", sans_b(14),
             (255, 255, 255))
    halo_text(d, 10, 92, "BAY OF BENGAL", sans_b(12), (255, 255, 255))
    return img


def voyager_art():
    img = Image.new("RGB", (464, 110), (7, 9, 26))
    d = ImageDraw.Draw(img)
    rng = random.Random(11)
    for _ in range(80):
        sx = rng.randint(4, 460)
        sy = rng.randint(4, 106)
        r = rng.choice([1, 1, 2])
        shade = rng.choice([(255, 255, 255), (180, 190, 220),
                            (140, 150, 190)])
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=shade)
    d.text((14, 8), "1 LIGHT-DAY", font=sans_b(25), fill=GOLD)
    d.text((14, 40), "SIGNAL TAKES 24H", font=sans_b(14),
           fill=(255, 255, 255))
    # Earth, far away at lower left.
    d.ellipse([43, 69, 65, 91], fill=(64, 124, 214))
    d.ellipse([47, 73, 61, 85], fill=(70, 170, 90))
    centered(d, 54, 95, "EARTH", sans_b(11), (255, 255, 255))
    # Signal rings travelling from the dish toward Earth.
    for r in (26, 48, 70, 92):
        d.arc([332 - r, 48 - r, 332 + r, 48 + r], start=100, end=260,
              fill=(212, 175, 55), width=3)
    # The probe: big golden dish facing left, bus, booms.
    d.ellipse([308, 12, 382, 80], fill=(216, 178, 60),
              outline=(245, 214, 130), width=2)
    d.ellipse([322, 24, 368, 68], fill=(186, 148, 42))
    d.line([(345, 46), (310, 46)], fill=(90, 70, 20), width=3)
    d.rectangle([302, 42, 312, 50], fill=(110, 86, 26))
    d.rectangle([386, 38, 412, 58], fill=(148, 150, 162),
                outline=(216, 178, 60), width=2)
    d.line([(404, 38), (440, 10)], fill=(170, 172, 182), width=3)
    d.rectangle([436, 6, 446, 14], fill=(200, 200, 210))
    d.line([(406, 58), (436, 82)], fill=(96, 96, 108), width=4)
    d.rectangle([430, 78, 450, 92], fill=(64, 64, 78))
    return img


def chip(d, x, y, text, bg, fg):
    fnt = sans_b(14)
    w = d.textlength(text, font=fnt) + 26
    d.rounded_rectangle([x, y, x + w, y + 26], radius=8, fill=bg)
    d.text((x + 13, y + 5), text, font=fnt, fill=fg)
    return x + w + 10


def story_card(img, d, x, y, art, kicker, kicker_color, headline,
               body):
    d.rounded_rectangle([x, y, x + 488, y + 248], radius=12, fill=CARD,
                        outline=BORDER, width=3)
    img.paste(art, (x + 12, y + 10))
    d.text((x + 14, y + 128), kicker, font=sans_b(15),
           fill=kicker_color)
    fit_headline(img, d, x + 14, y + 150, headline, 460)
    para(d, x + 14, y + 190, body, sans(17), INK, 460, 19)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead.
    d.rectangle([0, 0, W, 124], fill=NAVY)
    centered(d, W / 2, 6, "THE WORLD IN ONE DAY", serif_b(58),
             (255, 255, 255))
    centered(d, W / 2, 68, "THURSDAY 19 NOVEMBER 2026", sans_b(30),
             GOLD)
    centered(d, W / 2, 101,
             "Five stories that defined the day \u2014 from Vice City "
             "to interstellar space.", serif(15), (196, 204, 222))
    d.rectangle([0, 124, W, 131], fill=GOLD)

    # Lead story: GTA VI.
    d.rounded_rectangle([16, 138, 1008, 456], radius=12, fill=CARD,
                        outline=BORDER, width=3)
    img.paste(lead_art(), (28, 148))
    d.text((30, 312), "CULTURE  \u00b7  GAMES", font=sans_b(15),
           fill=PINK)
    d.text((30, 330), "VICE CITY OPENS ITS GATES", font=sans_b(44),
           fill=INK)
    body_end = para(d, 30, 382,
                    "Grand Theft Auto VI rolls out worldwide at "
                    "midnight local time, New Zealand first \u2014 13 "
                    "years after GTA V.", sans(18), INK, 950, 20)
    cx = 30
    cy = body_end + 10
    cx = chip(d, cx, cy, "METACRITIC 99", NAVY, GOLD)
    cx = chip(d, cx, cy, "~16M COPIES PRE-SOLD", PINK, (255, 255, 255))
    chip(d, cx, cy, "$79.99 \u00b7 PS5 & XBOX SERIES X|S", GOLD, NAVY)

    # Four story panels.
    story_card(img, d, 16, 464, flags_art(), "DIPLOMACY  \u00b7  "
               "SHENZHEN", (24, 60, 140), "THREE LEADERS, ONE TABLE",
               "Trump, Xi and Putin meet today \u2014 the first "
               "trilateral of the three presidents \u2014 at the APEC "
               "summit. Nuclear arms, AI, trade, Iran.")
    story_card(img, d, 520, 464, gulf_art(), "THE GULF", (198, 40, 40),
               "GULF EXCHANGES WIDEN",
               "US jets hit a missile site on Qeshm Island; Iran's "
               "drones reach Kuwait and Bahrain. Interceptions "
               "reported; no casualties.")
    story_card(img, d, 16, 720, cyclone_art(), "WEATHER  \u00b7  "
               "INDIA", (0, 105, 140), "CYCLONE AKVAN BEARS DOWN",
               "Strengthening over the Bay of Bengal, Akvan is due to "
               "cross the Andhra Pradesh coast between Machilipatnam "
               "and Puri on 20 Nov.")
    story_card(img, d, 520, 720, voyager_art(), "SPACE",
               (150, 110, 10), "VOYAGER, A DAY OF LIGHT AWAY",
               "NASA briefs today on Voyager 1, now about 16 billion "
               "miles out \u2014 a radio signal takes a full day to "
               "reach it. Launched 1977.")

    # Ticker.
    d.rounded_rectangle([16, 972, 1008, 1006], radius=6, fill=NAVY)
    label = "ALSO TODAY"
    lf = sans_b(14)
    d.text((30, 977), label, font=lf, fill=GOLD)
    tx = 30 + d.textlength(label, font=lf) + 12
    d.text((tx, 977),
           "House Democrats nominate Hakeem Jeffries for Speaker, "
           "251\u201311; full House vote 3 Jan.", font=sans(14),
           fill=(255, 255, 255))
    d.text((30, 991),
           "EU proposes a \u20ac45bn Ukraine loan, to be repaid "
           "after Russia pays reparations.", font=sans(14),
           fill=(255, 255, 255))

    # Footer.
    d.text((16, 1010),
           "Sources: Reuters  \u00b7  AP  \u00b7  NASA  \u00b7  The "
           "Hindu  \u00b7  APSDMA  \u2014  19 November 2026",
           font=sans(11), fill=MUTED)
    right = "Drawn by program \u2014 no photographs"
    rw = d.textlength(right, font=sans(11))
    d.text((1008 - rw, 1010), right, font=sans(11), fill=MUTED)

    img.save(os.path.join(HERE, "entry.png"), format="PNG",
             optimize=True)


if __name__ == "__main__":
    main()
