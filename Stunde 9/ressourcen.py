"""
=============================================================================
MODUL: ressourcen.py  —  Weltraum-Koloniespiel  (Stunde 6 + 7)
=============================================================================

Was ist ein Ressourcen-Modul?
    In Final Earth 2 produzieren Gebäude automatisch Ressourcen und
    verbrauchen andere. Ein Reaktor braucht zum Beispiel Holz, um
    Energie zu erzeugen. Dieses Modul verwaltet die Wirtschaft:
    - Baukosten: Was kostet es, ein Gebäude zu bauen?
    - Produktion: Was produziert jedes Gebäude?
    - Verbrauch: Was verbraucht jedes Gebäude?
    - Tick-System: 1× pro Sekunde werden alle Gebäude abgerechnet

Aufgabe dieses Moduls:
    Alles rund um die Wirtschaft des Spiels:
    - GEBAEUDE_WIRTSCHAFT — Wirtschaftsdaten für jeden Gebäudetyp
    - kann_bauen() — Prüft ob genug Ressourcen für ein Gebäude da sind
    - baukosten_abziehen() — Zieht die Baukosten von den Ressourcen ab
    - ressourcen_produzieren() — Lässt alle Gebäude produzieren (1×/Sekunde)

Konzepte in dieser Datei:
    ✓ Dictionary — Wirtschaftsdaten als Schlüssel-Wert-Paare
    ✓ Parallele Listen — GEBAEUDE_WIRTSCHAFT hat denselben Index
      wie GEBAEUDE_TYPEN in gebaeude.py (0=Basis, 1=Reaktor, ...)
    ✓ Funktionen mit Parametern und Return-Werten
    ✓ Werte dürfen nie negativ werden — Sicherheitsprüfung!
    ✓ Tick-System: Nur 1× pro Sekunde rechnen, nicht jeden Frame

Stunde 5 — Was der Spieler gelernt hat:
    ✓ Wirtschaftsdaten pro Gebäude (Baukosten, Produktion, Verbrauch)
    ✓ Prüfen ob Bauen möglich ist (Ressourcen-Voraussetzungen)
    ✓ Baukosten automatisch abziehen
    ✓ Produktion/Verbrauch läuft automatisch (Tick-System)
    ✓ Gebäude produziert nichts, wenn der Rohstoff fehlt
    ✓ Basis kann nur 1× gebaut werden

Stunde 6 — NEU dazu:
    ✓ Zwei neue Gebäude: Holzfäller und Steinmetz
    ✓ Neuer Rohstoff: Stein (vierter Rohstoff im Spiel)
    ✓ Wirtschaftsdaten auf 5 Gebäude erweitert (Indizes 0–4)

Stunde 7 — NEU dazu:
    ✓ Neues Gebäude: Wohnhaus
    ✓ Neuer Rohstoff: Bevölkerung (fünfter Rohstoff)
    ✓ Wirtschaftsdaten auf 7 Gebäude erweitert (Indizes 0–6)

Stunde 9 — NEU dazu:
    ✓ Gebäude abreißen können: ressourcen_zurueckerstatten() gibt nach dem
      Abriss 50 % der Baukosten zurück
    ✓ Stufenweise Freischaltung: Jedes Gebäude hat jetzt ein Feld
      "freischaltung" — es wird erst frei, wenn genug von einer Ressource
      vorhanden ist (z.B. Marktplatz ab 5 Bevölkerung)
    ✓ Neue Funktion ist_freigeschaltet(ressourcen_dict, typ_index)
    ✓ kann_bauen() prüft jetzt zuerst die Freischaltung

Stunde 10 — NEU dazu:
    ✓ Neues Gebäude: Labor (Index 7) — produziert die neue Ressource "forschung"
    ✓ Neuer Rohstoff: Forschungspunkte ("forschung")
    ✓ "freischaltung" kann jetzt ZWEI Arten von Bedingungen haben:
        {"typ": "ressource", ...}  → genug von einer Ressource (wie bisher)
        {"typ": "forschung", ...}  → eine Technologie muss erforscht sein
      Und sogar EINE LISTE mehrerer Bedingungen (alle müssen erfüllt sein)!
    ✓ ist_freigeschaltet() verarbeitet beide Formen automatisch
    ✓ import forschung (für die Technologie-Prüfung) — KEIN Import-Zirkel
=============================================================================
"""

