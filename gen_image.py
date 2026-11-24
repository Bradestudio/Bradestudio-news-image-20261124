"""Draw the front page that sums up Tuesday 24 November 2026.

Pillow only, no network, no clock, no randomness: two runs of this file
produce byte-identical PNGs. The page is a newspaper front page built
around three illustrated hero panels, a UTC timeline, a numbers strip,
nine briefs with drawn thumbnails, a dot-matrix world map and a numbered
list of the rest of the day's stories.
"""

from PIL import Image, ImageDraw, ImageFont

PAGE_W = 1024
PAGE_H = 1024
MARGIN = 22

INK = (24, 24, 26)
PAPER = (250, 247, 238)
RULE_RED = (176, 32, 28)
MUTED = (96, 90, 82)
PANEL = (255, 255, 255)
PANEL_EDGE = (206, 198, 186)
TAG_GREEN = (28, 110, 66)
TAG_AMBER = (166, 96, 8)
TAG_BLUE = (28, 84, 150)
SKY_NIGHT = (18, 26, 48)
SEA = (16, 58, 86)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    """Load a TrueType font, falling back to Pillow's built-in bitmap font
    when the file is missing (e.g. a minimal container without DejaVu)."""
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def shrink_to_fit(draw, text, path, size, max_w, min_size=7):
    """Largest font size <= size whose text fits max_w, else the smallest."""
    while size > min_size:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, min_size)


def wrap(draw, text, f, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, f, max_w, max_lines):
    """Wrap text and clip to max_lines, adding an ellipsis when clipped."""
    lines = wrap(draw, text, f, max_w)
    if len(lines) <= max_lines:
        return lines
    clipped = lines[:max_lines]
    last = clipped[-1]
    while last and draw.textlength(last + "…", font=f) > max_w:
        last = last[:-1]
    clipped[-1] = last + "…"
    return clipped


def tag_chip(draw, x, y, label, fill):
    """A small coloured certainty tag; returns the width it used."""
    f = font(SANS_B, 9)
    w = int(draw.textlength(label, font=f)) + 10
    draw.rounded_rectangle([x, y, x + w, y + 15], radius=3, fill=fill)
    draw.text((x + 5, y + 3), label, font=f, fill=(255, 255, 255))
    return w


# ---------------------------------------------------------------- stories

HEROES = [
    {
        "no": 1,
        "kicker": "INDONESIA · BANTEN",
        "head": "Candy factory fire kills 24; about 30 still missing",
        "body": "Fire tore through the Fonusa Agung Mulia sweet factory in Cikande; "
                "the search for the missing goes on.",
        "tag": "REPORTED",
        "art": "fire",
    },
    {
        "no": 2,
        "kicker": "UKRAINE · OFF LIBYA",
        "head": "Kyiv claims its sea drones sank a Russian warship",
        "body": "Zelenskyy says seven naval drones sank the corvette Merkury at "
                "Benghazi; satellite images show it capsized.",
        "tag": "CLAIM",
        "art": "ship",
    },
    {
        "no": 3,
        "kicker": "CLIMATE · ANTALYA",
        "head": "COP31 ends with no deal as the fossil-fuel fight sinks it",
        "body": "The summit closed two days late with no overall deal; the EU "
                "refused a text that never named fossil fuels.",
        "tag": "REPORTED",
        "art": "cop",
    },
]

