# =============================================================================
# PROJEKT: Weltraum-Koloniespiel
# STUNDE 02: Die Planeten-Oberfläche — wie Final Earth 2
# =============================================================================
#
# WORUM GEHT ES IN DIESEM SPIEL?
# ───────────────────────────────
# Du landest mit einem Raumschiff auf einem fremden Planeten.
# Deine Aufgabe: Baue eine Kolonie auf!
# - Erkunde die Planeten-Oberfläche
# - Finde gute Stellen für deine Gebäude
# - Baue die Kolonie immer weiter aus
#
# Dieses Spiel ist inspiriert von "Final Earth 2" — einem beliebten
# Kolonie-Aufbauspiel. In Final Earth 2 startest du auf einem fremden
# Planeten und musst aus dem Nichts eine blühende Kolonie erschaffen.
#
# WAS WIR HEUTE BAUEN:
# ────────────────────
# - Eine riesige Planeten-Oberfläche mit verschiedenen Böden
#   (Erde, Gras, Gestein, Sand) — wie in Final Earth 2
# - Einen Sternenhimmel im Weltraum-Hintergrund
# - Kamerasteuerung mit Pfeiltasten zum Erkunden der Karte
# - Eine zufällige Karten-Generation — jedes Spiel ist anders!
#
# WIE WIR ARBEITEN:
# ─────────────────
# Wir öffnen die Datei von Stunde 1 und fügen nach und nach neuen
# Code ein. Wir fangen NICHT neu an!
#
# ZUM NACHSCHLAGEN:
# ─────────────────
# Die fertige Datei liegt unter:
#   Unterricht/Schuster/Test/main.py
#
# Der Code in dieser .md Datei ist für den Lehrplan gedacht.
# Erklärungen stehen in den Kommentaren (### ... ###).
#
# =============================================================================
# INHALTSVERZEICHNIS
# =============================================================================
# 1. Was ist neu in Stunde 2?        —— Seite 3
# 2. Die große Übersicht              —— Seite 4
# 3. Konzepte & Erklärungen            —— Seite 5
# 4. Gemeinsamer Code                  —— Seite 8
# 5. Aufgaben für Schüler              —— Seite 16
# 6. Häufige Fehler & Lösungen        —— Seite 19
# 7. Zusammenfassung                   —— Seite 20
# =============================================================================


# =============================================================================
# 1. WAS IST NEU IN STUNDE 2?
# =============================================================================
#
# ┌────────────────────────────────────────────────────────────────────────┐
# │ STUNDE 1                    │  STUNDE 2                               │
# │ (hatten wir schon)          │  (kommt heute dazu)                     │
# ├────────────────────────────────────────────────────────────────────────┤
# │ Schwarzes Fenster           │  + Sterne im Hintergrund                │
# │ Info-Text                   │  + Planeten-Oberfläche (Karte)          │
# │ Spiel-Schleife              │  + 4 verschiedene Bodentypen            │
# │ ESC zum Beenden             │  + Pfeiltasten zum Scrollen             │
# │                             │  + Zufällige Karten-Generation          │
# │                             │  + Kamera (Position merken)             │
# │                             │  + Legende im HUD                       │
# └────────────────────────────────────────────────────────────────────────┘
#
# NEUE KONZEPTE in dieser Stunde:
# ────────────────────────────────
# 1. 2D-Arrays (Listen in Listen)
# 2. Verschachtelte for-Schleifen
# 3. Kamera-Prinzip (Position - Versatz)
# 4. Zufallszahlen mit random
# 5. Dictionaries (Wörterbücher)
# 6. continue (Schleifenrunde überspringen)
# 7. global (globale Variablen ändern)


