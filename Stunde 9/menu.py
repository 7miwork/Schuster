"""
=============================================================================
MODUL: menu.py  —  Weltraum-Koloniespiel  (Stunde 9)
=============================================================================

Was ist ein Baumenü?
    In Final Earth 2 kannst du dir jederzeit alle möglichen Gebäude ansehen.
    Dazu gibt es ein Menü, das über der Karte liegt. Wir bauen so etwas!

    Dieses Modul zeigt mit der Taste TAB ein Baumenü-Overlay, in dem
    ALLE Gebäudetypen gleichzeitig aufgelistet sind:
        - Kürzel (z.B. R für Reaktor)
        - Name
        - Baukosten
        - Die Taste zum Auswählen
        - Schloss-Symbol 🔒 für Gebäude, die noch nicht freigeschaltet sind

Aufgabe dieses Moduls:
    - Ein Overlay mit allen Gebäudetypen zeichnen (halbtransparenter Grund)
    - Den Zustand merken: Ist das Menü offen oder zu? (_menu_offen)
    - Gesperrte Gebäude (noch nicht freigeschaltet) ausgegraut zeigen

Konzepte in dieser Datei (Wiederholung aus anderen Stunden):
    ✓ Modul-Variablen mit _ (private Variablen), z.B. _menu_offen
    ✓ _initialisieren()-Funktion, die das Fenster bekommt
    ✓ Funktionen, die von main.py aufgerufen werden

Stunde 9 — NEU dazu:
    ✓ Neues Modul menu.py für das Baumenü
    ✓ Taste TAB togglet _menu_offen (in main.py)
    ✓ menu_zeichnen() liegt ganz zuletzt in der Zeichenreihenfolge
===========================================================================================
"""

import pygame

# ressourcen.py für die Freischaltungs-Prüfung importieren.
# Das ist KEIN Import-Zirkel: menu.py importiert ressourcen.py,
# aber ressourcen.py importiert menu.py NICHT.
import ressourcen


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: MODUL-VARIABLEN
# ═════════════════════════════════════════════════════════════════════════════
# _fenster    — das Pygame-Fenster (wird von main.py übergeben)
# _menu_offen — ist das Baumenü gerade offen? (True / False)
# ═════════════════════════════════════════════════════════════════════════════

_fenster    = None    # Das Pygame-Fenster
_menu_offen = False   # Das Menü startet geschlossen


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: INITIALISIERUNG
# ═════════════════════════════════════════════════════════════════════════════

def menu_initialisieren(fenster_obj):
    """
    Übergibt die Referenz auf das Pygame-Fenster an dieses Modul.
    Muss einmalig in spiel_starten() (main.py) aufgerufen werden,
    bevor das Menü gezeichnet wird — genau wie bei hud und gebaeude.
    """
    global _fenster
    _fenster = fenster_obj


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: MENÜ ZUSTAND UMSCHALTEN
# ═════════════════════════════════════════════════════════════════════════════

def menu_umschalten():
    """
    Schaltet das Baumenü an oder aus (toggle).

    Diese Funktion wird in main.py aufgerufen, wenn der Spieler TAB drückt.
    True  → wird zu False  (Menü schließt)
    False → wird zu True   (Menü öffnet)
    """
    global _menu_offen
    _menu_offen = not _menu_offen

    if _menu_offen:
        print("Baumenü geöffnet (TAB schließt es wieder)")
    else:
        print("Baumenü geschlossen")


def menu_ist_offen():
    """
    Gibt True zurück, wenn das Baumenü gerade offen ist.
    main.py braucht das evtl., um zu wissen ob das Menü sichtbar ist.
    """
    return _menu_offen


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: BAUMENÜ ZEICHNEN
# ═════════════════════════════════════════════════════════════════════════════
# Das ist die Hauptfunktion dieses Moduls. Sie zeichnet das Overlay
# mit allen Gebäudetypen über die Karte.
# ═════════════════════════════════════════════════════════════════════════════

