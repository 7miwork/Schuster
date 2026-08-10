"""
=============================================================================
MODUL: forschung.py  —  Weltraum-Koloniespiel  (Stunde 10)
=============================================================================

Was ist Forschung?
    In Final Earth 2 (und vielen Strategie-Spielen) kannst du mit gesammeltem
    Wissen neue Technologien freischalten. Das nennt man "Forschung".
    Du sammelst Forschungspunkte (die Ressource "forschung"), die das
    Labor produziert, und gibst sie hier für neue Technologien aus.

Aufgabe dieses Moduls:
    - Liste TECHNOLOGIEN mit allen Forschungsergebnissen
    - Forschungspunkte ausgeben, um neue Technologien zu erforschen
    - Merken, welche Technologien schon erforscht sind
    - Ein einfaches Forschungsmenü (Taste F) zeichnen

Konzepte in dieser Datei:
    ✓ Modul-Variablen mit _ (private Variablen), z.B. _erforschte_technologien
    ✓ Ein Set () — eine Sammlung OHNE doppelte Einträge
    ✓ Eine Liste von Dictionaries (TECHNOLOGIEN)

Stunde 10 — NEU dazu:
    ✓ Neues Modul forschung.py für das Technologie-System
    ✓ Taste F öffnet das Forschungsmenü
    ✓ Tasten F1/F2/F3 erforschen eine Technologie
===========================================================================================
"""

import pygame

# Für Meldungen im Spiel (z.B. "Nicht genug Forschungspunkte!").
# Das ist KEIN Import-Zirkel: forschung.py importiert hud.py,
# aber hud.py importiert forschung.py NICHT.
import hud


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: TECHNOLOGIEN
# ═════════════════════════════════════════════════════════════════════════════
# TECHNOLOGIEN ist eine Liste von Dictionaries — GENAU wie GEBAEUDE_TYPEN.
# Jede Technologie hat:
#   "id"                     — eindeutiger Name (z.B. "wohnbau")
#   "name"                   — Anzeige-Name
#   "beschreibung"           — kurze Erklärung, was die Technologie bringt
#   "kosten"                 — wie viele Forschungspunkte sie kostet
#   "schaltet_gebaeude_frei" — Index des Gebäudes, das sie freischaltet
#                              (oder None, wenn kein Gebäude freigeschaltet wird)
#   "voraussetzung"          — welche andere Technologie (id) vorher erforscht
#                              sein muss (oder None, wenn keine)
#
# Wichtig: Der Index in "schaltet_gebaeude_frei" muss zum selben Index in
# GEBAEUDE_TYPEN / GEBAEUDE_WIRTSCHAFT passen (6 = Wohnhaus)!
# ═════════════════════════════════════════════════════════════════════════════

TECHNOLOGIEN = [
    {
        "id": "wohnbau",
        "name": "Wohnbau",
        "beschreibung": "Ermoeglicht den Bau von Wohnhaeusern (Taste 7).",
        "kosten": 30,
        "schaltet_gebaeude_frei": 6,     # Index 6 = Wohnhaus
        "voraussetzung": None,
    },
    {
        "id": "produktion",
        "name": "Produktions-Boost",
        "beschreibung": "Alle Produktionsgebaeude produzieren 25% mehr.",
        "kosten": 50,
        "schaltet_gebaeude_frei": None,  # Kein neues Gebäude, nur ein Bonus
        "voraussetzung": "wohnbau",      # Erst muss "wohnbau" erforscht sein!
    },
    {
        "id": "stein_effizienz",
        "name": "Stein-Effizienz",
        "beschreibung": "Steinmetze verbrauchen 1 Energie weniger.",
        "kosten": 25,
        "schaltet_gebaeude_frei": None,  # Nur ein Bonus, kein Gebäude
        "voraussetzung": None,
    },
    {
        "id": "minenbau",
        "name": "Minenbau",
        "beschreibung": "Schaltet die Mine fuer Kohle und Eisen frei (Taste 9).",
        "kosten": 40,
        "schaltet_gebaeude_frei": 8,
        "voraussetzung": "stein_effizienz",
    },
    {
        "id": "reaktor_upgrade",
        "name": "Verbesserter Reaktor",
        "beschreibung": "Reaktoren erzeugen mehr Energie und verbrauchen Kohle.",
        "kosten": 60,
        "schaltet_gebaeude_frei": None,
        "voraussetzung": "minenbau",
    },
]


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: MODUL-VARIABLEN
# ═════════════════════════════════════════════════════════════════════════════