# =============================================================================
# 2. DIE GROSSE ÜBERSICHT
# =============================================================================
#
# So sieht unser komplettes Programm aus. Jeder Block hat eine Aufgabe.
# Später wird jeder Block in eine eigene Datei ausgelagert!
#
# ┌─────────────────────────────────────────────────────────────────────┐
# │  UNSERE main.py                                                     │
# │                                                                     │
# │  ┌─────────────────────────────────────────────────────────────┐    │
# │  │ BLOCK: KONSTANTEN (EINSTELLUNGEN)                         │    │
# │  │   → BILD_BREITE, KACHEL_GROESSE, FARBEN, ...              │    │
# │  │   → Spätere Datei: einstellungen.py                       │    │
# │  └─────────────────────────────────────────────────────────────┘    │
# │                               ↓                                     │
# │  ┌─────────────────────────────────────────────────────────────┐    │
# │  │ BLOCK: PYGAME INITIALISIERUNG                              │    │
# │  │   → pygame.init(), Fenster, Uhr                            │    │
# │  │   → Bleibt in main.py                                      │    │
# │  └─────────────────────────────────────────────────────────────┘    │
# │                               ↓                                     │
# │  ┌─────────────────────────────────────────────────────────────┐    │
# │  │ BLOCK: SPIELZUSTAND                                        │    │
# │  │   → kamera_x, kamera_y, karten_daten, sterne_liste         │    │
# │  │   → Bleibt in main.py (Daten-Zentrale)                     │    │
# │  └─────────────────────────────────────────────────────────────┘    │
# │                               ↓                                     │
# │  ┌─────────────────────────────────────────────────────────────┐    │
# │  │ BLOCK: PLANETEN-GENERIERUNG                                │    │
# │  │   → karte_generieren(), sterne_generieren()                │    │
# │  │   → Spätere Datei: planet.py                               │    │
# │  └─────────────────────────────────────────────────────────────┘    │
# │                               ↓                                     │
# │  ┌─────────────────────────────────────────────────────────────┐    │
# │  │ BLOCK: KARTE ZEICHNEN                                      │    │
# │  │   → karte_zeichnen(), kamera_begrenzen()                   │    │
# │  │   → Spätere Datei: karte.py                                │    │
# │  └─────────────────────────────────────────────────────────────┘    │
# │                               ↓                                     │
# │  ┌─────────────────────────────────────────────────────────────┐    │
# │  │ BLOCK: WELTRAUM-HINTERGRUND                                │    │
# │  │   → hintergrund_zeichnen()                                 │    │
# │  │   → Bleibt in main.py (später in hud.py)                   │    │
# │  └─────────────────────────────────────────────────────────────┘    │
# │                               ↓                                     │
# │  ┌─────────────────────────────────────────────────────────────┐    │
# │  │ BLOCK: HUD / ANZEIGE                                       │    │
# │  │   → info_text_zeichnen()                                   │    │
# │  │   → Spätere Datei: hud.py                                  │    │
# │  └─────────────────────────────────────────────────────────────┘    │
# │                               ↓                                     │
# │  ┌─────────────────────────────────────────────────────────────┐    │
# │  │ BLOCK: EREIGNISSE VERARBEITEN                              │    │
# │  │   → ereignisse_verarbeiten()                               │    │
# │  │   → Bleibt in main.py                                      │    │
# │  └─────────────────────────────────────────────────────────────┘    │
# │                               ↓                                     │
# │  ┌─────────────────────────────────────────────────────────────┐    │
# │  │ BLOCK: SPIELSCHLEIFE                                       │    │
# │  │   → spiel_starten()                                        │    │
# │  │   → Bleibt in main.py                                      │    │
# │  └─────────────────────────────────────────────────────────────┘    │
# │                               ↓                                     │
# │  ┌─────────────────────────────────────────────────────────────┐    │
# │  │ BLOCK: PROGRAMMSTART                                       │    │
# │  │   → if __name__ == "__main__":                             │    │
# │  │   → Bleibt immer ganz unten!                               │    │
# │  └─────────────────────────────────────────────────────────────┘    │
# └─────────────────────────────────────────────────────────────────────┘


