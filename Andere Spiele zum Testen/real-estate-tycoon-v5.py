"""
╔══════════════════════════════════════════════════════════════╗
║    BUSINESS TYCOON PRO V5 — Überarbeitete Version            ║
║    Linke Navigationsleiste | Neu balanciert | Neues Erfolge  ║
║    Marktsystem | Verkaufslogik | Zufallsereignisse           ║
║                                                              ║
║    Original: Michael (其米）  |  Überarbeitet: v5            ║
║    pip install pygame  →  python real-estate-tycoon-v5.py    ║
╚══════════════════════════════════════════════════════════════╝
"""

import pygame, random, sys, math, json
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum

# ═══════════════════════════════════════════════════════════
#  FARBEN
# ═══════════════════════════════════════════════════════════
BG          = (10,  14,  26)
PANEL       = (17,  24,  39)
PANEL2      = (31,  41,  55)
PANEL3      = (41,  51,  65)
BORDER      = (55,  65,  81)
ACCENT      = (59, 130, 246)
GREEN       = (16, 185, 129)
GREEN_DARK  = (6,  140, 90)
RED         = (239, 68,  68)
RED_DARK    = (180, 40, 40)
YELLOW      = (245, 158, 11)
CYAN        = (6,  182, 212)
GOLD        = (251, 191, 36)
WHITE       = (240, 240, 248)
MUTED       = (107, 114, 128)
ORANGE      = (249, 115, 22)
PURPLE      = (139, 92, 246)
TEAL        = (20,  184, 166)
PINK        = (236, 72,  153)
INDIGO      = (99,  102, 241)

pygame.init()
W, H = 1280, 760
screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
pygame.display.set_caption("Business Tycoon Pro V5 — by Michael (其米）")
clock = pygame.time.Clock()

# ═══════════════════════════════════════════════════════════
#  SCHWIERIGKEITSGRADE (angehobene Startkapital, aber geringeres Einkommen)
# ═══════════════════════════════════════════════════════════
DIFFICULTY = {
    "easy": {
        "label": "Einfach",
        "desc": "100.000 € Startkapital, leichte Wirtschaft",
        "start_cash": 100_000.0,
        "start_loan": 0.0,
        "income_mult": 1.15,
        "expense_mult": 0.90,
        "buy_chance_base": 0.45,
    },
    "medium": {
        "label": "Medium",
        "desc": "30.000 € Startkapital, ausgeglichene Wirtschaft",
        "start_cash": 30_000.0,
        "start_loan": 0.0,
        "income_mult": 1.0,
        "expense_mult": 1.0,
        "buy_chance_base": 0.35,
    },
    "hard": {
        "label": "Schwer",
        "desc": "50.000 € Startkapital + 60.000 € Schulden",
        "start_cash": 50_000.0,
        "start_loan": 60_000.0,
        "income_mult": 0.80,
        "expense_mult": 1.15,
        "buy_chance_base": 0.25,
    },
}

# ═══════════════════════════════════════════════════════════
#  SCHRIFTEN
# ═══════════════════════════════════════════════════════════
def _f(size, bold=False):
    for name in ["segoeui", "arial", "freesansbold" if bold else "freesans", "sans"]:
        try:
            return pygame.font.SysFont(name, size, bold=bold)
        except:
            pass
    return pygame.font.Font(None, size)

F = {
    "xs":   _f(11),
    "sm":   _f(13),
    "md":   _f(15),
    "lg":   _f(17, True),
    "xl":   _f(22, True),
    "title": _f(28, True),
}

# ═══════════════════════════════════════════════════════════
#  HILFSFUNKTIONEN
# ═══════════════════════════════════════════════════════════
def fmt(n: float) -> str:
    """Formatiere Zahlen in lesbare Währungsangaben."""
    n = float(n)
    if abs(n) >= 1e9:  return f"{n/1e9:.2f} Mrd €"
    if abs(n) >= 1e6:  return f"{n/1e6:.2f} Mio €"
    if abs(n) >= 1e3:  return f"{n/1e3:.1f}k €"
    return f"{n:,.0f} €".replace(",", ".")

def txt(surf, text, fkey, color, x, y, anchor="topleft", maxw=0):
    """Text auf Surface rendern."""
    f = F[fkey]
    s = str(text)
    if maxw > 0:
        while f.size(s)[0] > maxw and len(s) > 1:
            s = s[:-1]
        if s != str(text):
            s += "…"
    surf_t = f.render(s, True, color)
    r = surf_t.get_rect(**{anchor: (x, y)})
    surf.blit(surf_t, r)
    return r

def box(surf, color, rect, r=6, width=0):
    """Gerundetes Rechteck zeichnen."""
    pygame.draw.rect(surf, color, rect, width, border_radius=r)

def line(surf, color, p1, p2):
    """Linie zeichnen."""
    pygame.draw.line(surf, color, p1, p2)

def sparkline(surf, hist, x, y, w, h, col=None):
    """Sparkline (Mini-Liniendiagramm) zeichnen."""
    if len(hist) < 2:
        return
    mn, mx2 = min(hist), max(hist)
    if mx2 == mn:
        mx2 = mn + 0.001
    pts = [(x + int(i / (len(hist) - 1) * w),
            y + h - int((v - mn) / (mx2 - mn) * h))
           for i, v in enumerate(hist)]
    c = col or (GREEN if hist[-1] >= hist[0] else RED)
    if len(pts) >= 2:
        pygame.draw.lines(surf, c, False, pts, 2)

def progress_bar(surf, x, y, w, h, frac, color):
    """Fortschrittsbalken zeichnen."""
    box(surf, PANEL2, (x, y, w, h), 3)
    fw = max(0, min(w, int(w * frac)))
    if fw > 0:
        box(surf, color, (x, y, fw, h), 3)

def dim_overlay(surf):
    """Dunkle Überlagerung für Modals."""
    s = pygame.Surface((surf.get_width(), surf.get_height()), pygame.SRCALPHA)
    s.fill((0, 0, 0, 170))
    surf.blit(s, (0, 0))

# ═══════════════════════════════════════════════════════════
#  INPUT-BOX
# ═══════════════════════════════════════════════════════════
class InputBox:
    """Eingabefeld für Texte und Zahlen."""
    def __init__(self, x, y, w, h=34, hint="", numeric=True):
        self.rect = pygame.Rect(x, y, w, h)
        self.hint = hint
        self.text = ""
        self.active = False
        self.numeric = numeric

    def handle(self, ev):
        if ev.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(ev.pos)
        if ev.type == pygame.KEYDOWN and self.active:
            if ev.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif ev.unicode.isprintable():
                ch = ev.unicode
                if self.numeric:
                    if ch.isdigit() or (ch == '.' and '.' not in self.text):
                        self.text += ch
                else:
                    self.text += ch

    def val(self):
        try:
            return float(self.text)
        except:
            return 0.0

    def draw(self, surf):
        col = ACCENT if self.active else BORDER
        box(surf, PANEL2, self.rect, 5)
        box(surf, col, self.rect, 5, 1)
        show = self.text if self.text else self.hint
        color = WHITE if self.text else MUTED
        txt(surf, show, "sm", color, self.rect.x + 8, self.rect.centery, "midleft")

    def clear(self):
        self.text = ""

# ═══════════════════════════════════════════════════════════
#  BUTTON
# ═══════════════════════════════════════════════════════════
class Btn:
    """Klickbarer Button."""
    def __init__(self, x, y, w, h, label, color=None, tc=WHITE, fkey="sm"):
        self.rect = pygame.Rect(x, y, w, h)
        self.label = label
        self.color = color or ACCENT
        self.tc = tc
        self.fkey = fkey
        self.hover = False

    def draw(self, surf):
        c = tuple(min(255, v + 25) for v in self.color) if self.hover else self.color
        box(surf, c, self.rect, 6)
        txt(surf, self.label, self.fkey, self.tc,
            self.rect.centerx, self.rect.centery, "center")

    def update(self, pos):
        self.hover = self.rect.collidepoint(pos)

    def hit(self, ev):
        return (ev.type == pygame.MOUSEBUTTONDOWN
                and ev.button == 1
                and self.rect.collidepoint(ev.pos))

# ═══════════════════════════════════════════════════════════
#  KATALOGE (angepasste Preise für balanciertes Spiel)
# ═══════════════════════════════════════════════════════════
# Immobilien: (id, name, icon, price, rent, maint, lvl_max)
PROP_CATALOG = [
    ("studio",   "Studenten-Appartement", "Appart.",   25_000,    280,    50, 8),
    ("flat",     "Kleine Wohnung",        "Wohnung",   75_000,    480,    80, 8),
    ("duplex",   "Doppelhaushälfte",      "Doppel",   160_000,    900,   160, 8),
    ("house",    "Einfamilienhaus",       "Haus",     280_000,  1_200,   250, 8),
    ("town",     "Stadthaus",             "Stadt",    480_000,  2_100,   380, 8),
    ("condo",    "Luxus-Penthouse",       "Penthouse",750_000,  3_800,   580, 8),
    ("villa",    "Villa mit Pool",        "Villa",  2_200_000, 11_000, 1_700, 8),
    ("office",   "Bürogebäude",           "Büro",   3_800_000, 18_000, 2_600, 8),
    ("mall",     "Einkaufszentrum",       "Mall",   6_500_000, 35_000, 4_200, 8),
    ("hotel",    "Luxus-Hotel",           "Hotel",  9_500_000, 50_000, 6_800, 8),
    ("skyscr",   "Wolkenkratzer",         "Wolken", 25_000_000,120_000,17_000, 8),
    ("castle",   "Schloss-Anwesen",       "Schloss",55_000_000,240_000,38_000, 8),
    ("island",   "Privatinsel-Resort",    "Insel", 120_000_000,480_000,85_000, 8),
]

# Unternehmen: (id, name, icon, price, profit, maint, risk, lvl_max)
COMP_CATALOG = [
    ("foodtruck","Food-Truck",           "Truck",     10_000,    120,    30, 0.07, 8),
    ("cafe",     "Café / Kiosk",         "Café",      40_000,    320,    65, 0.06, 8),
    ("craft",    "Handwerksbetrieb",     "Handwerk",  150_000,  1_200,   240, 0.06, 8),
    ("retail",   "Einzelhandel",         "Handel",   380_000,  2_800,   550, 0.09, 8),
    ("logistik", "Logistikfirma",        "Logistik",  750_000,  5_500, 1_100, 0.08, 8),
    ("tech",     "Software-Startup",     "Software", 1_500_000,  8_500, 1_500, 0.14, 8),
    ("factory",  "Fabrik",               "Fabrik",  3_000_000, 22_000, 3_800, 0.07, 8),
    ("consult",  "Unternehmensberatung", "Beratung", 4_500_000, 28_000, 2_800, 0.10, 8),
    ("media",    "Medienkonzern",        "Medien",  6_500_000, 48_000, 8_500, 0.12, 8),
    ("biotech",  "Biotech-Unternehmen",  "BioTech",11_000_000, 82_000,13_000, 0.17, 8),
    ("pharma",   "Pharmaunternehmen",    "Pharma", 18_000_000,140_000,24_000, 0.15, 8),
    ("space",    "Raumfahrttechnik",     "Space",  30_000_000,260_000,42_000, 0.22, 8),
    ("ibank",    "Investmentbank",       "Bank",   50_000_000,480_000,72_000, 0.20, 8),
    ("megacorp", "Mega-Konzern",         "Mega",  100_000_000,850_000,125_000,0.25, 8),
]

# Autos: (id, name, icon, price, rental_income, maint, dep_rate, lvl_max)
CAR_CATALOG = [
    ("beetle",   "VW Käfer (Oldtimer)",  "Käfer",     10_000,    100,    35, 0.003, 8),
    ("golf",     "VW Golf VIII",         "Golf",      32_000,    300,    60, 0.006, 8),
    ("model3",   "Tesla Model 3",        "Tesla",     50_000,    480,    50, 0.005, 8),
    ("bmw3",     "BMW 3er",             "BMW",       55_000,    450,    75, 0.006, 8),
    ("mercedes", "Mercedes C-Klasse",   "MB",        60_000,    500,    80, 0.006, 8),
    ("porsche",  "Porsche 911",          "Porsche",  140_000,  1_100,   130, 0.004, 8),
    ("lambo",    "Lamborghini Huracán",  "Lambo",    280_000,  2_600,   220, 0.004, 8),
    ("ferrari",  "Ferrari 488",          "Ferrari",  320_000,  2_800,   240, 0.004, 8),
    ("sprinter", "Mercedes Sprinter",    "Sprinter",   48_000,    550,   100, 0.007, 8),
    ("bus",      "Reisebus",             "Bus",      200_000,  2_000,   380, 0.005, 8),
    ("teslasemi","Tesla Semi LKW",       "Semi",     170_000,  1_600,   300, 0.005, 8),
    ("rolls",    "Rolls-Royce Phantom",  "Rolls",    520_000,  4_800,   380, 0.003, 8),
]

# Autovermietungen: (id, name, icon, price, base_profit, maint, risk, lvl_max)
CAR_RENTAL_CATALOG = [
    ("budget","Budget Carsharing",      "Sharing",     30_000,    350,    65, 0.05, 8),
    ("taxi",  "City-Taxi Flotte",       "Taxi",        75_000,    800,   130, 0.06, 8),
    ("premium","Premium-Autovermietung","Premium",    180_000,  2_000,   270, 0.07, 8),
    ("luxury","Luxus-Fahrzeugvermietung","Luxus",     420_000,  5_000,   550, 0.08, 8),
    ("evfleet","E-Auto Flotte",         "E-Flotte",   250_000,  2_800,   200, 0.06, 8),
    ("vanrent","Transporter-Vermietung","Transporter", 120_000,  1_400,   200, 0.07, 8),
    ("classic","Oldtimer-Vermietung",   "Oldtimer",   300_000,  3_800,   320, 0.05, 8),
    ("ride",  "Ride-Sharing Plattform",  "Ride",      600_000,  7_500,   650, 0.09, 8),
    ("fleet", "Flottenmanagement",       "Flotte",   900_000, 11_000,   950, 0.08, 8),
    ("hub",   "Mobility-Hub Zentrale",   "Hub",     2_000_000,20_000, 1_600, 0.10, 8),
]

# Aktien: (sid, name, price, vol, div_pa, sector)
STOCK_CATALOG = [
    ("food",  "FoodChain",     42.0, 0.05, 0.030, "Konsum"),
    ("rc",    "RetailCorp",    60.0, 0.06, 0.022, "Konsum"),
    ("ene",   "EnergyCo",     110.0, 0.06, 0.020, "Energie"),
    ("bg",    "BankGroup",     70.0, 0.10, 0.012, "Finanzen"),
    ("inno",  "InnovateTech", 135.0, 0.11, 0.003, "Tech"),
    ("tg",    "TechGiant",    200.0, 0.12, 0.004, "Tech"),
    ("ac",    "AutoCorp",      92.0, 0.08, 0.015, "Auto"),
    ("ph",    "PharmaHealth", 240.0, 0.09, 0.006, "Gesundheit"),
    ("re",    "RealEstCorp",   98.0, 0.07, 0.025, "Immobilien"),
    ("ai",    "AI-Ventures",  420.0, 0.22, 0.001, "Tech"),
    ("cryp",  "CryptoBank",   500.0, 0.32, 0.000, "Finanzen"),
    ("green", "GreenEnergy",  145.0, 0.09, 0.012, "Energie"),
    ("cyber", "CyberSec",     310.0, 0.16, 0.002, "Tech"),
    ("ev",    "E-Auto Corp",  175.0, 0.14, 0.005, "Auto"),
    ("def",   "DefenseTech",  330.0, 0.11, 0.008, "Tech"),
]

# ═══════════════════════════════════════════════════════════
#  WIRTSCHAFTSPHASEN
# ═══════════════════════════════════════════════════════════
PHASES = {
    "BOOM":           {"label": "Boom",          "col": GREEN,  "stk": +.04, "rent": +.02, "profit": +.05},
    "STABLE":         {"label": "Stabil",        "col": CYAN,   "stk":  .00, "rent":  .00, "profit":  .00},
    "RECESSION":      {"label": "Rezession",     "col": YELLOW, "stk": -.03, "rent": -.01, "profit": -.03},
    "DEPRESSION":     {"label": "Depression",    "col": RED,    "stk": -.08, "rent": -.03, "profit": -.08},
    "STAGFLATION":    {"label": "Stagflation",   "col": ORANGE, "stk": -.02, "rent": +.01, "profit": -.04},
    "HYPERINFLATION": {"label": "Hyperinflation","col": PINK,   "stk": +.01, "rent": +.06, "profit": -.06},
}

# ═══════════════════════════════════════════════════════════
#  MIETER- UND KUNDENTYPEN
# ═══════════════════════════════════════════════════════════
TENANT_TYPES = [
    ("Privat-Mieter",  0.00, 0.03, 12),
    ("Student",       -0.10, 0.10,  6),
    ("Firmenkunde",   +0.25, 0.05, 24),
    ("Luxusmieter",   +0.40, 0.04, 18),
    ("Sozialmieter",  -0.20, 0.01, 36),
]

CAR_RENTAL_CUSTOMERS = [
    ("Tourist",       0.00, 0.03, 3),
    ("Student",      -0.15, 0.08, 2),
    ("Firmenkunde",  +0.20, 0.04, 6),
    ("Luxus-Kunde",  +0.35, 0.02, 4),
]

# ═══════════════════════════════════════════════════════════
#  MARKT-SYSTEM — Verkaufslogik
# ═══════════════════════════════════════════════════════════
def calc_market_value(purchase_price, months_held, phase, demand, condition):
    """
    Berechne den aktuellen Marktwert eines Objekts.
    - purchase_price: ursprünglicher Kaufpreis
    - months_held: Monate im Besitz
    - phase: aktuelle Wirtschaftsphase
    - demand: lokale Nachfrage (0.0 - 2.0)
    - condition: Zustand (0.0 - 1.0)
    """
    phase_factor = {
        "BOOM": 1.12, "STABLE": 1.0, "RECESSION": 0.88,
        "DEPRESSION": 0.75, "STAGFLATION": 0.85, "HYPERINFLATION": 1.05
    }.get(phase, 1.0)
    # Wertsteigerung über Zeit (max ~5% p.a.)
    time_factor = 1.0 + (months_held / 12.0) * 0.02
    # Zustand reduziert Wert
    condition_factor = 0.7 + condition * 0.3
    # Nachfrage beeinflusst Preis
    demand_factor = 0.8 + demand * 0.4
    return purchase_price * phase_factor * time_factor * condition_factor * demand_factor

def calc_buy_chance(sale_price, market_value, gs):
    """
    Berechne die Wahrscheinlichkeit, dass ein Objekt verkauft wird.
    Realistisches System: Preise nahe Marktwert haben gute Chancen,
    überhöhte Preise sinken dramatisch.
    """
    if sale_price <= 0 or market_value <= 0:
        return 0.0, "invalid"
    ratio = sale_price / market_value
    base = DIFFICULTY[gs.difficulty]["buy_chance_base"]

    # Preis-Leistungs-Faktor
    if ratio <= 0.7:
        price_factor = 2.8  # Unter Wert → hohe Nachfrage
    elif ratio <= 0.9:
        price_factor = 2.0 + (0.9 - ratio) * 4.0  # Noch attraktiv
    elif ratio <= 1.0:
        price_factor = 1.5 - (ratio - 0.9) * 5.0  # Fair → normal
    elif ratio <= 1.15:
        price_factor = 1.0 - (ratio - 1.0) * 5.0  # Leicht überteuert
    elif ratio <= 1.35:
        price_factor = 0.25 - (ratio - 1.15) * 1.0  # Teuer
    elif ratio <= 1.6:
        price_factor = 0.05 - (ratio - 1.35) * 0.15  # Stark überteuert
    else:
        price_factor = 0.01  # Extrem überteuert → fast keine Chance

    # Wirtschaftsphasen-Modifikator
    phase_mod = {
        "BOOM": 1.8, "STABLE": 1.2, "RECESSION": 0.6,
        "DEPRESSION": 0.3, "STAGFLATION": 0.5, "HYPERINFLATION": 0.4
    }.get(gs.phase, 1.0)

    # Marktstimmungs-Modifikator
    sentiment_mod = (gs.sentiment - 50) / 100.0
    sentiment_factor = 1.0 + sentiment_mod * 0.6

    # Zufällige Schwankung
    random_factor = 0.85 + random.random() * 0.3

    chance = base * price_factor * phase_mod * sentiment_factor * random_factor
    chance = max(0.0, min(1.0, chance))

    if chance >= 0.75:
        msg_key = "hot"
    elif chance >= 0.4:
        msg_key = "normal"
    elif chance >= 0.08:
        msg_key = "cold"
    else:
        msg_key = "dead"

    return chance, msg_key

def get_price_message(msg_key):
    messages = {
        "hot":    "Heiß begehrt! Käufer stehen Schlange.",
        "normal": "Angemessener Preis – moderate Nachfrage.",
        "cold":   "Zu teuer! Kaum Interesse am Markt.",
        "dead":   "Völlig überteuert! Kein Käufer in Sicht.",
        "invalid":"Ungültiger Preis.",
        "sold":   "Verkauft! Käufer gefunden.",
    }
    return messages.get(msg_key, "")

# ═══════════════════════════════════════════════════════════
#  ACHIEVEMENT-SYSTEM (Mehrstufig)
# ═══════════════════════════════════════════════════════════

# Immobilien-Achievements
ACHIEV_IMMO = {
    1:  {"title": "Erste Immobilie", "desc": "1 Gebäude besitzen",               "check": lambda g: len(g.props) >= 1},
    2:  {"title": "Kleiner Vermieter", "desc": "5 Gebäude besitzen",             "check": lambda g: len(g.props) >= 5},
    3:  {"title": "Immobilienbesitzer", "desc": "20 Gebäude besitzen",           "check": lambda g: len(g.props) >= 20},
    4:  {"title": "Großgrundbesitzer", "desc": "100 Gebäude besitzen",           "check": lambda g: len(g.props) >= 100},
    5:  {"title": "Immobilien-Magnat", "desc": "500 Gebäude besitzen",           "check": lambda g: len(g.props) >= 500},
}

# Auto-Achievements
ACHIEV_CARS = {
    1:  {"title": "Erstes Auto", "desc": "1 Auto besitzen",                       "check": lambda g: len(g.cars) >= 1},
    2:  {"title": "Autoliebhaber", "desc": "10 Autos besitzen",                  "check": lambda g: len(g.cars) >= 10},
    3:  {"title": "Autosammler", "desc": "50 Autos besitzen",                    "check": lambda g: len(g.cars) >= 50},
    4:  {"title": "Flottenbesitzer", "desc": "200 Autos besitzen",               "check": lambda g: len(g.cars) >= 200},
    5:  {"title": "Auto-König", "desc": "1000 Autos besitzen",                   "check": lambda g: len(g.cars) >= 1000},
}

# Filialen-Achievements
ACHIEV_FILIALEN = {
    1:  {"title": "Erste Filiale", "desc": "1 Autovermietung besitzen",            "check": lambda g: len(g.car_rentals) >= 1},
    2:  {"title": "Filial-Netz", "desc": "10 Autovermietungen besitzen",          "check": lambda g: len(g.car_rentals) >= 10},
    3:  {"title": "Regionalmarkt", "desc": "50 Autovermietungen besitzen",        "check": lambda g: len(g.car_rentals) >= 50},
    4:  {"title": "Landesweit", "desc": "200 Autovermietungen besitzen",          "check": lambda g: len(g.car_rentals) >= 200},
    5:  {"title": "Global Player", "desc": "1000 Autovermietungen besitzen",      "check": lambda g: len(g.car_rentals) >= 1000},
}

# Firmen-Achievements
ACHIEV_FIRMEN = {
    1:  {"title": "Erste Firma", "desc": "1 Unternehmen besitzen",                 "check": lambda g: len(g.comps) >= 1},
    2:  {"title": "Unternehmer", "desc": "5 Unternehmen besitzen",                "check": lambda g: len(g.comps) >= 5},
    3:  {"title": "Mittelständler", "desc": "20 Unternehmen besitzen",            "check": lambda g: len(g.comps) >= 20},
    4:  {"title": "Konzernchef", "desc": "100 Unternehmen besitzen",              "check": lambda g: len(g.comps) >= 100},
    5:  {"title": "Wirtschaftsimperium", "desc": "500 Unternehmen besitzen",      "check": lambda g: len(g.comps) >= 500},
}

# Vermögens-Achievements
ACHIEV_VERMOEGEN = {
    1:  {"title": "Bronze-Vermögen", "desc": "Nettovermögen > 100.000 €",          "check": lambda g: g.net_worth() >= 100_000},
    2:  {"title": "Silber-Vermögen", "desc": "Nettovermögen > 1 Mio €",            "check": lambda g: g.net_worth() >= 1_000_000},
    3:  {"title": "Gold-Vermögen", "desc": "Nettovermögen > 10 Mio €",             "check": lambda g: g.net_worth() >= 10_000_000},
    4:  {"title": "Platin-Vermögen", "desc": "Nettovermögen > 100 Mio €",          "check": lambda g: g.net_worth() >= 100_000_000},
    5:  {"title": "Diamant-Vermögen", "desc": "Nettovermögen > 1 Mrd €",           "check": lambda g: g.net_worth() >= 1_000_000_000},
    6:  {"title": "Legendäres Vermögen", "desc": "Nettovermögen > 10 Mrd €",       "check": lambda g: g.net_worth() >= 10_000_000_000},
}

