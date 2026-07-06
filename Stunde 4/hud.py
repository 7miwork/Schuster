"""
=============================================================================
MODUL: hud.py  —  Weltraum-Koloniespiel  (Stunde 4)
=============================================================================

Was ist ein HUD?
    HUD steht für "Heads-Up Display". Das ist die Anzeige am oberen Bildschirmrand,
    die wichtige Informationen zeigt — wie im Cockpit eines Raumschiffs oder in
    Final Earth 2. Informationen die du immer im Blick haben willst!

Aufgabe dieses Moduls:
    Alles was auf dem Bildschirm angezeigt wird (außer die Karte und Gebäude):
    - Ressourcen-Anzeige: Gold, Energie, Holz
    - Ausgewählter Gebäude-Typ (welches Gebäude wir bauen wollen)
    - Kameraposition und Steuerungshinweise

Konzepte in dieser Datei:
    ✓ Dictionary — Ressourcen als Schlüssel-Wert-Paare
    ✓ Texte zeichnen mit pygame.font.Font und render()
    ✓ Funktionen mit mehreren Parametern
    ✓ Modul-Variablen für gemeinsamen Zustand

Stunde 4 — Was der Spieler lernt:
    ✓ Ressourcen als Dictionary speichern (Gold, Energie, Holz)
    ✓ HUD am oberen Bildschirmrand zeichnen
    ✓ Mehrere Informationen auf dem Bildschirm anzeigen
    ✓ Tasten 1/2/3 für Gebäude-Auswahl (wie in Final Earth 2)
=============================================================================
"""

import pygame


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: MODUL-VARIABLEN
# ═════════════════════════════════════════════════════════════════════════════
# Diese Variablen gehören zum hud-Modul.
# Sie werden einmalig durch hud_initialisieren() gesetzt.
# ═════════════════════════════════════════════════════════════════════════════

_fenster = None   # Das Pygame-Fenster (wird von main.py übergeben)


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: INITIALISIERUNG
# ═════════════════════════════════════════════════════════════════════════════

def hud_initialisieren(fenster_obj):
    """
    Übergibt die Referenz auf das Pygame-Fenster.
    Muss einmalig in main.py aufgerufen werden bevor das HUD gezeichnet wird.
    
    Parameter:
        fenster_obj — das Pygame-Surface (fenster aus main.py)
    """
    global _fenster
    _fenster = fenster_obj


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: RESSOURCEN-ANZEIGE
# ═════════════════════════════════════════════════════════════════════════════
# Zeichnet oben am Bildschirm die aktuellen Ressourcen.
# Jede Ressource hat einen Namen, eine Farbe (als Icon) und einen Wert.
# ═════════════════════════════════════════════════════════════════════════════

def _ressourcen_leiste_zeichnen(ressourcen):
    """
    Zeichnet die Ressourcen-Leiste oben am Bildschirm.
    
    Was ist eine Ressourcen-Leiste?
        In Final Earth 2 siehst du oben immer wie viel Gold, Energie und Nahrung
        du hast. Das ist wichtig für die Planung:
        - Hast du genug Gold für ein neues Gebäude?
        - Reicht die Energie für alle Gebäude?
        
    Die Leiste zeigt:
        - Ein farbiges Icon (Kreis) für jede Ressource
        - Den Namen der Ressource
        - Den aktuellen Wert
    
    Parameter:
        ressourcen — Dictionary mit den aktuellen Ressourcen-Werten
                     z.B. {"gold": 100, "energie": 50, "holz": 30}
    """
    if _fenster is None:
        return   # Noch nicht initialisiert
    
    # Schriftart für die Ressourcen-Anzeige (Größe 24 Pixel)
    schrift = pygame.font.Font(None, 24)
    
    # ── Ressourcen definieren ─────────────────────────────────────────────
    # Jede Ressource hat:
    #   - "name": Anzeige-Name
    #   - "farbe": Farbe für das Icon (Kreis)
    #   - "schluessel": Schlüssel im ressourcen-Dictionary
    ressourcen_typen = [
        {
            "name":     "Gold",
            "farbe":    (255, 215, 0),      # Gold-Gelb
            "icon_pos": (20, 15),            # Position des Kreises
            "text_pos": (35, 12),            # Position des Textes
            "schluessel": "gold",
        },
        {
            "name":     "Energie",
            "farbe":    (255, 200, 50),      # Gelb-Orange
            "icon_pos": (120, 15),
            "text_pos": (135, 12),
            "schluessel": "energie",
        },
        {
            "name":     "Holz",
            "farbe":    (139, 90, 43),       # Braun (Holz-Farbe)
            "icon_pos": (240, 15),
            "text_pos": (255, 12),
            "schluessel": "holz",
        },
    ]
    
    # ── Hintergrund für die Leiste zeichnen ──────────────────────────────
    # Dunkler Balken oben über die volle Breite
    hintergrund_hoehe = 50
    hintergrund_rect = pygame.Rect(0, 0, _fenster.get_width(), hintergrund_hoehe)
    pygame.draw.rect(_fenster, (20, 20, 30), hintergrund_rect)   # Dunkelblau-Schwarz
    pygame.draw.rect(_fenster, (60, 60, 80), hintergrund_rect, 2)   # Hellerer Rahmen
    
    # ── Jede Ressource zeichnen ──────────────────────────────────────────
    for res in ressourcen_typen:
        # Kreis (Icon) zeichnen
        pygame.draw.circle(_fenster, res["farbe"], res["icon_pos"], 10)
        pygame.draw.circle(_fenster, (255, 255, 255), res["icon_pos"], 10, 1)   # Weißer Rahmen
        
        # Wert aus dem Dictionary lesen
        wert = ressourcen.get(res["schluessel"], 0)
        
        # Text rendern: "Gold: 100"
        text = schrift.render(f"{res['name']}: {wert}", True, (255, 255, 255))
        _fenster.blit(text, res["text_pos"])


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: GEBÄUDE-AUSWAHL ANZEIGE
# ═════════════════════════════════════════════════════════════════════════════
# Zeigt welches Gebäude gerade ausgewählt ist.
# ═════════════════════════════════════════════════════════════════════════════

