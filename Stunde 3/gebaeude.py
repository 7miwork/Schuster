"""
=============================================================================
MODUL: gebaeude.py  —  Weltraum-Koloniespiel  (Stunde 3)
=============================================================================

Was ist ein Modul?
    Ein Modul ist eine eigene Python-Datei die wir in main.py importieren.
    So können wir den Code übersichtlich aufteilen — jedes Modul hat
    eine klare Aufgabe. In Final Earth 2 gibt es auch viele solche Module!

Aufgabe dieses Moduls:
    Alles was mit Gebäuden zu tun hat:
    - Gebäude-Typen definieren (Basis, Reaktor, Farm)
    - Gebäude platzieren (Mausklick → Kachel)
    - Gebäude zeichnen (auf der Karte)

Konzepte in dieser Datei:
    ✓ Dictionary — eine Sammlung von Schlüssel-Wert-Paaren
    ✓ Liste von Dictionaries — mehrere Gebäude speichern
    ✓ Funktionen mit Parametern
    ✓ Modul-Variablen (Zustand des Moduls)

Stunde 3 — Was der Spieler lernt:
    ✓ Mausklick erkennen (pygame.MOUSEBUTTONDOWN)
    ✓ Bildschirm-Position → Kachel-Position umrechnen
    ✓ Gebäude als Dictionary speichern
    ✓ Duplikate vermeiden (nicht 2 Gebäude auf derselben Kachel)
=============================================================================
"""

import pygame


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: GEBÄUDE-TYPEN
# ═════════════════════════════════════════════════════════════════════════════
# Jeder Gebäude-Typ hat einen Namen, eine Farbe und ein Kürzel.
# In Final Earth 2 gibt es viele verschiedene Gebäudetypen.
#
# Ein Dictionary speichert Daten mit Schlüsseln:
#   { "schluessel": wert, "schluessel2": wert2 }
#
# GEBAEUDE_TYPEN ist eine Liste von Dictionaries:
#   GEBAEUDE_TYPEN[0] = Basis     (Index 0 = erstes Element)
#   GEBAEUDE_TYPEN[1] = Reaktor
#   GEBAEUDE_TYPEN[2] = Farm
# ═════════════════════════════════════════════════════════════════════════════

GEBAEUDE_TYPEN = [
    {
        "name":    "Basis",
        "farbe":   (100, 180, 255),   # Hellblau — das Hauptquartier
        "kuerzel": "B",
    },
    {
        "name":    "Reaktor",
        "farbe":   (255, 200, 50),    # Gelb-Orange — Energieversorgung
        "kuerzel": "R",
    },
    {
        "name":    "Farm",
        "farbe":   (80, 200, 100),    # Grün — Nahrungsversorgung
        "kuerzel": "F",
    },
]


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: MODUL-VARIABLEN
# ═════════════════════════════════════════════════════════════════════════════
# Diese Variablen gehören zum gebaeude-Modul.
# Sie werden einmalig durch gebaeude_initialisieren() gesetzt.
# ═════════════════════════════════════════════════════════════════════════════

_fenster        = None   # Das Pygame-Fenster (wird von main.py übergeben)
_kachel_groesse = 48     # Größe einer Kachel in Pixeln


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: INITIALISIERUNG
# ═════════════════════════════════════════════════════════════════════════════

def gebaeude_initialisieren(fenster_obj, kachel_groesse):
    """
    Übergibt die Referenz auf das Pygame-Fenster und die Kachelgröße.
    Muss einmalig in main.py aufgerufen werden bevor etwas gezeichnet wird.
    
    Parameter:
        fenster_obj    — das Pygame-Surface (fenster aus main.py)
        kachel_groesse — Größe einer Kachel in Pixeln (KACHEL_GROESSE aus main.py)
    """
    global _fenster, _kachel_groesse
    _fenster        = fenster_obj
    _kachel_groesse = kachel_groesse


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: GEBÄUDE PLATZIEREN
# ═════════════════════════════════════════════════════════════════════════════