_fenster = None               # Das Pygame-Fenster (wird von main.py übergeben)
_menu_offen = False           # Ist das Forschungsmenü gerade offen?

# Ein Set speichert die IDs aller schon erforschten Technologien.
# Warum ein Set statt einer Liste? Weil ein Set von selbst KEINE doppelten
# Einträge erlaubt — so kann eine Technologie nicht versehentlich zweimal
# erforscht werden!
_erforschte_technologien = set()


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: INITIALISIERUNG
# ═════════════════════════════════════════════════════════════════════════════

def forschung_initialisieren(fenster_obj):
    """
    Übergibt die Referenz auf das Pygame-Fenster an dieses Modul.
    Muss einmalig in spiel_starten() (main.py) aufgerufen werden,
    bevor das Forschungsmenü gezeichnet wird — genau wie bei menu und hud.
    """
    global _fenster
    _fenster = fenster_obj


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: FORSCHUNGSMENÜ ZUSTAND
# ═════════════════════════════════════════════════════════════════════════════

def forschung_menu_umschalten():
    """
    Öffnet oder schließt das Forschungsmenü (toggle).

    Diese Funktion wird in main.py aufgerufen, wenn der Spieler F drückt.
    True  → wird zu False  (Menü schließt)
    False → wird zu True   (Menü öffnet)
    """
    global _menu_offen
    _menu_offen = not _menu_offen

    if _menu_offen:
        print("Forschungsmenü geöffnet (F schließt es wieder)")
    else:
        print("Forschungsmenü geschlossen")


def forschung_menu_ist_offen():
    """
    Gibt True zurück, wenn das Forschungsmenü gerade offen ist.
    main.py braucht das, um die Tasten F1/F2/F3 richtig zuzuordnen.
    """
    return _menu_offen


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: TECHNOLOGIE-FUNKTIONEN
# ═════════════════════════════════════════════════════════════════════════════

def _technologie_finden(technologie_id):
    """
    Hilfsfunktion: Sucht eine Technologie anhand ihrer id in TECHNOLOGIEN.
    Gibt das Dictionary zurück (oder None, wenn nicht gefunden).
    """
    for technologie in TECHNOLOGIEN:
        if technologie["id"] == technologie_id:
            return technologie
    return None


def technologie_name(technologie_id):
    """
    Gibt den passenden Anzeige-Namen zu einer Technologie-id zurück.
    z.B. technologie_name("wohnbau") → "Wohnbau"
    Wird für den Sperr-Hinweis in menu.py / ressourcen.py genutzt.
    """
    technologie = _technologie_finden(technologie_id)
    if technologie is None:
        return technologie_id   # Fallback: einfach die id anzeigen
    return technologie["name"]


def ist_technologie_erforscht(technologie_id):
    """
    Prüft, ob eine Technologie schon erforscht wurde.

    Schaut einfach nach, ob die id im Set _erforschte_technologien steht.
    Diese Funktion wird von ressourcen.py (ist_freigeschaltet) aufgerufen,
    wenn ein Gebäude per "forschung"-Bedingung freigeschaltet werden soll.

    Parameter:
        technologie_id — die id der Technologie, z.B. "wohnbau"

    Rückgabe:
        True  — erforscht
        False — noch nicht erforscht
    """
    return technologie_id in _erforschte_technologien


