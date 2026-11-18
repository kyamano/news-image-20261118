#!/usr/bin/env python3
"""Build entry.png for make.fun news-image-20261118 — v2.

Draws a one-page newspaper infographic summing up the world news of
Wednesday 18 November 2026: 30 stories — 10 reported in depth and 20
one-line briefs — every one cross-checked in at least two independent
sources published on 18 Nov 2026 (or reporting that day's events)
before it was drawn.

In depth:
1.  Shenzhen: Xi Jinping met Vladimir Putin in Shenzhen and greeted
    Donald Trump on the tarmac as Trump landed in China; the first
    US-China-Russia trilateral summit follows on Thu 19 Nov at APEC.
2.  Ukraine: Zelenskyy confirmed a Ukrainian strike partially
    destroyed the Kerch (Crimean) Bridge.
3.  Gulf: after a US strike on Qeshm Island, Iran struck the US base
    at Ali Al Salem, Kuwait; an ADNOC tanker was struck in the
    Strait of Hormuz: 11 injured, 1 missing (Reuters).
4.  Gaza/Israel: Israel began a concentrated operation in three
    areas of central Gaza; the Knesset elected Matan Kahana as
    speaker.
5.  Alaska: Mary Peltola (D) defeated Sen. Dan Sullivan (R), giving
    Democrats a 56-44 Senate majority, the biggest flip since 1958;
    first Alaska Native US senator (AP).
6.  COP31, Antalya: the first draft deal carries two rival wordings
    on fossil fuels — "transition away" vs "phase out" — dividing
    nearly 200 nations; the EU called the draft untenable
    (Reuters/The News, Asia Today, AEC, Annahar).
7.  Nvidia: quarterly revenue more than doubled to $115.8bn on
    data-centre demand (+103% year on year); the board ruled out
    bringing back former CEO Jensen Huang (SEC filing via market
    briefs; Daily Mirror).
8.  Health: the US lost its measles-elimination status after more
    than 5,400 cases in 2026 (PAHO).
9.  Weather: Severe Cyclonic Storm Akvan headed for the Andhra
    Pradesh / Odisha coast, landfall expected Fri 20 Nov, winds of
    100-110 km/h (IMD).
10. Space: NASA's Voyager 1 became the first human-made object one
    light-day from Earth (25.9 billion km); a signal takes 24 hours.

Briefs (each verified in 2+ outlets on 18 Nov 2026):
11. Saudi air defences destroyed a Houthi cruise missile launched
    toward Riyadh (Open Chronicle; Zark/Reuters).
12. Gold slid below $3,800 to a one-year low (Daily Mirror; FP
    Markets / market briefs).
13. UK inflation rose to 3.6%, its highest in a year (ONS via CPA
    and Newsquawk briefs).
14. A man convicted in an Iran-linked plot to assassinate Trump was
    sentenced in the US to more than 27 years (Open Chronicle;
    Roman Report).
15. DR Congo's Ebola outbreak passed 11,000 cases and 5,500 deaths —
    the second-largest on record (Reuters; Africa CDC via Zark).
16. A Russian An-12 military transport crashed in Siberia killing
    all 19 aboard; investigators opened a case (Al Jazeera; Indian
    Express; Interfax reports).
17. Australia sanctioned three Israeli settlers and four groups,
    incl. settler leader Daniella Weiss, over West Bank expansion
    (Reuters; Times of Israel).
18. Grand Theft Auto VI's global rollout began, first unlocks in
    New Zealand; Sensor Tower estimated ~16m pre-orders (Reuters;
    Primetimer).
19. ECDC: carbapenem-resistant Klebsiella bloodstream infections up
    72% since 2019; Europe off track on most 2030 targets (ECDC
    release; Democrata).
20. Waymo halted driverless freeway rides across the US after
    California's DMV ban over construction-zone incursions
    (TechCrunch; Al Jazeera).
21. About 25,000 rallied in Bratislava against PM Fico on the
    Velvet Revolution anniversary (AP; Thursday Times).
22. Haiti formalised a security cooperation agreement with El
    Salvador as thousands marched in support of Salvadoran troops
    fighting gangs (AFP; Le Temps).
23. South Korea's Lee Jae Myung asked Xi Jinping for joint efforts
    on Korean Peninsula peace at APEC; Xi backed restarting
    North Korea-US dialogue (Yonhap; Korea Times).
24. Trump hailed the "biggest" trade deal with the Philippines in
    Manila; Manila said nothing was signed — only an understanding
    (Reuters; Rappler).
25. New Zealand cancelled a tsunami advisory within the hour after
    unexplained tidal-gauge activity off Napier and Gisborne; a
    possible underwater landslide (AFP; 1News).
26. All 36 Nigerian state assemblies approved the state-police
    constitutional amendment; it goes to President Tinubu for
    assent (Tribune; The Whistler).
27. Bangladesh garment workers demanding a Tk 30,000 minimum wage
    clashed with police; scores of factories shut (AP; Prothom Alo).
28. The European Commission proposed a new EUR 45bn loan to Ukraine
    for 2027, repayable only after Russia pays reparations
    (Reuters; Kyiv Independent).
29. A magnitude 5.9 earthquake struck off San Juan, Peru; no damage
    and no tsunami threat (USGS; Infobae).
30. Amnesty International: nine RSF drone strikes around El Obeid,
    Sudan, killed 37 civilians; it urged a war-crimes probe, the
    RSF denied responsibility (Amnesty; Eastleigh Voice).

The drawing is fully deterministic: fixed canvas, fixed fonts,
no randomness, no network. Output: entry.png next to this file.
"""