BRIEFS = [
    {
        "no": 4, "head": "Huang is back — Nvidia gains ~$1tn in a day",
        "body": "The board reinstated Jensen Huang as CEO 11 days after he quit; "
                "shares jumped about 31%.",
        "tag": "REPORTED", "art": "chip",
    },
    {
        "no": 5, "head": "Russian strikes hit Kyiv region; deaths in Dymer",
        "body": "Missiles and drones hammered targets across Ukraine overnight "
                "as Kyiv warned of more strikes.",
        "tag": "REPORTED", "art": "blast",
    },
    {
        "no": 6, "head": "Sparta II ablaze after drone hit in Gulf of Finland",
        "body": "The Russian cargo ship caught fire; all 16 crew were evacuated "
                "safely.",
        "tag": "REPORTED", "art": "tanker",
    },
    {
        "no": 7, "head": "ICJ: Myanmar committed genocide against Rohingya",
        "body": "The world court held Myanmar responsible by 9 votes to 6 in the "
                "case The Gambia filed in 2019.",
        "tag": "REPORTED", "art": "court",
    },
    {
        "no": 8, "head": "Trump blames Democrats as Wall Street sheds ~$1tn",
        "body": "Stocks slid after the midterm results; the president blamed the "
                "opposition.",
        "tag": "REPORTED", "art": "market",
    },
    {
        "no": 9, "head": "India–Nepal: 8 deals, Rs 15,000 crore package",
        "body": "PM Modi and Nepal's PM Shah signed eight MoUs on the first "
                "bilateral visit.",
        "tag": "REPORTED", "art": "hands",
    },
    {
        "no": 10, "head": "India v New Zealand, 1st Test ends in a draw",
        "body": "Rahul's 136 and Gill's 98 set it up; Pant passed 600 runs as "
                "Wellington ended level.",
        "tag": "REPORTED", "art": "cricket",
    },
    {
        "no": 11, "head": "Alcaraz wins his first ATP Finals title",
        "body": "The Spaniard beat Zverev in Turin to lift the season-ending "
                "trophy for the first time.",
        "tag": "REPORTED", "art": "trophy",
    },
    {
        "no": 12, "head": "World Chess Championship opens in Geneva",
        "body": "Gukesh faces Sindarov for the crown as the title match begins "
                "in Switzerland.",
        "tag": "REPORTED", "art": "chess",
    },
]

REST = [
    (13, "South Korea reshuffle: new foreign minister and first woman spy chief"),
    (14, "Armenia proposes a new constitution in a step toward peace with Azerbaijan"),
    (15, "China sets 2030 social-welfare targets for elderly care and childcare"),
    (16, "Bangladesh vows to arrest Sheikh Hasina if she returns from India"),
    (17, "Waymo halts driverless taxis on every US freeway"),
    (18, "Migrant boat sinks off Senegal; dozens missing"),
    (19, "Settler arson in the West Bank condemned as “Jewish terrorism”"),
    (20, "Sensex falls 1,484 points to 82,435"),
    (21, "Denmark's high court backs the “ghetto law” on immigration"),
    (22, "US appeals court lets Trump erase his hush-money conviction"),
    (23, "FIFA Congress picks hosts of the 2031 and 2035 Women's World Cups"),
    (24, "Supermoon meets the Seven Sisters (Pleiades) in the night sky"),
    (25, "Modi opens an AI centre at IIT Patna and a Rs 400 crore research park"),
    (26, "India–China military talks held in Arunachal Pradesh"),
    (27, "India's top court grants bail in the Godhra train-burning case"),
    (28, "De Bruyne: feelings for Man City “will never change”"),
    (29, "Zelenskyy: intelligence shows Russia is planning new strikes"),
    (30, "Moscow accuses Estonia of actions “on the verge of open war”"),
    (31, "US to blacklist Megaspeed chip firm linked to the Nvidia scandal"),
    (32, "Israeli strikes kill at least 3 in Gaza, including a UN worker"),
    (33, "Fourteen countries acknowledge the ICJ Rohingya ruling"),
    (34, "Denmark to propose a mobile-phone ban in schools from 2027"),
    (35, "Iran vows to counter the US naval blockade “by all means”"),
    (36, "Trump hosts a gala for investors in his plunging meme coin"),
    (37, "WHO: fighting near the Congo Ebola outbreak disrupts the response"),
    (38, "Finland summons Russia's envoy over a suspected helicopter incursion"),
    (39, "WFP: conflicts put food aid for 7m more people at risk"),
    (40, "EU unveils its latest sanctions package against Moscow"),
    (41, "South Korea's education minister quits over an exam-fraud scandal"),
    (42, "Democrats take the House with the widest margin in 50 years"),
    (43, "Afghanistan landmine blasts have killed 257 people this year"),
    (44, "Tajikistan withdraws from the International Criminal Court"),
]

TIMELINE = [
    ("02:00", "Zelenskyy claims the Merkury sinking"),
    ("06:00", "Serang toll confirmed at 24 dead"),
    ("09:30", "Nvidia soars as Huang returns"),
    ("13:00", "EU unveils new Russia sanctions"),
    ("16:00", "Seoul announces security reshuffle"),
    ("20:00", "India–Nepal sign eight MoUs"),
]