def gebaeude_platzieren(liste_gebaeude, typ_index, kachel_x, kachel_y):
    """
    Platziert ein neues Gebäude auf der Karte — wenn die Kachel frei ist.
    
    Was ist ein Dictionary?
        Ein Dictionary speichert zusammengehörige Daten:
        { "typ": 0, "kachel_x": 5, "kachel_y": 3 }
        So wie eine Karteikarte mit mehreren Feldern.
    
    Duplikate vermeiden:
        Bevor wir ein Gebäude platzieren prüfen wir ob auf dieser Kachel
        bereits ein Gebäude steht. Wenn ja → nichts tun.
    
    Parameter:
        liste_gebaeude — die Gebäude-Liste aus main.py (wird verändert!)
        typ_index      — welcher Gebäude-Typ (0=Basis, 1=Reaktor, 2=Farm)
        kachel_x       — x-Position auf der Karte (in Kacheln)
        kachel_y       — y-Position auf der Karte (in Kacheln)
    """
    # ── Schritt 1: Prüfen ob die Kachel schon belegt ist ─────────────────
    for gebaeude in liste_gebaeude:
        if gebaeude["kachel_x"] == kachel_x and gebaeude["kachel_y"] == kachel_y:
            print(f"Kachel ({kachel_x}, {kachel_y}) ist bereits belegt!")
            return
    
    # ── Schritt 2: Neues Gebäude als Dictionary erstellen ─────────────────
    # Ein Dictionary mit allen wichtigen Informationen des Gebäudes
    neues_gebaeude = {
        "typ":      typ_index,   # Index in GEBAEUDE_TYPEN
        "kachel_x": kachel_x,   # Position auf der Karte (Spalte)
        "kachel_y": kachel_y,   # Position auf der Karte (Zeile)
    }
    
    # ── Schritt 3: Zur Liste hinzufügen ───────────────────────────────────
    liste_gebaeude.append(neues_gebaeude)
    
    name = GEBAEUDE_TYPEN[typ_index]["name"]
    print(f"{name} auf Kachel ({kachel_x}, {kachel_y}) platziert!")


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: GEBÄUDE ZEICHNEN
# ═════════════════════════════════════════════════════════════════════════════

def gebaeude_zeichnen(liste_gebaeude, kamera_x, kamera_y):
    """
    Zeichnet alle platzierten Gebäude auf der Karte.
    
    Wie bei der Karte:
        pixel_x = kachel_x * kachel_groesse - kamera_x
        pixel_y = kachel_y * kachel_groesse - kamera_y
    
    Jedes Gebäude wird als farbiges Rechteck mit einem Kürzel gezeichnet.
    
    Parameter:
        liste_gebaeude — Liste aller platzierten Gebäude
        kamera_x       — aktuelle Kamera-x-Position (aus main.py)
        kamera_y       — aktuelle Kamera-y-Position (aus main.py)
    """
    if _fenster is None:
        return   # Noch nicht initialisiert
    
    schrift = pygame.font.Font(None, 28)
    
    for gebaeude in liste_gebaeude:
        
        # ── Bildschirm-Position berechnen (wie in karte_zeichnen) ─────────
        pixel_x = gebaeude["kachel_x"] * _kachel_groesse - kamera_x
        pixel_y = gebaeude["kachel_y"] * _kachel_groesse - kamera_y
        
        # ── Unsichtbare Gebäude überspringen ──────────────────────────────
        if pixel_x + _kachel_groesse < 0:   continue
        if pixel_y + _kachel_groesse < 0:   continue
        if pixel_x > _fenster.get_width():  continue
        if pixel_y > _fenster.get_height(): continue
        
        # ── Gebäude-Typ-Daten holen ───────────────────────────────────────
        typ_daten = GEBAEUDE_TYPEN[gebaeude["typ"]]
        farbe     = typ_daten["farbe"]
        kuerzel   = typ_daten["kuerzel"]
        
        # ── Gebäude-Rechteck zeichnen ─────────────────────────────────────
        # Etwas kleiner als die Kachel → man sieht den Boden darunter
        abstand      = 4
        gebaeude_rect = pygame.Rect(
            pixel_x + abstand,
            pixel_y + abstand,
            _kachel_groesse - 2 * abstand,
            _kachel_groesse - 2 * abstand,
        )
        pygame.draw.rect(_fenster, farbe, gebaeude_rect)
        pygame.draw.rect(_fenster, (255, 255, 255), gebaeude_rect, 2)   # weißer Rahmen
        
        # ── Kürzel in der Mitte des Gebäudes ──────────────────────────────
        text_surface = schrift.render(kuerzel, True, (20, 20, 20))
        text_rect    = text_surface.get_rect(center=gebaeude_rect.center)
        _fenster.blit(text_surface, text_rect)