import forschung   # Für die Technologie-Prüfung bei der Freischaltung (Stunde 10)


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: WIRTSCHAFTSDATEN
# ═════════════════════════════════════════════════════════════════════════════
# GEBAEUDE_WIRTSCHAFT ist eine Liste von Dictionaries — GENAU wie
# GEBAEUDE_TYPEN in gebaeude.py. Beide Listen haben denselben Index:
#   Index 0 = Basis       (GEBAEUDE_TYPEN[0])
#   Index 1 = Reaktor     (GEBAEUDE_TYPEN[1])
#   Index 2 = Farm        (GEBAEUDE_TYPEN[2])
#   Index 3 = Holzfäller  (GEBAEUDE_TYPEN[3]) — NEU in Stunde 6
#   Index 4 = Steinmetz   (GEBAEUDE_TYPEN[4]) — NEU in Stunde 6
#   Index 5 = Marktplatz  (GEBAEUDE_TYPEN[5])
#   Index 6 = Wohnhaus    (GEBAEUDE_TYPEN[6]) — NEU in Stunde 7
#   Index 7 = Labor       (GEBAEUDE_TYPEN[7]) — NEU in Stunde 10
#
# Das ist wichtig: Wenn wir später neue Gebäude hinzufügen, müssen
# beide Listen erweitert werden — und die Indizes müssen zusammenpassen!
#
# Jedes Dictionary enthält:
#   "baukosten"      — Dictionary: was kostet der Bau?
#                      z.B. {"gold": 20} bedeutet: kostet 20 Gold
#   "produktion"     — Dictionary: was wird pro Sekunde produziert?
#                      z.B. {"energie": 5} bedeutet: +5 Energie/Sekunde
#   "verbrauch"      — Dictionary: was wird pro Sekunde verbraucht?
#                      z.B. {"holz": 2} bedeutet: −2 Holz/Sekunde
#   "max_anzahl"     — Wie oft kann man dieses Gebäude bauen?
#                      1 = nur einmal (Basis), None = unbegrenzt
#   "freischaltung"  — NEU in Stunde 9, erweitert in Stunde 10: Ab wann kann
#                      man dieses Gebäude bauen?
#                      None = von Anfang an verfügbar.
#                      In Stunde 10 gibt es ZWEI Arten von Bedingungen:
#                        {"typ": "ressource", "ressource": X, "menge": N}
#                          → erst ab N von Ressource X (wie bisher)
#                        {"typ": "forschung", "technologie": "wohnbau"}
#                          → erst wenn die Technologie erforscht ist
#                      Außerdem kann es eine LISTE sein — dann müssen ALLE
#                      Bedingungen erfüllt sein (UND-Verknüpfung):
# ═════════════════════════════════════════════════════════════════════════════