NUMBERS = [
    ("24", "dead in Serang"),
    ("~30", "still missing"),
    ("7", "sea drones"),
    ("+31%", "Nvidia shares"),
    ("$1tn", "Nvidia regained"),
    ("1,484", "Sensex pts lost"),
    ("8", "India–Nepal MoUs"),
    ("258", "Dem House seats"),
]

# (x, y) in a 0..100 map grid, label, label offset (dx, dy), story no.
PINS = [
    (82, 62, "SERANG", (8, -4), 1),
    (48, 56, "BENGHAZI", (10, 16), 2),
    (55, 47, "ANTALYA", (10, 4), 3),
    (8, 44, "SILICON VALLEY", (8, 6), 4),
    (57, 27, "KYIV", (8, -4), 5),
    (55, 20, "GULF OF FINLAND", (-36, -15), 6),
    (44, 30, "THE HAGUE", (-66, -14), 7),
    (22, 42, "WASHINGTON", (-10, -14), 8),
    (72, 46, "KATHMANDU", (8, -4), 9),
    (96, 78, "WELLINGTON", (-80, -4), 10),
    (51, 43, "TURIN", (10, 14), 11),
    (46, 40, "GENEVA", (-64, 14), 12),
]

TAG_FILL = {"REPORTED": TAG_GREEN, "CLAIM": TAG_AMBER, "FORECAST": TAG_BLUE}


# ------------------------------------------------------- hero illustrations

def art_factory(draw, x, y, w, h):
    """A candy factory at night, one wall blown open by fire."""
    draw.rectangle([x, y, x + w, y + h], fill=(26, 22, 30))
    # dusk band and stars
    draw.rectangle([x, y, x + w, y + 26], fill=(58, 28, 34))
    for sx, sy in [(18, 10), (52, 6), (96, 14), (150, 8), (210, 12), (268, 7)]:
        draw.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 240, 200))
    # factory block
    fx, fy = x + 24, y + h - 62
    draw.rectangle([fx, fy, fx + 210, y + h], fill=(64, 58, 66))
    draw.rectangle([fx, fy, fx + 210, fy + 8], fill=(44, 40, 48))
    for i in range(5):
        wx = fx + 14 + i * 40
        draw.rectangle([wx, fy + 22, wx + 24, fy + 44], fill=(255, 214, 130))
    # chimney
    draw.rectangle([fx + 186, fy - 26, fx + 202, fy], fill=(52, 48, 56))
    # fire bursting from the middle windows
    cx = fx + 105
    for r, col in [(46, (255, 90, 20)), (34, (255, 150, 30)), (22, (255, 210, 80))]:
        draw.polygon([
            (cx - r, fy + 46), (cx - r * 0.55, fy - 6),
            (cx - r * 0.2, fy + 30), (cx + r * 0.15, fy - 18),
            (cx + r * 0.5, fy + 28), (cx + r * 0.85, fy + 2),
            (cx + r, fy + 46),
        ], fill=col)
    # smoke puffs, kept inside the panel
    for px, py, pr in [(cx - 48, fy - 14, 11), (cx - 26, fy - 24, 12),
                       (cx + 6, fy - 28, 11), (cx + 38, fy - 18, 10)]:
        draw.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(88, 82, 90))
    # ground line + search lights
    draw.rectangle([x, y + h - 6, x + w, y + h], fill=(16, 14, 18))
    draw.line([x + 40, y + h - 6, x + 90, y + 60], fill=(255, 240, 180), width=2)
    draw.line([x + w - 40, y + h - 6, x + w - 96, y + 66], fill=(255, 240, 180), width=2)