from pathlib import Path
import math

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
    size = start
    while size > min_size:
        fnt = font(path, size)
        if text_w(draw, s, fnt) <= max_w:
            return fnt
        size -= 2
    return font(path, min_size)


def wrap(draw, s, fnt, max_w):
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


def badge(draw, x, y, n, col):
    r = 11
    draw.ellipse([x, y, x + 2 * r, y + 2 * r], fill=col)
    s = str(n)
    f = font(BOLD, 13)
    draw.text((x + r - text_w(draw, s, f) / 2, y + r - 8), s, font=f, fill=(255, 255, 255))


def panel(draw, x, y, w, h, n, tag, tag_col, headline, body):
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=NAVY, width=3)
    draw.rectangle([x, y, x + w, y + 26], fill=tag_col)
    badge(draw, x + 6, y + 2, n, NAVY)
    draw.text((x + 34, y + 3), tag, font=font(BOLD, 16), fill=(255, 255, 255))
    hf = fit(draw, headline, BLACK, 25, 17, w - 20)
    hlines = wrap(draw, headline, hf, w - 20)
    yy = draw_lines(draw, hlines, x + 10, y + 33, hf, NAVY, hf.size + 3)
    bsize = 16
    while bsize > 13:
        bf = font(REG, bsize)
        blines = wrap(draw, body, bf, w - 20)
        if yy + 3 + len(blines) * (bsize + 4) <= y + h - 4:
            break
        bsize -= 1
    draw_lines(draw, blines, x + 10, yy + 3, bf, INK, bsize + 4)


def small_panel(draw, x, y, w, h, n, tag, tag_col, headline, body):
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=NAVY, width=3)
    draw.rectangle([x, y, x + w, y + 24], fill=tag_col)
    badge(draw, x + 5, y + 1, n, NAVY)
    draw.text((x + 32, y + 2), tag, font=font(BOLD, 15), fill=(255, 255, 255))
    hf = fit(draw, headline, BLACK, 20, 14, w - 18)
    draw.text((x + 9, y + 30), headline, font=hf, fill=NAVY)
    bf = font(REG, 14)
    blines = wrap(draw, body, bf, w - 18)
    draw_lines(draw, blines, x + 9, y + 58, bf, INK, 18)