GEBAEUDE_WIRTSCHAFT = [
    # ── Index 0: Basis (das Hauptquartier) ────────────────────────────────
    # Die Basis ist kostenlos, produziert/verbraucht nichts.
    # Sie kann nur 1× pro Spiel gebaut werden (max_anzahl = 1).
    {
        "baukosten":  {},                      # Kostenlos!
        "produktion": {},                      # Produziert nichts
        "verbrauch":  {},                      # Verbraucht nichts
        "max_anzahl": 1,                       # Nur 1× baubar
        "freischaltung": None,                 # NEU St. 9: sofort verfügbar
    },
    # ── Index 1: Reaktor (Energieproduktion) ──────────────────────────────
    # Kostet 20 Gold, produziert +5 Energie, verbraucht −2 Holz + 1 Arbeiter.
    # Kann beliebig oft gebaut werden (max_anzahl = None).
    {
        "baukosten":  {"gold": 20},            # Baukosten
        "produktion": {"energie": 5},          # Produziert Energie
        "verbrauch":  {"holz": 2, "arbeiter": 1},  # Verbraucht Holz + Arbeiter
        "max_anzahl": None,                    # Beliebig oft baubar
        "freischaltung": None,                 # NEU St. 9: sofort verfügbar
    },
    # ── Index 2: Farm (Nahrungsproduktion) ─────────────────────────────────
    # Kostet 15 Gold + 10 Energie, produziert +5 Nahrung,
    # verbraucht −2 Energie + 1 Arbeiter.
    # Kann beliebig oft gebaut werden (max_anzahl = None).
    {
        "baukosten":  {"gold": 15, "energie": 10},   # Baukosten
        "produktion": {"nahrung": 5},                 # Produziert Nahrung
        "verbrauch":  {"energie": 2, "arbeiter": 1}, # Verbraucht Energie + Arbeiter
        "max_anzahl": None,                           # Beliebig oft baubar
        "freischaltung": None,                        # NEU St. 9: sofort verfügbar
    },
    # ── Index 3: Holzfäller (Holzproduktion) — NEU in Stunde 6 ────────────
    # Kostet 10 Gold + 5 Energie, produziert +6 Holz,
    # verbraucht −2 Energie + 1 Arbeiter.
    # Der Holzfäller liefert Holz — das brauchen wir für Reaktoren!
    {
        "baukosten":  {"gold": 10, "energie": 5},    # Baukosten
        "produktion": {"holz": 6},                    # Produziert Holz
        "verbrauch":  {"energie": 2, "arbeiter": 1}, # Verbraucht Energie + Arbeiter
        "max_anzahl": None,                           # Beliebig oft baubar
        "freischaltung": None,                        # NEU St. 9: sofort verfügbar
    },
    # ── Index 4: Steinmetz (Steinproduktion) — NEU in Stunde 6 ────────────
    # Kostet 15 Gold + 10 Energie, produziert +5 Stein,
    # verbraucht −3 Energie + 1 Arbeiter.
    # Stein ist ein neuer Rohstoff — wird für spätere Gebäude wichtig!
    {
        "baukosten":  {"gold": 15, "energie": 10},   # Baukosten
        "produktion": {"stein": 5},                   # Produziert Stein
        "verbrauch":  {"energie": 3, "arbeiter": 1}, # Verbraucht Energie + Arbeiter
        "max_anzahl": None,                           # Beliebig oft baubar
        "freischaltung": None,                        # NEU St. 9: sofort verfügbar
    },
    # ── Index 5: Marktplatz (Steinverarbeitung) ────────────────────────────
    # Kostet 30 Gold + 15 Energie, produziert +12 Gold,
    # verbraucht −5 Stein + 2 Arbeiter.
    {
        "baukosten":  {"gold": 30, "energie": 15},
        "produktion": {"gold": 12},
        "verbrauch":  {"stein": 5, "arbeiter": 2},
        "max_anzahl": None,
        # NEU St. 9 + 10: Marktplatz erst ab 5 Bevölkerung freischalten.
        # Das bleibt eine RESSOURCEN-Bedingung (typ "ressource") — damit man
        # sieht, dass es BEIDE Arten nebeneinander gibt.
        "freischaltung": {"typ": "ressource", "ressource": "bevoelkerung", "menge": 5},
    },
    # ── Index 6: Wohnhaus (Bevölkerungsproduktion) — Limit: 10 ─────────────
    # Kostet 20 Gold + 15 Holz + 10 Stein, produziert +1 Bevölkerung,
    # verbraucht −3 Energie und −2 Nahrung.
    # Maximum 10 Wohnhäuser — dann ist die Kolonie voll!
    # Die Bevölkerung wird als Ressource "bevoelkerung" gespeichert.
    {
        "baukosten":  {"gold": 20, "holz": 15, "stein": 10},  # Baukosten
        "produktion": {"bevoelkerung": 1},                     # Produziert Bevölkerung
        "verbrauch":  {"energie": 3, "nahrung": 2},           # Verbraucht Energie + Nahrung
        "max_anzahl": 10,                                      # Maximum 10 Wohnhäuser
        # Stunde 10: Das Wohnhaus ist per FORSCHUNG gesperrt! Erst wenn die
        # Technologie "wohnbau" erforscht ist (im Forschungsmenü, Taste F),
        # kann man es bauen — egal wie viel Holz man hat.
        "freischaltung": {"typ": "forschung", "technologie": "wohnbau"},
    },
    # ── Index 7: Labor (Forschung) — NEU in Stunde 10 ──────────────────────
    # Das Labor produziert die neue Ressource "forschung" (Forschungspunkte).
    # Damit erforscht man im Forschungsmenü (Taste F) neue Technologien.
    # Mit Startrohstoffen SOLL der Spieler zuerst die Basis-Wirtschaft
    # (Reaktor, Farm, Holzfäller, Steinmetz) aufbauen — deshalb ist das Labor
    # erst ab 8 Bevölkerung UND 50 Gold verfügbar (beide Bedingungen = UND).
    {
        "baukosten":  {"gold": 40, "energie": 20},             # Baukosten
        "produktion": {"forschung": 5},                        # Produziert Forschungspunkte
        "verbrauch":  {"gold": 2, "energie": 3},               # Verbraucht Gold + Energie
        "max_anzahl": None,                                    # Beliebig oft baubar
        # Eine LISTE von Bedingungen: ALLE müssen erfüllt sein (UND)!
        #   a) mindestens 8 Bevölkerung
        #   b) mindestens 50 Gold
        "freischaltung": [
            {"typ": "ressource", "ressource": "bevoelkerung", "menge": 8},
            {"typ": "ressource", "ressource": "gold", "menge": 50},
        ],
    },
]


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: HILFSFUNKTION — Ressourcen prüfen
# ═════════════════════════════════════════════════════════════════════════════
# Diese kleine Hilfsfunktion prüft, ob in einem Dictionary (z.B. ressourcen)
# genug von einer bestimmten Ressource vorhanden ist.
#
# Beispiel: Hat der Spieler genug Gold?
#   hat_genug(ressourcen, "gold", 20) → True wenn ressourcen["gold"] >= 20
#
# Wichtig: Wenn eine Ressource im Dictionary nicht existiert, ist der Wert 0.
# Das verhindert KeyError-Abstürze!
# ═════════════════════════════════════════════════════════════════════════════