def art_warship(draw, x, y, w, h):
    """A corvette capsized at a pier, sea drones closing in, night sea."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY_NIGHT)
    draw.ellipse([x + w - 52, y + 12, x + w - 16, y + 48], fill=(238, 228, 190))
    for sx, sy in [(14, 12), (44, 22), (90, 8), (140, 18), (190, 10)]:
        draw.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    # pier
    draw.rectangle([x, y + h - 52, x + w, y + h - 40], fill=(52, 48, 44))
    # sea
    draw.rectangle([x, y + h - 40, x + w, y + h], fill=(14, 44, 70))
    for wy in range(y + h - 36, y + h - 2, 9):
        draw.line([x + 6, wy, x + w - 6, wy], fill=(34, 84, 120), width=1)
    # capsized hull: a long pale-grey hull heeled over, bow lifted clear
    hx, hy = x + 66, y + h - 78
    draw.polygon([(hx, hy + 34), (hx + 168, hy + 52), (hx + 184, hy + 38),
                  (hx + 176, hy + 22), (hx + 30, hy + 12)],
                 fill=(96, 100, 110))
    draw.polygon([(hx + 30, hy + 12), (hx + 176, hy + 22), (hx + 184, hy + 38),
                  (hx + 168, hy + 52), (hx + 160, hy + 44), (hx + 40, hy + 26)],
                 fill=(52, 54, 62))
    # superstructure block, tipped toward the water
    draw.polygon([(hx + 96, hy + 16), (hx + 128, hy + 20), (hx + 124, hy + 34),
                  (hx + 94, hy + 30)], fill=(86, 88, 96))
    # radar mast leaning out of the water near the bow
    draw.line([hx + 52, hy + 18, hx + 26, hy - 2], fill=(150, 152, 160), width=3)
    draw.line([hx + 26, hy - 2, hx + 40, hy - 8], fill=(150, 152, 160), width=2)
    # small fire on the deck, low and contained
    for r, col in [(16, (255, 110, 20)), (10, (255, 170, 40)), (5, (255, 224, 110))]:
        draw.ellipse([hx + 138 - r, hy + 26 - r, hx + 138 + r, hy + 26 + r], fill=col)
    # two sea drones with wakes
    for dx, dy in [(x + 22, y + h - 22), (x + 52, y + h - 12)]:
        draw.ellipse([dx, dy, dx + 16, dy + 6], fill=(210, 214, 220))
        draw.line([dx - 22, dy + 3, dx, dy + 3], fill=(180, 200, 220), width=2)
    # smoke column, kept inside the panel
    for px, py, pr in [(hx + 138, hy + 4, 10), (hx + 130, hy - 8, 11),
                       (hx + 142, hy - 16, 8)]:
        draw.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(70, 76, 88))


def art_summit(draw, x, y, w, h):
    """An empty summit hall in Antalya: a broken globe on a table."""
    draw.rectangle([x, y, x + w, y + h], fill=(34, 44, 62))
    # tall windows
    for i in range(3):
        wx = x + 22 + i * 96
        draw.rectangle([wx, y + 10, wx + 72, y + 74], fill=(120, 150, 190))
        draw.line([wx + 36, y + 10, wx + 36, y + 74], fill=(34, 44, 62), width=3)
    # table
    draw.rectangle([x + 30, y + h - 66, x + w - 30, y + h - 52], fill=(96, 68, 44))
    draw.rectangle([x + 44, y + h - 52, x + 58, y + h], fill=(70, 50, 34))
    draw.rectangle([x + w - 58, y + h - 52, x + w - 44, y + h], fill=(70, 50, 34))
    # broken globe: two halves with a crack of light between them
    gx, gy = x + w // 2, y + h - 78
    draw.pieslice([gx - 28, gy - 28, gx + 28, gy + 28], 90, 270, fill=(46, 110, 70))
    draw.pieslice([gx - 28, gy - 28, gx + 28, gy + 28], 270, 90, fill=(30, 84, 56))
    draw.arc([gx - 28, gy - 28, gx + 28, gy + 28], 0, 360, fill=(210, 220, 230), width=2)
    draw.polygon([(gx - 3, gy - 28), (gx + 6, gy - 8), (gx - 4, gy + 12),
                  (gx + 5, gy + 28)], fill=(250, 240, 180))
    # scattered papers and a gavel
    draw.rectangle([x + 46, y + h - 78, x + 92, y + h - 68], fill=(240, 238, 228))
    draw.rectangle([x + w - 96, y + h - 80, x + w - 52, y + h - 70], fill=(228, 226, 216))
    draw.rectangle([x + w // 2 - 46, y + h - 46, x + w // 2 - 10, y + h - 38],
                   fill=(120, 84, 40))
    draw.rectangle([x + w // 2 - 34, y + h - 52, x + w // 2 - 22, y + h - 38],
                   fill=(120, 84, 40))
    # empty chairs
    for cx in (x + 52, x + w - 52):
        draw.rectangle([cx - 16, y + h - 40, cx + 16, y + h - 8], fill=(58, 52, 60))
        draw.rectangle([cx - 16, y + h - 66, cx + 16, y + h - 40], fill=(72, 66, 74))


HERO_ART = {"fire": art_factory, "ship": art_warship, "cop": art_summit}


# ------------------------------------------------------- brief thumbnails

def thumb(draw, x, y, s, kind):
    """A 44px square thumbnail drawn with plain shapes."""
    draw.rectangle([x, y, x + s, y + s], outline=PANEL_EDGE, width=1)
    if kind == "chip":
        draw.rectangle([x, y, x + s, y + s], fill=(16, 26, 44))
        draw.rectangle([x + 8, y + 14, x + 36, y + 30], fill=(34, 130, 90))
        for i in range(4):
            draw.line([x + 12 + i * 6, y + 18, x + 12 + i * 6, y + 26],
                      fill=(200, 230, 210), width=2)
        draw.line([x + 6, y + 34, x + 38, y + 34], fill=(255, 200, 60), width=3)
    elif kind == "blast":
        draw.rectangle([x, y, x + s, y + s], fill=(30, 26, 34))
        for r, col in [(14, (255, 110, 20)), (9, (255, 180, 50)), (5, (255, 230, 120))]:
            draw.ellipse([x + 22 - r, y + 20 - r, x + 22 + r, y + 20 + r], fill=col)
        draw.rectangle([x + 6, y + 36, x + 38, y + s - 4], fill=(52, 48, 56))
    elif kind == "tanker":
        draw.rectangle([x, y, x + s, y + s], fill=(18, 52, 78))
        draw.rectangle([x + 4, y + 24, x + 40, y + 32], fill=(40, 42, 48))
        draw.rectangle([x + 26, y + 16, x + 34, y + 24], fill=(70, 72, 80))
        for r, col in [(7, (255, 120, 20)), (4, (255, 200, 80))]:
            draw.ellipse([x + 12 - r, y + 14 - r, x + 12 + r, y + 14 + r], fill=col)
        draw.rectangle([x, y + 34, x + s, y + s], fill=(12, 40, 64))
    elif kind == "court":
        draw.rectangle([x, y, x + s, y + s], fill=(232, 228, 216))
        draw.rectangle([x + 6, y + 34, x + 38, y + 38], fill=(90, 80, 66))
        for i in range(3):
            draw.rectangle([x + 9 + i * 11, y + 20, x + 13 + i * 11, y + 34],
                           fill=(110, 100, 84))
        draw.polygon([(x + 4, y + 20), (x + 22, y + 8), (x + 40, y + 20)],
                     fill=(140, 40, 34))
    elif kind == "market":
        draw.rectangle([x, y, x + s, y + s], fill=(245, 242, 234))
        draw.line([x + 6, y + 34, x + 14, y + 26, x + 22, y + 30, x + 30, y + 18,
                   x + 38, y + 12], fill=(176, 32, 28), width=3)
        draw.polygon([(x + 34, y + 8), (x + 40, y + 8), (x + 37, y + 15)],
                     fill=(176, 32, 28))
    elif kind == "hands":
        draw.rectangle([x, y, x + s, y + s], fill=(26, 60, 96))
        draw.ellipse([x + 8, y + 12, x + 36, y + 32], fill=(46, 110, 70))
        draw.arc([x + 8, y + 12, x + 36, y + 32], 0, 360, fill=(255, 255, 255), width=2)
        draw.line([x + 10, y + 22, x + 34, y + 22], fill=(255, 255, 255), width=2)
    elif kind == "cricket":
        draw.rectangle([x, y, x + s, y + s], fill=(52, 110, 52))
        draw.ellipse([x + 6, y + 6, x + 38, y + 38], fill=(120, 170, 90))
        draw.rectangle([x + 20, y + 8, x + 24, y + 36], fill=(240, 236, 220))
        draw.ellipse([x + 28, y + 26, x + 34, y + 32], fill=(176, 32, 28))
    elif kind == "trophy":
        draw.rectangle([x, y, x + s, y + s], fill=(30, 30, 44))
        draw.polygon([(x + 14, y + 10), (x + 30, y + 10), (x + 27, y + 24),
                      (x + 17, y + 24)], fill=(255, 200, 60))
        draw.rectangle([x + 20, y + 24, x + 24, y + 32], fill=(255, 200, 60))
        draw.rectangle([x + 14, y + 32, x + 30, y + 36], fill=(255, 200, 60))
        draw.arc([x + 8, y + 10, x + 16, y + 22], 90, 270, fill=(255, 200, 60), width=2)
        draw.arc([x + 28, y + 10, x + 36, y + 22], 270, 90, fill=(255, 200, 60), width=2)
    else:  # chess
        draw.rectangle([x, y, x + s, y + s], fill=(245, 242, 234))
        for r in range(4):
            for c in range(4):
                if (r + c) % 2 == 0:
                    draw.rectangle([x + 6 + c * 8, y + 6 + r * 8,
                                    x + 14 + c * 8, y + 14 + r * 8], fill=(40, 40, 44))
        draw.ellipse([x + 26, y + 8, x + 34, y + 16], fill=(24, 24, 26))
        draw.rectangle([x + 24, y + 16, x + 36, y + 20], fill=(24, 24, 26))


# ------------------------------------------------------------- page sections

def draw_masthead(draw):
    title = "THE WORLD IN ONE PAGE"
    tf = shrink_to_fit(draw, title, SERIF, 46, PAGE_W - 2 * MARGIN)
    draw.text(((PAGE_W - draw.textlength(title, font=tf)) / 2, 10),
              title, font=tf, fill=INK)
    date = "TUESDAY, 24 NOVEMBER 2026"
    df = font(SANS_B, 17)
    draw.text(((PAGE_W - draw.textlength(date, font=df)) / 2, 58),
              date, font=df, fill=RULE_RED)
    sub = "44 stories from the wires · one day · drawn from scratch"
    sf = font(SANS, 11)
    draw.text(((PAGE_W - draw.textlength(sub, font=sf)) / 2, 76),
              sub, font=sf, fill=MUTED)
    draw.rectangle([MARGIN, 94, PAGE_W - MARGIN, 97], fill=RULE_RED)


def draw_hero(draw, hero, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=PANEL, outline=PANEL_EDGE, width=1)
    art_h = 112
    HERO_ART[hero["art"]](draw, x + 1, y + 1, w - 2, art_h)
    ty = y + art_h + 8
    kf = font(SANS_B, 10)
    draw.text((x + 10, ty), hero["kicker"], font=kf, fill=RULE_RED)
    tag_chip(draw, x + w - 82, ty - 1, hero["tag"], TAG_FILL[hero["tag"]])
    hf = font(SERIF, 18)
    lines = fit_lines(draw, hero["head"], hf, w - 20, 2)
    hy = ty + 17
    for ln in lines:
        draw.text((x + 10, hy), ln, font=hf, fill=INK)
        hy += 20
    bf = font(SANS, 10)
    blines = fit_lines(draw, hero["body"], bf, w - 20, 2)
    by = hy + 3
    for ln in blines:
        draw.text((x + 10, by), ln, font=bf, fill=(52, 50, 48))
        by += 13
    # story number in a red disc, top-left over the art
    draw.ellipse([x + 8, y + 8, x + 32, y + 32], fill=RULE_RED)
    nf = font(SANS_B, 14)
    num = str(hero["no"])
    draw.text((x + 20 - draw.textlength(num, font=nf) / 2, y + 13),
              num, font=nf, fill=(255, 255, 255))


def draw_timeline(draw, y):
    draw.rectangle([MARGIN, y, PAGE_W - MARGIN, y + 66], fill=PANEL,
                   outline=PANEL_EDGE, width=1)
    tf = font(SANS_B, 11)
    draw.text((MARGIN + 10, y + 6), "THE DAY IN UTC", font=tf, fill=INK)
    note = "times approximate · UTC"
    nf = font(SANS, 9)
    draw.text((PAGE_W - MARGIN - 10 - draw.textlength(note, font=nf), y + 7),
              note, font=nf, fill=MUTED)
    line_y = y + 42
    draw.line([MARGIN + 16, line_y, PAGE_W - MARGIN - 16, line_y],
              fill=(180, 172, 158), width=2)
    slot_w = (PAGE_W - 2 * MARGIN - 32) / 6
    for i, (t, label) in enumerate(TIMELINE):
        cx = MARGIN + 16 + slot_w * i + slot_w / 2
        draw.ellipse([cx - 4, line_y - 4, cx + 4, line_y + 4], fill=RULE_RED)
        tf2 = font(SANS_B, 11)
        draw.text((cx - draw.textlength(t, font=tf2) / 2, line_y - 20),
                  t, font=tf2, fill=RULE_RED)
        lf = font(SANS, 8)
        for j, ln in enumerate(wrap(draw, label, lf, slot_w - 6)):
            draw.text((cx - draw.textlength(ln, font=lf) / 2, line_y + 8 + j * 10),
                      ln, font=lf, fill=(52, 50, 48))


def draw_numbers(draw, y):
    draw.rectangle([MARGIN, y, PAGE_W - MARGIN, y + 40], fill=INK)
    tf = font(SANS_B, 10)
    draw.text((MARGIN + 10, y + 4), "BY THE NUMBERS", font=tf, fill=(255, 210, 90))
    slot_w = (PAGE_W - 2 * MARGIN - 180) / len(NUMBERS)
    for i, (num, label) in enumerate(NUMBERS):
        cx = MARGIN + 180 + slot_w * i + slot_w / 2
        nf = font(SANS_B, 14)
        draw.text((cx - draw.textlength(num, font=nf) / 2, y + 5),
                  num, font=nf, fill=(255, 255, 255))
        lf = font(SANS, 8)
        lab = label if draw.textlength(label, font=lf) <= slot_w - 4 else label[:12]
        draw.text((cx - draw.textlength(lab, font=lf) / 2, y + 24),
                  lab, font=lf, fill=(200, 196, 188))


def draw_briefs(draw, y):
    cols, rows = 3, 3
    cw = (PAGE_W - 2 * MARGIN - 2 * 10) // cols
    ch = 58
    for idx, b in enumerate(BRIEFS):
        r, c = divmod(idx, cols)
        bx = MARGIN + c * (cw + 10)
        by = y + r * (ch + 6)
        draw.rectangle([bx, by, bx + cw, by + ch], fill=PANEL,
                       outline=PANEL_EDGE, width=1)
        thumb(draw, bx + 6, by + 7, 44, b["art"])
        tx = bx + 56
        hf = shrink_to_fit(draw, b["head"], SANS_B, 11, cw - 62)
        hl = fit_lines(draw, b["head"], hf, cw - 62, 2)
        hy = by + 5
        for ln in hl:
            draw.text((tx, hy), ln, font=hf, fill=INK)
            hy += 13
        bf = font(SANS, 8)
        bl = fit_lines(draw, b["body"], bf, cw - 62, 2)
        if len(bl) == 2:
            # keep the second line clear of the tag chip at bottom-right
            second = bl[1]
            while second and draw.textlength(second + "…", font=bf) > cw - 62 - 78:
                second = second[:-1]
            bl[1] = second + "…" if second != bl[1] else second
        for ln in bl:
            draw.text((tx, hy), ln, font=bf, fill=(72, 68, 64))
            hy += 11
        tag_chip(draw, bx + cw - 74, by + ch - 18, b["tag"], TAG_FILL[b["tag"]])


# ------------------------------------------------------- map, list, footer

LAND = [
    # (cx, cy, rx, ry) ellipses in a 0..100 map grid: rough continents.
    (15, 32, 14, 13),   # North America
    (28, 64, 8, 10),    # South America
    (48, 27, 8, 10),    # Europe
    (56, 56, 10, 12),   # Africa
    (72, 28, 17, 13),   # Asia
    (80, 52, 6, 5),     # South-East Asia
    (60, 40, 6, 5),     # Middle East
    (88, 74, 8, 6),     # Australia / Oceania
]


def draw_map(draw, y, h):
    draw.rectangle([MARGIN, y, PAGE_W - MARGIN, y + h], fill=PANEL,
                   outline=PANEL_EDGE, width=1)
    tf = font(SANS_B, 11)
    draw.text((MARGIN + 10, y + 5), "THE WORLD, PINNED — STORIES 1–12",
              font=tf, fill=INK)
    mx, my = MARGIN + 14, y + 24
    mw, mh = PAGE_W - 2 * MARGIN - 28, h - 32
    draw.rectangle([mx, my, mx + mw, my + mh], fill=(214, 230, 240))
    # dot-matrix continents: sample a fixed grid, keep dots inside ellipses
    step = 4
    for gy in range(0, 101, step):
        for gx in range(0, 101, step):
            inside = any(
                ((gx - cx) / rx) ** 2 + ((gy - cy) / ry) ** 2 <= 1
                for cx, cy, rx, ry in LAND
            )
            if inside:
                px = mx + gx / 100 * mw
                py = my + gy / 100 * mh
                draw.ellipse([px - 1.5, py - 1.5, px + 1.5, py + 1.5],
                             fill=(110, 140, 110))
    pf = font(SANS_B, 8)
    for gx, gy, label, (dx, dy), no in PINS:
        px = mx + gx / 100 * mw
        py = my + gy / 100 * mh
        lx, ly = px + dx, py + dy
        lw = draw.textlength(label, font=pf)
        lx = max(mx + 2, min(lx, mx + mw - lw - 2))
        ly = max(my + 1, min(ly, my + mh - 11))
        # leader line from the label to its pin when the label sits apart
        if abs(lx + lw / 2 - px) > 16 or abs(ly + 4 - py) > 12:
            draw.line([lx + lw / 2, ly + 4, px, py], fill=(120, 110, 100), width=1)
        draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RULE_RED,
                     outline=(255, 255, 255), width=1)
        ns = str(no)
        nf2 = font(SANS_B, 7)
        draw.text((px - draw.textlength(ns, font=nf2) / 2, py - 5),
                  ns, font=nf2, fill=(255, 255, 255))
        draw.text((lx, ly), label, font=pf, fill=INK)


def draw_list(draw, y, h):
    tf = font(SANS_B, 11)
    draw.text((MARGIN, y), "THE REST OF THE DAY — 13–44", font=tf, fill=INK)
    draw.line([MARGIN, y + 16, PAGE_W - MARGIN, y + 16], fill=PANEL_EDGE, width=1)
    col_w = (PAGE_W - 2 * MARGIN - 16) // 2
    row_h = (h - 22) / 16
    lf = font(SANS, 8)
    bf = font(SANS_B, 8)
    for idx, (no, text) in enumerate(REST):
        col, row = divmod(idx, 16)
        lx = MARGIN + col * (col_w + 16)
        ly = y + 20 + row * row_h
        draw.text((lx, ly), f"{no}.", font=bf, fill=RULE_RED)
        tw = col_w - 24
        line = text
        while line and draw.textlength(line, font=lf) > tw:
            line = line[:-1]
        draw.text((lx + 22, ly), line, font=lf, fill=(40, 38, 36))


def draw_footer(draw, y):
    draw.rectangle([MARGIN, y, PAGE_W - MARGIN, y + 50], fill=(238, 232, 220))
    tf = font(SANS_B, 10)
    draw.text((MARGIN + 10, y + 4), "DATE CHECK", font=tf, fill=RULE_RED)
    ff = font(SANS, 9)
    msg = ("Left out on purpose: the Kerch Bridge strikes (17 Nov) and the death "
           "of Fiona the hippo (19 Nov) are not 24 Nov news. The Serang fire began "
           "21 Nov; its confirmed toll and the search are today's news.")
    for i, ln in enumerate(fit_lines(draw, msg, ff, PAGE_W - 2 * MARGIN - 20, 2)):
        draw.text((MARGIN + 10, y + 17 + i * 11), ln, font=ff, fill=(52, 50, 48))
    lf = font(SANS, 8)
    legend = ("REPORTED = confirmed by officials or wires  ·  CLAIM = one side's "
              "account  ·  FORECAST = a plan or proposal  ·  Sources: Reuters, AP, "
              "AFP, UKMTO, ICJ, wire reports of 23–24 Nov 2026.")
    draw.text((MARGIN + 10, y + 40), legend, font=lf, fill=MUTED)


def build(path):
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    hero_y, hero_h = 104, 224
    hw = (PAGE_W - 2 * MARGIN - 2 * 10) // 3
    for i, hero in enumerate(HEROES):
        draw_hero(draw, hero, MARGIN + i * (hw + 10), hero_y, hw, hero_h)
    draw_timeline(draw, 336)
    draw_numbers(draw, 410)
    draw_briefs(draw, 458)
    draw_map(draw, 652, 132)
    draw_list(draw, 792, 170)
    draw_footer(draw, 970)
    img.save(path, format="PNG", optimize=True)


if __name__ == "__main__":
    import sys
    build(sys.argv[1] if len(sys.argv) > 1 else "entry.png")