# Spezial-Achievements (Erweiterte Kategorien)
ACHIEV_SPECIAL = [
    # Immobilienmogul
    ("mogul_1", "Immobilienmogul I",  "10 Immobilien auf Level 5+",        lambda g: sum(1 for p in g.props if p["level"] >= 5) >= 10),
    ("mogul_2", "Immobilienmogul II", "30 Immobilien auf Level 8",         lambda g: sum(1 for p in g.props if p["level"] >= 8) >= 30),
    ("mogul_3", "Immobilienmogul III","Alle Immobilien auf Max-Level",     lambda g: len(g.props) >= 5 and all(p["level"] >= p["lvl_max"] for p in g.props)),

    # Auto-Sammler
    ("auto_1",  "Auto-Sammler I",     "5 Autos auf Level 5+",             lambda g: sum(1 for c in g.cars if c["level"] >= 5) >= 5),
    ("auto_2",  "Auto-Sammler II",    "15 Autos auf Level 8",             lambda g: sum(1 for c in g.cars if c["level"] >= 8) >= 15),
    ("auto_3",  "Auto-Sammler III",   "Alle Autos auf Max-Level",         lambda g: len(g.cars) >= 5 and all(c["level"] >= c["lvl_max"] for c in g.cars)),

    # Unternehmer
    ("unter_1", "Unternehmer I",      "5 Firmen auf Level 5+",            lambda g: sum(1 for c in g.comps if c["level"] >= 5) >= 5),
    ("unter_2", "Unternehmer II",     "20 Firmen auf Level 8",            lambda g: sum(1 for c in g.comps if c["level"] >= 8) >= 20),
    ("unter_3", "Unternehmer III",    "Alle Firmen auf Max-Level",         lambda g: len(g.comps) >= 5 and all(c["level"] >= c["lvl_max"] for c in g.comps)),

    # Investor
    ("inv_1",   "Investor I",         "Aktienportfolio > 500.000 €",      lambda g: g.stock_value() >= 500_000),
    ("inv_2",   "Investor II",        "Aktienportfolio > 5 Mio €",        lambda g: g.stock_value() >= 5_000_000),
    ("inv_3",   "Investor III",       "Aktienportfolio > 50 Mio €",       lambda g: g.stock_value() >= 50_000_000),

    # Banker
    ("bank_1",  "Banker I",           "500.000 € auf dem Festgeldkonto",  lambda g: g.savings >= 500_000),
    ("bank_2",  "Banker II",          "5 Mio € auf dem Festgeldkonto",    lambda g: g.savings >= 5_000_000),
    ("bank_3",  "Banker III",         "Schuldenfrei (Kredit komplett getilgt)", lambda g: g.loan == 0 and g.net_worth() > 100_000),

    # Börsenprofi
    ("boerse_1","Börsenprofi I",      "5 verschiedene Aktien besitzen",    lambda g: sum(1 for qty in g.stocks.values() if qty > 0) >= 5),
    ("boerse_2","Börsenprofi II",     "ETF-Anteile > 100.000 €",          lambda g: g.etf * g.etf_price >= 100_000),
    ("boerse_3","Börsenprofi III",    "Aktien in allen Sektoren",         lambda g: len(set(g.stock_data[s]["sector"] for s,qty in g.stocks.items() if qty > 0)) >= 5),

    # Tycoon
    ("tyc_1",   "Tycoon I",           "Alle Kategorien besitzen",          lambda g: len(g.props) >= 1 and len(g.comps) >= 1 and len(g.cars) >= 1 and len(g.car_rentals) >= 1 and g.stock_value() > 0),
    ("tyc_2",   "Tycoon II",          "10 Immobilien + 10 Firmen + 10 Autos", lambda g: len(g.props) >= 10 and len(g.comps) >= 10 and len(g.cars) >= 10),
    ("tyc_3",   "Tycoon III",         "100 Immobilien + 50 Firmen + 50 Autos", lambda g: len(g.props) >= 100 and len(g.comps) >= 50 and len(g.cars) >= 50),

    # Langzeitspieler
    ("lang_1",  "Langzeitspieler I",  "5 Jahre Spielzeit",                lambda g: (g.year - 2024) >= 5),
    ("lang_2",  "Langzeitspieler II", "20 Jahre Spielzeit",               lambda g: (g.year - 2024) >= 20),
    ("lang_3",  "Langzeitspieler III","50 Jahre Spielzeit",               lambda g: (g.year - 2024) >= 50),
    ("lang_4",  "Langzeitspieler IV", "100 Jahre Spielzeit",              lambda g: (g.year - 2024) >= 100),

    # Rekordhalter
    ("rekord_1","Rekordhalter I",     "Monatlicher Cashflow > 50.000 €",  lambda g: g.net_monthly() >= 50_000),
    ("rekord_2","Rekordhalter II",    "Monatlicher Cashflow > 500.000 €", lambda g: g.net_monthly() >= 500_000),
    ("rekord_3","Rekordhalter III",   "Monatlicher Cashflow > 5 Mio €",   lambda g: g.net_monthly() >= 5_000_000),

    # Alleskönner
    ("all_1",   "Alleskönner",        "15 Immobilien + 15 Firmen + 15 Autos + 5 Mio Aktien", lambda g: len(g.props) >= 15 and len(g.comps) >= 15 and len(g.cars) >= 15 and g.stock_value() >= 5_000_000),

    # Hardcore
    ("hard_1",  "Hardcore-Überlebender","Schwerer Modus: 100 Mio NV",      lambda g: g.net_worth() >= 100_000_000 and g.difficulty == "hard"),

    # Perfektion
    ("perf_1",  "Perfektionist",      "Alle Erfolge freigeschaltet",       lambda g: True),  # Wird dynamisch geprüft
]

# ═══════════════════════════════════════════════════════════
#  SPIELZUSTAND (GameState)
# ═══════════════════════════════════════════════════════════
class GS:
    """Gesamter Spielzustand – zentrale Datenstruktur."""
    def __init__(self, difficulty="medium"):
        self.difficulty = difficulty
        diff = DIFFICULTY[difficulty]
        self.name = "Investor"
        self.cash = diff["start_cash"]
        self.loan = diff["start_loan"]
        self.savings = 0.0
        self.sav_rate = 0.0030  # Reduziert
        self.loan_rate = 0.006
        self.tax_rate = 0.28  # Höhere Steuern

        # Besitztümer
        self.props: List[dict] = []
        self.comps: List[dict] = []
        self.cars: List[dict] = []
        self.car_rentals: List[dict] = []
        self.stocks: Dict[str, float] = {}
        self.etf: float = 0.0
        self.stock_data = {
            sid: {"name": name, "price": price, "vol": vol,
                  "div": div, "sector": sector, "hist": [price]}
            for sid, name, price, vol, div, sector in STOCK_CATALOG
        }
        self.etf_price = 100.0
        self.etf_hist = [100.0]

        # Zeit
        self.month = 1
        self.year = 2024

        # Wirtschaft
        self.phase = "STABLE"
        self.phase_dur = 8
        self.base_rate = 5.0
        self.inflation = 0.002
        self.gdp = 2.0
        self.unemp = 5.0
        self.sentiment = 50.0

        # Markt-Nachfrage-Daten (lokal)
        self.local_demand = 1.0       # 0.0 - 2.0
        self.competition = 0.3        # 0.0 - 1.0
        self.market_trend = 0.0       # -0.1 - +0.1
        self.condition_base = 0.9     # Grundzustand neuer Objekte

        # Spieler
        self.reputation = 50

        # Achievements
        self.achiev_done = set()
        self.achiev_tiers = {}  # tier_id -> stufe erreicht

        # Logging
        self.log: List[tuple] = []
        self.news: List[str] = []
        self.nw_hist: List[float] = []
        self.cf_hist: List[float] = []
        self.market_messages: List[tuple] = []

        # Verkaufs-Tracking
        self.total_sales_value = 0.0
        self.total_purchase_value = 0.0

        # Überlebens-Tracking
        self._survived_dep_count = 0
        self._last_dep_phase = False

    def net_worth(self):
        """Berechne das Nettovermögen."""
        v = self.cash + self.savings
        for p in self.props:
            v += calc_market_value(
                p["price"], p.get("months_held", 0), self.phase,
                self.local_demand, p.get("condition", 0.9)
            )
        for c in self.comps:
            v += c["val"]
        for car in self.cars:
            v += car["price"]
        for cr in self.car_rentals:
            v += cr["val"]
        for sid, qty in self.stocks.items():
            v += qty * self.stock_data[sid]["price"]
        v += self.etf * self.etf_price
        v -= self.loan
        return v

    def stock_value(self):
        """Wert des Aktienportfolios."""
        v = sum(qty * self.stock_data[sid]["price"]
                for sid, qty in self.stocks.items() if qty > 0)
        return v + self.etf * self.etf_price

    def monthly_income(self):
        """Monatliche Brutto-Einnahmen."""
        diff = DIFFICULTY[self.difficulty]
        # Mieteinnahmen (beeinflusst von lokaler Nachfrage)
        i = sum(p["rent"] * (0.8 + self.local_demand * 0.3)
                for p in self.props if not p.get("vacant", True))
        i += sum(c["profit"] for c in self.comps)
        i += sum(car["rental"] for car in self.cars if car.get("rented"))
        i += sum(cr["profit"] for cr in self.car_rentals)
        # Dividenden
        i += sum(qty * self.stock_data[sid]["price"] * self.stock_data[sid]["div"] / 12
                 for sid, qty in self.stocks.items() if qty > 0)
        i += self.etf * self.etf_price * 0.002 / 12
        # Zinsen auf Festgeld
        i += self.savings * self.sav_rate
        return i * diff["income_mult"]

    def monthly_expenses(self):
        """Monatliche Brutto-Ausgaben."""
        diff = DIFFICULTY[self.difficulty]
        e = sum(p["maint"] for p in self.props)
        e += sum(c["maint"] for c in self.comps)
        e += sum(car["maint"] for car in self.cars)
        e += sum(cr["maint"] for cr in self.car_rentals)
        e += self.loan * (self.loan_rate + self.base_rate / 100 / 12)
        # Wettbewerbsfaktor: mehr Konkurrenz = höhere Kosten
        e *= 1.0 + self.competition * 0.15
        return e * diff["expense_mult"]

    def net_monthly(self):
        """Netto monatlicher Cashflow (nach Steuern)."""
        gross = self.monthly_income() - self.monthly_expenses()
        tax = max(0.0, gross * self.tax_rate)
        return gross - tax

    def add_log(self, msg, kind="info"):
        self.log.insert(0, (msg, kind))
        if len(self.log) > 100:
            self.log.pop()

    def add_news(self, msg):
        self.news.insert(0, msg)
        if len(self.news) > 25:
            self.news.pop()

    def add_market_msg(self, msg):
        self.market_messages.append((msg, pygame.time.get_ticks()))
        if len(self.market_messages) > 10:
            self.market_messages.pop(0)

    def name_of(self, item):
        return item.get("custom_name", item.get("name", "Unbekannt"))

    def get_total_achievements(self):
        """Gesamtanzahl möglicher Erfolge."""
        return (len(ACHIEV_IMMO) + len(ACHIEV_CARS) + len(ACHIEV_FILIALEN) +
                len(ACHIEV_FIRMEN) + len(ACHIEV_VERMOEGEN) + len(ACHIEV_SPECIAL))

    def get_earned_achievements(self):
        """Anzahl errungener Erfolge."""
        return len(self.achiev_done)

# ═══════════════════════════════════════════════════════════
#  FABRIKFUNKTIONEN
# ═══════════════════════════════════════════════════════════
def make_prop(catalog_row):
    tid, name, icon, price, rent, maint, lvl_max = catalog_row
    return {
        "id": tid, "name": name, "icon": icon, "custom_name": name,
        "price": float(price), "base_rent": float(rent), "rent": float(rent),
        "maint": float(maint), "level": 1, "lvl_max": lvl_max,
        "vacant": True, "listed": False, "tenant": None,
        "contract_left": 0, "rent_hist": [],
        "for_sale": False, "sale_price": 0.0, "months_on_market": 0,
        "condition": 0.95, "months_held": 0, "purchase_price": float(price),
    }

def make_comp(catalog_row):
    tid, name, icon, price, profit, maint, risk, lvl_max = catalog_row
    return {
        "id": tid, "name": name, "icon": icon, "custom_name": name,
        "base_price": float(price), "val": float(price),
        "base_profit": float(profit), "profit": float(profit),
        "maint": float(maint), "risk": risk, "level": 1, "lvl_max": lvl_max,
        "for_sale": False, "sale_price": 0.0, "months_on_market": 0,
        "months_held": 0,
    }

def make_car(catalog_row):
    tid, name, icon, price, rental_income, maint, dep_rate, lvl_max = catalog_row
    return {
        "id": tid, "name": name, "icon": icon, "custom_name": name,
        "price": float(price), "base_rental": float(rental_income),
        "rental": float(rental_income), "maint": float(maint),
        "dep_rate": dep_rate, "level": 1, "lvl_max": lvl_max,
        "rented": False, "rental_customer": None, "contract_left": 0,
        "rental_hist": [], "for_sale": False, "sale_price": 0.0,
        "months_on_market": 0, "condition": 0.95, "months_held": 0,
        "purchase_price": float(price),
    }

def make_car_rental(catalog_row):
    tid, name, icon, price, base_profit, maint, risk, lvl_max = catalog_row
    return {
        "id": tid, "name": name, "icon": icon, "custom_name": name,
        "base_price": float(price), "val": float(price),
        "base_profit": float(base_profit), "profit": float(base_profit),
        "maint": float(maint), "risk": risk, "level": 1, "lvl_max": lvl_max,
        "for_sale": False, "sale_price": 0.0, "months_on_market": 0,
        "months_held": 0,
    }

# ═══════════════════════════════════════════════════════════
#  VERKAUFSABWICKLUNG
# ═══════════════════════════════════════════════════════════
def process_sales(gs: GS):
    """Verarbeite Verkaufsangebote – prüfe auf Käufer."""
    state = None

    # Immobilien-Verkäufe
    for p in gs.props[:]:
        if p["for_sale"] and p["sale_price"] > 0:
            p["months_on_market"] += 1
            # Marktwert basierend auf Zustand, Nachfrage, etc.
            mw = calc_market_value(
                p["purchase_price"], p["months_held"], gs.phase,
                gs.local_demand, p.get("condition", 0.9)
            )
            chance, msg_key = calc_buy_chance(p["sale_price"], mw, gs)

            if p["months_on_market"] == 1 and chance < 0.08:
                gs.add_market_msg(f"{gs.name_of(p)}: {get_price_message('dead')}")
                gs.add_log(f"{gs.name_of(p)}: Preis zu hoch für Marktlage", "warn")
            elif p["months_on_market"] == 1 and chance >= 0.75:
                gs.add_market_msg(f"{gs.name_of(p)}: {get_price_message('hot')}")

            if random.random() < chance:
                proceeds = p["sale_price"]
                gs.cash += proceeds
                gs.total_sales_value += proceeds
                ratio = p["sale_price"] / mw
                if ratio < 0.7:
                    gs.add_news(f"Schnäppchenjäger kauft {gs.name_of(p)}!")
                    gs.add_log(f"{gs.name_of(p)} verkauft (unter Wert)", "warn")
                elif ratio > 1.2:
                    gs.add_news(f"Spitzenpreis! {gs.name_of(p)} luxuriös verkauft.")
                    gs.add_log(f"{gs.name_of(p)} verkauft (Spitzenpreis!)", "good")
                else:
                    gs.add_log(f"{gs.name_of(p)} verkauft für {fmt(proceeds)}", "info")
                gs.add_market_msg(f"{gs.name_of(p)}: {get_price_message('sold')}")
                gs.props.remove(p)

    # Firmen-Verkäufe
    for c in gs.comps[:]:
        if c["for_sale"] and c["sale_price"] > 0:
            c["months_on_market"] += 1
            chance, msg_key = calc_buy_chance(c["sale_price"], c["val"], gs)
            if random.random() < chance:
                proceeds = c["sale_price"]
                gs.cash += proceeds
                gs.total_sales_value += proceeds
                gs.add_log(f"{gs.name_of(c)} verkauft für {fmt(proceeds)}", "info")
                gs.add_market_msg(f"{gs.name_of(c)}: {get_price_message('sold')}")
                gs.comps.remove(c)

    # Auto-Verkäufe
    for car in gs.cars[:]:
        if car["for_sale"] and car["sale_price"] > 0:
            car["months_on_market"] += 1
            mw = calc_market_value(
                car["purchase_price"], car["months_held"], gs.phase,
                gs.local_demand, car.get("condition", 0.9)
            )
            chance, _ = calc_buy_chance(car["sale_price"], mw, gs)
            if random.random() < chance:
                proceeds = car["sale_price"]
                gs.cash += proceeds
                gs.total_sales_value += proceeds
                gs.add_log(f"{gs.name_of(car)} verkauft für {fmt(proceeds)}", "info")
                gs.add_market_msg(f"{gs.name_of(car)}: {get_price_message('sold')}")
                gs.cars.remove(car)

    # Autovermietungs-Verkäufe
    for cr in gs.car_rentals[:]:
        if cr["for_sale"] and cr["sale_price"] > 0:
            cr["months_on_market"] += 1
            chance, _ = calc_buy_chance(cr["sale_price"], cr["val"], gs)
            if random.random() < chance:
                proceeds = cr["sale_price"]
                gs.cash += proceeds
                gs.total_sales_value += proceeds
                gs.add_log(f"{gs.name_of(cr)} verkauft für {fmt(proceeds)}", "info")
                gs.car_rentals.remove(cr)

    return state

# ═══════════════════════════════════════════════════════════
#  ZUFALLSEREIGNISSE (erweitert)
# ═══════════════════════════════════════════════════════════
# Neue Markt-/Nachfrageereignisse
def _ev_market_boom(gs):
    """Lokale Nachfrage steigt stark."""
    gs.local_demand = min(2.0, gs.local_demand + 0.4)
    gs.add_log("Nachfrageboom! Lokale Wirtschaft brummt.", "good")
    gs.add_news("Lokale Nachfrage sprunghaft gestiegen!")

def _ev_market_crash(gs):
    """Lokale Nachfrage fällt."""
    gs.local_demand = max(0.3, gs.local_demand - 0.4)
    gs.add_log("Nachfrageeinbruch! Lokale Wirtschaft schwächelt.", "bad")
    gs.add_news("Warnung: Lokale Nachfrage eingebrochen!")

def _ev_competition_rise(gs):
    """Konkurrenz steigt."""
    gs.competition = min(1.0, gs.competition + 0.15)
    gs.add_log("Konkurrenz nimmt zu! Höhere Kosten erwartet.", "bad")
    gs.add_news("Neuer Wettbewerber betritt den Markt!")

def _ev_competition_fall(gs):
    """Konkurrenz sinkt."""
    gs.competition = max(0.0, gs.competition - 0.1)
    gs.add_log("Konkurrent ausgeschaltet! Mehr Marktmacht.", "good")

def _ev_trend_up(gs):
    """Markttrend positiv."""
    gs.market_trend = min(0.1, gs.market_trend + 0.03)
    gs.add_log("Positiver Markttrend: Steigende Immobilienwerte.", "good")

def _ev_trend_down(gs):
    """Markttrend negativ."""
    gs.market_trend = max(-0.1, gs.market_trend - 0.03)
    gs.add_log("Negativer Markttrend: Fallende Immobilienwerte.", "bad")

def _ev_fire(gs):
    if not gs.props: return
    p = random.choice(gs.props)
    dmg = p["price"] * 0.08
    gs.cash -= dmg
    p["condition"] = max(0.3, p.get("condition", 1.0) - 0.2)
    p["price"] -= dmg
    gs.add_log(f"Brandschaden: {gs.name_of(p)} -{fmt(dmg)}", "bad")

def _ev_vacancy(gs):
    occupied = [p for p in gs.props if not p.get("vacant", True)]
    if not occupied: return
    p = random.choice(occupied)
    p["tenant"] = None
    p["vacant"] = True
    p["contract_left"] = 0
    gs.add_log(f"Mieter ausgezogen: {gs.name_of(p)}", "bad")

def _ev_lawsuit(gs):
    if not gs.comps: return
    c = random.choice(gs.comps)
    pen = c["val"] * 0.08
    gs.cash -= pen
    gs.reputation = max(0, gs.reputation - 5)
    gs.add_log(f"Klage gegen {gs.name_of(c)}: -{fmt(pen)}", "bad")

def _ev_subsidy(gs):
    amt = 5_000 + random.random() * 30_000
    gs.cash += amt
    gs.add_log(f"Staatliche Förderung: +{fmt(amt)}", "good")

def _ev_crash(gs):
    for s in gs.stock_data.values():
        s["price"] *= 0.75 + random.random() * 0.10
    gs.add_log("Börsencrash! Aktien massiv gefallen.", "bad")
    gs.add_news("Börsencrash! Weltweite Aktienkurse stürzen ab!")

def _ev_rally(gs):
    for s in gs.stock_data.values():
        s["price"] *= 1.10 + random.random() * 0.10
    gs.add_log("Bullenmarkt! Aktien stark gestiegen.", "good")
    gs.add_news("Bullenrallye an den Börsen!")

def _ev_bad_press(gs):
    gs.reputation = max(0, gs.reputation - 12)
    gs.add_log("Negativschlagzeile: Ruf -12", "bad")

def _ev_good_press(gs):
    gs.reputation = min(100, gs.reputation + 10)
    gs.add_log("Positive Presse: Ruf +10", "good")

def _ev_tax_audit(gs):
    amt = gs.cash * 0.05
    gs.cash -= amt
    gs.add_log(f"Steuerprüfung: Nachzahlung -{fmt(amt)}", "bad")

def _ev_infra(gs):
    """Stadtentwicklung verbessert Immobilienwerte."""
    if not gs.props: return
    p = random.choice(gs.props)
    p["price"] *= 1.12
    p["condition"] = min(1.0, p.get("condition", 1.0) + 0.05)
    gs.add_log(f"Stadtentwicklung: {gs.name_of(p)} +12%", "good")

def _ev_regulation(gs):
    """Neue Regulierungen senken Unternehmensgewinne."""
    for c in gs.comps:
        c["profit"] *= 0.82
        c["base_profit"] *= 0.82
    gs.add_log("Neue Regulierung: Firmengewinne -18%", "bad")

def _ev_bank_run(gs):
    gs.base_rate *= 1.25
    gs.add_log("Bankenkrise! Leitzins gestiegen.", "bad")

def _ev_credit_crunch(gs):
    if gs.loan > 0:
        extra = gs.loan * 0.025
        gs.cash -= extra
        gs.add_log(f"Kreditklemme: Zusätzliche Gebühren -{fmt(extra)}", "bad")

def _ev_renovation_needed(gs):
    """Immobilie benötigt dringend Renovierung."""
    if not gs.props: return
    p = random.choice(gs.props)
    cost = p["price"] * 0.10
    if gs.cash >= cost:
        gs.cash -= cost
        p["condition"] = min(1.0, p.get("condition", 1.0) + 0.15)
        gs.add_log(f"Renovierung {gs.name_of(p)}: -{fmt(cost)}", "warn")
    else:
        p["condition"] = max(0.3, p.get("condition", 1.0) - 0.1)
        gs.add_log(f"{gs.name_of(p)} verfällt: Keine Mittel für Renovierung", "bad")

def _ev_strike(gs):
    """Streik bei einem Unternehmen."""
    if not gs.comps: return
    c = random.choice(gs.comps)
    loss = c["profit"] * 3
    gs.cash -= loss
    gs.reputation = max(0, gs.reputation - 3)
    gs.add_log(f"Streik bei {gs.name_of(c)}: -{fmt(loss)}", "bad")

def _random_events(gs: GS):
    """Führe zufällige Ereignisse aus."""
    events = [
        (0.020, lambda: _ev_fire(gs)),
        (0.018, lambda: _ev_vacancy(gs)),
        (0.012, lambda: _ev_lawsuit(gs)),
        (0.020, lambda: _ev_subsidy(gs)),
        (0.006, lambda: _ev_crash(gs)),
        (0.006, lambda: _ev_rally(gs)),
        (0.014, lambda: _ev_bad_press(gs)),
        (0.014, lambda: _ev_good_press(gs)),
        (0.008, lambda: _ev_tax_audit(gs)),
        (0.016, lambda: _ev_infra(gs)),
        (0.008, lambda: _ev_regulation(gs)),
        (0.010 if gs.difficulty == "hard" else 0.004, lambda: _ev_bank_run(gs)),
        (0.012 if gs.difficulty == "hard" else 0.006, lambda: _ev_credit_crunch(gs)),
        (0.015, lambda: _ev_renovation_needed(gs)),
        (0.008, lambda: _ev_strike(gs)),
        # Neue Markt-/Nachfrageereignisse
        (0.012, lambda: _ev_market_boom(gs)),
        (0.010, lambda: _ev_market_crash(gs)),
        (0.010, lambda: _ev_competition_rise(gs)),
        (0.008, lambda: _ev_competition_fall(gs)),
        (0.010, lambda: _ev_trend_up(gs)),
        (0.010, lambda: _ev_trend_down(gs)),
    ]
    for prob, fn in events:
        if random.random() < prob:
            fn()