def _hat_genug(ressourcen_dict, ressourcen_name, benoetigte_menge):
    """
    Prüft ob von einer Ressource genug vorhanden ist.
    
    Diese Funktion ist "privat" (beginnt mit _) — sie wird NUR innerhalb
    dieses Moduls aufgerufen. Von aussen (aus main.py) sieht man sie nicht.
    
    Parameter:
        ressourcen_dict  — das Ressourcen-Dictionary (z.B. {"gold": 100, ...})
        ressourcen_name  — Name der Ressource (z.B. "gold")
        benoetigte_menge — wie viel wird benötigt? (z.B. 20)
    
    Rückgabe:
        True  — wenn genug vorhanden ist
        False — wenn nicht genug da ist (oder Ressource fehlt)
    """
    # get() holt den Wert oder 0 wenn nicht vorhanden — sicherer als []
    vorhanden = ressourcen_dict.get(ressourcen_name, 0)
    return vorhanden >= benoetigte_menge


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: FREISCHALTUNG  —  NEU in Stunde 9
# ═════════════════════════════════════════════════════════════════════════════
# Die Schüler wollten: Manche Gebäude sollen erst später verfügbar sein,
# wenn man genug von einer Ressource gesammelt hat (Verbesserungsvorschlag 6).
# So wächst die Kolonie Stück für Stück — wie in Final Earth 2!
#
# WICHTIG: Das ist bewusst nur eine EINFACHE Version mit Schwellenwerten.
# Ein volles Forschungs-System kommt laut Roadmap erst in einer späteren
# Stunde als eigenes Modul (forschung.py).
#
# Jedes Gebäude in GEBAEUDE_WIRTSCHAFT hat jetzt das Feld "freischaltung":
#   None                                   → von Anfang an verfügbar
#   {"ressource": "holz", "menge": 20}     → erst ab 20 Holz (aktueller Wert)
# ═════════════════════════════════════════════════════════════════════════════

def ist_freigeschaltet(ressourcen_dict, typ_index):
    """
    Prüft ob ein Gebäude-Typ schon freigeschaltet ist.

    Liest das Feld "freischaltung" aus GEBAEUDE_WIRTSCHAFT.
    Es gibt DREI mögliche Formen:
      None                                    → sofort verfügbar (True)
      {"typ": "ressource", "ressource": X, "menge": N}
                                               → erst ab N von Ressource X
      {"typ": "forschung", "technologie": "id"}
                                               → erst wenn Technologie erforscht
      [ {...}, {...}, ... ] (Liste)            → ALLE Bedingungen müssen erfüllt
                                                sein (UND-Verknüpfung)

    Stunde 10 erweitert das System um den Typ "forschung" und um Listen.

    Parameter:
        ressourcen_dict  — das Ressourcen-Dictionary (z.B. {"gold": 100, ...})
        typ_index        — welcher Gebäude-Typ? (0=Basis, ..., 7=Labor)

    Rückgabe:
        True  — das Gebäude darf gebaut werden
        False — es fehlt noch etwas zum Freischalten
    """
    wirtschaft = GEBAEUDE_WIRTSCHAFT[typ_index]

    # freischaltung ohne .get() wäre riskant, wenn das Feld fehlt
    freischaltung = wirtschaft.get("freischaltung")

    # None bedeutet: direkt verfügbar, keine Bedingung
    if freischaltung is None:
        return True

    # ── Hilfsfunktion: Eine EINZELNE Bedingung prüfen ─────────────────────
    # Gibt True zurück, wenn diese eine Bedingung erfüllt ist.
    def _einzel_pruefen(einzel_bedingung):
        bed_typ = einzel_bedingung.get("typ", "ressource")

        if bed_typ == "forschung":
            # Technologie muss erforscht sein.
            tech_id = einzel_bedingung["technologie"]
            return forschung.ist_technologie_erforscht(tech_id)
        else:
            # Standard: Ressourcen-Menge prüfen (wie in Stunde 9)
            ress_name = einzel_bedingung["ressource"]
            menge     = einzel_bedingung["menge"]
            return _hat_genug(ressourcen_dict, ress_name, menge)

    # ── Jetzt die eigentliche Prüfung ─────────────────────────────────────
    if isinstance(freischaltung, list):
        # Liste von Bedingungen: ALLE müssen erfüllt sein (UND).
        # Beispiel Labor: [bevoelkerung>=8, gold>=50]
        for einzel in freischaltung:
            if not _einzel_pruefen(einzel):
                return False
        return True
    else:
        # Einzelnes Dictionary (wie in Stunde 9)
        return _einzel_pruefen(freischaltung)