def technologie_erforschen(technologie_id, ressourcen_dict):
    """
    Versucht eine Technologie zu erforschen.

    Ablauf:
      1. Schon erforscht? → Abbruch (kann man nicht doppelt erforschen).
      2. Voraussetzung erfüllt? → wenn nicht, Abbruch mit Meldung.
      3. Genug Forschungspunkte? → wenn nicht, Abbruch mit Meldung.
      4. Punkte abziehen und id ins Set _erforschte_technologien aufnehmen.

    Diese Funktion verändert das ressourcen_dict (zieht die Punkte ab).

    Parameter:
        technologie_id  — die id der Technologie, z.B. "wohnbau"
        ressourcen_dict — das Ressourcen-Dictionary (wird verändert!)

    Rückgabe:
        True  — die Technologie wurde erforscht
        False — es hat nicht geklappt (Grund wird als Meldung gezeigt)
    """
    global _erforschte_technologien

    # 1. Technologie überhaupt vorhanden?
    technologie = _technologie_finden(technologie_id)
    if technologie is None:
        print(f"Technologie '{technologie_id}' gibt es nicht!")
        return False

    # 2. Schon erforscht? Ein Set verhindert das eigentlich, aber wir
    #    prüfen es trotzdem für eine klare Meldung.
    if technologie_id in _erforschte_technologien:
        print(f"{technologie['name']} ist schon erforscht!")
        hud.meldung_anzeigen(f"{technologie['name']} schon erforscht!")
        return False

    # 3. Voraussetzung erfüllt? Manche Technologien brauchen zuerst eine
    #    andere (z.B. "produktion" braucht erst "wohnbau"). So entsteht
    #    ein einfacher Baum, der für Schüler gut nachvollziehbar bleibt.
    voraussetzung = technologie["voraussetzung"]
    if voraussetzung is not None:
        if voraussetzung not in _erforschte_technologien:
            voraus_name = technologie_name(voraussetzung)
            print(f"{technologie['name']}: Brauche zuerst '{voraus_name}'!")
            hud.meldung_anzeigen(
                f"Brauche zuerst: {voraus_name}!")
            return False

    # 4. Genug Forschungspunkte? Punktestand holen (0, wenn kein Labor).
    kosten = technologie["kosten"]
    punkte = ressourcen_dict.get("forschung", 0)

    if punkte < kosten:
        print(f"{technologie['name']}: Nicht genug Forschungspunkte!"
              f" Brauche {kosten}, habe {punkte}.")
        hud.meldung_anzeigen(
            f"Nicht genug Forschungspunkte! ({kosten} noetig)")
        return False

    # 5. Alles ok → Punkte abziehen und Technologie ins Set aufnehmen
    ressourcen_dict["forschung"] = punkte - kosten
    _erforschte_technologien.add(technologie_id)

    print(f"Technologie '{technologie['name']}' erforscht! "
          f"Punkte uebrig: {ressourcen_dict['forschung']}")
    return True


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: FORSCHUNGSMENÜ ZEICHNEN
# ═════════════════════════════════════════════════════════════════════════════
# Das Forschungsmenü (Taste F) zeigt alle Technologien. Es orientiert sich am
# Baumenü (menu.py), zeichnet aber eine eigene Liste mit dem Technologie-Status.
# ═════════════════════════════════════════════════════════════════════════════

