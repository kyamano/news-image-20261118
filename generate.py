#!/usr/bin/env python3
"""Build entry.png for make.fun news-image-20261118.

Draws a one-page newspaper infographic summing up the world news of
Wednesday 18 November 2026, from reporting published that day
(AP, Reuters, AFP, IMD, NASA, PAHO via multiple outlets).

Every story below was cross-checked in at least two independent
sources on 2026-11-18 / 19 before it was drawn:

1. Shenzhen: Xi Jinping met Vladimir Putin in Shenzhen and greeted
   Donald Trump on the tarmac as Trump landed in China; the first
   US-China-Russia trilateral summit follows on Thu 19 Nov at APEC.
   Xi backed open trade, Putin attacked Western sanctions.
2. Ukraine: Zelenskyy confirmed a Ukrainian strike partially
   destroyed the Kerch (Crimean) Bridge; Kyiv urged the summit
   leaders to pressure Putin.
3. Gulf: after a US strike on Qeshm Island, Iran struck the US base
   at Ali Al Salem, Kuwait (and targets in Bahrain); an ADNOC tanker
   was struck in the Strait of Hormuz: 11 injured, 1 missing.
4. Gaza/Israel: Israel began a concentrated operation in three
   areas of central Gaza; the Knesset elected Matan Kahana, backed
   by PM-elect Eisenkot's camp, as speaker.
5. Alaska: Mary Peltola (D) defeated Sen. Dan Sullivan (R) in the
   last Senate race called, giving Democrats a 56-44 majority, the
   biggest flip since 1958; first Alaska Native US senator.
6. Health: the US lost its measles-elimination status after more
   than 5,400 cases in 2026.
7. Weather: Severe Cyclonic Storm Akvan headed for the Andhra
   Pradesh / Odisha coast, landfall expected noon Fri 20 Nov with
   winds of 100-110 km/h (IMD); schools shut in six Odisha districts.
8. Space: NASA's Voyager 1, launched in 1977, became the first
   human-made object one light-day from Earth (25.9 billion km);
   a signal now takes 24 hours to reach it.

The drawing is fully deterministic: fixed canvas, fixed fonts,
no randomness, no network. Output: entry.png next to this file.
"""

from pathlib import Path
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
NAVY = (13, 34, 64)
NAVY2 = (22, 52, 92)
RED = (178, 34, 40)
INK = (24, 26, 30)
GREY = (88, 92, 100)
CARD = (255, 255, 255)
GOLD = (232, 176, 32)

FONT_DIR = Path("/usr/share/fonts/truetype/noto")
BLACK = str(FONT_DIR / "NotoSans-Black.ttf")
BOLD = str(FONT_DIR / "NotoSans-Bold.ttf")
REG = str(FONT_DIR / "NotoSans-Regular.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, fnt):
    return draw.textlength(s, font=fnt)


def fit(draw, s, path, start, min_size, max_w):
    """Largest font size (<= start) whose text fits max_w."""
    size = start
    while size > min_size:
        fnt = font(path, size)
        if text_w(draw, s, fnt) <= max_w:
            return fnt
        size -= 2
    return font(path, min_size)


def wrap(draw, s, fnt, max_w):
    """Greedy word wrap to max_w pixels."""
    words, lines, cur = s.split(), [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def star(draw, cx, cy, r, fill):
    import math

    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def flag_china(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    star(draw, x + w * 0.26, y + h * 0.32, h * 0.20, GOLD)
    for dx, dy in [(0.52, 0.14), (0.58, 0.34), (0.58, 0.56), (0.50, 0.74)]:
        star(draw, x + w * dx, y + h * dy, h * 0.09, GOLD)


def flag_russia(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h / 3], fill=(245, 245, 245))
    draw.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    draw.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 0, 50))


def flag_usa(draw, x, y, w, h):
    stripe = h / 7
    for i in range(7):
        col = (179, 34, 52) if i % 2 == 0 else (245, 245, 245)
        draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe], fill=col)
    draw.rectangle([x, y, x + w * 0.44, y + stripe * 4], fill=(10, 49, 97))
    for r in range(4):
        for c in range(5):
            star(draw, x + w * (0.06 + 0.085 * c), y + stripe * (0.55 + 0.85 * r),
                 stripe * 0.30, (245, 245, 245))