def freischaltung_hinweis(ressourcen_dict, typ_index):
    """
    Gibt einen lesbaren Hinweis zurück, warum ein Gebäude NOCH NICHT
    freigeschaltet ist.

    Wird von menu.py (Baumenü) verwendet, um den Sperr-Hinweis korrekt
    anzuzeigen — z.B. "Benötigt Technologie: Wohnbau" statt nur einer
    Rohstoffmenge, wenn die Freischaltung vom Typ "forschung" ist.

    Parameter:
        ressourcen_dict  — das Ressourcen-Dictionary
        typ_index        — welcher Gebäude-Typ?

    Rückgabe:
        Ein deutscher Hinweis-String, z.B.:
          "braucht 5 Bevoelkerung"
          "Benötigt Technologie: Wohnbau"
          "braucht 8 Bevoelkerung, 50 Gold"
        oder "" (wenn keine Freischaltung oder schon frei).
    """
    wirtschaft = GEBAEUDE_WIRTSCHAFT[typ_index]
    freischaltung = wirtschaft.get("freischaltung")

    if freischaltung is None:
        return ""

    # Hilfsfunktion: Eine einzelne Bedingung in Text umwandeln
    def _einzel_text(einzel):
        bed_typ = einzel.get("typ", "ressource")
        if bed_typ == "forschung":
            tech_id = einzel["technologie"]
            return f"Benötigt Technologie: {forschung.technologie_name(tech_id)}"
        else:
            ress_name = einzel["ressource"]
            menge     = einzel["menge"]
            # Schönen deutschen Namen holen (wie im HUD)
            return f"braucht {menge} {_ressourcen_name_fuer_hud(ress_name)}"

    if isinstance(freischaltung, list):
        teile = [_einzel_text(e) for e in freischaltung]
        return ", ".join(teile)
    else:
        return _einzel_text(freischaltung)


def _ressourcen_name_fuer_hud(ress_name):
    """
    Kleine Hilfsfunktion für die Anzeige: macht aus einem Schlüssel wie
    "bevoelkerung" einen schönen Namen "Bevoelkerung".
    """
    namen = {
        "gold": "Gold", "energie": "Energie", "holz": "Holz",
        "stein": "Stein", "bevoelkerung": "Bevoelkerung",
        "nahrung": "Nahrung", "forschung": "Forschungspunkte",
    }
    return namen.get(ress_name, ress_name)


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: ressourcen_zurueckerstatten() — Kostenrückerstattung bei Abriss
# ═════════════════════════════════════════════════════════════════════════════
# NEU in Stunde 9. Wenn der Spieler ein Gebäude abreißt (rechte Maustaste),
# bekommt er 50 % der Baukosten zurück. Diese Funktion fügt das wieder hinzu.
#
# Diese Funktion ist das Gegenstück zu baukosten_abziehen():
#   bauen     → baukosten_abziehen()      (Geld WEG)
#   abreissen → ressourcen_zurueckerstatten() (Geld ZURÜCK)
#
# 50 % abgerundet: kosten // 2 (Ganzzahl-Division rundet automatisch ab).
# ═════════════════════════════════════════════════════════════════════════════

def ressourcen_zurueckerstatten(ressourcen_dict, typ_index):
    """
    Erstattet 50 % der Baukosten eines Gebäudes nach dem Abriss.

    Diese Funktion verändert das ressourcen_dict direkt (fügt hinzu).

    WICHTIG: Nur aufrufen NACHDEM gebaeude_abreissen() einen typ_index
    zurückgegeben hat — sonst würde der Spieler Gold geschenkt bekommen!

    Parameter:
        ressourcen_dict  — das Ressourcen-Dictionary (wird verändert!)
        typ_index        — welcher Gebäude-Typ wurde abgerissen?

    Rückgabe:
        Ein Dictionary mit den erstatteten Beträgen,
        z.B. {"gold": 10, "energie": 5} → +10 Gold und +5 Energie
    """
    wirtschaft = GEBAEUDE_WIRTSCHAFT[typ_index]
    baukosten = wirtschaft["baukosten"]

    rueckerstattung = {}   # Hier sammeln wir, was zurückgegeben wird

    # Gehe jede Ressource der Baukosten durch
    for ress_name, kosten in baukosten.items():

        # 50 % der Baukosten, abgerundet (Ganzzahl-Division // )
        betrag = kosten // 2

        # Kosten von 1 → 0 zurück. Dann gibt es nichts zu erstatten.
        if betrag <= 0:
            continue

        # Betrag zu den Ressourcen wieder hinzufügen
        aktueller_wert = ressourcen_dict.get(ress_name, 0)
        ressourcen_dict[ress_name] = aktueller_wert + betrag

        # Für die Konsolenausgabe in main.py merken
        rueckerstattung[ress_name] = betrag

    return rueckerstattung


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: kann_bauen() — Baukosten prüfen
# ═════════════════════════════════════════════════════════════════════════════
# Bevor ein Gebäude platziert wird, müssen wir prüfen:
#   1. Ist die Basis (Index 0) schon gebaut? → Basis nur 1× erlaubt!
#   2. Sind genug Ressourcen für die Baukosten da?
#   3. Ist das Gebäude schon freigeschaltet? (NEU in Stunde 9)
#
# Diese Funktion gibt True oder False zurück — ein klares Ja/Nein.
# In main.py wird dann entschieden: bei True → bauen, bei False → nichts tun.
# ═════════════════════════════════════════════════════════════════════════════

