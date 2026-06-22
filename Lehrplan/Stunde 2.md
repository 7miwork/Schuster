# =============================================================================
# PROJEKT: Weltraum-Koloniespiel
# STUNDE 02: Die Mondkarte und Kamera-Scroll
# =============================================================================
# Was wir heute hinzufügen:
#   - Eine Karte aus Kacheln (Gitter) wird gezeichnet
#   - Mit den Pfeiltasten kann man über die Karte scrollen
#   - Die Kamera merkt sich wo wir hingeschaut haben
#
# WIE WIR ARBEITEN:
#   Wir öffnen unsere Datei von Stunde 1 und fügen den neuen Code ein.
#   Wir fangen NICHT neu an!
#
# NEU IN DIESER STUNDE (mit ### NEU ### markiert):
#   - Kachel-Konstanten (KACHEL_GROESSE, KARTE_BREITE, KARTE_HOEHE)
#   - Kamera-Variablen (kamera_x, kamera_y)
#   - karte_zeichnen() Funktion
#   - kamera_begrenzen() Funktion
#   - Pfeiltasten-Steuerung in ereignisse_verarbeiten()
#
# TIPP FÜR SPÄTER:
#   - Stunde 3: Auf Kacheln klicken → Koloniegebäude platzieren
#   - Stunde 4: Gold und Energie als Ressourcen einführen
#   - Stunde 6: Alien-Gegner erscheinen am Kartenrand
#
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  SPÄTERE DATEISTRUKTUR — das wird aus dieser einen Datei entstehen:     │
# │                                                                         │
# │  Diese Datei             →  Spätere Datei                               │
# │  ────────────────────────────────────────────────                       │
# │  Block EINSTELLUNGEN     →  einstellungen.py                            │
# │  Block KARTE             →  karte.py                                    │
# │  Block GEBAEUDE          →  gebaeude.py      (ab Stunde 3)              │
# │  Block GEGNER            →  gegner.py        (ab Stunde 6)              │
# │  Block HUD               →  hud.py           (ab Stunde 4)              │
# │  Block SPIELSCHLEIFE     →  main.py                                     │
# │                                                                         │
# │  Beim Refactoring (Stunde 10) schneiden wir jeden Block aus             │
# │  und fügen ihn in die jeweilige neue Datei ein. Kein Umbauen!           │
# └─────────────────────────────────────────────────────────────────────────┘
# =============================================================================


import pygame
import sys


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: EINSTELLUNGEN
# Später eigene Datei: einstellungen.py
# Enthält: alle Konstanten und Farben die das ganze Spiel nutzt
# ═════════════════════════════════════════════════════════════════════════════

# -----------------------------------------------------------------------------
# Fenster
# -----------------------------------------------------------------------------
BILD_BREITE         = 800
BILD_HOEHE          = 600
BILD_TITEL          = "Weltraum-Koloniespiel"
BILDER_PRO_SEKUNDE  = 60

# -----------------------------------------------------------------------------
# Karte                                                          ### NEU ###
# TIPP: Diese Werte kommen alle nach einstellungen.py
# -----------------------------------------------------------------------------
KACHEL_GROESSE  = 48    # Jede Kachel ist 48×48 Pixel groß
KARTE_BREITE    = 30    # Die Karte ist 30 Kacheln breit
KARTE_HOEHE     = 20    # Die Karte ist 20 Kacheln hoch
KAMERA_SPEED    = 5     # Wie viele Pixel die Kamera pro Frame scrollt

# -----------------------------------------------------------------------------
# Farben — Fenster und Allgemein
# -----------------------------------------------------------------------------
FARBE_SCHWARZ   = (0,   0,   0  )   # Weltraum-Hintergrund
FARBE_WEISS     = (255, 255, 255)
FARBE_GRAU      = (100, 100, 100)

# -----------------------------------------------------------------------------
# Farben — Mondkarte                                             ### NEU ###
# TIPP: Kommen später in einstellungen.py unter "Farben Karte"
# -----------------------------------------------------------------------------
FARBE_MOND_HELL     = (180, 180, 195)   # Helles Mondgrau
FARBE_MOND_DUNKEL   = (155, 155, 170)   # Etwas dunkleres Mondgrau
FARBE_GITTER_LINIE  = (130, 130, 145)   # Linien zwischen den Kacheln