def forschung_menu_zeichnen(ressourcen_dict, gebaeude_typen):
    """
    Zeichnet das Forschungsmenü-Overlay (halbtransparenter Hintergrund + Liste).

    Jede Technologie-Zeile zeigt:
        - Name und Beschreibung
        - Kosten in Forschungspunkten
        - Welches Gebäude sie freischaltet (falls eins)
        - Status:  ✓ erforscht (grün)
                   oder 🔒 gesperrt (grau), wenn die Voraussetzung fehlt
                   oder durchführbar (weiß), wenn man sie erforschen kann
        - Die F-Taste (F1/F2/F3), mit der man sie erforschen kann

    Parameter:
        ressourcen_dict   — aktuelle Ressourcen (um die Punkte anzuzeigen)
        gebaeude_typen    — Liste aller Gebäude-Typen (für den Freischalt-Hinweis)
    """
    if _fenster is None:
        return   # Noch nicht initialisiert

    # Nur zeichnen, wenn das Menü offen ist!
    if not _menu_offen:
        return

    # ── Halbtransparenter Hintergrund über der ganzen Karte ───────────────
    overlay = pygame.Surface(_fenster.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))   # Dunkler, aber leicht durchsichtig
    _fenster.blit(overlay, (0, 0))

    # ── Überschrift + aktueller Punktestand ───────────────────────────────
    schrift = pygame.font.Font(None, 32)
    ueberschrift = schrift.render(
        "FORSCHUNG  (F schließt)", True, (255, 255, 255))
    _fenster.blit(ueberschrift, (30, 20))

    punkte = ressourcen_dict.get("forschung", 0)
    punkte_text = schrift.render(
        f"Forschungspunkte: {punkte}", True, (120, 220, 255))
    _fenster.blit(punkte_text, (30, 46))

    # Kleinere Schrift für die Zeilen
    schrift_klein = pygame.font.Font(None, 20)

    start_y = 85          # Ab hier beginnen die Zeilen
    zeilen_abstand = 45   # Abstand zwischen zwei Zeilen (Platz für 2 Zeilen)

    # ── Jede Technologie-Zeile zeichnen ────────────────────────────────────
    for i, technologie in enumerate(TECHNOLOGIEN):
        tech_id   = technologie["id"]
        name      = technologie["name"]
        beschr    = technologie["beschreibung"]
        kosten    = technologie["kosten"]

        # ── Status bestimmen ───────────────────────────────────────────────
        erforscht = tech_id in _erforschte_technologien
        voraussetzung = technologie["voraussetzung"]
        voraussetzung_erfuellt = (voraussetzung is None or
                                  voraussetzung in _erforschte_technologien)

        if erforscht:
            status_text = "✓ ERFORSCHT"
            status_farbe = (120, 220, 120)     # Grün
        elif not voraussetzung_erfuellt:
            status_text = "🔒 gesperrt"
            status_farbe = (150, 150, 150)     # Grau
        else:
            status_text = "erforschbar"
            status_farbe = (255, 255, 255)     # Weiß

        # ── Welches Gebäude wird freigeschaltet? ───────────────────────────
        gebaeude_index = technologie["schaltet_gebaeude_frei"]
        if gebaeude_index is not None and gebaeude_index < len(gebaeude_typen):
            gebaeude_name = gebaeude_typen[gebaeude_index]["name"]
            gebaeude_info = f" → schaltet frei: {gebaeude_name}"
        else:
            gebaeude_info = ""

        # ── Zeile 1: Nummer, Name, Kosten, Status ──────────────────────────
        # Die Taste zum Erforschen wird aus dem Index abgeleitet (F1, F2, F3).
        taste = f"F{i + 1}"
        if erforscht:
            taste_hinweis = "  (schon erforscht)"
        else:
            taste_hinweis = f"  → druecke {taste}"

        zeile1 = (f"{i + 1}.  {name}  (kostet {kosten} Punkte)"
                  f"  [{status_text}]{taste_hinweis}")

        farbe_zeile = status_farbe

        # ── Zeile 2: Beschreibung und Gebäude-Hinweis ──────────────────────
        zeile2 = beschr + gebaeude_info

        text1 = schrift_klein.render(zeile1, True, farbe_zeile)
        text2 = schrift_klein.render(zeile2, True, (180, 180, 200))

        _fenster.blit(text1, (40, start_y + i * zeilen_abstand))
        _fenster.blit(text2, (40, start_y + i * zeilen_abstand + 20))


# =============================================================================
# ENDE STUNDE 10
# =============================================================================
# Wiederholung: Was wir in Stunde 10 in diesem Modul NEU gelernt haben
#
# Stunde 10 (NEU):
#   ✓ Neues Modul forschung.py für das Technologie-System
#   ✓ TECHNOLOGIEN — eine Liste von Dictionaries (wie GEBAEUDE_TYPEN)
#   ✓ Private Modul-Variablen: _fenster, _menu_offen, _erforschte_technologien
#   ✓ Ein Set() für die erforschten Technologien (verhindert Doppelte)
#   ✓ technologie_erforschen() — prüft Punkte + Voraussetzung, zieht ab, merkt es
#   ✓ ist_technologie_erforscht() / technologie_name() für andere Module
#   ✓ Forschungsmenü (Taste F) mit Status: erforscht / erforschbar / gesperrt
#
# HÄUFIGE FEHLER zum Merken (Stunde 10):
#   ✗ forschung_initialisieren() vergessen in spiel_starten()
#     → _fenster bleibt None und das Forschungsmenü zeichnet nichts!
#   ✗ Import-Zirkel: forschung.py darf NICHT ressourcen.py importieren
#     (denn ressourcen.py importiert forschung.py — das wäre ein Kreis!)
#   ✗ Forschungspunkte abziehen, aber die Technologie NICHT ins Set
#     aufnehmen → man zahlt, bekommt aber nichts!
#   ✗ "voraussetzung" nicht prüfen → man könnte Technologien in falscher
#     Reihenfolge erforschen.
# =============================================================================