def _gebaeude_auswahl_zeichnen(gebaeude_auswahl, gebaeude_typen):
    """
    Zeigt den aktuell ausgewählten Gebäude-Typ an.
    
    Wie in Final Earth 2:
        Unten rechts siehst du welches Gebäude du gerade baust.
        Mit Tasten 1/2/3 kannst du zwischen den Typen wechseln.
    
    Parameter:
        gebaeude_auswahl — Index des aktuell ausgewählten Gebäude-Typs (0, 1 oder 2)
        gebaeude_typen   — Liste mit allen Gebäude-Typen (aus gebaeude.py)
    """
    if _fenster is None:
        return   # Noch nicht initialisiert
    
    # Sicherstellen dass der Index gültig ist
    if gebaeude_auswahl < 0 or gebaeude_auswahl >= len(gebaeude_typen):
        return
    
    schrift = pygame.font.Font(None, 24)
    
    # ── Gebäude-Daten holen ──────────────────────────────────────────────
    gebaeude_daten = gebaeude_typen[gebaeude_auswahl]
    name = gebaeude_daten["name"]
    farbe = gebaeude_daten["farbe"]
    kuerzel = gebaeude_daten["kuerzel"]
    
    # ── Text erstellen ───────────────────────────────────────────────────
    # "Ausgewählt: Reaktor (Taste 2)"
    text_string = f"Ausgewaehlt: {name} (Taste {gebaeude_auswahl + 1})"
    text = schrift.render(text_string, True, (255, 255, 255))
    
    # ── Position: Mitte unten am Bildschirm ──────────────────────────────
    text_rect = text.get_rect(center=(_fenster.get_width() // 2, 
                                       _fenster.get_height() - 30))
    
    # ── Hintergrund für bessere Lesbarkeit ───────────────────────────────
    hintergrund_padding = 10
    hintergrund_rect = pygame.Rect(
        text_rect.x - hintergrund_padding,
        text_rect.y - hintergrund_padding,
        text_rect.width + 2 * hintergrund_padding,
        text_rect.height + 2 * hintergrund_padding,
    )
    pygame.draw.rect(_fenster, (20, 20, 30, 200), hintergrund_rect)   # Halb-transparent
    pygame.draw.rect(_fenster, farbe, hintergrund_rect, 2)   # Rahmen in Gebäude-Farbe
    
    # ── Text zeichnen ───────────────────────────────────────────────────
    _fenster.blit(text, text_rect)
    
    # ── Kleines Icon (Kürzel) daneben zeichnen ───────────────────────────
    icon_groesse = 20
    icon_x = hintergrund_rect.x + hintergrund_padding
    icon_y = hintergrund_rect.y + hintergrund_padding
    icon_rect = pygame.Rect(icon_x, icon_y, icon_groesse, icon_groesse)
    pygame.draw.rect(_fenster, farbe, icon_rect)
    pygame.draw.rect(_fenster, (255, 255, 255), icon_rect, 1)


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: KAMERA- UND STEUERUNGS-INFORMATIONEN
# ═════════════════════════════════════════════════════════════════════════════
# Zeigt Kameraposition und Bedienhinweise — vom Info-Text aus main.py übernommen.
# ═════════════════════════════════════════════════════════════════════════════