def kann_bauen(ressourcen_dict, liste_gebaeude, typ_index, boden_typ=None):
    """
    Prüft ob ein Gebäude gebaut werden kann.
    
    Vier Prüfungen:
    0. Freischaltungs-Check (NEU in Stunde 9): Ist das Gebäude schon freigeschaltet?
    1. Basis-Check (Index 0): Darf nur 1× gebaut werden!
    2. Ressourcen-Check: Sind genug Ressourcen für die Baukosten da?
    3. Boden-Check (NEU in Stunde 8): Passt der Bodentyp zum Gebäude?
    
    Parameter:
        ressourcen_dict  — das Ressourcen-Dictionary (z.B. {"gold": 100, ...})
        liste_gebaeude   — Liste aller bereits gebauten Gebäude
        typ_index        — welcher Gebäude-Typ soll gebaut werden?
                           (0=Basis, 1=Reaktor, 2=Farm, 3=Holzfaeller,
                            4=Steinmetz, 5=Marktplatz, 6=Wohnhaus)
        boden_typ        — (Optional) Bodentyp der Kachel (0=Erde, 1=Gras, 2=Gestein, 3=Sand)
                           Wenn None, wird keine Boden-Prüfung durchgeführt.
    
    Rückgabe:
        True  — Bauen ist möglich
        False — Bauen nicht möglich (Grund wird in der Konsole ausgegeben)
    """
    # ── Prüfung 0 (NEU in Stunde 9): Ist das Gebäude schon freigeschaltet? ─
    # Manche Gebäude brauchen erst genug von einer Ressource, z.B. der
    # Marktplatz ab 5 Bevölkerung. Wenn noch nicht freigeschaltet → nicht bauen.
    if not ist_freigeschaltet(ressourcen_dict, typ_index):
        wirtschaft = GEBAEUDE_WIRTSCHAFT[typ_index]
        freischaltung = wirtschaft["freischaltung"]
        ress_name = freischaltung["ressource"]
        menge     = freischaltung["menge"]
        gebaeude_namen = ["Basis", "Reaktor", "Farm", "Holzfaeller",
                          "Steinmetz", "Marktplatz", "Wohnhaus"]
        name = gebaeude_namen[typ_index] if typ_index < len(gebaeude_namen) else "Unbekannt"
        print(f"{name} ist noch nicht freigeschaltet!"
              f" Brauche {menge} {ress_name}")
        return False

    # ── Prüfung 3 (NEU in Stunde 8): Passt der Bodentyp zum Gebäude? ─────
    # Jedes Gebäude hat einen bevorzugten Bodentyp:
    #   - Farm (2) und Holzfäller (3) brauchen GRAS (1)
    #   - Steinmetz (4) braucht GESTEIN (2)
    #   - Basis, Reaktor, Marktplatz, Wohnhaus können überall gebaut werden
    if boden_typ is not None:
        # Definiere welche Gebäude welchen Boden brauchen
        boden_anforderung = {
            2: 1,  # Farm → Gras (Bodentyp 1)
            3: 1,  # Holzfäller → Gras (Bodentyp 1)
            4: 2,  # Steinmetz → Gestein (Bodentyp 2)
        }
        
        # Prüfe ob dieses Gebäude eine Boden-Anforderung hat
        if typ_index in boden_anforderung:
            benoetigter_boden = boden_anforderung[typ_index]
            if boden_typ != benoetigter_boden:
                gebaeude_namen = ["Basis", "Reaktor", "Farm", "Holzfaeller",
                                  "Steinmetz", "Marktplatz", "Wohnhaus"]
                name = gebaeude_namen[typ_index] if typ_index < len(gebaeude_namen) else "Unbekannt"
                boden_namen = {0: "Erde", 1: "Gras", 2: "Gestein", 3: "Sand"}
                benoetigt_name = boden_namen.get(benoetigter_boden, "Unbekannt")
                print(f"{name} kann nur auf {benoetigt_name} gebaut werden!"
                      f" (aktuell: {boden_namen.get(boden_typ, 'Unbekannt')})")
                return False
    
    # ── Prüfung 1: Darf dieses Gebäude nur 1× gebaut werden? ────────────
    # Hol die Wirtschaftsdaten für diesen Gebäude-Typ
    wirtschaft = GEBAEUDE_WIRTSCHAFT[typ_index]
    max_anzahl = wirtschaft["max_anzahl"]
    
    # max_anzahl = 1 bedeutet: Dieses Gebäude darf nur 1× existieren
    if max_anzahl is not None:
        # Zählen wie viele Gebäude dieses Typs schon gebaut wurden
        anzahl_vorhanden = 0
        for gebaeude in liste_gebaeude:
            if gebaeude["typ"] == typ_index:
                anzahl_vorhanden = anzahl_vorhanden + 1
        
        # Wenn schon genug da sind → nicht bauen
        if anzahl_vorhanden >= max_anzahl:
            gebaeude_name = "Basis" if typ_index == 0 else "dieses Gebaeude"
            print(f"Kann {gebaeude_name} nur 1× bauen — bereits vorhanden!")
            return False
    
    # ── Prüfung 2: Sind genug Ressourcen für die Baukosten da? ──────────
    # Baukosten ist selbst ein Dictionary: z.B. {"gold": 20}
    baukosten = wirtschaft["baukosten"]
    
    # Gehe durch alle benötigten Ressourcen in den Baukosten
    for ress_name, benoetigt in baukosten.items():
        if not _hat_genug(ressourcen_dict, ress_name, benoetigt):
            # Gebaeude-Namen aus den Indizes ableiten (ohne Import aus gebaeude.py,
            # um Import-Zirkel zu vermeiden)
            gebaeude_namen = ["Basis", "Reaktor", "Farm", "Holzfaeller",
                              "Steinmetz", "Marktplatz", "Wohnhaus"]
            name = gebaeude_namen[typ_index] if typ_index < len(gebaeude_namen) else "Unbekannt"
            print(f"Nicht genug Ressourcen fuer {name}!"
                  f" Brauche {benoetigt} {ress_name}")
            return False
    
    # ── Beide Prüfungen bestanden → Bauen ist möglich ────────────────────
    return True


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: baukosten_abziehen() — Ressourcen verbrauchen
# ═════════════════════════════════════════════════════════════════════════════
# Nachdem kann_bauen() True zurückgegeben hat, rufen wir diese Funktion auf.
# Sie zieht die Baukosten von den Ressourcen ab.
#
# Wichtig: Diese Funktion darf NUR aufgerufen werden wenn vorher
# kann_bauen() True war! Sonst könnte der Spieler Schulden machen.
# ═════════════════════════════════════════════════════════════════════════════

