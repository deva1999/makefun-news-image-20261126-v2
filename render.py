#!/usr/bin/env python3
"""THE WORLD TODAY — Thursday 26 November 2026 in one image (V2).

A broadsheet front page drawn with PIL: one lead story given real
hierarchy, a dotted world map with numbered markers, a UTC timeline,
and 35 further stories in a four-column grid — 36 stories in all,
every one verified against the day's reporting (see SOURCES.md).

The V1 poster carried 50 stories and lost dev duels on density and
lead hierarchy; this revision answers that grade: fewer stories,
bigger lead, cleaner columns.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 2000, 1960
PAPER = (247, 243, 234)
INK = (26, 26, 40)
MUTED = (96, 96, 110)
ACCENT = (179, 57, 46)
RULE = (26, 26, 40)
LIGHT_RULE = (198, 190, 172)
MAP_DOT = (120, 128, 140)
MAP_MARKER = (179, 57, 46)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"

# (dateline, headline, one-line dek) — story 1 is the lead.
LEAD = (
    "WASHINGTON",
    "US proposes broad new tariffs on 14 partners",
    "Duties of up to 20% draw immediate pushback from China, the European "
    "Union and Brazil, and set up a fresh round of trade friction heading "
    "into the holidays.",
)

STORIES = [
    ("NEW YORK", "Holiday storm knocks out power for nearly 900,000",
     "2,000+ flights delayed; the Macy's parade moves to Saturday."),
    ("JIZAN", "Houthi projectile strikes Saudi Arabia's Jizan Port",
     "Coalition forces intercept a drone near Jeddah and missiles over Riyadh."),
    ("GAZA", "Israeli strikes kill eight in Gaza despite ceasefire",
     "Overnight attacks land while the truce is meant to hold."),
    ("KUWAIT CITY", "Two Italian technicians killed in attack in Kuwait",
     "The strike is blamed on Iranian drones, widening the Gulf war."),
    ("DUBAI", "Projectile explodes by a tanker west of Dubai",
     "The Kun Peng's engine room is hit; one crew member seriously wounded."),
    ("KYIV", "Russia fires missiles and 113 drones at Ukrainian cities",
     "At least three killed; Zelenskyy warns of a major energy attack."),
    ("BRUSSELS", "Europe weighs €45 billion more for Ukraine",
     "Leaders confront hard choices on financing Kyiv through 2027."),
    ("STOCKHOLM", "Five European nations buy 430 CV90 combat vehicles",
     "The joint order deepens the continent's rearmament."),
    ("PYONGYANG", "Kim tours nuclear plants, vows more arms",
     "North Korea's leader inspects the programme and promises expansion."),
    ("WASHINGTON", "Trump disputes GDP revised up to 4.3%",
     "The president pushes back on the third-quarter figure."),
    ("MIAMI", "FedEx jet overrun stops Miami airport",
     "The FAA issues a ground stop after the cargo plane leaves the runway."),
    ("WASHINGTON", "FCC clears SpaceX plan for a million satellites",
     "The authorisation would dwarf today's orbital fleets."),
    ("SEOUL", "Bank of Korea raises rates to 3.25%",
     "The central bank tightens, balancing growth against prices."),
    ("FRANKFURT", "Spain's Hernández de Cos picked to lead the ECB",
     "The Bank of Spain governor is chosen as the next chief."),
    ("NEW DELHI", "France honours the victims of 26/11 in Delhi",
     "Tributes on the 18th anniversary of the Mumbai attacks."),
    ("CAIRO", "Giza fire death toll rises to 31",
     "Egypt's health minister visits the injured as the count climbs."),
    ("GENEVA", "Gukesh and Sindarov draw a 60-move Game 3",
     "The world championship match stays level at 1.5–1.5."),
    ("BANGKOK", "Refinery blast injures nine in Bangkok",
     "Crews bring the plant fire under control after the explosion."),
    ("NAYPYIDAW", "Myanmar rejects parts of ICJ genocide ruling",
     "The junta challenges the court's findings on the Rohingya."),
    ("BISSAU", "Guinea-Bissau's rulers delay elections to 2028",
     "The military government pushes the vote back by years."),
    ("KINSHASA", "Ebola emergency widens in Central Africa",
     "More than 12,000 cases confirmed in the DR Congo outbreak."),
    ("PORT-AU-PRINCE", "Emergency support reaches Haiti's health system",
     "Aid arrives as hospitals run short of staff, fuel and medicine."),
    ("BOGOR", "Rescuers search a flooded Indonesian gold mine",
     "Nine dead and 17 believed trapped after the mine flooded."),
    ("JIUQUAN", "China launches Pakistan's first space traveller",
     "Shenzhou-24 flies as Beijing urges peaceful use of space."),
    ("DARMSTADT", "ESA images the crater left by NASA's DART impact",
     "The stadium-size scar marks where humanity first moved an asteroid."),
    ("CHICAGO", "Bears edge Lions 39–35 in NFL thriller",
     "The Eagles also rally past the Cowboys 39–38."),
    ("LONDON", "Duran Duran's Andy Taylor dies at 65",
     "The band's original guitarist defined a pop era."),
    ("TEHRAN", "Iran sets seven conditions for engaging the US",
     "Ghalibaf warns of a broader war if talks are forced."),
    ("BAGHDAD", "Iraq sentences eight French nationals to life",
     "The court convicts them of Islamic State affiliation."),
    ("ISLAMABAD", "Pakistan, Saudi Arabia and Türkiye to discuss defence pact",
     "The three meet on putting their joint pact into operation."),
    ("DHAKA", "Report underlines 'assault on journalism' in Bangladesh",
     "It counts 84 journalist arrests and 19 deaths."),
    ("ROME", "Italy to recruit 500,000 foreign workers",
     "The 2026–2028 plan opens legal routes for labour shortages."),
    ("STRASBOURG", "European Parliament approves the 2027 EU budget",
     "The president signs the budget into law."),
    ("MADRID", "Record migrant arrivals press Spain's Canary Islands",
     "The surge strains reception centres on the islands."),
    ("BRUSSELS", "Von der Leyen: Russia took 50,000 casualties in October",
     "She says Moscow's campaign is stagnant despite the losses."),
]

TIMELINE = [
    ("05:41", "Houthi projectile strikes Jizan Port"),
    ("07:11", "Egypt confirms Giza fire toll at 31"),
    ("07:41", "France honours 26/11 victims in Delhi"),
    ("14:00", "Gukesh–Sindarov Game 3 opens in Geneva"),
    ("19:59", "Game 3 ends in a 60-move draw"),
]

# Coarse land rectangles (lon0, latTop, lon1, latBottom) for the
# dotted map — shaped in pieces so the continents read at a glance.
LAND = [
    # North America and Greenland
    (-165, 68, -140, 60), (-140, 66, -95, 50), (-95, 64, -75, 49),
    (-125, 49, -100, 32), (-100, 49, -80, 30), (-80, 47, -66, 25),
    (-82, 28, -75, 20), (-118, 32, -86, 15), (-90, 21, -79, 9),
    (-58, 76, -20, 64),
    # South America
    (-77, 7, -60, -5), (-70, -5, -50, -18), (-65, -18, -40, -30),
    (-70, -30, -62, -52),
    # Europe
    (-9, 43, 10, 36), (-5, 50, 20, 44), (10, 54, 30, 46),
    (5, 62, 30, 55), (-2, 58, -5, 50), (20, 66, 45, 60),
    # Africa and Madagascar
    (-17, 32, 10, 15), (10, 32, 35, 22), (-10, 15, 20, 5),
    (20, 15, 52, 8), (-15, 5, 12, -18), (12, 5, 28, -28),
    (28, -18, 36, -34), (43, 12, 51, 4), (43, -12, 50, -25),
    # Arabia and Asia
    (35, 42, 48, 29), (48, 29, 60, 24), (52, 26, 59, 12),
    (45, 68, 180, 50), (60, 50, 110, 42), (110, 50, 140, 42),
    (75, 42, 97, 35), (97, 42, 122, 30), (105, 30, 122, 22),
    (68, 35, 78, 24), (78, 24, 89, 8),
    (92, 28, 100, 15), (100, 15, 105, 6),
    (130, 45, 142, 34), (127, 40, 130, 34),
    # Indonesia, Papua, Australia, New Zealand
    (95, 5, 105, -5), (105, -6, 114, -8), (114, -8, 120, -10),
    (119, -2, 125, -9), (131, -3, 141, -8),
    (113, -22, 130, -12), (130, -12, 146, -28), (146, -28, 154, -37),
    (166, -34, 174, -41), (172, -41, 178, -47),
]

# (story number, lon, lat) — Geneva (18) is left off: it sits on top
# of Rome (33) at this scale, and the chess is in the timeline anyway.
MARKERS = [
    (1, -84, 36), (2, -74, 41), (3, 43, 17), (7, 31, 50),
    (14, 127, 38), (16, 77, 28), (17, 31, 30), (22, 15, -4),
    (24, 107, -7), (25, 98, 40), (29, 51, 36), (33, 13, 42),
]


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, max_w, leading):
    x, y = xy
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_map(draw, box):
    x0, y0, x1, y1 = box
    mw, mh = x1 - x0, y1 - y0

    def project(lon, lat):
        return (x0 + (lon + 180) / 360 * mw, y0 + (90 - lat) / 180 * mh)

    lon = -177
    while lon <= 177:
        lat = -57
        while lat <= 81:
            inside = any(a <= lon <= c and d <= lat <= b for a, b, c, d in LAND)
            if inside:
                px, py = project(lon, lat)
                r = 2.1
                draw.ellipse([px - r, py - r, px + r, py + r], fill=MAP_DOT)
            lat += 3
        lon += 3
    f_num = font(SANS_B, 17)
    for num, mlon, mlat in MARKERS:
        px, py = project(mlon, mlat)
        r = 11
        draw.ellipse([px - r, py - r, px + r, py + r], fill=MAP_MARKER)
        label = str(num)
        tw = draw.textlength(label, font=f_num)
        draw.text((px - tw / 2, py - 9), label, font=f_num, fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    margin = 56

    # Masthead.
    draw.line([margin, 34, W - margin, 34], fill=RULE, width=5)
    draw.line([margin, 46, W - margin, 46], fill=RULE, width=2)
    f_title = font(SERIF_B, 96)
    title = "THE WORLD TODAY"
    tw = draw.textlength(title, font=f_title)
    draw.text(((W - tw) / 2, 58), title, font=f_title, fill=INK)
    f_date = font(SANS_B, 24)
    date_line = ("Thursday, 26 November 2026  ·  One day · One image · "
                 "36 stories · All times UTC")
    dw = draw.textlength(date_line, font=f_date)
    draw.text(((W - dw) / 2, 168), date_line, font=f_date, fill=MUTED)
    draw.line([margin, 208, W - margin, 208], fill=RULE, width=3)

    # Lead story, left; map, right.
    lead_x, lead_w = margin, 1110
    draw.text((lead_x, 228), "THE LEAD — " + LEAD[0], font=font(SANS_B, 22),
              fill=ACCENT)
    y = text_block(draw, (lead_x, 262), LEAD[1], font(SERIF_B, 57), INK,
                   lead_w, 68)
    y = text_block(draw, (lead_x, y + 10), LEAD[2], font(SERIF, 26), INK,
                   lead_w, 36)
    chips = ["UP TO 20%", "14 PARTNERS", "PUSHBACK: CHINA · EU · BRAZIL"]
    cx = lead_x
    f_chip = font(SANS_B, 20)
    for chip in chips:
        cw = draw.textlength(chip, font=f_chip) + 28
        draw.rectangle([cx, 540, cx + cw, 578], outline=ACCENT, width=2)
        draw.text((cx + 14, 549), chip, font=f_chip, fill=ACCENT)
        cx += cw + 16
    draw_map(draw, (1210, 228, W - margin, 540))
    draw.text((1210, 548), "Where the day happened — numbered stories on the map",
              font=font(SANS, 17), fill=MUTED)

    # Timeline strip.
    tl_y = 606
    draw.line([margin, tl_y, W - margin, tl_y], fill=LIGHT_RULE, width=2)
    draw.text((margin, tl_y + 10), "THE DAY IN UTC", font=font(SANS_B, 19),
              fill=ACCENT)
    col_w = (W - 2 * margin) / 5
    f_time, f_ev = font(SANS_B, 22), font(SANS, 18)
    for i, (time, event) in enumerate(TIMELINE):
        ex = margin + i * col_w
        draw.text((ex, tl_y + 38), time, font=f_time, fill=INK)
        text_block(draw, (ex, tl_y + 68), event, f_ev, MUTED, col_w - 18, 23)
    draw.line([margin, tl_y + 122, W - margin, tl_y + 122], fill=LIGHT_RULE,
              width=2)

    # Story grid: four columns, 9 / 9 / 9 / 8.
    grid_y = tl_y + 142
    columns = [STORIES[0:9], STORIES[9:18], STORIES[18:27], STORIES[27:35]]
    gap = 28
    colw = (W - 2 * margin - 3 * gap) / 4
    f_date2, f_head, f_dek = font(SANS_B, 16), font(SERIF_B, 21), font(SANS, 16)
    for ci, col in enumerate(columns):
        x = margin + ci * (colw + gap)
        if ci:
            draw.line([x - gap / 2, grid_y, x - gap / 2, 1840],
                      fill=LIGHT_RULE, width=1)
        y = grid_y
        for si, (dateline, headline, dek) in enumerate(col):
            num = ci * 9 + si + 2
            draw.text((x, y), f"{num}. {dateline}", font=f_date2, fill=ACCENT)
            y = text_block(draw, (x, y + 22), headline, f_head, INK, colw, 24)
            y = text_block(draw, (x, y + 2), dek, f_dek, MUTED, colw, 19)
            y += 12

    # Footer.
    draw.line([margin, 1876, W - margin, 1876], fill=RULE, width=2)
    draw.text((margin, 1890),
              "Every story verified against reporting dated 26 November 2026 — "
              "full citations in SOURCES.md.",
              font=font(SANS, 17), fill=MUTED)
    draw.text((W - margin - 210, 1890), "Page 1 of 1 · The World",
              font=font(SANS, 17), fill=MUTED)

    # The competition gate accepts at most 1024x1024 pixels, so the
    # full-size render is downscaled (keeping the exact 2000:1960
    # proportions) before it is saved as the deliverable.
    final = img.resize((1024, 1004), Image.LANCZOS)
    final.save("entry.png")
    print("wrote entry.png", final.size, "downscaled from", img.size)


if __name__ == "__main__":
    main()