# =============================================================================
# 3. KONZEPTE & ERKLÄRUNGEN
# =============================================================================
#
# ─────────────────────────────────────────────────────────────────────────────
# KONZEPT 1: 2D-ARRAYS (Listen in Listen)
# ─────────────────────────────────────────────────────────────────────────────
#
# Stell dir ein Schachbrett vor. Es hat 8 Reihen (Zeilen) und 8 Spalten.
# Jedes Feld hat eine Position: Reihe 3, Spalte 5.
#
# In Python speichern wir so ein Gitter als "Liste von Listen":
#
#       karten_daten = [
#           [0, 0, 0, 0, 0, 0],   ← Zeile 0
#           [0, 0, 0, 0, 0, 0],   ← Zeile 1
#           [0, 0, 1, 0, 0, 0],   ← Zeile 2  (Hier ist eine 1 = Gras)
#           [0, 0, 0, 0, 0, 0],   ← Zeile 3
#           [0, 0, 0, 0, 0, 0],   ← Zeile 4
#       ]
#
# karten_daten[2][2] → Zeile 2, Spalte 2 → 1 (Gras)
# karten_daten[0][5] → Zeile 0, Spalte 5 → 0 (Erde)
#
# WICHTIG: Zuerst die ZEILE, dann die SPALTE!
#           karten_daten[ZEILE][SPALTE]
#
# Die Zahlen bedeuten:
#   0 = Erde      (häufigster Boden)
#   1 = Gras      (fruchtbar)
#   2 = Gestein   (Felsen)
#   3 = Sand      (Wüste)
#
#
# ─────────────────────────────────────────────────────────────────────────────
# KONZEPT 2: VERSCHACHTELTE for-SCHLEIFEN
# ─────────────────────────────────────────────────────────────────────────────
#
# Um auf jedes Feld eines Gitters zuzugreifen, brauchen wir zwei Schleifen:
# Eine für die Zeilen (y-Richtung) und eine für die Spalten (x-Richtung).
#
#   for zeile in range(KARTE_HOEHE):          # Äußere Schleife: Zeilen
#       for spalte in range(KARTE_BREITE):    # Innere Schleife: Spalten
#           # Hier sind wir auf Feld (zeile, spalte)
#           mache_irgendwas_mit(position)
#
# Stell es dir vor wie beim Frühstück:
# Du hast 4 Toast-Scheiben (Zeilen). Auf jede Scheibe kommen 3 Aufstriche
# (Spalten): Butter, Marmelade, Honig.
#
#   for scheibe in range(4):          # 4 Scheiben Toast
#       for aufstrich in range(3):    # 3 Aufstriche pro Scheibe
#           toast_bestreichen(scheibe, aufstrich)
#
# Innere Schleife läuft KOMPLETT durch, bevor äußere weitergeht!
# Ergebnis: 4 × 3 = 12 Aktionen.
#
#
# ─────────────────────────────────────────────────────────────────────────────
# KONZEPT 3: KAMERA-PRINZIP
# ─────────────────────────────────────────────────────────────────────────────
#
# Stell dir vor: Du hast eine riesige Zeitung auf dem Tisch (unsere Karte).
# Mit einer Lupe schaust du darauf (unser Fenster). Du kannst die Lupe
# verschieben — das ist die Kamera!
#
# Die Kamera merkt sich, wo sie gerade hinschaut:
#   kamera_x = wie weit rechts sind wir?
#   kamera_y = wie weit unten sind wir?
#
# Wenn eine Kachel gezeichnet wird, rechnen wir:
#
#   pixel_x = spalte * KACHEL_GROESSE - kamera_x
#   pixel_y = zeile  * KACHEL_GROESSE - kamera_y
#
# Beispiel:
#   Kachel (5, 3) bei Kachelgröße 48
#   Kamera bei (100, 50)
#
#   pixel_x = 5 * 48 - 100 = 240 - 100 = 140  (140 Pixel von links)
#   pixel_y = 3 * 48 - 50  = 144 - 50  = 94   (94 Pixel von oben)
#
# Wenn die Kamera nach rechts geht (kamera_x wird größer),
# rutscht die Kachel auf dem Bildschirm nach links.
# Das sieht aus als ob du nach rechts schaust!
#
# Kamera-Begrenzung:
#   Die Kamera darf nicht über den Rand der Karte gehen.
#   max_kamera_x = Kartengröße - Fenstergröße
#   kamera_x = max(0, min(max_kamera_x, kamera_x))
#
#
# ─────────────────────────────────────────────────────────────────────────────
# KONZEPT 4: ZUFALLSZAHLEN MIT random
# ─────────────────────────────────────────────────────────────────────────────
#
# import random   ← Zufalls-Werkzeug laden
#
# random.randint(1, 10)    → Zufallszahl zwischen 1 und 10 (z.B. 7)
# random.randint(5, 5)     → Immer 5 (kein Zufall)
# random.randint(0, 255)   → Zahl zwischen 0 und 255
#
# In Final Earth 2 wird jeder Planet zufällig generiert:
# - Zufällige Positionen für Grasflächen
# - Zufällige Größen für Felsen
# - Andere Anordnung von Sand-Wüsten
#
# Jedes Spiel startet anders! Das macht den Wiederspielwert aus.
#
#
# ─────────────────────────────────────────────────────────────────────────────
# KONZEPT 5: DICTIONARIES (Wörterbücher)
# ─────────────────────────────────────────────────────────────────────────────
#
# Ein Dictionary verbindet Schlüssel mit Werten:
#
#   farben = {
#       0: FARBE_ERDE_HELL,      # Schlüssel 0 → Erde-Farbe
#       1: FARBE_GRAS,           # Schlüssel 1 → Gras-Farbe
#       2: FARBE_GESTEIN,        # Schlüssel 2 → Gestein-Farbe
#       3: FARBE_SAND            # Schlüssel 3 → Sand-Farbe
#   }
#
# Wie ein richtiges Wörterbuch:
#   farben[0] → FARBE_ERDE_HELL  (Nachschlagen: "Was bedeutet 0?")
#   farben[2] → FARBE_GESTEIN    (Nachschlagen: "Was bedeutet 2?")
#
# Warum ist das praktisch?
# Statt 4 if-Abfragen zu schreiben:
#
#   if boden_typ == 0: farbe = FARBE_ERDE_HELL
#   elif boden_typ == 1: farbe = FARBE_GRAS
#   elif boden_typ == 2: farbe = FARBE_GESTEIN
#   elif boden_typ == 3: farbe = FARBE_SAND
#
# ...brauchen wir nur eine Zeile:
#
#   farbe = farben[boden_typ]
#
# Viel kürzer und übersichtlicher!
#
#
# ─────────────────────────────────────────────────────────────────────────────
# KONZEPT 6: continue
# ─────────────────────────────────────────────────────────────────────────────
#
# continue bedeutet: "Diese Schleifenrunde sofort beenden, nächste starten."
#
# Beispiel:
#   for i in range(10):
#       if i == 5:
#           continue        # Überspringe i=5
#       print(i)
#
#   Ausgabe: 0 1 2 3 4 6 7 8 9  (5 fehlt!)
#
# In unserem Spiel:
#   if pixel_x + KACHEL_GROESSE < 0:
#       continue    # Kachel ist links vom Fenster → nicht zeichnen!
#
# Das spart Rechenzeit: Warum eine Kachel zeichnen die niemand sieht?
#
#
# ─────────────────────────────────────────────────────────────────────────────
# KONZEPT 7: global
# ─────────────────────────────────────────────────────────────────────────────
#
# Normalerweise können Funktionen nur die Werte sehen die sie bekommen.
# Aber Kamera-Variablen (kamera_x, kamera_y) sind globale Variablen.
# Sie existieren außerhalb aller Funktionen.
#
# In Python müssen wir sagen: "Ich will die globale Variable ändern!"
# Dafür gibt es das Schlüsselwort global.
#
#   def kamera_begrenzen():
#       global kamera_x, kamera_y   # ← WICHTIG! Sonst Fehler!
#       kamera_x = max(0, kamera_x)
#       kamera_y = max(0, kamera_y)
#
# OHNE global:
#   Python denkt: "Aha, eine neue Variable namens kamera_x!"
#   → UnboundLocalError
#
# MIT global:
#   Python weiß: "Aha, die globale Variable kamera_x ändern!"
#   → Funktioniert