def baukosten_abziehen(ressourcen_dict, typ_index):
    """
    Zieht die Baukosten eines Gebäudes von den Ressourcen ab.
    
    Diese Funktion verändert das ressourcen_dict direkt (global).
    
    Wichtig: Nur aufrufen NACHDEM kann_bauen() True war!
    
    Parameter:
        ressourcen_dict  — das Ressourcen-Dictionary (wird verändert!)
        typ_index        — welcher Gebäude-Typ wird gebaut?
                           (0=Basis, 1=Reaktor, 2=Farm, 3=Holzfaeller,
                            4=Steinmetz, 5=Marktplatz, 6=Wohnhaus)
    """
    wirtschaft = GEBAEUDE_WIRTSCHAFT[typ_index]
    baukosten = wirtschaft["baukosten"]
    
    # Gebaeude-Namen aus den Indizes ableiten (ohne Import aus gebaeude.py)
    # WICHTIG (Stunde 9): Alle 7 Einträge 0-6, damit auch der Marktplatz (5)
    # richtig benannt wird — sonst stünde dort "Unbekannt".
    gebaeude_namen = ["Basis", "Reaktor", "Farm", "Holzfaeller",
                      "Steinmetz", "Marktplatz", "Wohnhaus"]
    name = gebaeude_namen[typ_index] if typ_index < len(gebaeude_namen) else "Unbekannt"
    
    # Gehe durch alle benötigten Ressourcen und ziehe sie ab
    for ress_name, kosten in baukosten.items():
        aktueller_wert = ressourcen_dict.get(ress_name, 0)
        neuer_wert = aktueller_wert - kosten
        ressourcen_dict[ress_name] = neuer_wert
        
        # Kurze Konsolenausgabe zum Testen — zeigt was abgezogen wurde
        print(f"Baue {name}: -{kosten} {ress_name} (neu: {neuer_wert})")


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: ressourcen_produzieren() — Tick-System
# ═════════════════════════════════════════════════════════════════════════════
# Diese Funktion wird 1× pro Sekunde aufgerufen (nicht jeden Frame!).
# Sie geht durch alle Gebäude und wendet Produktion/Verbrauch an.
#
# Wichtige Regel: Ressourcen dürfen NIEMALS unter 0 fallen!
# Wenn der nötige Rohstoff fehlt (z.B. kein Holz für den Reaktor),
# produziert das Gebäude in DIESEM Tick einfach nichts.
# Das Gebäude "schläft" dann — es arbeitet erst wieder wenn
# genug Rohstoffe da sind.
#
# Neu in Stunde 6: Die Funktion arbeitet automatisch mit allen 5 Gebäudetypen,
# weil sie einfach durch alle Gebäude in liste_gebaeude iteriert.
# Man muss nichts umbauen — neue Indizes funktionieren sofort!
#
# Neu in Stunde 7: Das gilt auch fürs Wohnhaus — kein Code nötig!
# ═════════════════════════════════════════════════════════════════════════════