# -----------------------------------------------------------------------------
# Farben — Gebäude                                    (kommt ab Stunde 3)
# TIPP: Kommen später in einstellungen.py unter "Farben Gebaeude"
# -----------------------------------------------------------------------------
# FARBE_BASIS      = (...)   ← Stunde 3
# FARBE_REAKTOR    = (...)   ← Stunde 3

# -----------------------------------------------------------------------------
# Farben — HUD                                        (kommt ab Stunde 4)
# TIPP: Kommen später in einstellungen.py unter "Farben HUD"
# -----------------------------------------------------------------------------
# FARBE_HUD_HINTERGRUND = (...)   ← Stunde 4
# FARBE_GOLD            = (...)   ← Stunde 4


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: PYGAME INITIALISIERUNG
# Bleibt später in main.py — wird nicht ausgelagert
# ═════════════════════════════════════════════════════════════════════════════

pygame.init()
fenster = pygame.display.set_mode((BILD_BREITE, BILD_HOEHE))
pygame.display.set_caption(BILD_TITEL)
uhr = pygame.time.Clock()


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: SPIELZUSTAND
# Bleibt später in main.py als zentrale Datenzentrale
# Alle anderen Blöcke lesen und schreiben diese Variablen
#
# TIPP: Hier kommt in jeder Stunde mehr dazu:
#   - Stunde 3: liste_gebaeude = []
#   - Stunde 4: gold = 200  |  energie = 100
#   - Stunde 6: liste_gegner = []
#   - Stunde 7: liste_projektile = []
#   - Stunde 8: leben = 10
# ═════════════════════════════════════════════════════════════════════════════

# Kamera-Position (wie weit haben wir schon gescrollt?)          ### NEU ###
# 0, 0 = Blick auf die obere linke Ecke der Mondkarte
kamera_x = 0    # Horizontaler Versatz in Pixeln
kamera_y = 0    # Vertikaler Versatz in Pixeln


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: KARTE
# Später eigene Datei: karte.py
# Enthält: alles was mit dem Zeichnen der Mondkarte zu tun hat
# ═════════════════════════════════════════════════════════════════════════════

def karte_zeichnen():                                           # ### NEU ###
    """
    Zeichnet alle Kacheln der Mondkarte auf den Bildschirm.
    Berücksichtigt dabei die Kamera-Position (kamera_x, kamera_y).

    Wie Kamera-Scroll funktioniert:
        Wir verschieben ALLE Kacheln um (-kamera_x, -kamera_y).
        Wenn kamera_x = 100 → alle Kacheln 100 Pixel nach links gezeichnet
        → Das sieht aus als ob wir 100 Pixel nach rechts geschaut haben!
    """
    # Durch alle Zeilen der Karte gehen (von oben nach unten)
    for zeile in range(KARTE_HOEHE):

        # Durch alle Spalten der Karte gehen (von links nach rechts)
        for spalte in range(KARTE_BREITE):

            # Berechne wo diese Kachel auf dem BILDSCHIRM gezeichnet wird
            # Formel: Gitterposition × Kachelgröße − Kamera-Versatz
            pixel_x = spalte * KACHEL_GROESSE - kamera_x
            pixel_y = zeile  * KACHEL_GROESSE - kamera_y

            # Unsichtbare Kacheln überspringen — spart Rechenzeit!
            # continue = "diese Schleifenrunde überspringen, nächste starten"
            if pixel_x + KACHEL_GROESSE < 0:   continue    # zu weit links
            if pixel_y + KACHEL_GROESSE < 0:   continue    # zu weit oben
            if pixel_x > BILD_BREITE:          continue    # zu weit rechts
            if pixel_y > BILD_HOEHE:           continue    # zu weit unten

            # Abwechselnde Farben — wie ein Schachbrett
            # (zeile + spalte) gerade → hell, ungerade → dunkel
            if (zeile + spalte) % 2 == 0:
                kachel_farbe = FARBE_MOND_HELL
            else:
                kachel_farbe = FARBE_MOND_DUNKEL

            # Das Rechteck für diese Kachel definieren
            # pygame.Rect(x, y, breite, hoehe)
            kachel_rect = pygame.Rect(pixel_x, pixel_y, KACHEL_GROESSE, KACHEL_GROESSE)

            # Kachel ausfüllen
            pygame.draw.rect(fenster, kachel_farbe, kachel_rect)

            # Gitterlinie als Rahmen zeichnen (1 Pixel dick)
            pygame.draw.rect(fenster, FARBE_GITTER_LINIE, kachel_rect, 1)