# =============================================================================
# 4. GEMEINSAMER CODE
# =============================================================================
#
# NEU GEGENÜBER STUNDE 1:
# ────────────────────────
# Alle neuen Zeilen sind mit  ### NEU ###  markiert.
# So siehst du genau was dazugekommen ist!
# ────────────────────────────────────────

import pygame
import sys
import random            ### NEU ### — Für zufällige Planeten-Generation


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: KONSTANTEN (EINSTELLUNGEN)
# ═════════════════════════════════════════════════════════════════════════════

# ── Fenster-Einstellungen ──────────────────────────────────────────────────
# In Stunde 1: 800 x 600 Pixel
# Jetzt:       1000 x 700 Pixel — mehr Platz zum Erkunden!
BILD_BREITE         = 1000
BILD_HOEHE          = 700
BILD_TITEL          = "Weltraum-Koloniespiel — wie Final Earth 2"
BILDER_PRO_SEKUNDE  = 60

# ── Karten-Einstellungen                    ### NEU ### — Alles!
# Diese Werte gab es in Stunde 1 noch nicht.
# Jede Kachel ist 48x48 Pixel — groß genug um Details zu sehen.
# 60x40 Kacheln = riesige Karte zum Erkunden!
KACHEL_GROESSE  = 48    # Jede Kachel ist 48x48 Pixel groß
KARTE_BREITE    = 60    # 60 Kacheln breit = 2880 Pixel
KARTE_HOEHE     = 40    # 40 Kacheln hoch = 1920 Pixel
KAMERA_SPEED    = 8     # Wie schnell die Kamera scrollt

# ── Farben — Weltraum (wie Stunde 1) ──────────────────────────────────────
FARBE_SCHWARZ       = (0,   0,   0  )   # Der Weltraum
FARBE_WEISS         = (255, 255, 255)
FARBE_GELB_STERN    = (255, 240, 200)   ### NEU ###
FARBE_BLAU_STERN    = (200, 220, 255)   ### NEU ###

# ── Farben — Planeten-Oberfläche             ### NEU ### — Alles!
# Wie in Final Earth 2: Verschiedene Böden für verschiedene Bereiche.
FARBE_ERDE_HELL     = (160, 140, 110)   # Normaler Erdboden
FARBE_ERDE_DUNKEL   = (130, 110, 80)    # Fruchtbare Erde
FARBE_GRAS          = (100, 160, 80)    # Grasfläche
FARBE_GESTEIN       = (90,  90,  95)    # Felsen / Gestein
FARBE_SAND          = (195, 185, 150)   # Sand / Wüste

# ── Farben — Gitterlinien                    ### NEU ###
FARBE_GITTER       = (60, 55, 50)        # Dunkle Gitterlinien

# ── Farben — Text und HUD                    ### NEU ###
FARBE_TEXT_HELL     = (220, 220, 220)
FARBE_TEXT_DUNKEL   = (150, 150, 160)


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: PYGAME INITIALISIERUNG
# ═════════════════════════════════════════════════════════════════════════════
# Wie in Stunde 1 — nur das Fenster ist jetzt größer.

pygame.init()
fenster = pygame.display.set_mode((BILD_BREITE, BILD_HOEHE))
pygame.display.set_caption(BILD_TITEL)
uhr = pygame.time.Clock()


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: SPIELZUSTAND (Globale Variablen)
# ═════════════════════════════════════════════════════════════════════════════
# In Stunde 1 gab es das noch nicht! Jetzt speichern wir den Spiel-Zustand.

# ── Kamera-Position                          ### NEU ###
kamera_x = 0    # Horizontaler Versatz in Pixeln
kamera_y = 0    # Vertikaler Versatz in Pixeln

# ── Karten-Daten                              ### NEU ###
# karten_daten[zeile][spalte] = Bodentyp (0-3)
karten_daten = []

# ── Sterne für den Hintergrund                ### NEU ###
# Liste von Dictionaries: {x, y, groesse, helligkeit}
sterne_liste = []


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: PLANETEN-GENERIERUNG                  ### NEU ### — Komplett neu!
# ═════════════════════════════════════════════════════════════════════════════
# Wie in Final Earth 2: Jeder Planet wird zufällig generiert!