def ressourcen_produzieren(ressourcen_dict, liste_gebaeude):
    """
    Wendet Produktion und Verbrauch für ALLE Gebäude an.
    
    Diese Funktion wird 1× pro Sekunde (alle 60 Frames) aufgerufen.
    
    So funktioniert ein Tick:
    1. Für jedes Gebäude in liste_gebaeude:
       a. Prüfen: Reichen die Ressourcen für den Verbrauch?
       b. Wenn ja: Verbrauch abziehen + Produktion hinzufügen
       c. Wenn nein: Gebäude produziert NICHTS in diesem Tick
    
    Wichtig: Ressourcenwerte dürfen nie negativ werden!
    
    Parameter:
        ressourcen_dict  — das Ressourcen-Dictionary (wird verändert!)
        liste_gebaeude   — Liste aller Gebäude auf der Karte
    """
    for gebaeude in liste_gebaeude:
        typ_index = gebaeude["typ"]
        wirtschaft = GEBAEUDE_WIRTSCHAFT[typ_index]
        
        # ── Schritt 1: Kann das Gebäude produzieren? ─────────────────────
        # Prüfe ob genug Ressourcen für den Verbrauch da sind.
        # Wenn z.B. der Reaktor 2 Holz braucht, aber nur 1 da ist →
        # dann kann er nicht produzieren.
        
        verbrauch = wirtschaft["verbrauch"]
        kann_produzieren = True
        
        for ress_name, menge in verbrauch.items():
            if not _hat_genug(ressourcen_dict, ress_name, menge):
                kann_produzieren = False
                break   # Sobald eine Ressource fehlt → abbrechen
        
        # ── Schritt 2: Wenn genug Ressourcen → produzieren ──────────────
        if kann_produzieren:
            # Zuerst: Verbrauchte Ressourcen abziehen
            for ress_name, menge in verbrauch.items():
                aktuell = ressourcen_dict.get(ress_name, 0)
                ressourcen_dict[ress_name] = aktuell - menge
                # Sicherheitscheck: Niemals unter 0!
                if ressourcen_dict[ress_name] < 0:
                    ressourcen_dict[ress_name] = 0
            
            # Dann: Produzierte Ressourcen hinzufügen
            produktion = wirtschaft["produktion"]
            for ress_name, menge in produktion.items():
                aktuell = ressourcen_dict.get(ress_name, 0)
                ressourcen_dict[ress_name] = aktuell + menge
        
        else:
            # Gebäude kann nicht produzieren — Grund ausgeben
            # Wir brauchen den Namen aus gebaeude.py... aber wir importieren
            # gebaeude.py hier NICHT (sonst gäbe es einen Import-Zirkel).
            # Stattdessen geben wir nur den Index aus — das reicht zum Testen.
            gebaeude_namen = ["Basis", "Reaktor", "Farm", "Holzfaeller",
                              "Steinmetz", "Marktplatz", "Wohnhaus"]
            name = gebaeude_namen[typ_index] if typ_index < len(gebaeude_namen) else "Unbekannt"
            print(f"{name} (Typ {typ_index}): Nicht genug Rohstoffe "
                  f"→ produziert nichts in diesem Tick")


# =============================================================================
# ENDE STUNDE 9
# =============================================================================
# Wiederholung: Was wir in Stunde 9 in diesem Modul NEU gelernt haben
#
# Stunde 9 (NEU):
#   ✓ GEBAEUDE_WIRTSCHAFT hat weiterhin 7 Einträge (0-6) — nur ergänzt!
#   ✓ Neues Feld "freischaltung" pro Gebäude (None = sofort verfügbar)
#   ✓ ist_freigeschaltet(ressourcen_dict, typ_index) — prüft den Schwellenwert
#   ✓ kann_bauen() prüft jetzt ZUERST die Freischaltung (Prüfung 0)
#   ✓ ressourcen_zurueckerstatten(ressourcen_dict, typ_index) — gibt nach dem
#     Abriss 50 % der Baukosten abgerundet zurück (kosten // 2)
#
# HÄUFIGE FEHLER zum Merken (Stunde 9):
#   ✗ Freischaltung vergessen bei neuen Gebäuden nachzutragen
#     → Beide Listen (GEBAEUDE_TYPEN und GEBAEUDE_WIRTSCHAFT) müssen immer
#       denselben Index und dieselbe Länge haben!
#   ✗ ressourcen_zurueckerstatten() OHNE vorherige Abriss-Prüfung aufrufen
#     → Erst gebaeude_abreissen() → prüfen ob typ_index None ist → DANN erstatten.
#       Sonst gibt es Gold geschenkt.
#   ✗ "freischaltung"-Feld im Wörterbuch vergessen → KeyError beim Zugriff
#     → deshalb nutzen wir wirtschaft.get("freischaltung") (liefert None).
# =============================================================================