def kamera_begrenzen():                                         # ### NEU ###
    """
    Verhindert dass die Kamera über den Rand der Mondkarte scrollt.
    Wird aufgerufen nachdem wir kamera_x oder kamera_y verändert haben.
    """
    global kamera_x, kamera_y  # global = wir ändern die globalen Variablen

    # Maximale Scroll-Weite = Kartengröße in Pixeln minus Fenstergröße
    max_kamera_x = KARTE_BREITE * KACHEL_GROESSE - BILD_BREITE
    max_kamera_y = KARTE_HOEHE  * KACHEL_GROESSE - BILD_HOEHE

    # max(0, ...) = nicht unter 0 (linker/oberer Rand)
    # min(max, ...) = nicht über Maximum (rechter/unterer Rand)
    kamera_x = max(0, min(max_kamera_x, kamera_x))
    kamera_y = max(0, min(max_kamera_y, kamera_y))


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: GEBAEUDE
# Später eigene Datei: gebaeude.py
# TIPP: Dieser Block ist jetzt noch leer — kommt komplett in Stunde 3!
#       Dann kommen hier rein:
#         GEBAEUDE_TYPEN = {...}
#         gebaeude_platzieren()
#         gebaeude_entfernen()
#         gebaeude_zeichnen()
# ═════════════════════════════════════════════════════════════════════════════

# → kommt in Stunde 3


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: GEGNER
# Später eigene Datei: gegner.py
# TIPP: Kommt in Stunde 6 — Aliens erscheinen am Kartenrand
#       Dann kommen hier rein:
#         gegner_spawnen()
#         gegner_bewegen()
#         gegner_zeichnen()
# ═════════════════════════════════════════════════════════════════════════════

# → kommt in Stunde 6


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: HUD
# Später eigene Datei: hud.py
# TIPP: Kommt in Stunde 4 — Ressourcenanzeige, Gebäude-Auswahl
#       Dann kommen hier rein:
#         hud_zeichnen()
#         feedback_zeichnen()
# ═════════════════════════════════════════════════════════════════════════════

def info_text_zeichnen():
    """
    Zeigt Kameraposition und Steuerungshinweis.
    TIPP: Diese Funktion wird in Stunde 4 durch hud_zeichnen() ersetzt.
          Dann kommt hud_zeichnen() in den Block HUD oben.
    """
    schrift = pygame.font.Font(None, 22)

    # Kameraposition anzeigen — gut zum Verstehen des Scroll-Prinzips
    kamera_info = schrift.render(
        f"Kamera: x={kamera_x}  y={kamera_y}",
        True, FARBE_WEISS
    )
    fenster.blit(kamera_info, (10, 10))

    steuerung = schrift.render(
        "Pfeiltasten = Scrollen  |  ESC = Beenden",
        True, FARBE_GRAU
    )
    fenster.blit(steuerung, (10, 35))


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: SPIELSCHLEIFE
# Bleibt später in main.py
# Enthält: Ereignisverarbeitung und die Hauptschleife
# ═════════════════════════════════════════════════════════════════════════════