def karte_generieren():
    """
    Generiert eine zufällige Planeten-Oberfläche.
    
    Wie es funktioniert:
    1. Leere Karte mit Erde füllen (60 x 40 Felder)
    2. 8 zufällige Gras-Flächen platzieren (Radius 4-10)
    3. 5 zufällige Gesteins-Flächen platzieren (Radius 3-7)
    4. 6 zufällige Sand-Flächen platzieren (Radius 3-8)
    
    Die Bereiche überlappen sich natürlich.
    Zum Beispiel: Gras auf Erde, Gestein auf Gras → interessante Landschaften!
    """
    global karten_daten
    
    # Leere Karte erstellen: Alles Erde (0)
    # 2D-Array: karten_daten[ZEILE][SPALTE]
    karten_daten = []
    for zeile in range(KARTE_HOEHE):          # 40 Zeilen
        neue_zeile = []
        for spalte in range(KARTE_BREITE):    # 60 Spalten
            neue_zeile.append(0)              # 0 = Erde
        karten_daten.append(neue_zeile)
    
    # Gras-Flächen: 8 Stück, zufällig platziert
    for _ in range(8):
        mitte_x = random.randint(5, 55)       # Zufällige x-Position
        mitte_y = random.randint(5, 35)       # Zufällige y-Position
        radius = random.randint(4, 10)        # Zufällige Größe
        
        # Alle Kacheln im Umkreis werden zu Gras
        for zeile in range(KARTE_HOEHE):
            for spalte in range(KARTE_BREITE):
                # Abstand zum Mittelpunkt (Pythagoras)
                abstand = ((spalte - mitte_x) ** 2 + (zeile - mitte_y) ** 2) ** 0.5
                if abstand < radius:
                    karten_daten[zeile][spalte] = 1  # 1 = Gras
    
    # Gestein: 5 Stück
    for _ in range(5):
        mitte_x = random.randint(5, 55)
        mitte_y = random.randint(5, 35)
        radius = random.randint(3, 7)
        
        for zeile in range(KARTE_HOEHE):
            for spalte in range(KARTE_BREITE):
                abstand = ((spalte - mitte_x) ** 2 + (zeile - mitte_y) ** 2) ** 0.5
                if abstand < radius:
                    karten_daten[zeile][spalte] = 2  # 2 = Gestein
    
    # Sand: 6 Stück
    for _ in range(6):
        mitte_x = random.randint(5, 55)
        mitte_y = random.randint(5, 35)
        radius = random.randint(3, 8)
        
        for zeile in range(KARTE_HOEHE):
            for spalte in range(KARTE_BREITE):
                abstand = ((spalte - mitte_x) ** 2 + (zeile - mitte_y) ** 2) ** 0.5
                if abstand < radius:
                    karten_daten[zeile][spalte] = 3  # 3 = Sand


def sterne_generieren():
    """
    Erzeugt zufällige Sterne für den Weltraum-Hintergrund.
    
    Jeder Stern ist ein Dictionary (Wörterbuch) mit:
    - x, y:        Position auf dem Bildschirm
    - groesse:     1, 2 oder 3 Pixel
    - helligkeit:  100-255 (dunkel bis hell)
    
    150 Sterne = schöner Sternenhimmel!
    """
    global sterne_liste
    sterne_liste = []
    
    for _ in range(150):
        stern = {
            "x": random.randint(0, BILD_BREITE),
            "y": random.randint(0, BILD_HOEHE),
            "groesse": random.randint(1, 3),
            "helligkeit": random.randint(100, 255)
        }
        sterne_liste.append(stern)


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: KARTE ZEICHNEN                          ### NEU ### — Komplett neu!
# ═════════════════════════════════════════════════════════════════════════════
# Das Herzstück dieser Stunde!

def karte_zeichnen():
    """
    Zeichnet alle Kacheln der Planeten-Oberfläche auf den Bildschirm.
    
    So wie in Final Earth 2:
    - Die Karte besteht aus vielen kleinen Kacheln (48x48 Pixel)
    - Jede Kachel hat eine Farbe je nach Bodentyp
    - Kamera-Versatz: pixel = gitter * groesse - kamera
    - Unsichtbare Kacheln werden übersprungen (Performance)
    """
    # Dictionary: Bodentyp → Farbe
    farben = {
        0: FARBE_ERDE_HELL,     # 0 = Erde
        1: FARBE_GRAS,          # 1 = Gras
        2: FARBE_GESTEIN,       # 2 = Gestein
        3: FARBE_SAND           # 3 = Sand
    }
    
    # Äußere Schleife: Zeilen (y-Richtung)
    for zeile in range(KARTE_HOEHE):
        
        # Innere Schleife: Spalten (x-Richtung)
        for spalte in range(KARTE_BREITE):
            
            # 1. Bildschirm-Position berechnen
            pixel_x = spalte * KACHEL_GROESSE - kamera_x
            pixel_y = zeile  * KACHEL_GROESSE - kamera_y
            
            # 2. Unsichtbare Kacheln überspringen
            if pixel_x + KACHEL_GROESSE < 0:   continue  # Links
            if pixel_y + KACHEL_GROESSE < 0:   continue  # Oben
            if pixel_x > BILD_BREITE:          continue  # Rechts
            if pixel_y > BILD_HOEHE:           continue  # Unten
            
            # 3. Bodentyp + Farbe
            boden_typ = karten_daten[zeile][spalte]
            kachel_farbe = farben[boden_typ]
            
            # 4. Kachel zeichnen (gefüllt + Gitterlinie)
            kachel_rect = pygame.Rect(pixel_x, pixel_y, KACHEL_GROESSE, KACHEL_GROESSE)
            pygame.draw.rect(fenster, kachel_farbe, kachel_rect)
            pygame.draw.rect(fenster, FARBE_GITTER, kachel_rect, 1)


def kamera_begrenzen():
    """
    Verhindert dass die Kamera über den Kartenrand scrollt.
    
    Mathematik:
    - max_kamera_x = Kartenbreite - Fensterbreite
    - kamera_x = max(0, min(max_kamera_x, kamera_x))
    """
    global kamera_x, kamera_y
    
    max_kamera_x = KARTE_BREITE * KACHEL_GROESSE - BILD_BREITE
    max_kamera_y = KARTE_HOEHE  * KACHEL_GROESSE - BILD_HOEHE
    
    kamera_x = max(0, min(max_kamera_x, kamera_x))
    kamera_y = max(0, min(max_kamera_y, kamera_y))


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: WELTRAUM-HINTERGRUND                    ### NEU ### — Sterne!
# ═════════════════════════════════════════════════════════════════════════════
# Wie Stunde 1 (schwarzer Hintergrund) + jetzt mit Sternen.