# ═══════════════════════════════════════════════════════════
#  WIRTSCHAFTS-UPDATE
# ═══════════════════════════════════════════════════════════
def _update_economy(gs: GS):
    """Aktualisiere Wirtschaftsindikatoren."""
    gs.phase_dur -= 1
    if gs.phase_dur <= 0:
        prev = gs.phase
        r = random.random()
        if r < 0.06:
            gs.phase, gs.phase_dur = "DEPRESSION", random.randint(2, 4)
        elif r < 0.20:
            gs.phase, gs.phase_dur = "RECESSION", random.randint(3, 6)
        elif r < 0.26:
            gs.phase, gs.phase_dur = "STAGFLATION", random.randint(2, 4)
        elif r < 0.28:
            gs.phase, gs.phase_dur = "HYPERINFLATION", random.randint(1, 2)
        elif r < 0.62:
            gs.phase, gs.phase_dur = "STABLE", random.randint(5, 10)
        else:
            gs.phase, gs.phase_dur = "BOOM", random.randint(3, 5)
        if gs.phase != prev:
            label = PHASES[gs.phase]["label"]
            gs.add_news(f"Wirtschaftswechsel: {label}")
            kind = "good" if gs.phase == "BOOM" else ("bad" if "DEPRESS" in gs.phase else "warn")
            gs.add_log(f"Wirtschaft: {label}", kind)

    delta = {"BOOM": +.05, "STABLE": 0, "RECESSION": -.08, "DEPRESSION": -.12,
             "STAGFLATION": 0, "HYPERINFLATION": 0}
    gs.base_rate = max(0.5, min(15, gs.base_rate + delta.get(gs.phase, 0)))
    gs.loan_rate = 0.004 + gs.base_rate / 100.0 / 12.0

    gs.gdp += {"BOOM": .12, "STABLE": 0, "RECESSION": -.15, "DEPRESSION": -.35,
               "STAGFLATION": -.08, "HYPERINFLATION": -.12}.get(gs.phase, 0)
    gs.unemp += {"BOOM": -.08, "STABLE": 0, "RECESSION": .20, "DEPRESSION": .40,
                 "STAGFLATION": .08, "HYPERINFLATION": .08}.get(gs.phase, 0)
    gs.gdp = max(-15, min(12, gs.gdp))
    gs.unemp = max(1, min(30, gs.unemp))
    gs.sentiment += (random.random() - 0.48) * 6
    gs.sentiment = max(0, min(100, gs.sentiment))

    # Markt-Nachfrage-Dynamik
    gs.local_demand += (random.random() - 0.48) * 0.05
    gs.local_demand = max(0.2, min(2.0, gs.local_demand))
    gs.competition += (random.random() - 0.5) * 0.02
    gs.competition = max(0.0, min(1.0, gs.competition))
    gs.market_trend += (random.random() - 0.5) * 0.005
    gs.market_trend = max(-0.1, min(0.1, gs.market_trend))

def _update_markets(gs: GS):
    """Aktualisiere Aktien- und ETF-Kurse."""
    ph = PHASES[gs.phase]
    sent = (gs.sentiment - 50) / 5000.0
    sector_bonus = {
        "Tech": ("BOOM", .015),
        "Energie": ("STAGFLATION", .02),
        "Finanzen": ("DEPRESSION", -.025),
        "Gesundheit": (None, .005),
        "Konsum": (None, .003),
    }
    for sid, s in gs.stock_data.items():
        se = 0.0
        for sec, (cond, val) in sector_bonus.items():
            if s["sector"] == sec and (cond is None or gs.phase == cond):
                se = val
        chg = (random.random() - 0.5) * 2 * s["vol"] + ph["stk"] + se + sent
        s["price"] = max(0.5, s["price"] * (1 + chg))
        s["hist"].append(round(s["price"], 2))
        if len(s["hist"]) > 40:
            s["hist"].pop(0)

    etf_chg = (random.random() - 0.48) * 0.04 + ph["stk"] * 0.5
    gs.etf_price = max(5, gs.etf_price * (1 + etf_chg))
    gs.etf_hist.append(round(gs.etf_price, 2))
    if len(gs.etf_hist) > 40:
        gs.etf_hist.pop(0)

# ═══════════════════════════════════════════════════════════
#  HAUPTSCHLEIFE (Monatlicher Tick)
# ═══════════════════════════════════════════════════════════
def tick(gs: GS):
    """Führe einen Monatsspielzug aus."""
    gs.month += 1
    if gs.month > 12:
        gs.month = 1
        gs.year += 1
        _year_end(gs)

    _update_economy(gs)
    _update_markets(gs)
    process_sales(gs)

    diff = DIFFICULTY[gs.difficulty]
    ph = PHASES[gs.phase]
    income = 0.0
    expenses = 0.0

    # --- Immobilien ---
    for p in gs.props:
        if p.get("for_sale"):
            if not p.get("vacant", True):
                p["tenant"] = None
                p["vacant"] = True
                p["contract_left"] = 0
                gs.add_log(f"Verkaufsabsicht: Mieter in {gs.name_of(p)} gekündigt", "warn")
            continue

        # Monate im Besitz erhöhen
        p["months_held"] = p.get("months_held", 0) + 1
        # Zustand verschlechtert sich langsam
        p["condition"] = max(0.5, p.get("condition", 1.0) - 0.002)

        # Mietvertrags-Management
        if p.get("tenant") is not None and p.get("contract_left", 0) > 0:
            p["contract_left"] -= 1
            if p["contract_left"] == 0:
                tname = TENANT_TYPES[p["tenant"]][0]
                gs.add_log(f"Mietvertrag abgelaufen: {gs.name_of(p)} ({tname})", "warn")
                p["vacant"] = True
                p["tenant"] = None

        # Neue Mieter suchen (automatisch)
        if p.get("listed") and p.get("vacant"):
            base_chance = 0.35 * (0.8 + gs.local_demand * 0.3)
            phase_adj = {"BOOM": 1.5, "STABLE": 1.0, "RECESSION": 0.6,
                         "DEPRESSION": 0.25, "STAGFLATION": 0.4, "HYPERINFLATION": 0.3}
            chance = base_chance * phase_adj.get(gs.phase, 1.0)
            if random.random() < chance:
                weights = [4, 3, 2, 1, 2]
                ti = random.choices(range(len(TENANT_TYPES)), weights=weights)[0]
                tname, bonus, _, months = TENANT_TYPES[ti]
                p["tenant"] = ti
                p["vacant"] = False
                p["contract_left"] = months
                p["rent"] = p.get("base_rent", 0) * (1 + bonus)
                gs.add_log(f"Neuer Mieter: {tname} in {gs.name_of(p)}", "good")

        # Mieterschäden
        if not p.get("vacant") and p.get("tenant") is not None:
            dmg_risk = TENANT_TYPES[p["tenant"]][2]
            if random.random() < dmg_risk * 0.3:
                dmg = p.get("maint", 0) * (0.3 + random.random() * 0.5)
                expenses += dmg
                p["condition"] = max(0.5, p.get("condition", 1.0) - 0.05)
                gs.add_log(f"Mieterschaden in {gs.name_of(p)}: -{fmt(dmg)}", "bad")

        # Mieteinnahmen + Instandhaltung
        rent = p.get("rent", 0) * (1 + ph["rent"]) if not p.get("vacant") else 0.0
        # Nachfrage beeinflusst Mietpreise
        demand_factor = 0.85 + gs.local_demand * 0.2
        rent *= demand_factor
        income += rent
        expenses += p.get("maint", 0)

        p["rent_hist"].append(round(rent))
        if len(p["rent_hist"]) > 24:
            p["rent_hist"].pop(0)

        # Marktwert-Entwicklung
        p["price"] = calc_market_value(
            p["purchase_price"], p["months_held"], gs.phase,
            gs.local_demand, p.get("condition", 0.9)
        )
        p["base_rent"] *= 1 + gs.inflation * 0.3

    # --- Unternehmen ---
    rep_bonus = (gs.reputation - 50) / 2000.0
    for c in gs.comps:
        if c.get("for_sale"):
            continue
        c["months_held"] = c.get("months_held", 0) + 1
        # Wettbewerb senkt Gewinne
        comp_factor = 1.0 - gs.competition * 0.2
        # Markttrend beeinflusst
        trend_factor = 1.0 + gs.market_trend
        eff = c.get("base_profit", 0) * (1 + ph["profit"] + rep_bonus) * comp_factor * trend_factor
        c["profit"] = max(0.0, eff)

        if random.random() < c.get("risk", 0.05) * 0.3:
            dmg = c["profit"] * (0.1 + random.random() * 0.2)
            expenses += dmg
            gs.add_log(f"Schaden bei {gs.name_of(c)}: -{fmt(dmg)}", "bad")

        income += c["profit"]
        expenses += c.get("maint", 0)
        c["val"] *= 1 + gs.inflation * 0.3
        c["base_profit"] *= 1 + gs.inflation * 0.15

    # --- Autos ---
    for car in gs.cars:
        if car.get("for_sale"):
            continue
        car["months_held"] = car.get("months_held", 0) + 1
        car["condition"] = max(0.4, car.get("condition", 1.0) - 0.003)

        # Mietvertrag
        if car.get("contract_left", 0) > 0:
            car["contract_left"] -= 1
            if car["contract_left"] == 0:
                car["rented"] = False
                car["rental_customer"] = None
                gs.add_log(f"{gs.name_of(car)}: Mieter abgereist", "warn")

        # Automatische Vermietung
        if not car.get("rented") and not car.get("for_sale"):
            base_ch = 0.30 * (0.8 + gs.local_demand * 0.3)
            phase_ch = {"BOOM": 1.6, "STABLE": 1.0, "RECESSION": 0.5,
                        "DEPRESSION": 0.2, "STAGFLATION": 0.3, "HYPERINFLATION": 0.2}
            ch = base_ch * phase_ch.get(gs.phase, 1.0)
            if random.random() < ch:
                ci = random.choices(range(len(CAR_RENTAL_CUSTOMERS)), weights=[4, 3, 2, 1])[0]
                cname, bonus, _, months = CAR_RENTAL_CUSTOMERS[ci]
                car["rented"] = True
                car["rental_customer"] = ci
                car["contract_left"] = months
                car["rental"] = car.get("base_rental", 0) * (1 + bonus)
                gs.add_log(f"{gs.name_of(car)} vermietet an {cname} ({months}M)", "good")

        car_rent = car.get("rental", 0) * (1 + ph["rent"]) if car.get("rented") else 0.0
        income += car_rent
        expenses += car.get("maint", 0)
        car["rental_hist"].append(round(car_rent))
        if len(car["rental_hist"]) > 24:
            car["rental_hist"].pop(0)
        # Wertverlust
        car["price"] *= (1 - car.get("dep_rate", 0.005))
        car["base_rental"] *= 1 + gs.inflation * 0.25

    # --- Autovermietungen ---
    for cr in gs.car_rentals:
        if cr.get("for_sale"):
            continue
        cr["months_held"] = cr.get("months_held", 0) + 1
        comp_factor = 1.0 - gs.competition * 0.15
        trend_factor = 1.0 + gs.market_trend * 0.5
        eff = cr.get("base_profit", 0) * (1 + ph["profit"] + rep_bonus) * comp_factor * trend_factor
        cr["profit"] = max(0.0, eff)
        if random.random() < cr.get("risk", 0.05) * 0.3:
            dmg = cr["profit"] * (0.1 + random.random() * 0.2)
            expenses += dmg
            gs.add_log(f"Schaden bei {gs.name_of(cr)}: -{fmt(dmg)}", "bad")
        income += cr["profit"]
        expenses += cr.get("maint", 0)
        cr["val"] *= 1 + gs.inflation * 0.25
        cr["base_profit"] *= 1 + gs.inflation * 0.12

    # --- Kreditzinsen ---
    eff_rate = gs.loan_rate + gs.base_rate / 100.0 / 12.0
    expenses += gs.loan * eff_rate

    # --- Festgeldzinsen ---
    income += gs.savings * gs.sav_rate

    # --- Dividenden ---
    for sid, qty in gs.stocks.items():
        if qty > 0:
            income += qty * gs.stock_data[sid]["price"] * gs.stock_data[sid]["div"] / 12.0
    income += gs.etf * gs.etf_price * 0.002 / 12.0

    # --- Zufallsereignisse ---
    _random_events(gs)

    # --- Steuern & Cashflow ---
    gross = income - expenses
    tax = max(0.0, gross * gs.tax_rate)
    expenses += tax
    cf = income - expenses
    gs.cash += cf

    # Historien aktualisieren
    gs.cf_hist.append(cf)
    gs.nw_hist.append(gs.net_worth())
    if len(gs.cf_hist) > 24:
        gs.cf_hist.pop(0)
    if len(gs.nw_hist) > 24:
        gs.nw_hist.pop(0)

    # --- Inflation ---
    gs.inflation = 0.001 + random.random() * 0.003
    if gs.phase == "HYPERINFLATION":
        gs.inflation *= 4

    # --- Krisenüberlebens-Check ---
    if gs.phase == "DEPRESSION" and gs.net_worth() > 0 and gs.cash > 0:
        if not gs._last_dep_phase:
            gs._survived_dep_count += 1
            gs._last_dep_phase = True
            gs.add_log(f"Depression #{gs._survived_dep_count} überstanden!", "good")
    else:
        gs._last_dep_phase = (gs.phase == "DEPRESSION")

    # --- Bankrott-Prüfung ---
    if gs.net_worth() < -15_000:
        gs.add_log("KRISE: Nettovermögen stark negativ!", "bad")
        if gs.cash < -75_000 and gs.loan > 0:
            gs.add_news("Zahlungsunfähigkeit droht!")
            if gs.cash < -150_000:
                return "bankrott"

    if gs.loan > 0 and gs.net_worth() > 0 and gs.loan > gs.net_worth() * 4:
        gs.add_log("ÜBERSCHULDUNG! Gläubiger werden aktiv!", "bad")
        if gs.cash < -gs.loan * 0.05:
            return "bankrott"

    # --- Härtefall: Tilgung im schweren Modus ---
    if gs.difficulty == "hard" and gs.loan > 0:
        min_payment = gs.loan * 0.004
        if gs.cash >= min_payment:
            gs.cash -= min_payment
            gs.loan = max(0, gs.loan - min_payment)
        else:
            gs.add_log("WARNUNG: Mindesttilgung nicht möglich!", "bad")
            gs.loan *= 1.015
            if gs.loan > gs.net_worth() * 3 and gs.cash < 0:
                return "bankrott"

    return None

def _year_end(gs: GS):
    """Jahresend-Aktionen."""
    gs.add_news(f"Jahresabschluss {gs.year - 1}: NV {fmt(gs.net_worth())}")
    if gs.net_worth() > 3_000_000:
        wt = (gs.net_worth() - 3_000_000) * 0.006
        gs.cash -= wt
        gs.add_log(f"Vermögenssteuer: -{fmt(wt)}", "bad")

# ═══════════════════════════════════════════════════════════
#  ACHIEVEMENT-CHECK
# ═══════════════════════════════════════════════════════════
def check_achievements(gs: GS):
    """Prüfe alle Achievements und schalte neue frei."""
    new_achievements = []
    all_achievements = {}

    # Kategorien durchgehen
    for cat_id, cat_data in [
        ("immo", ACHIEV_IMMO), ("cars", ACHIEV_CARS),
        ("filialen", ACHIEV_FILIALEN), ("firmen", ACHIEV_FIRMEN),
        ("vermoegen", ACHIEV_VERMOEGEN),
    ]:
        for tier, info in cat_data.items():
            aid = f"{cat_id}_{tier}"
            all_achievements[aid] = info
            if aid not in gs.achiev_done and info["check"](gs):
                gs.achiev_done.add(aid)
                gs.achiev_tiers[f"{cat_id}_max"] = tier
                new_achievements.append((info["title"], info["desc"]))

    # Spezial-Achievements prüfen
    for aid, title, desc, check in ACHIEV_SPECIAL:
        all_achievements[aid] = {"title": title, "desc": desc}
        if aid not in gs.achiev_done:
            # Perfektionist: alle anderen müssen freigeschaltet sein
            if aid == "perf_1":
                # Alle anderen (außer perf_1 selbst) müssen freigeschaltet sein
                total_others = sum(1 for a, _, _, _ in ACHIEV_SPECIAL if a != "perf_1")
                # Prüfe alle Kategorie-Achievements
                cat_count = (len(ACHIEV_IMMO) + len(ACHIEV_CARS) + len(ACHIEV_FILIALEN) +
                             len(ACHIEV_FIRMEN) + len(ACHIEV_VERMOEGEN))
                # Prüfe: alle Kategorie-ACH + alle anderen Spezial-ACH außer perf_1
                other_ids = [a for a, _, _, _ in ACHIEV_SPECIAL if a != "perf_1"]
                earned_others = gs.achiev_done.intersection(other_ids)
                # Für Perfektionist: alle (cat_count + total_others) müssen erreicht sein
                # Aber das ist extrem schwer – vereinfacht: cat_count * 80%
                if len(gs.achiev_done) >= int((cat_count + total_others) * 0.8):
                    gs.achiev_done.add(aid)
                    new_achievements.append((title, desc))
            elif check(gs):
                gs.achiev_done.add(aid)
                new_achievements.append((title, desc))

    return new_achievements

# ═══════════════════════════════════════════════════════════
#  UI-KOMPONENTE: AKkordeon-Navigation (linke Seitenleiste)
# ═══════════════════════════════════════════════════════════
class NavCategory:
    """Eine Kategorie im Akkordeon-Menü."""
    def __init__(self, label, icon="▶", default_open=False):
        self.label = label
        self.icon = icon
        self.open = default_open
        self.items: List[NavItem] = []

    def add_item(self, key, label, action=None):
        self.items.append(NavItem(key, label, action))

    def toggle(self):
        self.open = not self.open

class NavItem:
    """Ein Menüpunkt innerhalb einer Kategorie."""
    def __init__(self, key, label, action=None):
        self.key = key
        self.label = label
        self.action = action
        self.active = False
        self.hover = False