def ereignisse_verarbeiten():
    """
    Verarbeitet alle Eingaben des Spielers.
    Gibt True zurück solange das Spiel läuft, False zum Beenden.

    TIPP: Hier kommen in jeder Stunde neue Eingaben dazu:
      - Stunde 3: Mausklick → Gebäude platzieren
      - Stunde 4: Tasten 1/2/3 → Gebäude-Typ wechseln
    """
    global kamera_x, kamera_y  # Wir ändern die Kamera-Variablen

    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            return False
        if ereignis.type == pygame.KEYDOWN:
            if ereignis.key == pygame.K_ESCAPE:
                return False

        # Maus-Klick                                  (kommt in Stunde 3)
        # TIPP: Hier wird später gebaeude_platzieren() aufgerufen
        # if ereignis.type == pygame.MOUSEBUTTONDOWN:
        #     pass

    # Kamera scrollen mit gehaltenen Pfeiltasten     ### NEU ###
    # get_pressed() = reagiert solange Taste gedrückt ist (nicht nur einmal)
    gedrueckte_tasten = pygame.key.get_pressed()

    if gedrueckte_tasten[pygame.K_LEFT]:
        kamera_x -= KAMERA_SPEED
    if gedrueckte_tasten[pygame.K_RIGHT]:
        kamera_x += KAMERA_SPEED
    if gedrueckte_tasten[pygame.K_UP]:
        kamera_y -= KAMERA_SPEED
    if gedrueckte_tasten[pygame.K_DOWN]:
        kamera_y += KAMERA_SPEED

    # Kamera-Grenzen prüfen nach jeder Bewegung
    kamera_begrenzen()

    return True


def spiel_starten():
    """
    Startet die Hauptspielschleife.
    Diese Funktion bleibt immer in main.py.
    """
    laeuft = True

    while laeuft:

        # --- SCHRITT 1: EINGABEN ---
        laeuft = ereignisse_verarbeiten()

        # --- SCHRITT 2: LOGIK ---
        # TIPP: Ab Stunde 3: gebaeude_update() falls nötig
        # TIPP: Ab Stunde 5: ressourcen_update()
        # TIPP: Ab Stunde 6: gegner_update()
        # TIPP: Ab Stunde 7: projektile_update()
        pass

        # --- SCHRITT 3: ZEICHNEN ---
        # Reihenfolge ist wichtig: was zuletzt gezeichnet wird liegt oben!
        fenster.fill(FARBE_SCHWARZ)     # 1. Schwarzer Weltraum-Hintergrund
        karte_zeichnen()                # 2. Mondkarte          ### NEU ###
        # TIPP: Ab Stunde 3: gebaeude_zeichnen()
        # TIPP: Ab Stunde 6: gegner_zeichnen()
        # TIPP: Ab Stunde 7: projektile_zeichnen()
        info_text_zeichnen()            # 3. Text immer ZULETZT (liegt oben)
        # TIPP: Ab Stunde 4: info_text_zeichnen() → hud_zeichnen()

        pygame.display.flip()
        uhr.tick(BILDER_PRO_SEKUNDE)


# ═════════════════════════════════════════════════════════════════════════════
# PROGRAMMSTART
# Bleibt immer ganz unten in main.py
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    spiel_starten()
    pygame.quit()
    sys.exit()


# =============================================================================
# ENDE STUNDE 2
# Was wir gelernt haben:
#   ✓ Verschachtelte Schleifen (for zeile ... for spalte ...)
#   ✓ Kamera-Prinzip: pixel_x = spalte × KACHEL_GROESSE − kamera_x
#   ✓ continue = Schleifenrunde überspringen
#   ✓ pygame.key.get_pressed() für gehaltene Tasten
#   ✓ global Keyword zum Ändern globaler Variablen
#   ✓ Blöcke mit Namen = spätere Dateien
#
# HÄUFIGE FEHLER:
#   ✗ karte_zeichnen() in der Spielschleife vergessen
#   ✗ global kamera_x, kamera_y vergessen → UnboundLocalError
#   ✗ hintergrund NACH karte zeichnen → Karte wird übermalt!
#
# Was als nächstes kommt (Stunde 3):
#   → BLOCK GEBAEUDE wird befüllt
#   → Mausklick erkennen und Kachel berechnen
#   → Erste Koloniegebäude auf der Mondkarte platzieren
# =============================================================================