def _kamera_info_zeichnen(kamera_x, kamera_y, karte_breite, karte_hoehe, 
                          kachel_groesse, bild_breite, bild_hoehe):
    """
    Zeigt Kameraposition und Steuerungshinweise an.
    
    Wie in Final Earth 2 siehst du Informationen:
    - Wo bist du gerade auf der Karte? (Kameraposition)
    - Wie bedienst du das Spiel? (Steuerung)
    - Was bedeuten die Farben? (Legende der Bodentypen)
    
    Parameter:
        kamera_x      — aktuelle Kamera-x-Position (aus main.py)
        kamera_y      — aktuelle Kamera-y-Position (aus main.py)
        karte_breite  — Breite der Karte in Kacheln
        karte_hoehe   — Höhe der Karte in Kacheln
        kachel_groesse — Größe einer Kachel in Pixeln
        bild_breite   — Breite des Fensters in Pixeln
        bild_hoehe    — Höhe des Fensters in Pixeln
    """
    if _fenster is None:
        return   # Noch nicht initialisiert
    
    schrift = pygame.font.Font(None, 20)
    
    # ── Kameraposition ──────────────────────────────────────────────────
    # Welche Kachel sehen wir gerade in der oberen linken Ecke?
    kachel_x = max(0, kamera_x // kachel_groesse)
    kachel_y = max(0, kamera_y // kachel_groesse)
    
    kamera_info = schrift.render(
        f"Kamera: Kachel ({kachel_x}, {kachel_y})  |  x={kamera_x}  y={kamera_y}",
        True, (220, 220, 220)
    )
    _fenster.blit(kamera_info, (15, 60))
    
    # ── Karten-Größe und Steuerung ──────────────────────────────────────
    steuerung_info = schrift.render(
        f"Karte: {karte_breite} x {karte_hoehe} Kacheln  |  "
        f"Pfeiltasten scrollen  |  ESC = Beenden",
        True, (150, 150, 160)
    )
    _fenster.blit(steuerung_info, (15, 85))
    
    # ── Legende der Bodentypen ───────────────────────────────────────────
    legende_text = schrift.render(
        "Boden:  Erde  |  Gras  |  Gestein  |  Sand",
        True, (150, 150, 160)
    )
    _fenster.blit(legende_text, (15, 110))


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: HUD ZEICHNEN (HAUPTFUNKTION)
# ═════════════════════════════════════════════════════════════════════════════
# Diese Funktion wird von main.py aufgerufen.
# Sie zeichnet ALLE HUD-Elemente auf den Bildschirm.
# ═════════════════════════════════════════════════════════════════════════════

def hud_zeichnen(ressourcen, gebaeude_auswahl, gebaeude_typen,
                 kamera_x, kamera_y):
    """
    Zeichnet das gesamte HUD (Heads-Up Display) auf den Bildschirm.
    
    Das HUD besteht aus mehreren Teilen:
    1. Ressourcen-Leiste oben (Gold, Energie, Holz)
    2. Ausgewählter Gebäude-Typ (unten mittig)
    3. Kameraposition und Steuerungshinweise (oben links)
    
    Aufruf in main.py:
        hud.hud_zeichnen(ressourcen, gebaeude_auswahl, gebaeude.GEBAEUDE_TYPEN,
                         kamera_x, kamera_y)
    
    Parameter:
        ressourcen        — Dictionary mit Ressourcen: {"gold": 100, "energie": 50, ...}
        gebaeude_auswahl  — Index des ausgewählten Gebäude-Typs (0=Basis, 1=Reaktor, 2=Farm)
        gebaeude_typen    — Liste aller Gebäude-Typen (GEBAEUDE_TYPEN aus gebaeude.py)
        kamera_x          — aktuelle Kamera-x-Position
        kamera_y          — aktuelle Kamera-y-Position
    """
    # ── Teil 1: Ressourcen-Leiste oben zeichnen ─────────────────────────
    # Zeigt Gold, Energie und Holz mit farbigen Icons und Werten
    _ressourcen_leiste_zeichnen(ressourcen)
    
    # ── Teil 2: Ausgewähltes Gebäude anzeigen ───────────────────────────
    # Zeigt unten in der Mitte welches Gebäude wir bauen wollen
    _gebaeude_auswahl_zeichnen(gebaeude_auswahl, gebaeude_typen)
    
    # ── Teil 3: Kameraposition und Steuerung ────────────────────────────
    # Zeigt wo wir sind und wie wir steuern
    # Konstanten aus main.py als Parameter übergeben
    _kamera_info_zeichnen(
        kamera_x, kamera_y,
        60, 40, 48,  # KARTE_BREITE, KARTE_HOEHE, KACHEL_GROESSE aus main.py
        _fenster.get_width() if _fenster else 1000,   # BILD_BREITE
        _fenster.get_height() if _fenster else 700,    # BILD_HOEHE
    )