class SidebarNav:
    """Linke Navigationsleiste mit Akkordeon-Struktur."""
    def __init__(self):
        self.categories: List[NavCategory] = []
        self.width = 200
        self.active_key = None
        self._build_menu()

    def _build_menu(self):
        """Erstelle die Menüstruktur."""
        # Dashboard
        cat = NavCategory("Dashboard", "📊", True)
        cat.add_item("dashboard", "Übersicht")
        self.categories.append(cat)

        # Einstellungen
        cat = NavCategory("Einstellungen", "⚙️")
        cat.add_item("settings_general", "Allgemein")
        cat.add_item("settings_graphics", "Grafik")
        cat.add_item("settings_audio", "Audio")
        cat.add_item("settings_gameplay", "Gameplay")
        self.categories.append(cat)

        # Immobilien
        cat = NavCategory("Immobilien", "🏠")
        cat.add_item("buy_prop", "Kaufen")
        cat.add_item("sell_prop", "Verkaufen")
        cat.add_item("rent_prop", "Verwaltung")
        cat.add_item("upg_prop", "Renovieren")
        cat.add_item("rename_prop", "Umbenennen")
        cat.add_item("stats_prop", "Statistik")
        self.categories.append(cat)

        # Autos
        cat = NavCategory("Autos", "🚗")
        cat.add_item("buy_car", "Kaufen")
        cat.add_item("sell_car", "Verkaufen")
        cat.add_item("rent_car", "Garage")
        cat.add_item("upgrade_car", "Tuning")
        cat.add_item("rename_car", "Umbenennen")
        cat.add_item("stats_car", "Statistik")
        self.categories.append(cat)

        # Filialen (Autovermietung)
        cat = NavCategory("Autovermietung", "🏪")
        cat.add_item("buy_car_rental", "Kaufen")
        cat.add_item("sell_car_rental", "Verkaufen")
        cat.add_item("upgrade_car_rental", "Verwalten")
        cat.add_item("rename_car_rental", "Umbenennen")
        cat.add_item("stats_rental", "Finanzen")
        self.categories.append(cat)

        # Firmen
        cat = NavCategory("Unternehmen", "🏢")
        cat.add_item("buy_comp", "Gründen")
        cat.add_item("sell_comp", "Verkaufen")
        cat.add_item("upg_comp", "Erweitern")
        cat.add_item("rename_comp", "Umbenennen")
        cat.add_item("stats_comp", "Finanzen")
        self.categories.append(cat)

        # Bank
        cat = NavCategory("Bank", "🏦")
        cat.add_item("bank_loan", "Kredit")
        cat.add_item("bank_repay", "Tilgung")
        cat.add_item("bank_savings", "Festgeld")
        cat.add_item("bank_etf", "ETF")
        cat.add_item("bank_stocks", "Aktien")
        self.categories.append(cat)

        # System
        cat = NavCategory("System", "💾")
        cat.add_item("save_game", "Speichern")
        cat.add_item("load_game", "Laden")
        cat.add_item("backup", "Backup")
        cat.add_item("import_export", "Import/Export")
        self.categories.append(cat)

        # Erfolge & Statistiken
        cat = NavCategory("Erfolge", "🏆")
        cat.add_item("achievements", "Erfolge")
        self.categories.append(cat)

        cat = NavCategory("Statistiken", "📈")
        cat.add_item("stats_overview", "Statistiken")
        cat.add_item("log_view", "Log")
        self.categories.append(cat)

    def get_action(self, key):
        """Finde die Aktion zu einem Key (für Callback-Mapping)."""
        for cat in self.categories:
            for item in cat.items:
                if item.key == key:
                    return key  # Wir geben den Key zurück, der als Action fungiert
        return None

    def handle_click(self, mx, my, sidebar_x, sidebar_y):
        """Verarbeite Klicks auf die Navigation."""
        # Prüfe Kategorie-Köpfe
        y = sidebar_y + 10
        cat_font = F["sm"]
        item_font = F["xs"]

        for cat in self.categories:
            cat_h = 28
            if pygame.Rect(sidebar_x, y, self.width, cat_h).collidepoint(mx, my):
                cat.toggle()
                return None

            y += cat_h

            if cat.open:
                for item in cat.items:
                    item_h = 24
                    if pygame.Rect(sidebar_x, y, self.width, item_h).collidepoint(mx, my):
                        self.active_key = item.key
                        return item.key
                    y += item_h

        return None

    def draw(self, surf, x, y, h):
        """Zeichne die Navigationsleiste."""
        box(surf, PANEL, (x, y, self.width, h))
        line(surf, BORDER, (x + self.width, y), (x + self.width, y + h))

        y_pos = y + 10
        cat_font = F["sm"]
        item_font = F["xs"]

        for cat in self.categories:
            # Kategorie-Header
            cat_h = 28
            header_rect = pygame.Rect(x, y_pos, self.width, cat_h)
            box(surf, PANEL2, header_rect, 4)

            # Icon + Label
            icon = "▼" if cat.open else "▶"
            txt(surf, f"{icon} {cat.label}", "sm", WHITE, x + 12, y_pos + cat_h // 2, "midleft")
            y_pos += cat_h

            if cat.open:
                for item in cat.items:
                    item_h = 24
                    item_rect = pygame.Rect(x + 8, y_pos, self.width - 8, item_h)

                    # Aktiver Punkt hervorheben
                    is_active = self.active_key == item.key
                    if is_active:
                        box(surf, ACCENT, item_rect, 4)
                        txt(surf, f"   {item.label}", "xs", WHITE, x + 12, y_pos + item_h // 2, "midleft")
                    else:
                        txt(surf, f"   {item.label}", "xs", MUTED, x + 12, y_pos + item_h // 2, "midleft")
                    y_pos += item_h

# ═══════════════════════════════════════════════════════════
#  NAME-SCREEN (Startbildschirm)
# ═══════════════════════════════════════════════════════════
class NameScreen:
    def __init__(self):
        self.box = InputBox(W // 2 - 120, H // 2 - 85, 240, 38, "Dein Name", numeric=False)
        self.diff_selected = "medium"
        btn_w = 150; btn_h = 56; spacing = 12
        total_w = 3 * btn_w + 2 * spacing; start_x = W // 2 - total_w // 2
        self.diff_btns = {}
        diff_colors = {"easy": (GREEN[0] // 2, GREEN[1] // 2, GREEN[2] // 2),
                       "medium": (YELLOW[0] // 2, YELLOW[1] // 2, YELLOW[2] // 2),
                       "hard": (RED[0] // 2, RED[1] // 2, RED[2] // 2)}
        for i, key in enumerate(["easy", "medium", "hard"]):
            bx2 = start_x + i * (btn_w + spacing)
            self.diff_btns[key] = Btn(bx2, H // 2 - 18, btn_w, btn_h, DIFFICULTY[key]["label"],
                                      color=diff_colors[key], fkey="lg")
        self.start_btn = Btn(W // 2 - 70, H // 2 + 110, 140, 42, "Spielen", GREEN, BG, "lg")

    def handle(self, ev):
        self.box.handle(ev)
        for key, btn in self.diff_btns.items():
            btn.update(pygame.mouse.get_pos())
            if btn.hit(ev):
                self.diff_selected = key
        if self.start_btn.hit(ev) or (ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN):
            name = self.box.text.strip() or "Investor"
            return (name, self.diff_selected)
        return None

    def draw(self, surf):
        surf.fill(BG)
        txt(surf, "BUSINESS TYCOON PRO V5", "title", GOLD, W // 2, H // 2 - 200, "center")
        txt(surf, "Das ultimative Wirtschaftssimulations-Erlebnis", "md", MUTED, W // 2, H // 2 - 165, "center")
        txt(surf, "Wie heißt du, Tycoon?", "md", WHITE, W // 2, H // 2 - 120, "center")
        self.box.draw(surf)
        txt(surf, "Schwierigkeitsgrad", "sm", MUTED, W // 2, H // 2 - 45, "center")
        for btn in self.diff_btns.values():
            btn.draw(surf)
        sel_btn = self.diff_btns[self.diff_selected]
        border_col = {"easy": GREEN, "medium": YELLOW, "hard": RED}[self.diff_selected]
        box(surf, border_col, (sel_btn.rect.x - 3, sel_btn.rect.y - 3,
                               sel_btn.rect.w + 6, sel_btn.rect.h + 6), 10, 2)
        diff = DIFFICULTY[self.diff_selected]
        desc_bg = pygame.Rect(W // 2 - 220, H // 2 + 48, 440, 34)
        box(surf, PANEL2, desc_bg, 8)
        txt(surf, diff["desc"], "sm", WHITE, W // 2, H // 2 + 65, "center", 420)
        self.start_btn.update(pygame.mouse.get_pos())
        self.start_btn.draw(surf)

        # Legende
        leg_y = H // 2 + 175
        legends = [
            ("Einfach", "100k € Start, moderate Wirtschaft", GREEN),
            ("Medium", "30k € Start, ausgewogen", YELLOW),
            ("Schwer", "50k € + 60k Schulden, harte Tilgung!", RED),
        ]
        for i, (lbl, desc, col) in enumerate(legends):
            txt(surf, f"{lbl}:", "xs", col, W // 2 - 240, leg_y + i * 18)
            txt(surf, desc, "xs", MUTED, W // 2 - 170, leg_y + i * 18)

        txt(surf, "Drücke ENTER oder klicke 'Spielen'", "xs", MUTED, W // 2, H // 2 + 230, "center")

# ═══════════════════════════════════════════════════════════
#  HAUPTSPIEL-BILDSCHIRM (GameScreen)
# ═══════════════════════════════════════════════════════════
class GameScreen:
    """Hauptspiel-UI mit Sidebar-Navigation und Inhalt."""
    def __init__(self, gs: GS):
        self.gs = gs
        self.nav = SidebarNav()
        self.sidebar_width = self.nav.width
        self.speed = 2000
        self.paused = False
        self.last_tick = pygame.time.get_ticks()
        self.modal = None
        self._ach_popup = None
        self._inputs = {}
        self._scroll = 0
        self._content_key = "dashboard"

        # Tabs für Unter-Ansichten (innerhalb des Content-Bereichs)
        self.stock_tab = 0  # 0 = Aktien, 1 = ETF

    def update(self):
        return None

    def maybe_tick(self):
        if self.paused or self.modal:
            return None
        now = pygame.time.get_ticks()
        if now - self.last_tick >= self.speed:
            self.last_tick = now
            result = tick(self.gs)
            # Achievements prüfen
            new_achs = check_achievements(self.gs)
            for title, desc in new_achs:
                self.gs.add_log(f"Erfolg: {title}", "good")
                self._ach_popup = (title, desc, pygame.time.get_ticks())
            if result == "bankrott":
                return "bankrott"
        return None

    def handle(self, ev):
        for ib in self._inputs.values():
            ib.handle(ev)

        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                self._close_modal()
            if ev.key == pygame.K_SPACE and not self.modal:
                self.paused = not self.paused

        if ev.type == pygame.MOUSEWHEEL:
            # Scroll only when a modal is open; otherwise ignore
            if self.modal:
                self._scroll = max(0, self._scroll - ev.y * 30)

        if ev.type != pygame.MOUSEBUTTONDOWN or ev.button != 1:
            return None

        mx, my = ev.pos

        # Modal-Klicks zuerst behandeln
        if self.modal:
            return self._handle_modal_click(mx, my)

        # Sidebar-Klick
        nav_result = self.nav.handle_click(mx, my, 0, 44)
        if nav_result:
            self._content_key = nav_result
            # Reset scroll when changing content view
            self._scroll = 0
            self._inputs = {}
            self._handle_nav_action(nav_result)
            return None

        # Topbar-Klicks (Geschwindigkeit, Pause)
        if pygame.Rect(W - 240, 9, 38, 26).collidepoint(mx, my):
            self.speed = 2000
            return None
        if pygame.Rect(W - 196, 9, 38, 26).collidepoint(mx, my):
            self.speed = 800
            return None
        if pygame.Rect(W - 152, 9, 38, 26).collidepoint(mx, my):
            self.speed = 300
            return None
        if pygame.Rect(W - 100, 9, 88, 26).collidepoint(mx, my):
            self.paused = not self.paused
            return None

        return None

    def _handle_nav_action(self, key):
        """Verarbeite Navigations-Klicks."""
        actions = {
            # Immobilien
            "buy_prop": self._open_buy_prop,
            "sell_prop": self._open_sell_prop,
            "upg_prop": self._open_upg_prop,
            "rent_prop": self._open_rent_prop,
            "rename_prop": self._open_rename_prop,
            "stats_prop": self._open_stats_prop,
            # Autos
            "buy_car": self._open_buy_car,
            "sell_car": self._open_sell_car,
            "rent_car": self._open_rent_car,
            "upgrade_car": self._open_upgrade_car,
            "rename_car": self._open_rename_car,
            "stats_car": self._open_stats_car,
            # Autovermietung
            "buy_car_rental": self._open_buy_car_rental,
            "sell_car_rental": self._open_sell_car_rental,
            "upgrade_car_rental": self._open_upgrade_car_rental,
            "rename_car_rental": self._open_rename_car_rental,
            "stats_rental": self._open_stats_rental,
            # Firmen
            "buy_comp": self._open_buy_comp,
            "sell_comp": self._open_sell_comp,
            "upg_comp": self._open_upg_comp,
            "rename_comp": self._open_rename_comp,
            "stats_comp": self._open_stats_comp,
            # Bank
            "bank_loan": self._open_loan,
            "bank_repay": self._open_repay,
            "bank_savings": self._open_savings,
            "bank_etf": self._open_buy_etf,
            "bank_stocks": self._open_stocks,
            # System
            "save_game": self._save_game,
            "load_game": self._load_game,
            # Erfolge
            "achievements": self._open_achievements,
            # Statistiken
            "stats_overview": self._open_stats_overview,
            "log_view": self._open_log_view,
        }
        action = actions.get(key)
        if action:
            # When opening a modal, ensure scroll is reset
            if isinstance(action, type(lambda: None)):
                # Reset scroll for modal actions
                self._scroll = 0
            action()

    # ── Modal-Öffner ──
    def _open_buy_prop(self):
        self._inputs = {}; self.modal = {"type": "buy_prop"}; self._scroll = 0

    def _open_sell_prop(self):
        self._inputs = {"price": InputBox(0, 0, 200, 34, "Verkaufspreis (€)", True)}
        self.modal = {"type": "sell_prop"}; self._scroll = 0

    def _open_upg_prop(self):
        self._inputs = {}; self.modal = {"type": "upg_prop"}; self._scroll = 0

    def _open_rent_prop(self):
        self._inputs = {}; self.modal = {"type": "rent_prop"}; self._scroll = 0

    def _open_rename_prop(self):
        self._inputs = {"name": InputBox(0, 0, 260, 34, "Neuer Name", False)}
        self.modal = {"type": "rename_prop"}; self._scroll = 0

    def _open_stats_prop(self):
        self._inputs = {}; self.modal = {"type": "stats_prop"}; self._scroll = 0

    def _open_buy_car(self):
        self._inputs = {}; self.modal = {"type": "buy_car"}; self._scroll = 0

    def _open_sell_car(self):
        self._inputs = {"price": InputBox(0, 0, 200, 34, "Verkaufspreis (€)", True)}
        self.modal = {"type": "sell_car"}; self._scroll = 0

    def _open_rent_car(self):
        self._inputs = {}; self.modal = {"type": "rent_car"}; self._scroll = 0

    def _open_upgrade_car(self):
        self._inputs = {}; self.modal = {"type": "upgrade_car"}; self._scroll = 0

    def _open_rename_car(self):
        self._inputs = {"name": InputBox(0, 0, 260, 34, "Neuer Name", False)}
        self.modal = {"type": "rename_car"}; self._scroll = 0

    def _open_stats_car(self):
        self._inputs = {}; self.modal = {"type": "stats_car"}; self._scroll = 0

    def _open_buy_car_rental(self):
        self._inputs = {}; self.modal = {"type": "buy_car_rental"}; self._scroll = 0

    def _open_sell_car_rental(self):
        self._inputs = {"price": InputBox(0, 0, 200, 34, "Verkaufspreis (€)", True)}
        self.modal = {"type": "sell_car_rental"}; self._scroll = 0

    def _open_upgrade_car_rental(self):
        self._inputs = {}; self.modal = {"type": "upgrade_car_rental"}; self._scroll = 0

    def _open_rename_car_rental(self):
        self._inputs = {"name": InputBox(0, 0, 260, 34, "Neuer Name", False)}
        self.modal = {"type": "rename_car_rental"}; self._scroll = 0

    def _open_stats_rental(self):
        self._inputs = {}; self.modal = {"type": "stats_rental"}; self._scroll = 0

    def _open_buy_comp(self):
        self._inputs = {}; self.modal = {"type": "buy_comp"}; self._scroll = 0

    def _open_sell_comp(self):
        self._inputs = {"price": InputBox(0, 0, 200, 34, "Verkaufspreis (€)", True)}
        self.modal = {"type": "sell_comp"}; self._scroll = 0

    def _open_upg_comp(self):
        self._inputs = {}; self.modal = {"type": "upg_comp"}; self._scroll = 0

    def _open_rename_comp(self):
        self._inputs = {"name": InputBox(0, 0, 260, 34, "Neuer Name", False)}
        self.modal = {"type": "rename_comp"}; self._scroll = 0

    def _open_stats_comp(self):
        self._inputs = {}; self.modal = {"type": "stats_comp"}; self._scroll = 0

    def _open_loan(self):
        self._inputs = {"amount": InputBox(0, 0, 220, 34, "Betrag in €")}
        self.modal = {"type": "loan"}

    def _open_repay(self):
        self._inputs = {"amount": InputBox(0, 0, 220, 34, "Betrag in €")}
        self.modal = {"type": "repay"}

    def _open_savings(self):
        self._inputs = {"amount": InputBox(0, 0, 220, 34, "Betrag in €")}
        self.modal = {"type": "savings"}

    def _open_buy_etf(self):
        self._inputs = {"qty": InputBox(0, 0, 180, 34, "Anzahl Anteile")}
        self.modal = {"type": "buy_etf"}

    def _open_stocks(self):
        self._inputs = {}; self.modal = {"type": "stocks"}; self._scroll = 0

    def _open_buy_stock(self, sid):
        self._inputs = {"qty": InputBox(0, 0, 180, 34, "Anzahl Aktien")}
        self.modal = {"type": "buy_stock", "sid": sid}

    def _open_sell_stock(self, sid):
        self._inputs = {"qty": InputBox(0, 0, 180, 34, "Anzahl verkaufen")}
        self.modal = {"type": "sell_stock", "sid": sid}

    def _open_achievements(self):
        self._inputs = {}; self.modal = {"type": "achievements"}; self._scroll = 0

    def _open_stats_overview(self):
        self._inputs = {}; self.modal = {"type": "stats_overview"}; self._scroll = 0

    def _open_log_view(self):
        self._inputs = {}; self.modal = {"type": "log_view"}; self._scroll = 0

    def _open_dashboard(self):
        self._content_key = "dashboard"
        self._scroll = 0

    def _close_modal(self):
        self.modal = None; self._inputs = {}

    # ── Spiel speichern/laden ──
    def _save_game(self):
        gs = self.gs
        data = {
            "difficulty": gs.difficulty, "name": gs.name,
            "cash": gs.cash, "loan": gs.loan, "savings": gs.savings,
            "props": gs.props, "comps": gs.comps, "cars": gs.cars,
            "car_rentals": gs.car_rentals, "stocks": gs.stocks,
            "etf": gs.etf,
            "month": gs.month, "year": gs.year,
            "phase": gs.phase, "phase_dur": gs.phase_dur,
            "base_rate": gs.base_rate, "inflation": gs.inflation,
            "gdp": gs.gdp, "unemp": gs.unemp, "sentiment": gs.sentiment,
            "reputation": gs.reputation,
            "local_demand": gs.local_demand, "competition": gs.competition,
            "market_trend": gs.market_trend,
            "achiev_done": list(gs.achiev_done),
            "nw_hist": gs.nw_hist, "cf_hist": gs.cf_hist,
            "_survived_dep_count": gs._survived_dep_count,
        }
        try:
            with open("savegame_v5.json", "w") as f:
                json.dump(data, f, indent=2)
            gs.add_log("Spiel erfolgreich gespeichert!", "good")
        except Exception as e:
            gs.add_log(f"Speicherfehler: {e}", "bad")
        self._close_modal()

    def _load_game(self):
        try:
            with open("savegame_v5.json", "r") as f:
                data = json.load(f)
            gs = self.gs
            gs.difficulty = data.get("difficulty", "medium")
            gs.name = data["name"]
            gs.cash = data["cash"]; gs.loan = data["loan"]
            gs.savings = data["savings"]
            gs.props = data["props"]; gs.comps = data["comps"]
            gs.cars = data.get("cars", []); gs.car_rentals = data.get("car_rentals", [])
            gs.stocks = data["stocks"]; gs.etf = data["etf"]
            gs.month = data["month"]; gs.year = data["year"]
            gs.phase = data["phase"]; gs.phase_dur = data["phase_dur"]
            gs.base_rate = data["base_rate"]; gs.inflation = data["inflation"]
            gs.gdp = data["gdp"]; gs.unemp = data["unemp"]
            gs.sentiment = data["sentiment"]; gs.reputation = data["reputation"]
            gs.local_demand = data.get("local_demand", 1.0)
            gs.competition = data.get("competition", 0.3)
            gs.market_trend = data.get("market_trend", 0.0)
            gs.achiev_done = set(data["achiev_done"])
            gs.nw_hist = data["nw_hist"]; gs.cf_hist = data["cf_hist"]
            gs._survived_dep_count = data.get("_survived_dep_count", 0)
            gs.add_log(f"Spielstand geladen: {gs.year}, Monat {gs.month}", "info")
        except FileNotFoundError:
            self.gs.add_log("Kein Speicherstand gefunden!", "bad")
        except Exception as e:
            self.gs.add_log(f"Ladefehler: {e}", "bad")
        self._close_modal()

    # ── Modal-Klick-Handler ──
    def _handle_modal_click(self, mx, my):
        """Handle mouse clicks when a modal is open.

        The modal size adapts to the current window dimensions (``W`` and ``H``).
        Previously the function only checked the close‑button and then processed
        the rest of the modal actions without verifying that the click was
        actually inside the modal rectangle. After resizing the window this
        could cause clicks outside the visible modal to be interpreted as
        interactions with modal elements, leading to layout mis‑alignment.
        The updated implementation first computes the modal rectangle and
        returns early if the click lies outside it.
        """
        mt = self.modal.get("type", "")
        # Modal size is dynamic (see _draw_modal)
        max_w, max_h = 760, 560
        mw = min(max_w, max(200, W - 80))
        mh = min(max_h, max(200, H - 120))
        bx = (W - mw) // 2
        by = (H - mh) // 2

        # Full modal rectangle for hit‑testing
        modal_rect = pygame.Rect(bx, by, mw, mh)
        if not modal_rect.collidepoint(mx, my):
            # Click outside the modal – ignore it
            return None

        # Close‑button (same coordinates as in _draw_modal)
        close_rect = pygame.Rect(bx + mw - 32, by + 6, 24, 24)
        if close_rect.collidepoint(mx, my):
            self._close_modal()
            return None

        gs = self.gs

        # ── Immobilien kaufen ──
        if mt == "buy_prop":
            row_h = 72
            for i, row in enumerate(PROP_CATALOG):
                ry = i * row_h - self._scroll
                if ry + row_h < 0 or ry > mh - 65:
                    continue
                if pygame.Rect(bx + mw - 112, by + 55 + ry + 20, 90, 30).collidepoint(mx, my):
                    price = float(row[3])
                    if gs.cash >= price:
                        gs.cash -= price
                        gs.props.append(make_prop(row))
                        gs.add_log(f"Immobilie gekauft: {row[1]} ({fmt(price)})", "good")
                    self._close_modal()
                    return None

        # ── Immobilien verkaufen ──
        elif mt == "sell_prop":
            row_h = 80
            ib = self._inputs.get("price")
            for i, p in enumerate(gs.props):
                ry = i * row_h - self._scroll
                if ry + row_h < 0 or ry > mh - 60:
                    continue
                if p.get("for_sale"):
                    if pygame.Rect(bx + mw - 128, by + 50 + ry + 14, 110, 28).collidepoint(mx, my):
                        p["for_sale"] = False
                        p["sale_price"] = 0
                        p["months_on_market"] = 0
                        gs.add_log(f"Verkauf von {gs.name_of(p)} abgebrochen", "info")
                        self._close_modal()
                        return None
                else:
                    if ib:
                        ib.rect = pygame.Rect(bx + 18, by + 50 + ry + 44, 140, 28)
                    if pygame.Rect(bx + mw - 128, by + 50 + ry + 14, 110, 28).collidepoint(mx, my):
                        sale_price = ib.val() if ib else 0
                        if sale_price > 0:
                            # Marktwert berechnen
                            mw_val = calc_market_value(
                                p["purchase_price"], p.get("months_held", 0),
                                gs.phase, gs.local_demand, p.get("condition", 0.9)
                            )
                            chance, msg_key = calc_buy_chance(sale_price, mw_val, gs)
                            msg = get_price_message(msg_key)
                            p["for_sale"] = True
                            p["sale_price"] = sale_price
                            p["months_on_market"] = 0
                            gs.add_log(f"{gs.name_of(p)} für {fmt(sale_price)} angeboten", "info")
                            gs.add_market_msg(f"{gs.name_of(p)}: {msg}")
                            if chance >= 0.75:
                                gs.add_log("Marktlage: Heiß begehrt!", "good")
                            elif chance < 0.08:
                                gs.add_log("Warnung: Preis zu hoch für Marktlage!", "bad")
                        self._close_modal()
                        return None

        # ── Immobilien renovieren ──
        elif mt == "upg_prop":
            row_h = 72
            for i, p in enumerate(gs.props):
                ry = i * row_h - self._scroll
                if ry + row_h < 0 or ry > mh - 60:
                    continue
                cost = p["price"] * 0.12
                maxed = p["level"] >= p["lvl_max"]
                if not maxed and pygame.Rect(bx + mw - 112, by + 50 + ry + 22, 90, 28).collidepoint(mx, my):
                    if gs.cash >= cost and not p.get("for_sale"):
                        gs.cash -= cost
                        p["level"] += 1
                        p["price"] *= 1.08
                        p["base_rent"] *= 1.12
                        p["rent"] *= 1.12
                        p["maint"] *= 1.05
                        p["condition"] = min(1.0, p.get("condition", 1.0) + 0.1)
                        gs.add_log(f"Renoviert: {gs.name_of(p)} → Level {p['level']}", "good")
                    self._close_modal()
                    return None

        # ── Immobilien vermieten ──
        elif mt == "rent_prop":
            row_h = 100
            for i, p in enumerate(gs.props):
                ry = i * row_h - self._scroll
                if ry + row_h < 0 or ry > mh - 64:
                    continue
                btn_rect = pygame.Rect(bx + mw - 128, by + 54 + ry + 20, 108, 30)
                if p.get("vacant") and not p.get("listed") and not p.get("for_sale"):
                    if btn_rect.collidepoint(mx, my):
                        p["listed"] = True
                        gs.add_log(f"{gs.name_of(p)} auf Mietmarkt angeboten", "info")
                        self._close_modal(); return None
                elif not p.get("vacant") and not p.get("for_sale"):
                    if btn_rect.collidepoint(mx, my):
                        tname = TENANT_TYPES[p["tenant"]][0] if p["tenant"] is not None else "Mieter"
                        penalty = p.get("rent", 0) * 2
                        p["tenant"] = None; p["vacant"] = True; p["listed"] = False
                        p["contract_left"] = 0
                        gs.cash -= penalty
                        gs.add_log(f"{tname} rausgekündigt: -{fmt(penalty)}", "bad")
                        self._close_modal(); return None
                elif p.get("vacant") and p.get("listed") and not p.get("for_sale"):
                    if btn_rect.collidepoint(mx, my):
                        p["listed"] = False
                        gs.add_log(f"{gs.name_of(p)} vom Markt genommen", "info")
                        self._close_modal(); return None

        # ── Immobilie umbenennen ──
        elif mt == "rename_prop":
            ib = self._inputs.get("name")
            if ib:
                ib.rect = pygame.Rect(bx + 30, by + 60, 260, 34)
            row_h = 50
            for i, p in enumerate(gs.props):
                ry = i * row_h - self._scroll
                if ry + row_h < 0 or ry > mh - 130:
                    continue
                if pygame.Rect(bx + mw - 130, by + 120 + ry + 10, 110, 28).collidepoint(mx, my):
                    new_name = ib.text.strip() if ib else ""
                    if new_name:
                        p["custom_name"] = new_name
                        gs.add_log(f"Immobilie umbenannt: {new_name}", "info")
                    self._close_modal(); return None

        # ── Unternehmen kaufen ──
        elif mt == "buy_comp":
            row_h = 72
            for i, row in enumerate(COMP_CATALOG):
                ry = i * row_h - self._scroll
                if ry + row_h < 0 or ry > mh - 65:
                    continue
                if pygame.Rect(bx + mw - 112, by + 55 + ry + 20, 90, 30).collidepoint(mx, my):
                    price = float(row[3])
                    if gs.cash >= price:
                        gs.cash -= price
                        gs.comps.append(make_comp(row))
                        gs.add_log(f"Firma gegründet: {row[1]} ({fmt(price)})", "good")
                    self._close_modal(); return None

        # ── Unternehmen verkaufen ──
        elif mt == "sell_comp":
            row_h = 80
            ib = self._inputs.get("price")
            for i, c in enumerate(gs.comps):
                ry = i * row_h - self._scroll
                if ry + row_h < 0 or ry > mh - 60:
                    continue
                if c.get("for_sale"):
                    if pygame.Rect(bx + mw - 128, by + 50 + ry + 14, 110, 28).collidepoint(mx, my):
                        c["for_sale"] = False; c["sale_price"] = 0; c["months_on_market"] = 0
                        gs.add_log(f"Verkauf von {gs.name_of(c)} abgebrochen", "info")
                        self._close_modal(); return None
                else:
                    if ib:
                        ib.rect = pygame.Rect(bx + 18, by + 50 + ry + 44, 140, 28)
                    if pygame.Rect(bx + mw - 128, by + 50 + ry + 14, 110, 28).collidepoint(mx, my):
                        sp = ib.val() if ib else 0
                        if sp > 0:
                            c["for_sale"] = True; c["sale_price"] = sp; c["months_on_market"] = 0
                            gs.add_log(f"{gs.name_of(c)} für {fmt(sp)} angeboten", "info")
                        self._close_modal(); return None

        # ── Unternehmen erweitern ──
        elif mt == "upg_comp":
            row_h = 72
            for i, c in enumerate(gs.comps):
                ry = i * row_h - self._scroll
                if ry + row_h < 0 or ry > mh - 60:
                    continue
                cost = c["val"] * 0.15
                maxed = c["level"] >= c["lvl_max"]
                if not maxed and pygame.Rect(bx + mw - 112, by + 50 + ry + 22, 90, 28).collidepoint(mx, my):
                    if gs.cash >= cost and not c.get("for_sale"):
                        gs.cash -= cost; c["level"] += 1
                        c["val"] *= 1.12; c["base_profit"] *= 1.20
                        c["profit"] = c["base_profit"]; c["maint"] *= 1.08
                        gs.add_log(f"Firma erweitert: {gs.name_of(c)} Level {c['level']}", "good")
                    self._close_modal(); return None

        # ── Unternehmen umbenennen ──
        elif mt == "rename_comp":
            ib = self._inputs.get("name")
            if ib:
                ib.rect = pygame.Rect(bx + 30, by + 60, 260, 34)
            row_h = 50
            for i, c in enumerate(gs.comps):
                ry = i * row_h - self._scroll
                if ry + row_h < 0 or ry > mh - 130:
                    continue
                if pygame.Rect(bx + mw - 130, by + 120 + ry + 10, 110, 28).collidepoint(mx, my):
                    new = ib.text.strip() if ib else ""
                    if new:
                        c["custom_name"] = new
                        gs.add_log(f"Firma umbenannt: {new}", "info")
                    self._close_modal(); return None

        # ── Auto kaufen ──
        elif mt == "buy_car":
            row_h = 72
            for i, row in enumerate(CAR_CATALOG):
                ry = i * row_h - self._scroll
                if ry + row_h < 0 or ry > mh - 65:
                    continue
                if pygame.Rect(bx + mw - 112, by + 55 + ry + 20, 90, 30).collidepoint(mx, my):
                    price = float(row[3])
                    if gs.cash >= price:
                        gs.cash -= price; gs.cars.append(make_car(row))
                        gs.add_log(f"Auto gekauft: {row[1]} ({fmt(price)})", "good")
                    self._close_modal(); return None

        # ── Auto verkaufen ──
        elif mt == "sell_car":
            row_h = 80
            ib = self._inputs.get("price")
            for i, car in enumerate(gs.cars):
                ry = i * row_h - self._scroll
                if ry + row_h < 0 or ry > mh - 60:
                    continue
                if car.get("for_sale"):
                    if pygame.Rect(bx + mw - 128, by + 50 + ry + 14, 110, 28).collidepoint(mx, my):
                        car["for_sale"] = False; car["sale_price"] = 0; car["months_on_market"] = 0
                        gs.add_log(f"Verkauf von {gs.name_of(car)} abgebrochen", "info")
                        self._close_modal(); return None
                else:
                    if ib:
                        ib.rect = pygame.Rect(bx + 18, by + 50 + ry + 44, 140, 28)
                    if pygame.Rect(bx + mw - 128, by + 50 + ry + 14, 110, 28).collidepoint(mx, my):
                        sp = ib.val() if ib else 0
                        if sp > 0:
                            car["for_sale"] = True; car["sale_price"] = sp; car["months_on_market"] = 0
                            gs.add_log(f"{gs.name_of(car)} für {fmt(sp)} angeboten", "info")
                        self._close_modal(); return None

        # ── Auto tunen ──
        elif mt == "upgrade_car":
            row_h = 72
            for i, car in enumerate(gs.cars):
                ry = i * row_h - self._scroll
                if ry + row_h < 0 or ry > mh - 60:
                    continue
                cost = car["price"] * 0.15
                maxed = car["level"] >= car["lvl_max"]
                if not maxed and pygame.Rect(bx + mw - 112, by + 50 + ry + 22, 90, 28).collidepoint(mx, my):
                    if gs.cash >= cost and not car.get("for_sale"):
                        gs.cash -= cost; car["level"] += 1
                        car["price"] *= 1.10; car["base_rental"] *= 1.15
                        car["rental"] = car["base_rental"]; car["maint"] *= 1.07
                        car["condition"] = min(1.0, car.get("condition", 1.0) + 0.08)
                        gs.add_log(f"Auto getunt: {gs.name_of(car)} Level {car['level']}", "good")
                    self._close_modal(); return None

        # ── Auto vermieten ──
        elif mt == "rent_car":
            row_h = 72
            for i, car in enumerate(gs.cars):
                ry = i * row_h - self._scroll
                if ry + row_h < 0 or ry > mh - 65:
                    continue
                btn = pygame.Rect(bx + mw - 128, by + 55 + ry + 20, 108, 30)
                if not car.get("for_sale") and btn.collidepoint(mx, my):
                    if car.get("rented"):
                        car["rented"] = False; car["rental_customer"] = None
                        car["contract_left"] = 0
                        gs.add_log(f"{gs.name_of(car)}: Mieter gekündigt", "warn")
                    self._close_modal(); return None

        # ── Auto umbenennen ──
        elif mt == "rename_car":
            ib = self._inputs.get("name")
            if ib:
                ib.rect = pygame.Rect(bx + 30, by + 60, 260, 34)
            row_h = 50
            for i, car in enumerate(gs.cars):
                ry = i * row_h - self._scroll
                if ry + row_h < 0 or ry > mh - 110:
                    continue
                if pygame.Rect(bx + mw - 130, by + 100 + ry + 10, 110, 28).collidepoint(mx, my):
                    new = ib.text.strip() if ib else ""
                    if new:
                        car["custom_name"] = new
                        gs.add_log(f"Auto umbenannt: {new}", "info")
                    self._close_modal(); return None

        # ── Autovermietung kaufen ──
        elif mt == "buy_car_rental":
            row_h = 72
            for i, row in enumerate(CAR_RENTAL_CATALOG):
                ry = i * row_h - self._scroll
                if ry + row_h < 0 or ry > mh - 65:
                    continue
                if pygame.Rect(bx + mw - 112, by + 55 + ry + 20, 90, 30).collidepoint(mx, my):
                    price = float(row[3])
                    if gs.cash >= price:
                        gs.cash -= price; gs.car_rentals.append(make_car_rental(row))
                        gs.add_log(f"Vermietung gegründet: {row[1]} ({fmt(price)})", "good")
                    self._close_modal(); return None

        # ── Autovermietung verkaufen ──
        elif mt == "sell_car_rental":
            row_h = 80; ib = self._inputs.get("price")
            for i, cr in enumerate(gs.car_rentals):
                ry = i * row_h - self._scroll
                if ry + row_h < 0 or ry > mh - 60:
                    continue
                if cr.get("for_sale"):
                    if pygame.Rect(bx + mw - 128, by + 50 + ry + 14, 110, 28).collidepoint(mx, my):
                        cr["for_sale"] = False; cr["sale_price"] = 0; cr["months_on_market"] = 0
                        gs.add_log(f"Verkauf von {gs.name_of(cr)} abgebrochen", "info")
                        self._close_modal(); return None
                else:
                    if ib:
                        ib.rect = pygame.Rect(bx + 18, by + 50 + ry + 44, 140, 28)
                    if pygame.Rect(bx + mw - 128, by + 50 + ry + 14, 110, 28).collidepoint(mx, my):
                        sp = ib.val() if ib else 0
                        if sp > 0:
                            cr["for_sale"] = True; cr["sale_price"] = sp; cr["months_on_market"] = 0
                            gs.add_log(f"{gs.name_of(cr)} für {fmt(sp)} angeboten", "info")
                        self._close_modal(); return None

        # ── Autovermietung erweitern ──
        elif mt == "upgrade_car_rental":
            row_h = 72
            for i, cr in enumerate(gs.car_rentals):
                ry = i * row_h - self._scroll
                if ry + row_h < 0 or ry > mh - 60:
                    continue
                cost = cr["val"] * 0.15; maxed = cr["level"] >= cr["lvl_max"]
                if not maxed and pygame.Rect(bx + mw - 112, by + 50 + ry + 22, 90, 28).collidepoint(mx, my):
                    if gs.cash >= cost and not cr.get("for_sale"):
                        gs.cash -= cost; cr["level"] += 1
                        cr["val"] *= 1.12; cr["base_profit"] *= 1.20
                        cr["profit"] = cr["base_profit"]; cr["maint"] *= 1.08
                        gs.add_log(f"Vermietung erweitert: {gs.name_of(cr)} Level {cr['level']}", "good")
                    self._close_modal(); return None

        # ── Bank: Kredit ──
        elif mt == "loan":
            ib = self._inputs.get("amount")
            if ib:
                ib.rect = pygame.Rect(bx + 30, by + 128, 220, 34)
            if pygame.Rect(bx + 260, by + 128, 120, 34).collidepoint(mx, my):
                amt = ib.val() if ib else 0
                max_l = max(0, gs.net_worth() * 0.4 - gs.loan)
                if 0 < amt <= max_l:
                    gs.cash += amt; gs.loan += amt
                    gs.add_log(f"Kredit aufgenommen: +{fmt(amt)}", "warn")
                self._close_modal(); return None

        # ── Bank: Tilgung ──
        elif mt == "repay":
            ib = self._inputs.get("amount")
            if ib:
                ib.rect = pygame.Rect(bx + 30, by + 128, 220, 34)
            if pygame.Rect(bx + 260, by + 128, 120, 34).collidepoint(mx, my):
                amt = min(ib.val() if ib else 0, gs.cash, gs.loan)
                if amt > 0:
                    gs.cash -= amt; gs.loan = max(0, gs.loan - amt)
                    gs.add_log(f"Kredit getilgt: -{fmt(amt)}", "good")
                self._close_modal(); return None
            if pygame.Rect(bx + 30, by + 180, 160, 34).collidepoint(mx, my):
                amt = min(gs.cash, gs.loan)
                if amt > 0:
                    gs.cash -= amt; gs.loan = max(0, gs.loan - amt)
                    gs.add_log(f"Alle Schulden getilgt: -{fmt(amt)}", "good")
                self._close_modal(); return None

        # ── Bank: Festgeld ──
        elif mt == "savings":
            ib = self._inputs.get("amount")
            if ib:
                ib.rect = pygame.Rect(bx + 30, by + 128, 220, 34)
            if pygame.Rect(bx + 260, by + 128, 120, 34).collidepoint(mx, my):
                amt = ib.val() if ib else 0
                if 0 < amt <= gs.cash:
                    gs.cash -= amt; gs.savings += amt
                    gs.add_log(f"Festgeld eingelegt: {fmt(amt)}", "info")
                self._close_modal(); return None
            if pygame.Rect(bx + 30, by + 180, 160, 34).collidepoint(mx, my):
                if gs.savings > 0:
                    gs.cash += gs.savings
                    gs.add_log(f"Festgeld ausgezahlt: {fmt(gs.savings)}", "info")
                    gs.savings = 0
                self._close_modal(); return None

        # ── Aktien kaufen ──
        elif mt == "buy_stock":
            sid = self.modal["sid"]
            ib = self._inputs.get("qty")
            if ib:
                ib.rect = pygame.Rect(bx + 30, by + 130, 180, 34)
            if pygame.Rect(bx + 220, by + 130, 110, 34).collidepoint(mx, my):
                qty = int(ib.val() if ib else 0)
                cost = qty * gs.stock_data[sid]["price"]
                if qty > 0 and gs.cash >= cost:
                    gs.cash -= cost
                    gs.stocks[sid] = gs.stocks.get(sid, 0.0) + qty
                    gs.add_log(f"Aktie gekauft: {qty}x {gs.stock_data[sid]['name']}", "good")
                self._close_modal(); return None

        # ── Aktien verkaufen ──
        elif mt == "sell_stock":
            sid = self.modal["sid"]
            ib = self._inputs.get("qty")
            if ib:
                ib.rect = pygame.Rect(bx + 30, by + 130, 180, 34)
            if pygame.Rect(bx + 220, by + 130, 110, 34).collidepoint(mx, my):
                qty = min(int(ib.val() if ib else 0), int(gs.stocks.get(sid, 0.0)))
                if qty > 0:
                    proceeds = qty * gs.stock_data[sid]["price"]
                    gs.cash += proceeds
                    gs.stocks[sid] = gs.stocks.get(sid, 0.0) - qty
                    gs.add_log(f"Aktie verkauft: {qty}x {gs.stock_data[sid]['name']}", "info")
                self._close_modal(); return None
            if pygame.Rect(bx + 30, by + 180, 160, 34).collidepoint(mx, my):
                owned = gs.stocks.get(sid, 0.0)
                if owned > 0:
                    proceeds = owned * gs.stock_data[sid]["price"]
                    gs.cash += proceeds
                    gs.stocks[sid] = 0
                    gs.add_log(f"Alle {gs.stock_data[sid]['name']} verkauft: +{fmt(proceeds)}", "info")
                self._close_modal(); return None

        # ── ETF kaufen ──
        elif mt == "buy_etf":
            ib = self._inputs.get("qty")
            if ib:
                ib.rect = pygame.Rect(bx + 30, by + 130, 180, 34)
            if pygame.Rect(bx + 220, by + 130, 110, 34).collidepoint(mx, my):
                qty = ib.val() if ib else 0
                cost = qty * gs.etf_price
                if qty > 0 and gs.cash >= cost:
                    gs.cash -= cost; gs.etf += qty
                    gs.add_log(f"ETF gekauft: {qty:.1f} Anteile ({fmt(cost)})", "good")
                self._close_modal(); return None
            if pygame.Rect(bx + 30, by + 180, 160, 34).collidepoint(mx, my):
                if gs.etf > 0:
                    proceeds = gs.etf * gs.etf_price
                    gs.cash += proceeds
                    gs.add_log(f"Alle ETF-Anteile verkauft: +{fmt(proceeds)}", "info")
                    gs.etf = 0
                self._close_modal(); return None

        # ── Aktien-Markt-Übersicht ──
        elif mt == "stocks":
            self._close_modal(); return None

        # ── Statistik/Log-Modals: einfach schließen ──
        elif mt in ("stats_prop", "stats_car", "stats_rental",
                    "stats_comp", "stats_overview", "log_view"):
            self._close_modal(); return None

        # ── Erfolge: Kategorien & Karten anklickbar ──
        elif mt == "achievements":
            # 1) Prüfe Kategorie-Klicks (linke Spalte)
            if hasattr(self, '_ach_cat_rects'):
                for cat_id, cat_rect in self._ach_cat_rects:
                    if cat_rect.collidepoint(mx, my):
                        self._ach_selected_cat = cat_id
                        self._ach_scroll = 0
                        return None

            # 2) Prüfe Achievement-Karten-Klicks (mittlere Spalte)
            if hasattr(self, '_ach_card_rects'):
                for aid, info, prefix, is_earned, card_rect in self._ach_card_rects:
                    if card_rect.collidepoint(mx, my):
                        self._ach_detail_target = (aid, info, prefix, is_earned)
                        return None

            # 3) Kein Treffer → Modal bleibt offen (nicht schließen)
            return None

        return None

    # ═══════════════════════════════════════════════════════
    #  ZEICHNEN
    # ═══════════════════════════════════════════════════════
    def draw(self):
        screen.fill(BG)
        self._draw_topbar()
        self.nav.draw(screen, 0, 44, H - 44 - 20)
        self._draw_content()
        self._draw_newsbar()
        self._draw_market_msgs()

        if self.modal:
            dim_overlay(screen)
            self._draw_modal()

        if self._ach_popup:
            self._draw_ach_popup()

    def _draw_topbar(self):
        gs = self.gs
        box(screen, PANEL, (0, 0, W, 44))
        line(screen, BORDER, (0, 44), (W, 44))
        txt(screen, f"Business Tycoon V5 [{DIFFICULTY[gs.difficulty]['label']}]",
            "lg", GOLD, 200 + 10, 22, "midleft")

        stats = [
            ("Bargeld", fmt(gs.cash), gs.cash >= 0),
            ("Nettoverm.", fmt(gs.net_worth()), True),
            (f"{gs.month:02d}.{gs.year}", "", True),
            ("Schulden", fmt(gs.loan), gs.loan == 0),
            ("Ruf", str(int(gs.reputation)), gs.reputation >= 50),
        ]
        x = 320
        for label, val, good in stats:
            if not val:
                txt(screen, label, "sm", CYAN, x + 50, 22, "center")
                x += 100
                continue
            box(screen, PANEL2, (x, 6, 120, 32), 16)
            txt(screen, f"{label}:", "xs", MUTED, x + 8, 22, "midleft")
            txt(screen, val, "sm", GREEN if good else RED, x + 112, 22, "midright")
            x += 128

        # Geschwindigkeits-Buttons
        for i, (ms, lbl) in enumerate([(2000, "1x"), (800, "3x"), (300, "10x")]):
            r = pygame.Rect(W - 240 + i * 44, 9, 38, 26)
            c = ACCENT if self.speed == ms else PANEL2
            box(screen, c, r, 6)
            box(screen, BORDER, r, 6, 1)
            txt(screen, lbl, "sm", WHITE, r.centerx, r.centery, "center")

        pr = pygame.Rect(W - 100, 9, 88, 26)
        pc = GREEN if not self.paused else YELLOW
        box(screen, pc, pr, 13)
        txt(screen, "Pause" if not self.paused else "Weiter", "sm", BG,
            pr.centerx, pr.centery, "center")

    def _draw_content(self):
        """Zeichne den Haupt-Content-Bereich basierend auf _content_key."""
        x = self.nav.width + 4
        y = 48
        w = W - x - 4
        h = H - y - 24

        gs = self.gs
        pad = 10

        if self._content_key == "dashboard":
            self._draw_dashboard(x, y, w, h)
        elif self._content_key == "achievements":
            self._draw_achievements_view(x, y, w, h)
        elif self._content_key == "log_view":
            self._draw_log_view(x, y, w, h)
        elif self._content_key == "stats_overview":
            self._draw_stats_overview(x, y, w, h)
        elif self._content_key.startswith("settings"):
            self._draw_settings(x, y, w, h)
        else:
            # Standard-Dashboard wenn keine spezifische View
            self._draw_dashboard(x, y, w, h)

    def _draw_dashboard(self, x, y, w, h):
        gs = self.gs
        pad = 10
        cw = (w - pad * 4) // 3
        ch2 = 90

        tiles = [
            ("Bargeld", fmt(gs.cash), gs.cash >= 0),
            ("Nettovermögen", fmt(gs.net_worth()), True),
            ("Immobilien", f"{len(gs.props)} Objekte", True),
            ("Autos", f"{len(gs.cars)} Fahrzeuge", True),
            ("Autovermietung", f"{len(gs.car_rentals)} Filialen", True),
            ("Unternehmen", f"{len(gs.comps)} Firmen", True),
            ("Monat. Einnahmen", fmt(gs.monthly_income()), True),
            ("Monat. Ausgaben", fmt(gs.monthly_expenses()), False),
        ]

        for i, (label, val, good) in enumerate(tiles):
            row, ci = divmod(i, 3)
            tx = x + pad + ci * (cw + pad)
            ty = y + pad + row * (ch2 + pad)
            box(screen, PANEL2, (tx, ty, cw, ch2), 8)
            box(screen, BORDER, (tx, ty, cw, ch2), 8, 1)
            txt(screen, label, "xs", MUTED, tx + 10, ty + 12)
            txt(screen, val, "lg", GREEN if good else RED, tx + 10, ty + 42)

        # Wirtschaftsphase
        ph = PHASES[gs.phase]
        py = y + pad + 2 * (ch2 + pad) + 8
        box(screen, PANEL2, (x + pad, py, w - pad * 2, 50), 8)
        pygame.draw.rect(screen, ph["col"], (x + pad, py, 5, 50), 2)
        txt(screen, "Wirtschaft:", "xs", MUTED, x + pad + 14, py + 6)
        txt(screen, ph["label"], "xl", ph["col"], x + pad + 14, py + 26)
        txt(screen, f"Verbleibend: ~{gs.phase_dur} Monate", "xs", MUTED,
             x + w - pad - 120, py + 26)

        # Sparkline
        chart_y = py + 58
        chart_h = h - (chart_y - y) - 10
        if chart_h > 50 and len(gs.nw_hist) >= 2:
            box(screen, PANEL2, (x + pad, chart_y, w - pad * 2, chart_h), 8)
            box(screen, BORDER, (x + pad, chart_y, w - pad * 2, chart_h), 8, 1)
            txt(screen, "Nettovermögen (24 Monate)", "xs", MUTED, x + pad + 10, chart_y + 8)
            sparkline(screen, gs.nw_hist, x + pad + 10, chart_y + 24,
                      w - pad * 2 - 20, chart_h - 36, CYAN)

    def _draw_achievements_view(self, x, y, w, h):
        gs = self.gs
        total = gs.get_total_achievements()
        earned = gs.get_earned_achievements()
        txt(screen, f"Erfolge {earned} / {total}", "xl", GOLD, x + 16, y + 10)

        # Alle Kategorien anzeigen
        all_categories = [
            ("Immobilien", ACHIEV_IMMO, "immo"),
            ("Autos", ACHIEV_CARS, "cars"),
            ("Autovermietung", ACHIEV_FILIALEN, "filialen"),
            ("Unternehmen", ACHIEV_FIRMEN, "firmen"),
            ("Vermögen", ACHIEV_VERMOEGEN, "vermoegen"),
        ]

        cat_y = y + 40
        for cat_name, cat_data, prefix in all_categories:
            txt(screen, cat_name, "md", ACCENT, x + 16, cat_y)
            cat_y += 20
            for tier, info in cat_data.items():
                aid = f"{prefix}_{tier}"
                earned_flag = aid in gs.achiev_done
                col = GREEN if earned_flag else MUTED
                icon = "✓" if earned_flag else "○"
                txt(screen, f"  {icon} {info['title']}: {info['desc']}", "xs",
                    col, x + 20, cat_y)
                cat_y += 16
            cat_y += 6

        # Spezial-Achievements
        txt(screen, "Spezial-Erfolge", "md", GOLD, x + 16, cat_y + 10)
        cat_y += 30
        shown = 0
        for aid, title, desc, _ in ACHIEV_SPECIAL:
            if cat_y + 16 < y + h - 20:
                earned_flag = aid in gs.achiev_done
                col = GREEN if earned_flag else MUTED
                icon = "✓" if earned_flag else "○"
                txt(screen, f"  {icon} {title}: {desc}", "xs", col, x + 20, cat_y)
                cat_y += 16
                shown += 1

    def _draw_log_view(self, x, y, w, h):
        gs = self.gs
        txt(screen, "Aktivitätslog", "xl", GOLD, x + 16, y + 10)
        kind_col = {"good": GREEN, "bad": RED, "warn": YELLOW, "info": CYAN}
        row_h = 22
        max_rows = (h - 30) // row_h
        for i, (msg, kind) in enumerate(gs.log[:max_rows]):
            ly = y + 38 + i * row_h
            col = kind_col.get(kind, MUTED)
            pygame.draw.rect(screen, col, (x + 12, ly + 4, 3, 14))
            txt(screen, msg, "sm", WHITE, x + 22, ly + 11, "midleft", w - 40)

    def _draw_stats_overview(self, x, y, w, h):
        gs = self.gs
        txt(screen, "Statistiken", "xl", GOLD, x + 16, y + 10)

        stats_data = [
            ("Spielzeit", f"{(gs.year - 2024)} Jahre, {gs.month} Monate"),
            ("Bargeld", fmt(gs.cash)),
            ("Nettovermögen", fmt(gs.net_worth())),
            ("Monatlicher Cashflow", fmt(gs.net_monthly())),
            ("Immobilien", str(len(gs.props))),
            ("Unternehmen", str(len(gs.comps))),
            ("Autos", str(len(gs.cars))),
            ("Autovermietungen", str(len(gs.car_rentals))),
            ("Aktienportfolio", fmt(gs.stock_value())),
            ("Festgeld", fmt(gs.savings)),
            ("Schulden", fmt(gs.loan)),
            ("Reputation", str(int(gs.reputation))),
            ("Lokale Nachfrage", f"{gs.local_demand:.2f}"),
            ("Konkurrenz", f"{gs.competition:.2f}"),
            ("Markttrend", f"{gs.market_trend:+.3f}"),
            ("Wirtschaftsphase", PHASES[gs.phase]["label"]),
            ("Leitzins", f"{gs.base_rate:.2f}%"),
            ("Inflation", f"{gs.inflation * 100:.2f}%"),
            ("Arbeitslosigkeit", f"{gs.unemp:.1f}%"),
            ("Stimmung", f"{int(gs.sentiment)}/100"),
        ]

        sy = y + 40
        col_w = (w - 40) // 2
        for i, (label, val) in enumerate(stats_data):
            sx = x + 20 + (i % 2) * col_w
            sy2 = sy + (i // 2) * 20
            if sy2 < y + h - 20:
                txt(screen, f"{label}:", "sm", MUTED, sx, sy2)
                txt(screen, val, "sm", WHITE, sx + 180, sy2)

    def _draw_settings(self, x, y, w, h):
        txt(screen, "Einstellungen", "xl", GOLD, x + 16, y + 10)
        txt(screen, "Einstellungen sind im Spiel integriert.", "md", MUTED, x + 16, y + 50)
        txt(screen, "• Schwierigkeitsgrad beim Start wählbar", "sm", WHITE, x + 16, y + 80)
        txt(screen, "• Geschwindigkeit: 1x / 3x / 10x über Topbar", "sm", WHITE, x + 16, y + 104)
        txt(screen, "• Pause: Leertaste oder Klick auf Pause-Button", "sm", WHITE, x + 16, y + 128)
        txt(screen, "• Fenstergröße: Ziehen am Rand zum Anpassen", "sm", WHITE, x + 16, y + 152)

    def _draw_newsbar(self):
        box(screen, PANEL, (0, H - 20, W, 20))
        line(screen, BORDER, (0, H - 20), (W, H - 20))
        gs = self.gs
        news_str = "  //  ".join(gs.news[:5]) if gs.news else "Willkommen bei Business Tycoon Pro V5!"
        # Laufender Text
        scroll = getattr(self, "_news_scroll", 0)
        self._news_scroll = scroll - 1.2
        txt(screen, news_str, "sm", MUTED, int(self._news_scroll), H - 10, "midleft")

    def _draw_market_msgs(self):
        gs = self.gs
        now = pygame.time.get_ticks()
        y_start = H - 48
        x_start = self.nav.width + 10
        gs.market_messages = [(m, t) for m, t in gs.market_messages if now - t < 4000]
        for i, (msg, t) in enumerate(reversed(gs.market_messages)):
            alpha = 255 if now - t < 3000 else int(255 * (1 - (now - t - 3000) / 1000))
            if alpha <= 0:
                continue
            f = F["xs"]
            txt_surf = f.render(msg, True, (255, 255, 255))
            txt_surf.set_alpha(alpha)
            screen.blit(txt_surf, (x_start, y_start - i * 14))

    # ═══════════════════════════════════════════════════════
    #  MODAL ZEICHNEN
    # ═══════════════════════════════════════════════════════
    def _draw_modal(self):
        mt = self.modal.get("type", "")
        # Make modal size responsive to current window dimensions
        max_w, max_h = 760, 560
        # Ensure at least 40px margin on each side
        mw = min(max_w, max(200, W - 80))
        mh = min(max_h, max(200, H - 120))
        bx = (W - mw) // 2
        by = (H - mh) // 2

        box(screen, PANEL, (bx, by, mw, mh), 12)
        box(screen, ACCENT, (bx, by, mw, mh), 12, 1)

        # Schließen-Button
        close_rect = pygame.Rect(bx + mw - 32, by + 6, 24, 24)
        box(screen, RED, close_rect, 12)
        txt(screen, "X", "sm", WHITE, close_rect.centerx, close_rect.centery, "center")

        draw_map = {
            "buy_prop": self._draw_m_buy_prop,
            "sell_prop": self._draw_m_sell_prop,
            "upg_prop": self._draw_m_upg_prop,
            "rent_prop": self._draw_m_rent_prop,
            "rename_prop": self._draw_m_rename_prop,
            "stats_prop": self._draw_m_stats_prop,
            "buy_car": self._draw_m_buy_car,
            "sell_car": self._draw_m_sell_car,
            "upgrade_car": self._draw_m_upgrade_car,
            "rent_car": self._draw_m_rent_car,
            "rename_car": self._draw_m_rename_car,
            "stats_car": self._draw_m_stats_car,
            "buy_car_rental": self._draw_m_buy_car_rental,
            "sell_car_rental": self._draw_m_sell_car_rental,
            "upgrade_car_rental": self._draw_m_upgrade_car_rental,
            "rename_car_rental": self._draw_m_rename_car_rental,
            "stats_rental": self._draw_m_stats_rental,
            "buy_comp": self._draw_m_buy_comp,
            "sell_comp": self._draw_m_sell_comp,
            "upg_comp": self._draw_m_upg_comp,
            "rename_comp": self._draw_m_rename_comp,
            "stats_comp": self._draw_m_stats_comp,
            "loan": self._draw_m_loan,
            "repay": self._draw_m_repay,
            "savings": self._draw_m_savings,
            "buy_etf": self._draw_m_etf,
            "stocks": self._draw_m_stocks,
            "buy_stock": self._draw_m_stock,
            "sell_stock": self._draw_m_stock,
            "achievements": self._draw_m_achievements,
            "stats_overview": self._draw_m_stats_overview,
            "log_view": self._draw_m_log_view,
        }

        draw_func = draw_map.get(mt)
        if draw_func:
            draw_func(bx, by, mw, mh)

    # ── Hilfsfunktion für scrollbare Listen in Modals ──
    def _draw_scrollable_list(self, bx, by, mw, mh, items, row_h, draw_row_fn):
        """Zeichne eine scrollbare Liste mit Elementen."""
        view_area = pygame.Rect(bx, by + 50, mw, mh - 60)
        y_offset = by + 50
        for i, item in enumerate(items):
            ry = i * row_h - self._scroll
            if ry + row_h < 0 or ry > mh - 60:
                continue
            draw_row_fn(item, bx, y_offset, mw, mh, ry)

    # ── Modale Zeichenmethoden ──
    def _draw_m_buy_prop(self, bx, by, mw, mh):
        gs = self.gs
        txt(screen, "Immobilie kaufen", "lg", GOLD, bx + 16, by + 16)
        txt(screen, f"Bargeld: {fmt(gs.cash)}", "sm", CYAN, bx + 16, by + 42)
        row_h = 72
        for i, row in enumerate(PROP_CATALOG):
            ry = i * row_h - self._scroll
            if ry + row_h < 0 or ry > mh - 65:
                continue
            tid, name, icon, price, rent, maint, lvl_max = row
            can = gs.cash >= price
            box(screen, PANEL2 if can else (25, 28, 38), (bx + 8, by + 55 + ry, mw - 16, row_h - 4), 7)
            box(screen, GREEN if can else BORDER, (bx + 8, by + 55 + ry, mw - 16, row_h - 4), 7, 1)
            txt(screen, f"{icon}  {name}", "md", WHITE if can else MUTED, bx + 18, by + 55 + ry + 10)
            txt(screen, f"Preis: {fmt(price)}", "xs", MUTED, bx + 18, by + 55 + ry + 32)
            txt(screen, f"Miete: +{fmt(rent)}/Monat", "xs", GREEN, bx + 220, by + 55 + ry + 32)
            txt(screen, f"Kosten: -{fmt(maint)}/Monat", "xs", RED, bx + 400, by + 55 + ry + 32)
            txt(screen, f"Netto: {fmt(rent - maint)}/Monat", "xs", CYAN, bx + 18, by + 55 + ry + 50)
            col = ACCENT if can else BORDER
            box(screen, col, (bx + mw - 112, by + 55 + ry + 20, 90, 30), 6)
            txt(screen, "Kaufen" if can else "Kein Geld", "sm", WHITE,
                bx + mw - 67, by + 55 + ry + 35, "center")

    def _draw_m_sell_prop(self, bx, by, mw, mh):
        gs = self.gs
        txt(screen, "Immobilie verkaufen", "lg", GOLD, bx + 16, by + 16)
        txt(screen, "Preis festlegen → Käufer suchen (Marktwert-abhängig)", "xs", RED,
            bx + 16, by + 40)
        if not gs.props:
            txt(screen, "Keine Immobilien vorhanden.", "md", MUTED, bx + 16, by + 80)
            return
        row_h = 80
        for i, p in enumerate(gs.props):
            ry = i * row_h - self._scroll
            if ry + row_h < 0 or ry > mh - 60:
                continue
            bg = (40, 35, 20) if p.get("for_sale") else PANEL2
            bc = ORANGE if p.get("for_sale") else BORDER
            box(screen, bg, (bx + 8, by + 50 + ry, mw - 16, row_h - 4), 7)
            box(screen, bc, (bx + 8, by + 50 + ry, mw - 16, row_h - 4), 7, 1)

            # Marktwert berechnen
            mw_val = calc_market_value(
                p["purchase_price"], p.get("months_held", 0),
                gs.phase, gs.local_demand, p.get("condition", 0.9)
            )
            txt(screen, f"{gs.name_of(p)}  (Lvl {p['level']})", "md", WHITE,
                bx + 18, by + 50 + ry + 10)
            txt(screen, f"Marktwert: {fmt(mw_val)}  |  Zustand: {p.get('condition', 1.0):.2f}",
                "xs", MUTED, bx + 18, by + 50 + ry + 32)

            if p.get("for_sale"):
                txt(screen, f"ANGEBOTEN für: {fmt(p['sale_price'])}  |  {p['months_on_market']} Monate",
                    "xs", ORANGE, bx + 18, by + 50 + ry + 50)
                box(screen, RED, (bx + mw - 128, by + 50 + ry + 14, 110, 28), 6)
                txt(screen, "Stornieren", "xs", WHITE, bx + mw - 73, by + 50 + ry + 28, "center")
            else:
                ib = self._inputs.get("price")
                if ib:
                    ib.rect = pygame.Rect(bx + 18, by + 50 + ry + 44, 140, 28)
                    ib.draw(screen)
                box(screen, GREEN, (bx + mw - 128, by + 50 + ry + 14, 110, 28), 6)
                txt(screen, "Anbieten", "sm", BG, bx + mw - 73, by + 50 + ry + 28, "center")

    def _draw_m_upg_prop(self, bx, by, mw, mh):
        gs = self.gs
        txt(screen, "Immobilie renovieren", "lg", GOLD, bx + 16, by + 16)
        txt(screen, "Kosten: 12% des Werts | +12% Miete, +8% Wert", "xs", MUTED,
            bx + 16, by + 42)
        if not gs.props:
            txt(screen, "Keine Immobilien.", "md", MUTED, bx + 16, by + 70)
            return
        row_h = 72
        for i, p in enumerate(gs.props):
            ry = i * row_h - self._scroll
            if ry + row_h < 0 or ry > mh - 60:
                continue
            cost = p["price"] * 0.12
            maxed = p["level"] >= p["lvl_max"]
            can = gs.cash >= cost and not maxed and not p.get("for_sale")
            box(screen, PANEL2, (bx + 8, by + 50 + ry, mw - 16, row_h - 4), 7)
            box(screen, BORDER, (bx + 8, by + 50 + ry, mw - 16, row_h - 4), 7, 1)
            txt(screen, gs.name_of(p), "md", WHITE, bx + 18, by + 50 + ry + 10)
            txt(screen, f"Level {p['level']}/{p['lvl_max']}  |  Kosten: {fmt(cost)}",
                "xs", MUTED, bx + 18, by + 50 + ry + 32)
            progress_bar(screen, bx + 18, by + 50 + ry + 52, 200, 6,
                         p["level"] / p["lvl_max"], ACCENT)
            if p.get("for_sale"):
                box(screen, BORDER, (bx + mw - 112, by + 50 + ry + 22, 90, 28), 6)
                txt(screen, "Im Verkauf", "xs", MUTED, bx + mw - 67, by + 50 + ry + 36, "center")
            elif maxed:
                box(screen, BORDER, (bx + mw - 112, by + 50 + ry + 22, 90, 28), 6)
                txt(screen, "Max Level", "xs", MUTED, bx + mw - 67, by + 50 + ry + 36, "center")
            else:
                box(screen, ACCENT if can else BORDER,
                    (bx + mw - 112, by + 50 + ry + 22, 90, 28), 6)
                txt(screen, "Renovieren" if can else "Kein Geld", "xs", WHITE,
                    bx + mw - 67, by + 50 + ry + 36, "center")

    def _draw_m_rent_prop(self, bx, by, mw, mh):
        gs = self.gs
        txt(screen, "Vermietungs-Verwaltung", "lg", GOLD, bx + 16, by + 16)
        txt(screen, "Leere Immobilien vermieten → Mieter kommen automatisch.",
            "xs", MUTED, bx + 16, by + 40)
        if not gs.props:
            txt(screen, "Keine Immobilien.", "md", MUTED, bx + 16, by + 80)
            return
        row_h = 100
        for i, p in enumerate(gs.props):
            ry = i * row_h - self._scroll
            if ry + row_h < 0 or ry > mh - 64:
                continue
            if p.get("for_sale"):
                box(screen, (40, 30, 15), (bx + 8, by + 54 + ry, mw - 16, row_h - 6), 8)
                box(screen, ORANGE, (bx + 8, by + 54 + ry, mw - 16, row_h - 6), 8, 1)
                txt(screen, f"{gs.name_of(p)}  Lvl {p['level']}", "lg", ORANGE,
                    bx + 22, by + 54 + ry + 10)
                txt(screen, "ZUM VERKAUF – keine Vermietung", "sm", RED,
                    bx + 22, by + 54 + ry + 40)
                continue
            if p.get("vacant") and not p.get("listed"):
                bg, bc = (40, 25, 25), RED
            elif p.get("vacant") and p.get("listed"):
                bg, bc = (40, 38, 15), YELLOW
            else:
                bg, bc = (20, 40, 28), GREEN
            box(screen, bg, (bx + 8, by + 54 + ry, mw - 16, row_h - 6), 8)
            box(screen, bc, (bx + 8, by + 54 + ry, mw - 16, row_h - 6), 8, 1)
            pygame.draw.rect(screen, bc, (bx + 8, by + 54 + ry, 5, row_h - 6), 2)
            txt(screen, f"{gs.name_of(p)}  Lvl {p['level']}", "lg", WHITE,
                bx + 22, by + 54 + ry + 10)
            if p.get("vacant") and not p.get("listed"):
                status = "LEER"
                sc = RED
            elif p.get("vacant") and p.get("listed"):
                status = "SUCHE MIETER..."
                sc = YELLOW
            else:
                ti = p["tenant"]
                tname = TENANT_TYPES[ti][0] if ti is not None else "Mieter"
                status = f"VERMIETET: {tname}  ({p['contract_left']} Monate)"
                sc = GREEN
            txt(screen, status, "sm", sc, bx + 22, by + 54 + ry + 34)
            if not p.get("vacant"):
                txt(screen, f"Miete: {fmt(p['rent'])}/Monat", "xs", CYAN,
                    bx + 22, by + 54 + ry + 56)
                txt(screen, f"Netto: {fmt(p['rent'] - p['maint'])}/Monat", "xs", GREEN,
                    bx + 200, by + 54 + ry + 56)
            if p.get("vacant") and not p.get("listed"):
                box(screen, GREEN, (bx + mw - 128, by + 54 + ry + 20, 108, 30), 6)
                txt(screen, "Anbieten", "sm", BG, bx + mw - 74, by + 54 + ry + 35, "center")
            elif p.get("vacant") and p.get("listed"):
                box(screen, YELLOW, (bx + mw - 128, by + 54 + ry + 20, 108, 30), 6)
                txt(screen, "Stoppen", "xs", BG, bx + mw - 74, by + 54 + ry + 35, "center")
            else:
                box(screen, RED, (bx + mw - 128, by + 54 + ry + 20, 108, 30), 6)
                txt(screen, "Kündigen (-2M)", "xs", WHITE,
                    bx + mw - 74, by + 54 + ry + 35, "center")

    def _draw_m_rename_prop(self, bx, by, mw, mh):
        gs = self.gs
        txt(screen, "Immobilie umbenennen", "lg", GOLD, bx + 16, by + 16)
        ib = self._inputs.get("name")
        if ib:
            ib.rect = pygame.Rect(bx + 30, by + 60, 260, 34)
            ib.draw(screen)
        if not gs.props:
            txt(screen, "Keine Immobilien.", "md", MUTED, bx + 30, by + 100)
            return
        txt(screen, "Wähle eine Immobilie:", "xs", MUTED, bx + 30, by + 100)
        row_h = 50
        for i, p in enumerate(gs.props):
            ry = i * row_h - self._scroll
            if ry + row_h < 0 or ry > mh - 130:
                continue
            box(screen, PANEL2, (bx + 8, by + 120 + ry, mw - 16, row_h - 4), 7)
            box(screen, BORDER, (bx + 8, by + 120 + ry, mw - 16, row_h - 4), 7, 1)
            txt(screen, f"{gs.name_of(p)}", "sm", WHITE, bx + 18, by + 120 + ry + 16)
            box(screen, ACCENT, (bx + mw - 130, by + 120 + ry + 10, 110, 28), 6)
            txt(screen, "Umbenennen", "xs", WHITE, bx + mw - 75, by + 120 + ry + 24, "center")

    def _draw_m_stats_prop(self, bx, by, mw, mh):
        gs = self.gs
        txt(screen, "Immobilien-Statistik", "lg", GOLD, bx + 16, by + 16)
        if not gs.props:
            txt(screen, "Keine Immobilien.", "md", MUTED, bx + 16, by + 60)
            return
        total_val = sum(p["price"] for p in gs.props)
        total_rent = sum(p.get("rent", 0) for p in gs.props if not p.get("vacant"))
        vacant = sum(1 for p in gs.props if p.get("vacant"))
        txt(screen, f"Anzahl: {len(gs.props)}", "md", WHITE, bx + 16, by + 50)
        txt(screen, f"Gesamtwert: {fmt(total_val)}", "md", WHITE, bx + 16, by + 74)
        txt(screen, f"Mieteinnahmen: {fmt(total_rent)}/Monat", "md", GREEN, bx + 16, by + 98)
        txt(screen, f"Leerstand: {vacant}", "md", RED if vacant > 0 else WHITE,
            bx + 16, by + 122)
        avg_condition = sum(p.get("condition", 1.0) for p in gs.props) / max(1, len(gs.props))
        txt(screen, f"Durchschnittszustand: {avg_condition:.2f}", "md", WHITE,
            bx + 16, by + 146)
        box(screen, GOLD, (bx + 16, by + 170, mw - 32, 30), 6)
        txt(screen, "Klicke Schließen (X) um zurückzukehren", "xs", MUTED,
            bx + mw // 2, by + 185, "center")

    # ── Auto-Modals ──
    def _draw_m_buy_car(self, bx, by, mw, mh):
        gs = self.gs
        txt(screen, "Auto kaufen", "lg", GOLD, bx + 16, by + 16)
        txt(screen, f"Bargeld: {fmt(gs.cash)}", "sm", CYAN, bx + 16, by + 42)
        row_h = 72
        for i, row in enumerate(CAR_CATALOG):
            ry = i * row_h - self._scroll
            if ry + row_h < 0 or ry > mh - 65:
                continue
            tid, name, icon, price, rental, maint, dep, lvl_max = row
            can = gs.cash >= price
            box(screen, PANEL2 if can else (25, 28, 38), (bx + 8, by + 55 + ry, mw - 16, row_h - 4), 7)
            box(screen, GREEN if can else BORDER, (bx + 8, by + 55 + ry, mw - 16, row_h - 4), 7, 1)
            txt(screen, f"{icon}  {name}", "md", WHITE if can else MUTED, bx + 18, by + 55 + ry + 10)
            txt(screen, f"Preis: {fmt(price)}", "xs", MUTED, bx + 18, by + 55 + ry + 32)
            txt(screen, f"Miete: +{fmt(rental)}/Monat", "xs", GREEN, bx + 220, by + 55 + ry + 32)
            txt(screen, f"Kosten: -{fmt(maint)}/Monat", "xs", RED, bx + 380, by + 55 + ry + 32)
            txt(screen, f"Wertverlust: {dep * 100:.1f}%/M", "xs", CYAN,
                bx + 18, by + 55 + ry + 50)
            col = ACCENT if can else BORDER
            box(screen, col, (bx + mw - 112, by + 55 + ry + 20, 90, 30), 6)
            txt(screen, "Kaufen" if can else "Kein Geld", "sm", WHITE,
                bx + mw - 67, by + 55 + ry + 35, "center")

    def _draw_m_sell_car(self, bx, by, mw, mh):
        gs = self.gs
        txt(screen, "Auto verkaufen", "lg", GOLD, bx + 16, by + 16)
        if not gs.cars:
            txt(screen, "Keine Autos.", "md", MUTED, bx + 16, by + 80); return
        row_h = 80
        for i, car in enumerate(gs.cars):
            ry = i * row_h - self._scroll
            if ry + row_h < 0 or ry > mh - 60: continue
            bg = (40, 35, 20) if car.get("for_sale") else PANEL2
            bc = ORANGE if car.get("for_sale") else BORDER
            box(screen, bg, (bx + 8, by + 50 + ry, mw - 16, row_h - 4), 7)
            box(screen, bc, (bx + 8, by + 50 + ry, mw - 16, row_h - 4), 7, 1)
            status = "VERMIETET" if car.get("rented") else "FREI"
            txt(screen, f"{gs.name_of(car)}  (Lvl {car['level']})  {status}", "md", WHITE,
                bx + 18, by + 50 + ry + 10)
            mw_val = calc_market_value(car["purchase_price"], car.get("months_held", 0),
                                       gs.phase, gs.local_demand, car.get("condition", 0.9))
            txt(screen, f"Marktwert: {fmt(mw_val)}", "xs", MUTED,
                bx + 18, by + 50 + ry + 32)
            if car.get("for_sale"):
                txt(screen, f"ANGEBOTEN für: {fmt(car['sale_price'])}", "xs", ORANGE,
                    bx + 18, by + 50 + ry + 50)
                box(screen, RED, (bx + mw - 128, by + 50 + ry + 14, 110, 28), 6)
                txt(screen, "Stornieren", "xs", WHITE, bx + mw - 73, by + 50 + ry + 28, "center")
            else:
                ib = self._inputs.get("price")
                if ib:
                    ib.rect = pygame.Rect(bx + 18, by + 50 + ry + 44, 140, 28)
                    ib.draw(screen)
                box(screen, GREEN, (bx + mw - 128, by + 50 + ry + 14, 110, 28), 6)
                txt(screen, "Anbieten", "sm", BG, bx + mw - 73, by + 50 + ry + 28, "center")

    def _draw_m_upgrade_car(self, bx, by, mw, mh):
        gs = self.gs
        txt(screen, "Auto tunen", "lg", GOLD, bx + 16, by + 16)
        txt(screen, "Kosten: 15% des Werts | +15% Miete, +10% Wert", "xs", MUTED,
            bx + 16, by + 42)
        if not gs.cars:
            txt(screen, "Keine Autos.", "md", MUTED, bx + 16, by + 70); return
        row_h = 72
        for i, car in enumerate(gs.cars):
            ry = i * row_h - self._scroll
            if ry + row_h < 0 or ry > mh - 60: continue
            cost = car["price"] * 0.15
            maxed = car["level"] >= car["lvl_max"]
            can = gs.cash >= cost and not maxed and not car.get("for_sale")
            box(screen, PANEL2, (bx + 8, by + 50 + ry, mw - 16, row_h - 4), 7)
            box(screen, BORDER, (bx + 8, by + 50 + ry, mw - 16, row_h - 4), 7, 1)
            txt(screen, gs.name_of(car), "md", WHITE, bx + 18, by + 50 + ry + 10)
            txt(screen, f"Level {car['level']}/{car['lvl_max']}  |  Kosten: {fmt(cost)}",
                "xs", MUTED, bx + 18, by + 50 + ry + 32)
            progress_bar(screen, bx + 18, by + 50 + ry + 52, 200, 6,
                         car["level"] / car["lvl_max"], ORANGE)
            if car.get("for_sale"):
                box(screen, BORDER, (bx + mw - 112, by + 50 + ry + 22, 90, 28), 6)
                txt(screen, "Im Verkauf", "xs", MUTED,
                    bx + mw - 67, by + 50 + ry + 36, "center")
            elif maxed:
                box(screen, BORDER, (bx + mw - 112, by + 50 + ry + 22, 90, 28), 6)
                txt(screen, "Max Level", "xs", MUTED,
                    bx + mw - 67, by + 50 + ry + 36, "center")
            else:
                box(screen, ACCENT if can else BORDER,
                    (bx + mw - 112, by + 50 + ry + 22, 90, 28), 6)
                txt(screen, "Tunen" if can else "Kein Geld", "xs", WHITE,
                    bx + mw - 67, by + 50 + ry + 36, "center")

    def _draw_m_rent_car(self, bx, by, mw, mh):
        gs = self.gs
        txt(screen, "Auto-Garage", "lg", GOLD, bx + 16, by + 16)
        txt(screen, "Autos werden automatisch vermietet.", "xs", MUTED, bx + 16, by + 40)
        if not gs.cars:
            txt(screen, "Keine Autos.", "md", MUTED, bx + 16, by + 80); return
        row_h = 72
        for i, car in enumerate(gs.cars):
            ry = i * row_h - self._scroll
            if ry + row_h < 0 or ry > mh - 65: continue
            if car.get("for_sale"): continue
            bg = (20, 40, 28) if car.get("rented") else (40, 25, 25)
            bc = GREEN if car.get("rented") else RED
            box(screen, bg, (bx + 8, by + 55 + ry, mw - 16, row_h - 4), 7)
            box(screen, bc, (bx + 8, by + 55 + ry, mw - 16, row_h - 4), 7, 1)
            txt(screen, f"{gs.name_of(car)}  Lvl {car['level']}", "md", WHITE,
                bx + 18, by + 55 + ry + 10)
            if car.get("rented"):
                ci = car.get("rental_customer", 0)
                cname = CAR_RENTAL_CUSTOMERS[ci][0] if ci < len(CAR_RENTAL_CUSTOMERS) else "?"
                txt(screen, f"VERMIETET an {cname}  ({car['contract_left']}M)  +{fmt(car['rental'])}/M",
                    "sm", GREEN, bx + 18, by + 55 + ry + 32)
            else:
                txt(screen, "FREI – automatische Vermietung aktiv", "sm", MUTED,
                    bx + 18, by + 55 + ry + 32)

    def _draw_m_rename_car(self, bx, by, mw, mh):
        gs = self.gs
        txt(screen, "Auto umbenennen", "lg", GOLD, bx + 16, by + 16)
        ib = self._inputs.get("name")
        if ib:
            ib.rect = pygame.Rect(bx + 30, by + 60, 260, 34); ib.draw(screen)
        if not gs.cars:
            txt(screen, "Keine Autos.", "md", MUTED, bx + 30, by + 100); return
        row_h = 50
        for i, car in enumerate(gs.cars):
            ry = i * row_h - self._scroll
            if ry + row_h < 0 or ry > mh - 110: continue
            box(screen, PANEL2, (bx + 8, by + 100 + ry, mw - 16, row_h - 4), 7)
            box(screen, BORDER, (bx + 8, by + 100 + ry, mw - 16, row_h - 4), 7, 1)
            txt(screen, f"{gs.name_of(car)}", "sm", WHITE, bx + 18, by + 100 + ry + 16)
            box(screen, ACCENT, (bx + mw - 130, by + 100 + ry + 10, 110, 28), 6)
            txt(screen, "Umbenennen", "xs", WHITE, bx + mw - 75, by + 100 + ry + 24, "center")

    def _draw_m_stats_car(self, bx, by, mw, mh):
        gs = self.gs
        txt(screen, "Auto-Statistik", "lg", GOLD, bx + 16, by + 16)
        if not gs.cars:
            txt(screen, "Keine Autos.", "md", MUTED, bx + 16, by + 60); return
        total_val = sum(c["price"] for c in gs.cars)
        rented = sum(1 for c in gs.cars if c.get("rented"))
        txt(screen, f"Anzahl: {len(gs.cars)}", "md", WHITE, bx + 16, by + 50)
        txt(screen, f"Gesamtwert: {fmt(total_val)}", "md", WHITE, bx + 16, by + 74)
        txt(screen, f"Vermietet: {rented}/{len(gs.cars)}", "md", GREEN if rented > 0 else RED,
            bx + 16, by + 98)

    # ── Autovermietung-Modals ──
    def _draw_m_buy_car_rental(self, bx, by, mw, mh):
        gs = self.gs
        txt(screen, "Autovermietung gründen", "lg", GOLD, bx + 16, by + 16)
        txt(screen, f"Bargeld: {fmt(gs.cash)}", "sm", CYAN, bx + 16, by + 42)
        row_h = 72
        for i, row in enumerate(CAR_RENTAL_CATALOG):
            ry = i * row_h - self._scroll
            if ry + row_h < 0 or ry > mh - 65: continue
            tid, name, icon, price, profit, maint, risk, lvl_max = row
            can = gs.cash >= price
            box(screen, PANEL2 if can else (25, 28, 38),
                (bx + 8, by + 55 + ry, mw - 16, row_h - 4), 7)
            box(screen, GREEN if can else BORDER,
                (bx + 8, by + 55 + ry, mw - 16, row_h - 4), 7, 1)
            txt(screen, f"{icon}  {name}", "md", WHITE if can else MUTED,
                bx + 18, by + 55 + ry + 10)
            txt(screen, f"Preis: {fmt(price)}", "xs", MUTED, bx + 18, by + 55 + ry + 32)
            txt(screen, f"Gewinn: +{fmt(profit)}/Monat", "xs", GREEN,
                bx + 220, by + 55 + ry + 32)
            txt(screen, f"Risiko: {risk * 100:.0f}%", "xs", YELLOW,
                bx + 400, by + 55 + ry + 32)
            col = ACCENT if can else BORDER
            box(screen, col, (bx + mw - 112, by + 55 + ry + 20, 90, 30), 6)
            txt(screen, "Gründen" if can else "Kein Geld", "sm", WHITE,
                bx + mw - 67, by + 55 + ry + 35, "center")

    def _draw_m_sell_car_rental(self, bx, by, mw, mh):
        gs = self.gs
        txt(screen, "Autovermietung verkaufen", "lg", GOLD, bx + 16, by + 16)
        if not gs.car_rentals:
            txt(screen, "Keine Vermietungen.", "md", MUTED, bx + 16, by + 80); return
        row_h = 80
        for i, cr in enumerate(gs.car_rentals):
            ry = i * row_h - self._scroll
            if ry + row_h < 0 or ry > mh - 60: continue
            bg = (40, 35, 20) if cr.get("for_sale") else PANEL2
            bc = ORANGE if cr.get("for_sale") else BORDER
            box(screen, bg, (bx + 8, by + 50 + ry, mw - 16, row_h - 4), 7)
            box(screen, bc, (bx + 8, by + 50 + ry, mw - 16, row_h - 4), 7, 1)
            txt(screen, f"{gs.name_of(cr)}  (Lvl {cr['level']})", "md", WHITE,
                bx + 18, by + 50 + ry + 10)
            txt(screen, f"Wert: {fmt(cr['val'])}  |  Gewinn: {fmt(cr['profit'])}/Monat",
                "xs", MUTED, bx + 18, by + 50 + ry + 32)
            if cr.get("for_sale"):
                txt(screen, f"ANGEBOTEN: {fmt(cr['sale_price'])}", "xs", ORANGE,
                    bx + 18, by + 50 + ry + 50)
                box(screen, RED, (bx + mw - 128, by + 50 + ry + 14, 110, 28), 6)
                txt(screen, "Stornieren", "xs", WHITE,
                    bx + mw - 73, by + 50 + ry + 28, "center")
            else:
                ib = self._inputs.get("price")
                if ib:
                    ib.rect = pygame.Rect(bx + 18, by + 50 + ry + 44, 140, 28)
                    ib.draw(screen)
                box(screen, GREEN, (bx + mw - 128, by + 50 + ry + 14, 110, 28), 6)
                txt(screen, "Anbieten", "sm", BG,
                    bx + mw - 73, by + 50 + ry + 28, "center")

    def _draw_m_upgrade_car_rental(self, bx, by, mw, mh):
        gs = self.gs
        txt(screen, "Autovermietung erweitern", "lg", GOLD, bx + 16, by + 16)
        txt(screen, "Kosten: 15% des Werts | +20% Gewinn, +12% Wert", "xs", MUTED,
            bx + 16, by + 42)
        if not gs.car_rentals:
            txt(screen, "Keine Vermietungen.", "md", MUTED, bx + 16, by + 70); return
        row_h = 72
        for i, cr in enumerate(gs.car_rentals):
            ry = i * row_h - self._scroll
            if ry + row_h < 0 or ry > mh - 60: continue
            cost = cr["val"] * 0.15
            maxed = cr["level"] >= cr["lvl_max"]
            can = gs.cash >= cost and not maxed and not cr.get("for_sale")
            box(screen, PANEL2, (bx + 8, by + 50 + ry, mw - 16, row_h - 4), 7)
            box(screen, BORDER, (bx + 8, by + 50 + ry, mw - 16, row_h - 4), 7, 1)
            txt(screen, gs.name_of(cr), "md", WHITE, bx + 18, by + 50 + ry + 10)
            txt(screen, f"Level {cr['level']}/{cr['lvl_max']}  |  Kosten: {fmt(cost)}",
                "xs", MUTED, bx + 18, by + 50 + ry + 32)
            progress_bar(screen, bx + 18, by + 50 + ry + 52, 200, 6,
                         cr["level"] / cr["lvl_max"], PURPLE)
            if cr.get("for_sale"):
                box(screen, BORDER, (bx + mw - 112, by + 50 + ry + 22, 90, 28), 6)
                txt(screen, "Im Verkauf", "xs", MUTED,
                    bx + mw - 67, by + 50 + ry + 36, "center")
            elif maxed:
                box(screen, BORDER, (bx + mw - 112, by + 50 + ry + 22, 90, 28), 6)
                txt(screen, "Max Level", "xs", MUTED,
                    bx + mw - 67, by + 50 + ry + 36, "center")
            else:
                box(screen, ACCENT if can else BORDER,
                    (bx + mw - 112, by + 50 + ry + 22, 90, 28), 6)
                txt(screen, "Erweitern" if can else "Kein Geld", "xs", WHITE,
                    bx + mw - 67, by + 50 + ry + 36, "center")

    def _draw_m_rename_car_rental(self, bx, by, mw, mh):
        gs = self.gs
        txt(screen, "Autovermietung umbenennen", "lg", GOLD, bx + 16, by + 16)
        ib = self._inputs.get("name")
        if ib:
            ib.rect = pygame.Rect(bx + 30, by + 60, 260, 34); ib.draw(screen)
        if not gs.car_rentals:
            txt(screen, "Keine Vermietungen.", "md", MUTED, bx + 30, by + 100); return
        row_h = 50
        for i, cr in enumerate(gs.car_rentals):
            ry = i * row_h - self._scroll
            if ry + row_h < 0 or ry > mh - 110: continue
            box(screen, PANEL2, (bx + 8, by + 100 + ry, mw - 16, row_h - 4), 7)
            box(screen, BORDER, (bx + 8, by + 100 + ry, mw - 16, row_h - 4), 7, 1)
            txt(screen, f"{gs.name_of(cr)}", "sm", WHITE, bx + 18, by + 100 + ry + 16)
            box(screen, ACCENT, (bx + mw - 130, by + 100 + ry + 10, 110, 28), 6)
            txt(screen, "Umbenennen", "xs", WHITE, bx + mw - 75, by + 100 + ry + 24, "center")

    # ── Firmen-Modals ──
    def _draw_m_buy_comp(self, bx, by, mw, mh):
        gs = self.gs
        txt(screen, "Unternehmen gründen", "lg", GOLD, bx + 16, by + 16)
        txt(screen, f"Bargeld: {fmt(gs.cash)}", "sm", CYAN, bx + 16, by + 42)
        row_h = 72
        for i, row in enumerate(COMP_CATALOG):
            ry = i * row_h - self._scroll
            if ry + row_h < 0 or ry > mh - 65: continue
            tid, name, icon, price, profit, maint, risk, lvl_max = row
            can = gs.cash >= price
            box(screen, PANEL2 if can else (25, 28, 38),
                (bx + 8, by + 55 + ry, mw - 16, row_h - 4), 7)
            box(screen, GREEN if can else BORDER,
                (bx + 8, by + 55 + ry, mw - 16, row_h - 4), 7, 1)
            txt(screen, f"{icon}  {name}", "md", WHITE if can else MUTED,
                bx + 18, by + 55 + ry + 10)
            txt(screen, f"Preis: {fmt(price)}", "xs", MUTED, bx + 18, by + 55 + ry + 32)
            txt(screen, f"Gewinn: +{fmt(profit)}/Monat", "xs", GREEN,
                bx + 220, by + 55 + ry + 32)
            txt(screen, f"Risiko: {risk * 100:.0f}%", "xs", YELLOW,
                bx + 400, by + 55 + ry + 32)
            col = ACCENT if can else BORDER
            box(screen, col, (bx + mw - 112, by + 55 + ry + 20, 90, 30), 6)
            txt(screen, "Gründen" if can else "Kein Geld", "sm", WHITE,
                bx + mw - 67, by + 55 + ry + 35, "center")

    def _draw_m_sell_comp(self, bx, by, mw, mh):
        gs = self.gs
        txt(screen, "Unternehmen verkaufen", "lg", GOLD, bx + 16, by + 16)
        txt(screen, "Marktwert-basierter Verkauf", "xs", RED, bx + 16, by + 40)
        if not gs.comps: txt(screen, "Keine Unternehmen.", "md", MUTED, bx + 16, by + 80); return
        row_h = 80
        for i, c in enumerate(gs.comps):
            ry = i * row_h - self._scroll
            if ry + row_h < 0 or ry > mh - 60: continue
            bg = (40, 35, 20) if c.get("for_sale") else PANEL2
            bc = ORANGE if c.get("for_sale") else BORDER
            box(screen, bg, (bx + 8, by + 50 + ry, mw - 16, row_h - 4), 7)
            box(screen, bc, (bx + 8, by + 50 + ry, mw - 16, row_h - 4), 7, 1)
            txt(screen, f"{gs.name_of(c)}  (Lvl {c['level']})", "md", WHITE,
                bx + 18, by + 50 + ry + 10)
            txt(screen, f"Wert: {fmt(c['val'])}  |  Gewinn: {fmt(c['profit'])}/Monat",
                "xs", MUTED, bx + 18, by + 50 + ry + 32)
            if c.get("for_sale"):
                txt(screen, f"ANGEBOTEN: {fmt(c['sale_price'])}", "xs", ORANGE,
                    bx + 18, by + 50 + ry + 50)
                box(screen, RED, (bx + mw - 128, by + 50 + ry + 14, 110, 28), 6)
                txt(screen, "Stornieren", "xs", WHITE, bx + mw - 73, by + 50 + ry + 28, "center")
            else:
                ib = self._inputs.get("price")
                if ib: ib.rect = pygame.Rect(bx + 18, by + 50 + ry + 44, 140, 28); ib.draw(screen)
                box(screen, GREEN, (bx + mw - 128, by + 50 + ry + 14, 110, 28), 6)
                txt(screen, "Anbieten", "sm", BG, bx + mw - 73, by + 50 + ry + 28, "center")

    def _draw_m_upg_comp(self, bx, by, mw, mh):
        gs = self.gs
        txt(screen, "Unternehmen erweitern", "lg", GOLD, bx + 16, by + 16)
        txt(screen, "Kosten: 15% | +20% Gewinn, +12% Wert", "xs", MUTED, bx + 16, by + 42)
        if not gs.comps: txt(screen, "Keine Unternehmen.", "md", MUTED, bx + 16, by + 70); return
        row_h = 72
        for i, c in enumerate(gs.comps):
            ry = i * row_h - self._scroll
            if ry + row_h < 0 or ry > mh - 60: continue
            cost = c["val"] * 0.15; maxed = c["level"] >= c["lvl_max"]
            can = gs.cash >= cost and not maxed and not c.get("for_sale")
            box(screen, PANEL2, (bx + 8, by + 50 + ry, mw - 16, row_h - 4), 7)
            box(screen, BORDER, (bx + 8, by + 50 + ry, mw - 16, row_h - 4), 7, 1)
            txt(screen, gs.name_of(c), "md", WHITE, bx + 18, by + 50 + ry + 10)
            txt(screen, f"Level {c['level']}/{c['lvl_max']}  |  Kosten: {fmt(cost)}",
                "xs", MUTED, bx + 18, by + 50 + ry + 32)
            progress_bar(screen, bx + 18, by + 50 + ry + 52, 200, 6,
                         c["level"] / c["lvl_max"], PURPLE)
            if c.get("for_sale"):
                box(screen, BORDER, (bx + mw - 112, by + 50 + ry + 22, 90, 28), 6)
                txt(screen, "Im Verkauf", "xs", MUTED, bx + mw - 67, by + 50 + ry + 36, "center")
            elif maxed:
                box(screen, BORDER, (bx + mw - 112, by + 50 + ry + 22, 90, 28), 6)
                txt(screen, "Max Level", "xs", MUTED, bx + mw - 67, by + 50 + ry + 36, "center")
            else:
                box(screen, ACCENT if can else BORDER,
                    (bx + mw - 112, by + 50 + ry + 22, 90, 28), 6)
                txt(screen, "Erweitern" if can else "Kein Geld", "xs", WHITE,
                    bx + mw - 67, by + 50 + ry + 36, "center")

    def _draw_m_rename_comp(self, bx, by, mw, mh):
        gs = self.gs
        txt(screen, "Unternehmen umbenennen", "lg", GOLD, bx + 16, by + 16)
        ib = self._inputs.get("name")
        if ib: ib.rect = pygame.Rect(bx + 30, by + 60, 260, 34); ib.draw(screen)
        if not gs.comps: txt(screen, "Keine Unternehmen.", "md", MUTED, bx + 30, by + 100); return
        row_h = 50
        for i, c in enumerate(gs.comps):
            ry = i * row_h - self._scroll
            if ry + row_h < 0 or ry > mh - 110: continue
            box(screen, PANEL2, (bx + 8, by + 100 + ry, mw - 16, row_h - 4), 7)
            box(screen, BORDER, (bx + 8, by + 100 + ry, mw - 16, row_h - 4), 7, 1)
            txt(screen, f"{gs.name_of(c)}", "sm", WHITE, bx + 18, by + 100 + ry + 16)
            box(screen, ACCENT, (bx + mw - 130, by + 100 + ry + 10, 110, 28), 6)
            txt(screen, "Umbenennen", "xs", WHITE, bx + mw - 75, by + 100 + ry + 24, "center")

    def _draw_m_stats_comp(self, bx, by, mw, mh):
        gs = self.gs
        txt(screen, "Unternehmens-Statistik", "lg", GOLD, bx + 16, by + 16)
        if not gs.comps: txt(screen, "Keine Unternehmen.", "md", MUTED, bx + 16, by + 60); return
        total = sum(c["val"] for c in gs.comps)
        total_profit = sum(c.get("profit", 0) for c in gs.comps)
        txt(screen, f"Anzahl: {len(gs.comps)}", "md", WHITE, bx + 16, by + 50)
        txt(screen, f"Gesamtwert: {fmt(total)}", "md", WHITE, bx + 16, by + 74)
        txt(screen, f"Monatsgewinn: {fmt(total_profit)}", "md", GREEN, bx + 16, by + 98)

    # ── Bank-Modals ──
    def _draw_m_loan(self, bx, by, mw, mh):
        gs = self.gs
        txt(screen, "Kredit aufnehmen", "lg", GOLD, bx + 16, by + 16)
        max_l = max(0, gs.net_worth() * 0.4 - gs.loan)
        rate = (gs.loan_rate + gs.base_rate / 100 / 12) * 12 * 100
        txt(screen, f"Aktuelle Schulden: {fmt(gs.loan)}", "sm", RED, bx + 16, by + 50)
        txt(screen, f"Max. Rahmen: {fmt(max_l)}", "sm", CYAN, bx + 16, by + 74)
        txt(screen, f"Eff. Jahreszins: {rate:.2f}%", "sm", YELLOW, bx + 16, by + 98)
        ib = self._inputs.get("amount")
        if ib: ib.rect = pygame.Rect(bx + 30, by + 128, 220, 34); ib.draw(screen)
        box(screen, ACCENT, (bx + 260, by + 128, 120, 34), 7)
        txt(screen, "Aufnehmen", "sm", WHITE, bx + 320, by + 145, "center")

    def _draw_m_repay(self, bx, by, mw, mh):
        gs = self.gs
        txt(screen, "Kredit tilgen", "lg", GOLD, bx + 16, by + 16)
        txt(screen, f"Offene Schulden: {fmt(gs.loan)}", "sm", RED, bx + 16, by + 50)
        txt(screen, f"Bargeld: {fmt(gs.cash)}", "sm", CYAN, bx + 16, by + 74)
        ib = self._inputs.get("amount")
        if ib: ib.rect = pygame.Rect(bx + 30, by + 128, 220, 34); ib.draw(screen)
        box(screen, GREEN, (bx + 260, by + 128, 120, 34), 7)
        txt(screen, "Tilgen", "sm", WHITE, bx + 320, by + 145, "center")
        box(screen, YELLOW, (bx + 30, by + 180, 160, 34), 7)
        txt(screen, "Alles tilgen", "sm", BG, bx + 110, by + 197, "center")

    def _draw_m_savings(self, bx, by, mw, mh):
        gs = self.gs
        rate = gs.sav_rate * 12 * 100
        txt(screen, "Festgeld-Konto", "lg", GOLD, bx + 16, by + 16)
        txt(screen, f"Einlage: {fmt(gs.savings)}", "sm", CYAN, bx + 16, by + 50)
        txt(screen, f"Zins: {rate:.2f}% p.a. = {fmt(gs.savings * gs.sav_rate)}/M", "sm", GREEN,
            bx + 16, by + 74)
        txt(screen, f"Bargeld: {fmt(gs.cash)}", "sm", MUTED, bx + 16, by + 98)
        ib = self._inputs.get("amount")
        if ib: ib.rect = pygame.Rect(bx + 30, by + 128, 220, 34); ib.draw(screen)
        box(screen, ACCENT, (bx + 260, by + 128, 120, 34), 7)
        txt(screen, "Einzahlen", "sm", WHITE, bx + 320, by + 145, "center")
        if gs.savings > 0:
            box(screen, YELLOW, (bx + 30, by + 180, 160, 34), 7)
            txt(screen, "Auszahlen", "sm", BG, bx + 110, by + 197, "center")

    # ── Aktien/ETF-Modals ──
    def _draw_m_stocks(self, bx, by, mw, mh):
        gs = self.gs
        txt(screen, "Aktienmarkt", "lg", GOLD, bx + 16, by + 16)
        txt(screen, "Klicke auf eine Aktie für Kauf/Verkauf", "xs", MUTED, bx + 16, by + 42)
        col_w = (mw - 30) // 2; row_h = 62
        sids = list(gs.stock_data.keys())
        for i, sid in enumerate(sids):
            s = gs.stock_data[sid]
            rx = bx + 12 + (i % 2) * (col_w + 6)
            ry = by + 50 + (i // 2) * row_h
            qty = gs.stocks.get(sid, 0)
            box(screen, PANEL2, (rx, ry, col_w, row_h - 4), 6)
            box(screen, BORDER, (rx, ry, col_w, row_h - 4), 6, 1)
            pchg = (s["hist"][-1] / s["hist"][-2] - 1) * 100 if len(s["hist"]) >= 2 else 0
            txt(screen, s["name"], "sm", WHITE, rx + 8, ry + 10)
            txt(screen, fmt(s["price"]), "sm", CYAN, rx + 8, ry + 30)
            txt(screen, f"{pchg:+.1f}%", "xs", GREEN if pchg >= 0 else RED, rx + 8, ry + 48)
            txt(screen, f"Div: {s['div'] * 100:.1f}%", "xs", MUTED, rx + col_w // 2, ry + 10)
            if qty > 0:
                txt(screen, f"{qty:.0f} = {fmt(qty * s['price'])}", "xs", PURPLE,
                    rx + col_w // 2, ry + 30)
            # Click-Buttons
            buy_r = pygame.Rect(rx, ry, col_w * 0.5, row_h - 4)
            sell_r = pygame.Rect(rx + col_w * 0.5, ry, col_w * 0.5, row_h - 4)
            # Wir zeichnen keine separaten Buttons, die Klicklogik teilt die Zeile auf
        txt(screen, "→ Klick links = Kaufen | Klick rechts = Verkaufen", "xs", YELLOW,
            bx + mw // 2, by + mh - 20, "center")

    def _draw_m_stock(self, bx, by, mw, mh):
        gs = self.gs
        mt = self.modal["type"]; sid = self.modal["sid"]
        s = gs.stock_data[sid]; qty_owned = gs.stocks.get(sid, 0)
        label = "Aktie kaufen" if mt == "buy_stock" else "Aktie verkaufen"
        txt(screen, label, "lg", GOLD, bx + 16, by + 16)
        txt(screen, f"{s['name']}  |  Kurs: {fmt(s['price'])}  |  Div: {s['div'] * 100:.1f}%",
            "md", WHITE, bx + 16, by + 50)
        txt(screen, f"Besitz: {qty_owned:.0f} = {fmt(qty_owned * s['price'])}",
            "sm", CYAN, bx + 16, by + 76)
        txt(screen, f"Bargeld: {fmt(gs.cash)}", "sm", MUTED, bx + 16, by + 100)
        ib = self._inputs.get("qty")
        if ib: ib.rect = pygame.Rect(bx + 30, by + 130, 180, 34); ib.draw(screen)
        bc = ACCENT if mt == "buy_stock" else RED
        box(screen, bc, (bx + 220, by + 130, 110, 34), 7)
        btn_label = "Kaufen" if mt == "buy_stock" else "Verkaufen"
        txt(screen, btn_label, "sm", WHITE, bx + 275, by + 147, "center")
        if mt == "sell_stock" and qty_owned > 0:
            box(screen, YELLOW, (bx + 30, by + 180, 160, 34), 7)
            txt(screen, "Alles verkaufen", "sm", BG, bx + 110, by + 197, "center")
        if len(s["hist"]) >= 2:
            sparkline(screen, s["hist"], bx + 30, by + 240, mw - 60, 100)
            txt(screen, "Kursverlauf", "xs", MUTED, bx + 30, by + 228)

    def _draw_m_etf(self, bx, by, mw, mh):
        gs = self.gs
        txt(screen, "Welt-ETF", "lg", GOLD, bx + 16, by + 16)
        txt(screen, f"Kurs: {fmt(gs.etf_price)}  |  Besitz: {gs.etf:.1f} = {fmt(gs.etf * gs.etf_price)}",
            "md", WHITE, bx + 16, by + 50)
        txt(screen, "Diversifiziert, geringes Risiko, 2.4% Div.", "sm", GREEN,
            bx + 16, by + 76)
        txt(screen, f"Bargeld: {fmt(gs.cash)}", "sm", MUTED, bx + 16, by + 100)
        ib = self._inputs.get("qty")
        if ib: ib.rect = pygame.Rect(bx + 30, by + 130, 180, 34); ib.draw(screen)
        box(screen, ACCENT, (bx + 220, by + 130, 110, 34), 7)
        txt(screen, "Kaufen", "sm", WHITE, bx + 275, by + 147, "center")
        if gs.etf > 0:
            box(screen, RED, (bx + 30, by + 180, 160, 34), 7)
            txt(screen, "Alle verkaufen", "sm", WHITE, bx + 110, by + 197, "center")
        if len(gs.etf_hist) >= 2:
            sparkline(screen, gs.etf_hist, bx + 30, by + 240, mw - 60, 100)

# ═══════════════════════════════════════════════════════════
#  ACHIEVEMENT-UI – Modernes Steam/Xbox-Stil Layout
# ═══════════════════════════════════════════════════════════
    def _init_achievement_data(self):
        """Berechne Achievement-Daten für die UI."""
        gs = self.gs
        # Alle Achievement-Kategorien für die Navigation
        self._ach_categories = [
            ("immobilien", "Immobilien", ACHIEV_IMMO, "immo"),
            ("autos", "Autos", ACHIEV_CARS, "cars"),
            ("filialen", "Autovermietung", ACHIEV_FILIALEN, "filialen"),
            ("firmen", "Unternehmen", ACHIEV_FIRMEN, "firmen"),
            ("vermoegen", "Vermögen", ACHIEV_VERMOEGEN, "vermoegen"),
        ]
        # Spezial-Kategorien
        self._ach_special_groups = {
            "mogul": ("Immobilienmogul", [a for a in ACHIEV_SPECIAL if a[0].startswith("mogul")]),
            "auto": ("Auto-Sammler", [a for a in ACHIEV_SPECIAL if a[0].startswith("auto")]),
            "unter": ("Unternehmer", [a for a in ACHIEV_SPECIAL if a[0].startswith("unter")]),
            "inv": ("Investor", [a for a in ACHIEV_SPECIAL if a[0].startswith("inv")]),
            "bank": ("Banker", [a for a in ACHIEV_SPECIAL if a[0].startswith("bank")]),
            "boerse": ("Börsenprofi", [a for a in ACHIEV_SPECIAL if a[0].startswith("boerse")]),
            "tyc": ("Tycoon", [a for a in ACHIEV_SPECIAL if a[0].startswith("tyc")]),
            "lang": ("Langzeitspieler", [a for a in ACHIEV_SPECIAL if a[0].startswith("lang")]),
            "rekord": ("Rekordhalter", [a for a in ACHIEV_SPECIAL if a[0].startswith("rekord")]),
            "sonstige": ("Sonstige", [a for a in ACHIEV_SPECIAL if a[0] in ("all_1", "hard_1", "perf_1")]),
        }
        # Kategorie-Fortschritt berechnen
        self._ach_category_progress = {}
        for cat_id, cat_name, cat_data, prefix in self._ach_categories:
            total = len(cat_data)
            earned = sum(1 for t in cat_data if f"{prefix}_{t}" in gs.achiev_done)
            self._ach_category_progress[cat_id] = (earned, total)

        # Spezial-Fortschritt
        for group_key, (group_name, items) in self._ach_special_groups.items():
            total = len(items)
            earned = sum(1 for a in items if a[0] in gs.achiev_done)
            self._ach_category_progress[f"spec_{group_key}"] = (earned, total)

    def _get_ach_rarity(self, aid, cat_type):
        """Berechne Seltenheitswert eines Achievements."""
        # Basierend auf Stufe und Kategorie
        if cat_type == "vermoegen":
            tier = int(aid.split("_")[1]) if "_" in aid else 1
            return tier  # 1-6
        tier = int(aid.split("_")[1]) if "_" in aid else 1
        return tier  # 1-5

    def _get_ach_xp_reward(self, aid, cat_type):
        """Berechne XP-Belohnung für Achievement."""
        rarity = self._get_ach_rarity(aid, cat_type)
        rewards = {1: 500, 2: 1000, 3: 2500, 4: 5000, 5: 10000, 6: 25000}
        return rewards.get(rarity, 500)

    def _get_ach_color(self, earned, in_progress=False, is_legendary=False):
        """Farbe für Achievement basierend auf Status."""
        if is_legendary:
            return GOLD
        if earned:
            return GREEN
        if in_progress:
            return ACCENT  # Blau = in Arbeit
        return MUTED  # Grau = gesperrt

    def _get_ach_icon(self, earned, in_progress):
        """Symbol für Achievement-Status."""
        if earned: return "★"
        if in_progress: return "◎"
        return "○"

    def _calculate_ach_progress(self, check_func, gs):
        """Berechne den Fortschritt eines Achievements (0.0 - 1.0)."""
        # Wir prüfen verschiedene Bedingungen
        for aid, title, desc, check in ACHIEV_SPECIAL:
            pass  # Spezial-Checks sind komplex

        # Generische Fortschrittsberechnung für Kategorie-Achievements
        # Versuche aus der check-Funktion einen Fortschritt abzuleiten
        # (vereinfacht: wir schauen auf die Besitzstände)
        if "len(g.props)" in str(check_func):
            total = 500
            current = min(len(gs.props), total)
            return current / total
        if "len(g.cars)" in str(check_func):
            total = 1000
            current = min(len(gs.cars), total)
            return current / total
        if "len(g.car_rentals)" in str(check_func):
            total = 1000
            current = min(len(gs.car_rentals), total)
            return current / total
        if "len(g.comps)" in str(check_func):
            total = 500
            current = min(len(gs.comps), total)
            return current / total
        if "net_worth" in str(check_func):
            # Vermögens-Fortschritt
            max_worths = [100_000, 1_000_000, 10_000_000, 100_000_000, 1_000_000_000, 10_000_000_000]
            nw = gs.net_worth()
            for i, mw in enumerate(reversed(max_worths)):
                if nw >= mw:
                    return 1.0
            return min(1.0, nw / max_worths[0])
        if "stock_value" in str(check_func):
            max_vals = [500_000, 5_000_000, 50_000_000]
            sv = gs.stock_value()
            for i, mv in enumerate(max_vals):
                if sv >= mv: return 1.0
            return min(1.0, sv / max_vals[0])
        if "savings" in str(check_func):
            max_vals = [500_000, 5_000_000]
            sv = gs.savings
            for mv in max_vals:
                if sv >= mv: return 1.0
            return min(1.0, sv / max_vals[0])
        return 0.5  # Fallback

    def _draw_m_achievements(self, bx, by, mw, mh):
        """Modernes Achievement-UI mit 3-spaltigem Layout."""
        gs = self.gs

        # Initialisiere Daten
        self._init_achievement_data()

        # Gesamtstatistik
        total = gs.get_total_achievements()
        earned = gs.get_earned_achievements()
        progress = earned / max(1, total)
        ach_points = sum(self._get_ach_xp_reward(aid, "immo") for aid in gs.achiev_done)

        # Bestimme höchste Seltenheit
        rarity_names = ["Bronze", "Silber", "Gold", "Platin", "Diamant", "Legendär"]
        highest_rarity = 0
        for aid in gs.achiev_done:
            for cat_id, _, cat_data, prefix in self._ach_categories:
                for tier in cat_data:
                    if f"{prefix}_{tier}" == aid:
                        highest_rarity = max(highest_rarity, self._get_ach_rarity(aid, cat_id))
        for group_key, (_, items) in self._ach_special_groups.items():
            for a in items:
                if a[0] in gs.achiev_done:
                    highest_rarity = max(highest_rarity, self._get_ach_rarity(a[0], group_key))
        rarity_label = rarity_names[min(highest_rarity, len(rarity_names) - 1)]

        # ── Obere Übersichtsleiste ──
        header_h = 50
        box(screen, PANEL2, (bx + 10, by + 10, mw - 20, header_h), 8)
        # Linke Seite: Erfolge gesamt
        txt(screen, f"🏆 ERFOLGE  {earned} / {total}", "xl", GOLD, bx + 24, by + 14)
        # Fortschrittsbalken
        bar_x = bx + 320
        bar_w = 180
        progress_bar(screen, bar_x, by + 22, bar_w, 16, progress, GOLD)
        txt(screen, f"{progress * 100:.0f}%", "sm", WHITE, bar_x + bar_w + 8, by + 30, "midleft")
        # Achievement-Punkte
        txt(screen, f"A Punkte: {ach_points}", "md", CYAN, bx + 540, by + 30, "midleft")
        # Seltenheit
        rarity_cols = [MUTED, (192, 192, 192), GOLD, CYAN, PURPLE, GOLD]
        ri = min(highest_rarity, len(rarity_cols) - 1)
        rc = rarity_cols[ri]
        txt(screen, f"Rang: {rarity_label}", "sm", rc, bx + mw - 120, by + 30, "midleft")

        # ── Layout: 3 Spalten ──
        left_w = 150       # Kategorien
        center_w = mw - left_w - 220  # Achievements-Liste
        right_w = 200      # Details
        gap = 8

        left_x = bx + 10
        center_x = left_x + left_w + gap
        right_x = center_x + center_w + gap
        list_y = by + header_h + 20
        list_h = mh - header_h - 30

        # ── LINKE SPALTE: Kategorienliste ──
        box(screen, PANEL, (left_x, list_y, left_w, list_h), 6)
        txt(screen, "KATEGORIEN", "sm", ACCENT, left_x + 10, list_y + 6)

        # Initialisiere ausgewählte Kategorie
        if not hasattr(self, '_ach_selected_cat') or self._ach_selected_cat is None:
            self._ach_selected_cat = "immobilien"
            self._ach_scroll = 0

        cat_y = list_y + 26
        for cat_id, cat_name, cat_data, prefix in self._ach_categories:
            e, t = self._ach_category_progress.get(cat_id, (0, len(cat_data)))
            is_active = (self._ach_selected_cat == cat_id)
            bg = ACCENT if is_active else PANEL2
            box(screen, bg, (left_x + 4, cat_y, left_w - 8, 38), 5)
            txt(screen, cat_name, "sm", WHITE if is_active else MUTED, left_x + 10, cat_y + 6)
            txt(screen, f"{e}/{t}", "xs", ACCENT if is_active else MUTED, left_x + left_w - 14, cat_y + 6, "topright")
            # Mini-Fortschritt
            mini_p = e / max(1, t)
            box(screen, PANEL2, (left_x + 10, cat_y + 26, left_w - 20, 4), 2)
            if mini_p > 0:
                box(screen, ACCENT if is_active else MUTED,
                    (left_x + 10, cat_y + 26, int((left_w - 20) * mini_p), 4), 2)
            cat_y += 42

        # Spezial-Kategorien
        txt(screen, "SPEZIAL", "sm", GOLD, left_x + 10, cat_y + 4)
        cat_y += 20
        for group_key, (group_name, items) in self._ach_special_groups.items():
            spec_id = f"spec_{group_key}"
            e, t = self._ach_category_progress.get(spec_id, (0, len(items)))
            is_active = (self._ach_selected_cat == spec_id)
            bg = ACCENT if is_active else PANEL2
            box(screen, bg, (left_x + 4, cat_y, left_w - 8, 38), 5)
            txt(screen, group_name[:10], "sm", WHITE if is_active else MUTED, left_x + 10, cat_y + 6)
            txt(screen, f"{e}/{t}", "xs", ACCENT if is_active else (120, 120, 120), left_x + left_w - 14, cat_y + 6, "topright")
            mini_p = e / max(1, t)
            box(screen, PANEL2, (left_x + 10, cat_y + 26, left_w - 20, 4), 2)
            if mini_p > 0:
                box(screen, GOLD if is_active else MUTED,
                    (left_x + 10, cat_y + 26, int((left_w - 20) * mini_p), 4), 2)
            cat_y += 42

        # ── MITTLERE SPALTE: Achievement-Karten ──
        box(screen, PANEL, (center_x, list_y, center_w, list_h), 6)

        # Hole die Items für die ausgewählte Kategorie
        current_items = []
        current_prefix = ""
        for cat_id, cat_name, cat_data, prefix in self._ach_categories:
            if self._ach_selected_cat == cat_id:
                current_items = [(f"{prefix}_{t}", info) for t, info in cat_data.items()]
                current_prefix = prefix
                break
        else:
            # Spezial-Kategorie
            for group_key, (group_name, items) in self._ach_special_groups.items():
                if self._ach_selected_cat == f"spec_{group_key}":
                    current_items = [(a[0], {"title": a[1], "desc": a[2], "check": a[3]}) for a in items]
                    current_prefix = group_key
                    break

        if not current_items:
            txt(screen, "Keine Erfolge in dieser Kategorie.", "sm", MUTED,
                center_x + 10, list_y + 20)
        else:
            # Scroll-Parameter
            card_h = 80
            card_gap = 6
            visible_h = list_h - 10
            max_scroll = max(0, len(current_items) * (card_h + card_gap) - visible_h + 10)
            self._ach_scroll = min(self._ach_scroll, max_scroll)

            # Kategorie-Titel in der Mitte
            cat_title = "Spezial"
            for cat_id, cat_name, _, _ in self._ach_categories:
                if cat_id == self._ach_selected_cat:
                    cat_title = cat_name
                    break
            txt(screen, cat_title, "md", ACCENT, center_x + 10, list_y + 6)

            # Clip-Bereich für Achievement-Liste
            clip_rect = pygame.Rect(center_x + 2, list_y + 24, center_w - 4, list_h - 28)
            old_clip = screen.get_clip()
            screen.set_clip(clip_rect)

            for i, (aid, info) in enumerate(current_items):
                # Prüfe ob freigeschaltet
                is_earned = aid in gs.achiev_done
                # Prüfe Fortschritt (vereinfacht)
                in_progress = not is_earned

                # Position berechnen (mit Scroll)
                ry = list_y + 28 + i * (card_h + card_gap) - self._ach_scroll
                if ry + card_h < list_y + 24 or ry > list_y + list_h:
                    continue

                # Karte zeichnen
                card_color = self._get_ach_color(is_earned, in_progress,
                    "Legendär" in info.get("title", ""))
                bg_color = (42, 55, 35) if is_earned else (38, 44, 52) if in_progress else (30, 34, 40)
                border_c = card_color

                box(screen, bg_color, (center_x + 6, ry, center_w - 12, card_h - 2), 6)
                box(screen, border_c, (center_x + 6, ry, center_w - 12, card_h - 2), 6, 1)

                # Linker Rand-Akzent
                pygame.draw.rect(screen, card_color, (center_x + 6, ry, 4, card_h - 2), 0, border_radius=6)

                # Status-Icon
                icon_text = "★" if is_earned else "◎" if in_progress else "○"
                icon_col = card_color
                txt(screen, icon_text, "lg", icon_col, center_x + 20, ry + 12)

                # Titel und Beschreibung
                txt(screen, info["title"], "md", WHITE if is_earned else (200, 200, 200),
                    center_x + 42, ry + 8, "topleft", center_w - 70)
                desc = info.get("desc", "")
                txt(screen, desc, "xs", MUTED, center_x + 42, ry + 32, "topleft", center_w - 70)

                # Fortschrittsbalken
                progress_val = 1.0 if is_earned else 0.3  # Vereinfacht
                bar_h = 6
                bar_w2 = min(150, center_w - 160)
                bar_y = ry + 54
                box(screen, (25, 30, 35), (center_x + 42, bar_y, bar_w2, bar_h), 3)
                if progress_val > 0:
                    box(screen, card_color, (center_x + 42, bar_y, int(bar_w2 * progress_val), bar_h), 3)

                # Prozentsatz
                txt(screen, f"{int(progress_val * 100)}%", "xs", card_color,
                    center_x + 42 + bar_w2 + 6, bar_y + 3, "midleft")

                # XP-Belohnung
                xp = self._get_ach_xp_reward(aid, current_prefix)
                txt(screen, f"+{xp} XP", "xs", CYAN, center_x + 42, ry + card_h - 16)

                if is_earned:
                    txt(screen, "✅", "sm", GREEN, center_x + center_w - 30, ry + 8)

            screen.set_clip(old_clip)

        # ── RECHTE SPALTE: Detail-Ansicht ──
        box(screen, PANEL, (right_x, list_y, right_w, list_h), 6)
        txt(screen, "DETAILS", "sm", ACCENT, right_x + 10, list_y + 6)

        # Zeige Details des zuletzt angeklickten Achievements
        detail_ach = getattr(self, '_ach_detail_target', None)
        if detail_ach:
            aid, info, prefix, is_earned = detail_ach
            detail_y = list_y + 30

            # Titel
            box(screen, PANEL2, (right_x + 6, detail_y, right_w - 12, 50), 6)
            txt(screen, info["title"], "md", WHITE, right_x + 14, detail_y + 6)
            rarity = self._get_ach_rarity(aid, prefix)
            rarity_names_d = {1: "Bronze", 2: "Silber", 3: "Gold", 4: "Platin", 5: "Diamant", 6: "Legendär"}
            rn = rarity_names_d.get(rarity, "Bronze")
            txt(screen, rn, "xs", GOLD if rarity >= 5 else MUTED, right_x + 14, detail_y + 32)
            detail_y += 56

            # Beschreibung
            txt(screen, info.get("desc", ""), "sm", (200, 200, 200),
                right_x + 10, detail_y, "topleft", right_w - 20)
            detail_y += 30

            # Status
            status_text = "✅ FREIGESCHALTET" if is_earned else "🔒 GESPERRT"
            status_col = GREEN if is_earned else RED
            txt(screen, status_text, "sm", status_col, right_x + 10, detail_y)
            detail_y += 24

            # XP Belohnung
            xp = self._get_ach_xp_reward(aid, prefix)
            txt(screen, f"Belohnung: +{xp} XP", "sm", CYAN, right_x + 10, detail_y)
            detail_y += 24

            # Fortschritt Detail
            if is_earned:
                txt(screen, "Fortschritt: 100% ✅", "xs", GREEN, right_x + 10, detail_y)
            else:
                # Zeige Ziel-Werte für verbreitete Achievements
                detail_y = self._draw_ach_detail_progress(aid, prefix, gs, right_x, detail_y, right_w)
        else:
            txt(screen, "Wähle einen Erfolg\naus der Liste aus.", "sm", MUTED,
                right_x + 10, list_y + 40)

        # ── Speichere Kategorie-Klick-Bereiche für handle ──
        self._ach_cat_rects = []
        cat_y = list_y + 26
        for cat_id, cat_name, _, _ in self._ach_categories:
            self._ach_cat_rects.append((cat_id, pygame.Rect(left_x + 4, cat_y, left_w - 8, 38)))
            cat_y += 42
        for group_key, _ in self._ach_special_groups.items():
            spec_id = f"spec_{group_key}"
            self._ach_cat_rects.append((spec_id, pygame.Rect(left_x + 4, cat_y, left_w - 8, 38)))
            cat_y += 42
        # Speichere Achievement-Karten-Bereiche
        self._ach_card_rects = []
        for i, (aid, info) in enumerate(current_items):
            is_earned = aid in gs.achiev_done
            ry2 = list_y + 28 + i * (card_h + card_gap) - self._ach_scroll
            self._ach_card_rects.append((
                aid, info, current_prefix, is_earned,
                pygame.Rect(center_x + 6, ry2, center_w - 12, card_h - 2)
            ))

    def _draw_ach_detail_progress(self, aid, prefix, gs, rx, ry, rw):
        """Zeichne detaillierten Fortschritt für ein Achievement."""
        # Extrahiere Informationen aus dem Achievement-Namen/ID
        txt(screen, "Aktueller Fortschritt:", "xs", MUTED, rx + 10, ry)
        ry += 18

        # Prüfe bekannte Achievement-Typen
        if "len(g.props)" in str(aid) or prefix == "immo":
            current = len(gs.props)
            # Finde Zielwert
            for t, info in ACHIEV_IMMO.items():
                if f"immo_{t}" == aid:
                    # Extrahiere Ziel aus Beschreibung
                    desc = info.get("desc", "")
                    for word in desc.split():
                        if word.isdigit():
                            target = int(word)
                            break
                    else:
                        target = 500
                    break
            else:
                target = 500
            p = min(1.0, current / target)
            txt(screen, f"{current} / {target}", "sm", WHITE, rx + 10, ry)
            progress_bar(screen, rx + 10, ry + 16, rw - 20, 8, p, ACCENT)
            txt(screen, f"{int(p * 100)}%", "xs", ACCENT, rx + rw - 14, ry + 20, "midright")
        elif prefix == "cars":
            current = len(gs.cars)
            for t, info in ACHIEV_CARS.items():
                if f"cars_{t}" == aid:
                    for word in info.get("desc", "").split():
                        if word.isdigit(): target = int(word); break
                    else: target = 1000
                    break
            else: target = 1000
            p = min(1.0, current / target)
            txt(screen, f"{current} / {target} Autos", "sm", WHITE, rx + 10, ry)
            progress_bar(screen, rx + 10, ry + 16, rw - 20, 8, p, ACCENT)
            txt(screen, f"{int(p * 100)}%", "xs", ACCENT, rx + rw - 14, ry + 20, "midright")
        elif prefix in ("filialen",):
            current = len(gs.car_rentals)
            for t, info in ACHIEV_FILIALEN.items():
                if f"filialen_{t}" == aid:
                    for word in info.get("desc", "").split():
                        if word.isdigit(): target = int(word); break
                    else: target = 1000
                    break
            else: target = 1000
            p = min(1.0, current / target)
            txt(screen, f"{current} / {target} Vermietungen", "sm", WHITE, rx + 10, ry)
            progress_bar(screen, rx + 10, ry + 16, rw - 20, 8, p, ACCENT)
            txt(screen, f"{int(p * 100)}%", "xs", ACCENT, rx + rw - 14, ry + 20, "midright")
        elif prefix == "firmen":
            current = len(gs.comps)
            for t, info in ACHIEV_FIRMEN.items():
                if f"firmen_{t}" == aid:
                    for word in info.get("desc", "").split():
                        if word.isdigit(): target = int(word); break
                    else: target = 500
                    break
            else: target = 500
            p = min(1.0, current / target)
            txt(screen, f"{current} / {target} Firmen", "sm", WHITE, rx + 10, ry)
            progress_bar(screen, rx + 10, ry + 16, rw - 20, 8, p, ACCENT)
            txt(screen, f"{int(p * 100)}%", "xs", ACCENT, rx + rw - 14, ry + 20, "midright")
        elif prefix == "vermoegen":
            from decimal import Decimal
            targets = [100_000, 1_000_000, 10_000_000, 100_000_000, 1_000_000_000, 10_000_000_000]
            # Finde richtiges Ziel
            tier = int(aid.split("_")[1]) if "_" in aid else 1
            idx = tier - 1
            current = gs.net_worth()
            target_val = targets[idx] if idx < len(targets) else targets[-1]
            if idx > 0:
                prev = targets[idx - 1]
                p = min(1.0, (current - prev) / (target_val - prev))
            else:
                p = min(1.0, current / target_val)
            p = max(0, p)
            txt(screen, f"{fmt(current)} / {fmt(target_val)}", "sm", WHITE, rx + 10, ry)
            progress_bar(screen, rx + 10, ry + 16, rw - 20, 8, p, GOLD)
            txt(screen, f"{int(p * 100)}%", "xs", GOLD, rx + rw - 14, ry + 20, "midright")
        else:
            txt(screen, "Spezial-Erfolg – Details prüfen", "xs", MUTED, rx + 10, ry)
        return ry + 50

    # ── Statistiken-Modal ──
    def _draw_m_stats_overview(self, bx, by, mw, mh):
        gs = self.gs
        txt(screen, "STATISTIKEN", "xl", GOLD, bx + 16, by + 16)
        data = [
            ("Spielzeit", f"{(gs.year - 2024)} J. {gs.month} M."),
            ("Bargeld", fmt(gs.cash)),
            ("Nettovermögen", fmt(gs.net_worth())),
            ("Monatlicher Cashflow", fmt(gs.net_monthly())),
            ("Immobilien", str(len(gs.props))),
            ("Unternehmen", str(len(gs.comps))),
            ("Autos", str(len(gs.cars))),
            ("Vermietungen", str(len(gs.car_rentals))),
            ("Aktien", fmt(gs.stock_value())),
            ("Festgeld", fmt(gs.savings)),
            ("Schulden", fmt(gs.loan)),
            ("Reputation", str(int(gs.reputation))),
            ("Nachfrage", f"{gs.local_demand:.2f}"),
            ("Konkurrenz", f"{gs.competition:.2f}"),
            ("Trend", f"{gs.market_trend:+.3f}"),
            ("Phase", PHASES[gs.phase]["label"]),
        ]
        col_w = (mw - 40) // 2
        for i, (label, val) in enumerate(data):
            sx = bx + 20 + (i % 2) * col_w
            sy = by + 50 + (i // 2) * 20
            txt(screen, f"{label}:", "sm", MUTED, sx, sy)
            txt(screen, val, "sm", WHITE, sx + 160, sy)

    # ── Log-Modal ──
    def _draw_m_log_view(self, bx, by, mw, mh):
        gs = self.gs
        txt(screen, "AKTIVITÄTSLOG", "xl", GOLD, bx + 16, by + 16)
        kind_col = {"good": GREEN, "bad": RED, "warn": YELLOW, "info": CYAN}
        row_h = 22
        max_rows = (mh - 40) // row_h
        for i, (msg, kind) in enumerate(gs.log[:max_rows]):
            ly = by + 40 + i * row_h
            col = kind_col.get(kind, MUTED)
            pygame.draw.rect(screen, col, (bx + 12, ly + 4, 3, 14))
            txt(screen, msg, "sm", WHITE, bx + 22, ly + 11, "midleft", mw - 40)

    # ── Statistik-Modals (Rental) ──
    def _draw_m_stats_rental(self, bx, by, mw, mh):
        gs = self.gs
        txt(screen, "Autovermietung-Statistik", "lg", GOLD, bx + 16, by + 16)
        if not gs.car_rentals:
            txt(screen, "Keine Vermietungen.", "md", MUTED, bx + 16, by + 60); return
        total = sum(cr["val"] for cr in gs.car_rentals)
        total_profit = sum(cr.get("profit", 0) for cr in gs.car_rentals)
        txt(screen, f"Anzahl: {len(gs.car_rentals)}", "md", WHITE, bx + 16, by + 50)
        txt(screen, f"Gesamtwert: {fmt(total)}", "md", WHITE, bx + 16, by + 74)
        txt(screen, f"Monatsgewinn: {fmt(total_profit)}", "md", GREEN, bx + 16, by + 98)

    # ── Achievement-Popup ──
    def _draw_ach_popup(self):
        title, desc, t0 = self._ach_popup
        elapsed = pygame.time.get_ticks() - t0
        if elapsed > 4000:
            self._ach_popup = None
            return
        alpha = 255 if elapsed < 3000 else int(255 * (1 - (elapsed - 3000) / 1000))
        pw, ph2 = 320, 58
        px, py2 = W - pw - 16, H - ph2 - 28
        s = pygame.Surface((pw, ph2), pygame.SRCALPHA)
        s.fill((80, 40, 140, alpha))
        screen.blit(s, (px, py2))
        pygame.draw.rect(screen, (139, 92, 246), (px, py2, pw, ph2), 1, 8)
        txt(screen, f"Erfolg: {title}", "md", GOLD, px + 12, py2 + 14)
        txt(screen, desc, "xs", MUTED, px + 12, py2 + 38)


# ═══════════════════════════════════════════════════════════
#  BANKROTT-SCREEN
# ═══════════════════════════════════════════════════════════
class BankruptScreen:
    def __init__(self, gs: GS):
        self.gs = gs
        self.btn = Btn(W // 2 - 90, H // 2 + 80, 180, 40, "Neu starten", GREEN, BG, "lg")

    def handle(self, ev):
        self.btn.update(pygame.mouse.get_pos())
        return "restart" if self.btn.hit(ev) else None

    def draw(self, surf):
        surf.fill(BG)
        txt(surf, "BANKROTT", "title", RED, W // 2, H // 2 - 100, "center")
        txt(surf, "Du bist zahlungsunfähig!", "lg", WHITE, W // 2, H // 2 - 50, "center")
        txt(surf, f"Nettovermögen: {fmt(self.gs.net_worth())}", "md", MUTED,
            W // 2, H // 2 - 14, "center")
        txt(surf,
            f"Gespielte Monate: {(self.gs.year - 2024) * 12 + self.gs.month}",
            "md", MUTED, W // 2, H // 2 + 20, "center")
        txt(surf, f"Schwierigkeit: {DIFFICULTY[self.gs.difficulty]['label']}",
            "md", MUTED, W // 2, H // 2 + 50, "center")
        self.btn.draw(surf)


# ═══════════════════════════════════════════════════════════
#  HAUPTSCHLEIFE (Main Loop)
# ═══════════════════════════════════════════════════════════
def main():
    state = "name"
    name_screen = NameScreen()
    game_screen = None
    bankr_screen = None
    gs = None

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.VIDEORESIZE:
                global W, H
                W, H = ev.w, ev.h

            if state == "name":
                result = name_screen.handle(ev)
                if result:
                    name, difficulty = result
                    gs = GS(difficulty=difficulty)
                    gs.name = name
                    diff_label = DIFFICULTY[difficulty]['label']
                    gs.add_log(f"Willkommen, {gs.name}! Modus: {diff_label}", "info")
                    gs.add_log(f"Startkapital: {fmt(gs.cash)}  |  Schulden: {fmt(gs.loan)}", "info")
                    gs.add_news("Spielstart! Strategisch planen und langsam wachsen.")
                    if difficulty == "hard":
                        gs.add_news("Du startest mit Schulden! Tilge sie strategisch!")
                    game_screen = GameScreen(gs)
                    state = "game"

            elif state == "game":
                if ev.type == pygame.MOUSEWHEEL:
                    # Scroll in Modals
                    if game_screen.modal:
                        game_screen._scroll = max(0, game_screen._scroll - ev.y * 30)
                else:
                    result = game_screen.handle(ev)
                    if result == "bankrott":
                        bankr_screen = BankruptScreen(gs)
                        state = "bankrott"

            elif state == "bankrott":
                result = bankr_screen.handle(ev)
                if result == "restart":
                    state = "name"
                    name_screen = NameScreen()

        # Zeichnen
        if state == "name":
            name_screen.draw(screen)
        elif state == "game":
            result = game_screen.maybe_tick()
            if result == "bankrott":
                bankr_screen = BankruptScreen(gs)
                state = "bankrott"
            else:
                game_screen.draw()
        elif state == "bankrott":
            bankr_screen.draw(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