BRIEFS = [
    ("RIYADH", "Saudi defences down Houthi cruise missile"),
    ("GOLD", "Price slides under $3,800 — a one-year low"),
    ("LONDON", "UK inflation climbs to 3.6%, highest in a year"),
    ("US COURT", "Iran-linked Trump plotter jailed 27+ years"),
    ("CONGO", "Ebola passes 11,000 cases, 5,500 dead"),
    ("SIBERIA", "An-12 crash kills all 19 aboard; inquiry opens"),
    ("CANBERRA", "Australia sanctions 3 settlers, 4 groups"),
    ("GAMES", "GTA VI rollout begins in NZ; ~16m pre-orders"),
    ("EUROPE", "Resistant infections up 72% since 2019 — ECDC"),
    ("TECH", "Waymo halts freeway rides after California ban"),
    ("BRATISLAVA", "25,000 rally against Fico's government"),
    ("HAITI", "Security pact with El Salvador formalised"),
    ("SEOUL", "Lee asks Xi for help on peninsula peace"),
    ("MANILA", "Trump hails trade deal; Manila: none signed"),
    ("NEW ZEALAND", "Mystery tsunami advisory cancelled in an hour"),
    ("NIGERIA", "All 36 states back state-police amendment"),
    ("BANGLADESH", "Garment wage clashes shut scores of factories"),
    ("BRUSSELS", "EU proposes €45bn Ukraine loan for 2027"),
    ("PERU", "M5.9 quake off San Juan; no damage reported"),
    ("SUDAN", "Amnesty: RSF strikes killed 37 in El Obeid"),
]


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, W - 10, H - 10], outline=NAVY, width=5)

    # ---- Masthead -------------------------------------------------
    d.rectangle([28, 24, W - 28, 52], fill=RED)
    kick = "W O R L D   N E W S   •   O N E   D A Y   •   O N E   P I C T U R E"
    kf = fit(d, kick, BOLD, 21, 13, W - 80)
    d.text(((W - text_w(d, kick, kf)) / 2, 29), kick, font=kf, fill=(255, 255, 255))
    date = "WEDNESDAY 18 NOVEMBER 2026"
    df = fit(d, date, BLACK, 52, 30, W - 56)
    d.text(((W - text_w(d, date, df)) / 2, 58), date, font=df, fill=NAVY)
    sub = "30 STORIES  •  SIX CONTINENTS  •  EVERY STORY FROM THIS ONE DAY"
    sf = fit(d, sub, BOLD, 19, 12, W - 56)
    d.text(((W - text_w(d, sub, sf)) / 2, 116), sub, font=sf, fill=RED)
    d.line([28, 142, W - 28, 142], fill=NAVY, width=3)

    # ---- Lead story: Shenzhen trilateral --------------------------
    lx, ly, lw, lh = 28, 152, W - 56, 180
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=NAVY)
    d.rectangle([lx + 12, ly + 12, lx + 380, ly + 44], fill=RED)
    d.text((lx + 22, ly + 17), "1  •  TOP STORY — APEC, SHENZHEN", font=font(BOLD, 19),
           fill=(255, 255, 255))
    lead_head = "XI + PUTIN MEET — TRUMP LANDS IN CHINA"
    hf = fit(d, lead_head, BLACK, 38, 24, lw - 32)
    d.text((lx + 16, ly + 54), lead_head, font=hf, fill=(255, 255, 255))
    lead_body = ("Xi Jinping met Vladimir Putin in Shenzhen, then greeted Donald Trump on the "
                 "tarmac. Their first-ever US–China–Russia trilateral summit follows Thu 19 Nov. "
                 "Xi backed open trade; Putin attacked sanctions.")
    bf = font(REG, 19)
    draw_lines(d, wrap(d, lead_body, bf, lw - 32), lx + 16, ly + 100, bf, (226, 232, 242), 25)
    fy = ly + 146
    fx = lx + 16
    for draw_flag, name in [(flag_china, "XI • CHINA"), (flag_russia, "PUTIN • RUSSIA"),
                            (flag_usa, "TRUMP • USA")]:
        draw_flag(d, fx, fy, 58, 30)
        d.rectangle([fx, fy, fx + 58, fy + 30], outline=(255, 255, 255), width=2)
        d.text((fx + 64, fy + 8), name, font=font(BOLD, 13), fill=(255, 255, 255))
        fx += 176
    note = "FIRST TRILATERAL SUMMIT: THU 19 NOV"
    nf2 = font(BLACK, 16)
    d.text((lx + lw - 16 - text_w(d, note, nf2), fy + 7), note, font=nf2, fill=GOLD)

    # ---- Row A: war & diplomacy -----------------------------------
    gw = (W - 56 - 2 * 12) // 3
    panel(d, 28, 344, gw, 158, 2, "UKRAINE WAR", (0, 91, 172),
          "UKRAINE HITS CRIMEAN BRIDGE",
          "Zelenskyy confirms the strike partially destroyed the Kerch Bridge "
          "to Crimea. Kyiv urges summit leaders to pressure Putin.")
    panel(d, 28 + gw + 12, 344, gw, 158, 3, "MIDDLE EAST • HORMUZ", RED,
          "IRAN–US CLASH: TANKER HIT",
          "Iran struck the US base in Kuwait after a US strike on Qeshm Island. "
          "ADNOC tanker hit in Hormuz: 11 injured, 1 missing.")
    panel(d, 28 + 2 * (gw + 12), 344, gw, 158, 4, "GAZA • ISRAEL", (96, 84, 160),
          "ISRAEL OPENS NEW GAZA OPERATION",
          "Army begins a concentrated operation in three areas of central Gaza. "
          "Knesset elects opposition-backed speaker Kahana.")

    # ---- Row B: politics, climate, business ------------------------
    panel(d, 28, 514, gw, 158, 5, "US MIDTERMS • ALASKA", (0, 110, 84),
          "DEMOCRATS TAKE SENATE 56–44",
          "Mary Peltola defeats Sen. Sullivan in the last race called — first "
          "Alaska Native senator. Biggest Senate flip since 1958.")
    panel(d, 28 + gw + 12, 514, gw, 158, 6, "CLIMATE • COP31", (0, 120, 110),
          "COP31 SPLITS OVER FOSSIL PHASE-OUT",
          "A draft deal's rival wordings divide nearly 200 nations in Antalya. "
          "The EU calls the text untenable; deadline Friday.")
    panel(d, 28 + 2 * (gw + 12), 514, gw, 158, 7, "BUSINESS • NVIDIA", (70, 70, 120),
          "NVIDIA REVENUE DOUBLES TO $115.8BN",
          "Data-centre demand drives sales up 103%. The board rules out a "
          "return for former CEO Jensen Huang.")

    # ---- Row C: health / weather / space ---------------------------
    small_panel(d, 28, 684, gw, 100, 8, "HEALTH • USA", RED,
                "US LOSES MEASLES STATUS",
                "Elimination status gone after 5,400+ cases in 2026.")
    small_panel(d, 28 + gw + 12, 684, gw, 100, 9, "WEATHER • INDIA", (0, 91, 172),
                "CYCLONE AKVAN NEARS COAST",
                "Severe storm: landfall Andhra–Odisha Fri 20 Nov, 100–110 km/h.")
    small_panel(d, 28 + 2 * (gw + 12), 684, gw, 100, 10, "SPACE • NASA", NAVY2,
                "VOYAGER 1: ONE LIGHT-DAY",
                "First object 25.9bn km away. A signal now takes 24 hours.")

    # ---- Also on Wednesday: 20 briefs ------------------------------
    ay = 792
    d.rectangle([28, ay, W - 28, ay + 26], fill=NAVY)
    d.text((40, ay + 4), "ALSO ON WEDNESDAY — 20 MORE STORIES",
           font=font(BOLD, 17), fill=(255, 255, 255))
    tally = "EUROPE 6 · M. EAST 3 · ASIA 6 · AFRICA 4 · AMERICAS 6 · OCEANIA 3 · GLOBAL 2"
    tf = font(BOLD, 13)
    d.text((W - 40 - text_w(d, tally, tf), ay + 6), tally, font=tf, fill=GOLD)
    col_w = (W - 56 - 16) // 2
    bf2 = font(REG, 14)
    bfb = font(BOLD, 14)
    for i, (place, text) in enumerate(BRIEFS):
        col = 0 if i < 10 else 1
        row = i % 10
        x = 28 + col * (col_w + 16)
        y = ay + 36 + row * 15
        num = f"{11 + i}"
        d.text((x, y), num, font=font(BOLD, 13), fill=RED)
        px = x + 24
        d.text((px, y), place + " — ", font=bfb, fill=NAVY)
        px += text_w(d, place + " — ", bfb)
        d.text((px, y), text, font=bf2, fill=INK)
    d.line([28 + col_w + 8, ay + 34, 28 + col_w + 8, ay + 190], fill=(190, 184, 168), width=1)

    # ---- Footer ----------------------------------------------------
    foot = ("Every story reported on Wed 18 Nov 2026 and checked in 2+ outlets • Sources: AP • Reuters • AFP • "
            "Al Jazeera • Yonhap • ECDC • ONS • IMD • NASA • PAHO • USGS • Amnesty")
    ff = fit(d, foot, REG, 14, 10, W - 56)
    d.text(((W - text_w(d, foot, ff)) / 2, 986), foot, font=ff, fill=GREY)

    out = Path(__file__).with_name("entry.png")
    img.save(out, format="PNG", optimize=True)
    return out


if __name__ == "__main__":
    p = build()
    print(p, p.stat().st_size, "bytes")