def menu_zeichnen(gebaeude_typen, gebaeude_wirtschaft, ressourcen_dict=None):
    """
    Zeichnet das Baumenü-Overlay (halbtransparenter Hintergrund + Liste).

    Es werden ALLE Gebäudetypen gleichzeitig angezeigt — nicht nur der
    aktuell ausgewählte. Jede Zeile zeigt:
        - Kürzel und Name
        - Baukosten
        - Die Taste zum Auswählen (Index + 1)
        - 🔒 + Hinweistext, wenn das Gebäude noch nicht freigeschaltet ist

    Neu in Stunde 9 (stufenweise Freischaltung):
        Gebäude, die noch nicht freigeschaltet sind, werden ausgegraut
        angezeigt und mit einem Schloss-Symbol 🔒 markiert. Darunter steht,
        was zum Freischalten noch fehlt (z.B. "braucht 5 Bevölkerung").

    Parameter:
        gebaeude_typen       — Liste aller Gebäude-Typen (aus gebaeude.py)
        gebaeude_wirtschaft  — Liste mit Wirtschaftsdaten (aus ressourcen.py)
        ressourcen_dict      — aktuelle Ressourcen (für die Freischaltung)
    """
    if _fenster is None:
        return   # Noch nicht initialisiert

    # Nur zeichnen, wenn das Menü offen ist!
    if not _menu_offen:
        return

    # ── Halbtransparenter Hintergrund über der ganzen Karte ───────────────
    # Das Menü soll klar sichtbar über der Karte liegen. Mit einer
    # Sonderfläche (Surface) mit Alpha-Kanal machen wir den Hintergrund
    # dunkel, aber trotzdem noch leicht durchsichtig.
    overlay = pygame.Surface(_fenster.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))   # Schwarz mit 63 % Deckkraft
    _fenster.blit(overlay, (0, 0))

    # ── Überschrift ────────────────────────────────────────────────────────
    schrift = pygame.font.Font(None, 32)
    ueberschrift = schrift.render("BAUMENÜ  (TAB schließt)", True, (255, 255, 255))
    _fenster.blit(ueberschrift, (30, 20))

    # Kleinere Schrift für die Zeilen
    schrift_klein = pygame.font.Font(None, 22)

    start_y = 60          # Ab hier beginnen die Zeilen
    zeilen_abstand = 32   # Abstand zwischen zwei Zeilen

    # ── Jede Gebäude-Zeile zeichnen ────────────────────────────────────────
    for i in range(len(gebaeude_typen)):
        typ_daten    = gebaeude_typen[i]
        name         = typ_daten["name"]
        kuerzel      = typ_daten["kuerzel"]
        farbe        = typ_daten["farbe"]

        # Baukosten aus den Wirtschaftsdaten holen
        if i < len(gebaeude_wirtschaft):
            baukosten = gebaeude_wirtschaft[i].get("baukosten", {})
        else:
            baukosten = {}

        # ── Freischaltung prüfen (NEU in Stunde 9) ────────────────────────
        # Ist das Gebäude schon freigeschaltet? Dazu brauchen wir die
        # aktuellen Ressourcen. Wenn wir keine bekommen haben, zeigen wir
        # alles als freigeschaltet an.
        if ressourcen_dict is not None:
            freigeschaltet = ressourcen.ist_freigeschaltet(ressourcen_dict, i)
        else:
            freigeschaltet = True

        # Zeilenfarbe: freigeschaltet → weiß, sonst grau (ausgegraut)
        if freigeschaltet:
            text_farbe = (255, 255, 255)
        else:
            text_farbe = (120, 120, 120)   # Ausgegraut = gesperrt

        # ── Baukosten als String formatieren ──────────────────────────────
        if baukosten:
            kosten_teile = []
            for ress_name, menge in baukosten.items():
                kosten_teile.append(f"{menge} {_ressourcen_name(ress_name)}")
            kosten_string = ", ".join(kosten_teile)
        else:
            kosten_string = "kostenlos"

        # ── Freischaltungs-Hinweis (wenn gesperrt) ────────────────────────
        if not freigeschaltet:
            freischaltung = gebaeude_wirtschaft[i]["freischaltung"]
            braucht_ress = freischaltung["ressource"]
            braucht_menge = freischaltung["menge"]
            hinweis = f"  🔒 braucht {braucht_menge} {_ressourcen_name(braucht_ress)}"
        else:
            hinweis = ""

        # ── Zeile zusammenbauen ────────────────────────────────────────────
        # z.B. "1:  B  Basis     kostenlos"
        # z.B. "7:  W  Wohnhaus  20 Gold, 15 Holz, 10 Stein   🔒 braucht 20 Holz"
        zeile = (f"{i + 1}:  {kuerzel}  {name}"
                 f"     {kosten_string}{hinweis}")

        text_surface = schrift_klein.render(zeile, True, text_farbe)
        _fenster.blit(text_surface, (40, start_y + i * zeilen_abstand))

        # ── Kleines Farbquadrat vor dem Gebäude (wie in der Karte) ────────
        quadrat_x = 25
        quadrat_y = start_y + i * zeilen_abstand + 3
        quadrat_rect = pygame.Rect(quadrat_x, quadrat_y, 12, 12)
        pygame.draw.rect(_fenster, farbe, quadrat_rect)
        pygame.draw.rect(_fenster, (255, 255, 255), quadrat_rect, 1)


def _ressourcen_name(ress_name):
    """
    Kleine Hilfsfunktion — macht aus einem Ressourcen-Schlüssel einen
    schönen deutschen Namen (z.B. "bevoelkerung" → "Bevoelkerung").
    """
    namen = {
        "gold":          "Gold",
        "energie":       "Energie",
        "holz":          "Holz",
        "stein":         "Stein",
        "bevoelkerung":  "Bevoelkerung",
        "nahrung":       "Nahrung",
        "arbeiter":      "Arbeiter",
    }
    return namen.get(ress_name, ress_name)


# =============================================================================
# ENDE STUNDE 9
# =============================================================================
# Wiederholung: Was wir in Stunde 9 in diesem Modul NEU gelernt haben
#
# Stunde 9 (NEU):
#   ✓ Neues Modul menu.py für das Baumenü (Taste TAB)
#   ✓ Modul-Zustand _menu_offen (private Variable)
#   ✓ menu_initialisieren(), menu_umschalten(), menu_ist_offen()
#   ✓ menu_zeichnen() zeigt ALLE Gebäudetypen gleichzeitig
#   ✓ Gesperrte Gebäude werden ausgegraut + mit 🔒 + Hinweistext angezeigt
#
# HÄUFIGE FEHLER zum Merken (Stunde 9):
#   ✗ TAB-Menü blockiert nicht den Mausklick — daran denken!
#     → Das Menü ist nur eine Anzeige. Solange es offen ist, kann man
#       trotzdem bauen. Wenn du das ändern willst, musst du es in main.py
#       abfragen (menu.menu_ist_offen()).
#   ✗ menu_zeichnen() vergessen in der Zeichenreihenfolge einzubauen
#     → Das Menü wäre nie sichtbar. Es muss GANZ ZULETZT gezeichnet werden.
#   ✗ Vergessen, menu_initialisieren() in spiel_starten() aufzurufen
#     → _fenster bleibt None und das Menü zeichnet nichts.
# =============================================================================