def hintergrund_zeichnen():
    """
    Zeichnet den Weltraum-Hintergrund mit Sternen.
    
    1. Alles schwarz färben (Weltraum)
    2. 150 Sterne als kleine Kreise malen
    """
    fenster.fill(FARBE_SCHWARZ)
    
    for stern in sterne_liste:
        h = stern["helligkeit"]
        
        # Zufällige Sternfarben (20% blau, 20% gelb, 60% weiß)
        if random.randint(0, 10) < 2:
            stern_farbe = (h - 55, h - 35, h)      # Bläulich
        elif random.randint(0, 10) < 2:
            stern_farbe = (h, h - 15, h - 55)       # Gelblich
        else:
            stern_farbe = (h, h, h)                  # Weiß
        
        pygame.draw.circle(fenster, stern_farbe, (stern["x"], stern["y"]), stern["groesse"])


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: HUD / ANZEIGE                             ### NEU ### — Erweitert!
# ═════════════════════════════════════════════════════════════════════════════
# In Stunde 1: Nur "Spiel wird hier entstehen"
# Jetzt:       Kameraposition + Karteninfo + Legende!

def info_text_zeichnen():
    """
    Zeigt wichtige Informationen auf dem Bildschirm:
    - Kameraposition (welche Kachel sehen wir?)
    - Kartengröße und Steuerungshinweise
    - Legende der Bodentypen (mit Farbkästchen)
    """
    schrift = pygame.font.Font(None, 24)
    schrift_klein = pygame.font.Font(None, 18)
    
    # Kameraposition (in Kacheln umgerechnet)
    kachel_x = max(0, kamera_x // KACHEL_GROESSE)
    kachel_y = max(0, kamera_y // KACHEL_GROESSE)
    
    kamera_info = schrift.render(
        f"Position: Kachel ({kachel_x}, {kachel_y})  |  Kamera: x={kamera_x}  y={kamera_y}",
        True, FARBE_TEXT_HELL
    )
    fenster.blit(kamera_info, (15, 15))
    
    # Steuerung
    karten_info = schrift_klein.render(
        f"Karte: {KARTE_BREITE} x {KARTE_HOEHE} Kacheln  |  "
        f"Pfeiltasten zum Scrollen  |  ESC = Beenden",
        True, FARBE_TEXT_DUNKEL
    )
    fenster.blit(karten_info, (15, 45))
    
    # Legende
    legende_text = schrift_klein.render(
        "Legende:  █ Erde  █ Gras  █ Gestein  █ Sand",
        True, FARBE_TEXT_DUNKEL
    )
    fenster.blit(legende_text, (15, 70))
    
    # Farbkästchen für Legende
    farben_legende = [FARBE_ERDE_HELL, FARBE_GRAS, FARBE_GESTEIN, FARBE_SAND]
    for i, farbe in enumerate(farben_legende):
        kasten_x = 330 + i * 55
        kasten_rect = pygame.Rect(kasten_x, 70, 14, 14)
        pygame.draw.rect(fenster, farbe, kasten_rect)
        pygame.draw.rect(fenster, FARBE_GITTER, kasten_rect, 1)


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: EREIGNISSE VERARBEITEN
# ═════════════════════════════════════════════════════════════════════════════
# Wie in Stunde 1 — aber jetzt mit Pfeiltasten-Scrolling!

def ereignisse_verarbeiten():
    """
    Verarbeitet alle Eingaben des Spielers.
    Gibt True zurück solange das Spiel läuft.
    
    NEU in Stunde 2:
    - Pfeiltasten scrollen die Kamera
    - kamera_begrenzen() verhindert Rand-Überschreitung
    """
    global kamera_x, kamera_y
    
    # Einmal-Ereignisse (Klick, Tastendruck)
    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            return False
        if ereignis.type == pygame.KEYDOWN:
            if ereignis.key == pygame.K_ESCAPE:
                return False
    
    # Gehaltene Tasten (flüssiges Scrollen!)
    gedrueckte_tasten = pygame.key.get_pressed()
    
    if gedrueckte_tasten[pygame.K_LEFT]:    kamera_x -= KAMERA_SPEED
    if gedrueckte_tasten[pygame.K_RIGHT]:   kamera_x += KAMERA_SPEED
    if gedrueckte_tasten[pygame.K_UP]:      kamera_y -= KAMERA_SPEED
    if gedrueckte_tasten[pygame.K_DOWN]:    kamera_y += KAMERA_SPEED
    
    kamera_begrenzen()
    return True


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: SPIELSCHLEIFE (GAME LOOP)
# ═════════════════════════════════════════════════════════════════════════════
# Wie Stunde 1 — nur dass jetzt Karte + Hintergrund + HUD gezeichnet werden.

def spiel_starten():
    """
    Startet die Hauptspielschleife.
    
    NEU in Stunde 2:
    - karte_generieren() vor dem Start
    - sterne_generieren() vor dem Start
    - hintergrund_zeichnen() im Loop (mit Sternen!)
    - karte_zeichnen() im Loop
    - Ausführlichere info_text_zeichnen()
    """
    print("Generiere Planeten-Oberfläche...")
    karte_generieren()
    
    print("Erzeuge Sternenhimmel...")
    sterne_generieren()
    
    print(f"Spiel gestartet! Karte: {KARTE_BREITE} x {KARTE_HOEHE}")
    
    laeuft = True
    
    while laeuft:
        # Schritt 1: Eingaben
        laeuft = ereignisse_verarbeiten()
        
        # Schritt 2: Logik (kommt später)
        pass
        
        # Schritt 3: Zeichnen (Reihenfolge wichtig!)
        hintergrund_zeichnen()    # 1. Weltall + Sterne
        karte_zeichnen()          # 2. Planeten-Oberfläche
        info_text_zeichnen()      # 3. HUD (immer oben!)
        
        pygame.display.flip()
        uhr.tick(BILDER_PRO_SEKUNDE)


# ═════════════════════════════════════════════════════════════════════════════
# PROGRAMMSTART
# ═════════════════════════════════════════════════════════════════════════════
# Wie in Stunde 1 — unverändert!

if __name__ == "__main__":
    spiel_starten()
    pygame.quit()
    sys.exit()


# =============================================================================
# 5. AUFGABEN FÜR SCHÜLER
# =============================================================================
#
# ─────────────────────────────────────────────────────────────────────────────
# 🔹 AUFGABE 1: Die neuen Teile finden (15 Minuten)
# ─────────────────────────────────────────────────────────────────────────────
#
# Öffne die Datei Unterricht/Schuster/Lehrplan/Stunde 1.md und vergleiche
# sie mit dem Code in dieser Datei. Alle neuen Teile sind mit ### NEU ###
# markiert.
#
# 📌 FRAGEN:
# a) Welche neuen KONSTANTEN sind in Stunde 2 dazugekommen? Zähle sie auf.
# b) Welche neuen FUNKTIONEN wurden hinzugefügt?
# c) Welche neuen IMPORTs wurden hinzugefügt? Wofür brauchen wir sie?
#
#
# ─────────────────────────────────────────────────────────────────────────────
# 🔹 AUFGABE 2: 2D-Arrays verstehen (15 Minuten)
# ─────────────────────────────────────────────────────────────────────────────
#
# Stell dir vor, du hast dieses 2D-Array:
#
#   karte = [
#       [0, 0, 0, 1, 0],   # Zeile 0
#       [0, 0, 0, 1, 0],   # Zeile 1
#       [0, 1, 1, 0, 0],   # Zeile 2
#       [0, 0, 0, 0, 0],   # Zeile 3
#   ]
#
# 📌 FRAGEN:
# a) Welchen Wert hat karte[2][1]?
# b) Welchen Wert hat karte[0][3]?
# c) Welcher Bodentyp ist an Position (zeile=1, spalte=3)?
# d) Zeichne die Karte auf ein Blatt Papier. Male die Felder farbig aus:
#    0 = braun (Erde), 1 = grün (Gras)
#
#
# ─────────────────────────────────────────────────────────────────────────────
# 🔹 AUFGABE 3: Kamera-Prinzip (15 Minuten)
# ─────────────────────────────────────────────────────────────────────────────
#
# Eine Kachel ist an Position (spalte=10, zeile=5).
# KACHEL_GROESSE = 48
# kamera_x = 100, kamera_y = 50
#
# Pixel-Position:
#   pixel_x = spalte * KACHEL_GROESSE - kamera_x
#   pixel_y = zeile  * KACHEL_GROESSE - kamera_y
#
# 📌 FRAGEN:
# a) Berechne pixel_x und pixel_y für diese Kachel.
# b) Die Kamera bewegt sich auf kamera_x = 200. Was passiert mit der Kachel?
#    Wird sie weiter links oder weiter rechts angezeigt?
# c) Die Karte ist 60 Kacheln breit. Wie viele Pixel ist die Karte insgesamt breit?
# d) Das Fenster ist 1000 Pixel breit. Wie weit kann die Kamera maximal scrollen?
#
#
# ─────────────────────────────────────────────────────────────────────────────
# 🔹 AUFGABE 4: Landschaft planen (20 Minuten)
# ─────────────────────────────────────────────────────────────────────────────
#
# Starte das Spiel mehrmals (ESC und neu starten).
# Jedes Mal sieht die Karte anders aus!
#
# 📌 AUFGABE:
# a) Starte das Spiel 3 Mal. Zeichne jede Karte grob auf (Position der
#    Grasflächen, Felsen und Sandwüsten).
# b) Welche Karte gefällt dir am besten? Warum?
# c) Wenn du etwas an der Generierung ändern könntest: Was würdest du ändern?
#    (Mehr Gras? Weniger Sand? Größere Felsen?)
#
#
# ─────────────────────────────────────────────────────────────────────────────
# 🔹 AUFGABE 5: Sterne zählen (10 Minuten)
# ─────────────────────────────────────────────────────────────────────────────
#
# Im Code werden 150 Sterne erzeugt. Jeder Stern hat eine zufällige
# Helligkeit zwischen 100 und 255.
#
# 📌 FRAGEN:
# a) Wie viele helle Sterne (Helligkeit > 200) gibt es ungefähr?
#    (Tipp: Bereich 100-255 = 156 mögliche Werte. Werte > 200 = 55 Werte.
#     55/156 ≈ 35%. 35% von 150 ≈ ?)
# b) Ein Stern hat Helligkeit 100 und Größe 1. Ein anderer hat Helligkeit 255
#    und Größe 3. Welcher Stern leuchtet heller und ist größer?
# c) Was passiert wenn du sterne_liste = [] leer lässt? (Tipp: Keine Schleife)
#
#
# ─────────────────────────────────────────────────────────────────────────────
# 🔹 AUFGABE 6: Neue Bodenfarbe (15 Minuten)
# ─────────────────────────────────────────────────────────────────────────────
#
# Füge einen neuen Bodentyp hinzu: Wasser (blau)!
#
# 📌 AUFGABE:
# a) Füge eine neue Konstante ein: FARBE_WASSER = (50, 100, 200)
# b) Füge im Dictionary farben in karte_zeichnen() einen Eintrag hinzu:
#    4: FARBE_WASSER
# c) Füge in karte_generieren() einen neuen Block für Wasserflächen.
#    (Tipp: Kopiere den Sand-Block und ändere typ = 3 zu typ = 4)
# d) Füge in info_text_zeichnen() "█ Wasser" zur Legende hinzu.
# e) Teste: Starte das Spiel. Siehst du blaue Wasserflächen?
#
#
# ─────────────────────────────────────────────────────────────────────────────
# 🔹 AUFGABE 7: Debuggen — Was stimmt hier nicht? (10 Minuten)
# ─────────────────────────────────────────────────────────────────────────────
#
# Ein Schüler hat diesen Code geschrieben. Finde die Fehler!
#
#   def karte_zeichnen():
#       for zeile in range(KARTE_BREITE):      ← Fehler 1?
#           for spalte in range(KARTE_HOEHE):   ← Fehler 2?
#               pixel_x = spalte * KACHEL_GROESSE - kamera_x
#               pixel_y = zeile * KACHEL_GROESSE - kamera_y
#               boden_typ = karten_daten[spalte][zeile]  ← Fehler 3?
#               pygame.draw.rect(fenster, farbe, rect)
#
# 📌 FRAGEN:
# a) Welche drei Fehler sind im Code?
# b) Was würde passieren wenn man das Programm so startet?
# c) Schreibe die korrigierte Version auf.


# =============================================================================
# 6. HÄUFIGE FEHLER & LÖSUNGEN
# =============================================================================
#
# ┌─────────────────────────────────────────────────────────────────────┐
# │ FEHLER                    │ URSACHE                 │ LÖSUNG        │
# ├─────────────────────────────────────────────────────────────────────┤
# │ Nur schwarzer Bildschirm │ karte_zeichnen()        │ In der        │
# │ (keine Karte zu sehen)    │ wird nicht aufgerufen   │ Spielschleife │
# │                           │                         │ aufrufen!     │
# ├─────────────────────────────────────────────────────────────────────┤
# │ UnboundLocalError:         │ global kamera_x,       │ global-       │
# │ "kamera_x" not assigned   │ kamera_y vergessen     │ Schlüsselwort │
# │                           │                         │ hinzufügen    │
# ├─────────────────────────────────────────────────────────────────────┤
# │ Karte flackert            │ Falsche Reihenfolge:    │ hintergrund_  │
# │                           │ karte ZUERST, dann     │ zeichnen()    │
# │                           │ hintergrund zeichnen   │ muss VOR      │
# │                           │ → Karte wird übermalt  │ karte_zeichnen│
# ├─────────────────────────────────────────────────────────────────────┤
# │ IndexError:                │ karten_daten[spalte]   │ Zuerst Zeile, │
# │ list index out of range   │ [zeile] statt Zeile    │ dann Spalte:  │
# │                           │ zuerst                 │ [zeile][spalte│
# ├─────────────────────────────────────────────────────────────────────┤
# │ Kamera scrollt            │ kamera_begrenzen()     │ Nach jeder    │
# │ über den Rand             │ nicht aufgerufen       │ Bewegung      │
# │                           │                         │ aufrufen!     │
# ├─────────────────────────────────────────────────────────────────────┤
# │ import random nicht       │ Bibliothek nicht       │ import random │
# │ gefunden / NameError      │ importiert             │ am Anfang     │
# │ 'random' not defined      │                         │ hinzufügen    │
# └─────────────────────────────────────────────────────────────────────┘


# =============================================================================
# 7. ZUSAMMENFASSUNG
# =============================================================================
#
# WAS HABEN WIR IN STUNDE 2 GELERNT?
# ────────────────────────────────────
#
# ✓ 2D-Arrays         — karten_daten[zeile][spalte] speichert den Bodentyp
# ✓ Verschachtelte    — for zeile ... for spalte ... um über alles
#   for-Schleifen       zu iterieren
# ✓ Kamera-Prinzip    — pixel_x = spalte × größe − kamera_x
# ✓ Zufallsgenerierung — random.randint() für zufällige Planetenerzeugung
# ✓ Dictionaries      — farben = {0: erde, 1: gras, ...}
# ✓ continue          — unsichtbare Kacheln überspringen
# ✓ global            — globale Variablen in Funktionen ändern
# ✓ Verschiedene      — Erde, Gras, Gestein, Sand
#   Bodentypen
# ✓ Sternenhimmel     — 150 zufällige Sterne im Hintergrund
#
# WAS KOMMT IN STUNDE 3?
# ────────────────────────
#   → Gebäude platzieren (Basis, Reaktor, Farm) wie in Final Earth 2!
#   → Mausklick auf Kachel → Gebäude setzen
#   → Gebäude speichern in liste_gebaeude = []
#   → Auf verschiedenen Böden bauen
#   → Gebäude-Farben und Symbole zeichnen
#
# =============================================================================
# ENDE STUNDE 2
# =============================================================================