def panel(draw, x, y, w, h, tag, tag_col, headline, body, head_size=30):
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=NAVY, width=3)
    draw.rectangle([x, y, x + w, y + 34], fill=tag_col)
    draw.text((x + 12, y + 5), tag, font=font(BOLD, 21), fill=(255, 255, 255))
    # headline: prefer one line, shrink before wrapping to two
    hf = fit(draw, headline, BLACK, head_size, 20, w - 24)
    hlines = wrap(draw, headline, hf, w - 24)
    yy = draw_lines(draw, hlines, x + 12, y + 44, hf, NAVY, hf.size + 4)
    # body: shrink until it fits the space left in the panel
    bsize = 20
    while bsize > 15:
        bf = font(REG, bsize)
        blines = wrap(draw, body, bf, w - 24)
        if yy + 4 + len(blines) * (bsize + 5) <= y + h - 6:
            break
        bsize -= 1
    draw_lines(draw, blines, x + 12, yy + 4, bf, INK, bsize + 5)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, W - 10, H - 10], outline=NAVY, width=5)

    # ---- Masthead -------------------------------------------------
    d.rectangle([28, 26, W - 28, 62], fill=RED)
    kick = "W O R L D   N E W S   •   O N E   D A Y   •   O N E   P I C T U R E"
    kf = fit(d, kick, BOLD, 24, 14, W - 80)
    d.text(((W - text_w(d, kick, kf)) / 2, 33), kick, font=kf, fill=(255, 255, 255))
    date = "WEDNESDAY 18 NOVEMBER 2026"
    df = fit(d, date, BLACK, 56, 30, W - 56)
    d.text(((W - text_w(d, date, df)) / 2, 70), date, font=df, fill=NAVY)
    sub = "SHENZHEN SUMMIT  •  UKRAINE  •  HORMUZ  •  GAZA  •  ALASKA  •  MEASLES  •  CYCLONE  •  VOYAGER 1"
    sf = fit(d, sub, BOLD, 20, 12, W - 56)
    d.text(((W - text_w(d, sub, sf)) / 2, 134), sub, font=sf, fill=RED)
    d.line([28, 162, W - 28, 162], fill=NAVY, width=3)

    # ---- Lead story: Shenzhen trilateral --------------------------
    lx, ly, lw, lh = 28, 174, W - 56, 286
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=NAVY)
    d.rectangle([lx + 14, ly + 14, lx + 356, ly + 50], fill=RED)
    d.text((lx + 26, ly + 20), "TOP STORY — APEC, SHENZHEN", font=font(BOLD, 21),
           fill=(255, 255, 255))
    lead_head = "XI + PUTIN MEET — TRUMP LANDS IN CHINA"
    hf = fit(d, lead_head, BLACK, 41, 26, lw - 36)
    d.text((lx + 18, ly + 60), lead_head, font=hf, fill=(255, 255, 255))
    lead_body = ("Xi Jinping met Vladimir Putin in Shenzhen, then greeted Donald Trump "
                 "on the tarmac. Their first-ever US–China–Russia trilateral summit "
                 "follows Thu 19 Nov. Xi backed open trade; Putin attacked sanctions.")
    bf = font(REG, 22)
    draw_lines(d, wrap(d, lead_body, bf, lw - 36), lx + 18, ly + 112, bf,
               (226, 232, 242), 28)
    # flags row
    fy = ly + 208
    fx = lx + 18
    for draw_flag, name in [(flag_china, "XI • CHINA"), (flag_russia, "PUTIN • RUSSIA"),
                            (flag_usa, "TRUMP • USA")]:
        draw_flag(d, fx, fy, 92, 52)
        d.rectangle([fx, fy, fx + 92, fy + 52], outline=(255, 255, 255), width=2)
        nf = font(BOLD, 16)
        d.text((fx + (92 - text_w(d, name, nf)) / 2, fy + 56), name, font=nf,
               fill=(255, 255, 255))
        fx += 124
    note = "FIRST TRILATERAL\nSUMMIT: THU 19 NOV"
    nf2 = font(BLACK, 21)
    d.multiline_text((lx + lw - 268, fy - 2), note, font=nf2, fill=GOLD, spacing=5)

    # ---- Middle grid 2 x 2 ----------------------------------------
    gy, gh, gw, gap = 472, 356, (W - 56 - 12) // 2, 12
    ph = (gh - gap) // 2
    panel(d, 28, gy, gw, ph, "UKRAINE WAR", (0, 91, 172),
          "UKRAINE HITS CRIMEAN BRIDGE",
          "Zelenskyy confirms the strike partially destroyed the Kerch Bridge "
          "to Crimea. Kyiv urges summit leaders to pressure Putin.")
    panel(d, 28 + gw + gap, gy, gw, ph, "MIDDLE EAST • STRAIT OF HORMUZ", RED,
          "IRAN–US CLASH: TANKER HIT",
          "Iran struck the US base in Kuwait after a US strike on Qeshm Island. "
          "ADNOC tanker hit in Hormuz: 11 injured, 1 missing.")
    panel(d, 28, gy + ph + gap, gw, ph, "GAZA • ISRAEL", (96, 84, 160),
          "ISRAEL OPENS NEW GAZA OPERATION",
          "Army begins a concentrated operation in three areas of central Gaza. "
          "Knesset elects opposition-backed speaker Kahana.")
    panel(d, 28 + gw + gap, gy + ph + gap, gw, ph, "US MIDTERMS • ALASKA", (0, 110, 84),
          "DEMOCRATS TAKE SENATE 56–44",
          "Mary Peltola defeats Sen. Sullivan in the last race called — first "
          "Alaska Native senator. Biggest Senate flip since 1958.")

    # ---- Bottom strip: health / weather / space -------------------
    by, bh = 840, 118
    bw = (W - 56 - 2 * gap) // 3
    small = [
        ("HEALTH • USA", RED, "US LOSES MEASLES STATUS",
         "Elimination status gone after 5,400+ cases in 2026."),
        ("WEATHER • INDIA", (0, 91, 172), "CYCLONE AKVAN NEARS COAST",
         "Severe storm: landfall Andhra–Odisha Fri 20 Nov, 100–110 km/h."),
        ("SPACE • NASA", NAVY2, "VOYAGER 1: ONE LIGHT-DAY",
         "First object 25.9bn km away. A signal now takes 24 hours."),
    ]
    for i, (tag, col, head, body) in enumerate(small):
        x = 28 + i * (bw + gap)
        d.rectangle([x, by, x + bw, by + bh], fill=CARD, outline=NAVY, width=3)
        d.rectangle([x, by, x + bw, by + 30], fill=col)
        d.text((x + 10, by + 4), tag, font=font(BOLD, 18), fill=(255, 255, 255))
        hf2 = fit(d, head, BLACK, 22, 15, bw - 20)
        d.text((x + 10, by + 38), head, font=hf2, fill=NAVY)
        bsize = 18
        bl = wrap(d, body, font(REG, bsize), bw - 20)
        while bsize > 14 and by + 68 + len(bl) * (bsize + 4) > by + bh - 4:
            bsize -= 1
            bl = wrap(d, body, font(REG, bsize), bw - 20)
        draw_lines(d, bl, x + 10, by + 68, font(REG, bsize), INK, bsize + 4)

    # ---- Footer ----------------------------------------------------
    foot = "Reported on 18 Nov 2026 • Sources: AP • Reuters • AFP • India Meteorological Dept • NASA • PAHO"
    ff = fit(d, foot, REG, 17, 11, W - 56)
    d.text(((W - text_w(d, foot, ff)) / 2, 972), foot, font=ff, fill=GREY)

    out = Path(__file__).with_name("entry.png")
    img.save(out, format="PNG", optimize=True)
    return out


if __name__ == "__main__":
    p = build()
    print(p, p.stat().st_size, "bytes")
