"""
=============================================================================
PROJEKT: Weltraum-Koloniespiel  —  wie FINAL EARTH 2
STUNDE 7 — Bevölkerung & Wohnungen
=============================================================================

Worum geht es?
    In diesem Spiel landest du auf einem fremden Planeten und baust
    eine Kolonie auf. Du startest mit einem kleinen Raumschiff und
    musst Ressourcen sammeln, Gebäude bauen und die Kolonie erweitern.
    Das Ziel: Eine blühende Kolonie auf einem fremden Planeten!

    Dieses Spiel ist inspiriert von "Final Earth 2" — einem Kolonie-
    Aufbauspiel auf einem fremden Planeten.

Bisher gelernt (Stunde 1 — Das Fundament):
    ✓ pygame.init() startet Pygame
    ✓ display.set_mode() erstellt das Fenster
    ✓ Die Spielschleife: Eingaben → Logik → Zeichnen
    ✓ Farben als (R, G, B) Tupel
    ✓ Konstanten in GROSSBUCHSTABEN
    ✓ Funktionen mit def
    ✓ Schwarzer Weltraum-Hintergrund

Bisher gelernt (Stunde 2 — Die Mondkarte und Kamera-Scroll):
    ✓ Karte aus Kacheln (Gitter) wird gezeichnet
    ✓ Mit Pfeiltasten über die Karte scrollen
    ✓ Kamera merkt sich wo wir hingeschaut haben
    ✓ Mond-Oberfläche mit verschiedenen Boden-Farben
    ✓ Sterne im Weltraum-Hintergrund
    ✓ Wie in Final Earth 2!

Bisher gelernt (Stunde 3 — Gebäude bauen):
    ✓ Mausklick erkennen mit pygame.MOUSEBUTTONDOWN
    ✓ Kachel unter dem Mauszeiger berechnen
    ✓ Gebäude auf der Karte platzieren (wie in Final Earth 2!)
    ✓ Gebäude zeichnen (farbige Rechtecke auf der Karte)
    ✓ Erste Kolonie-Gebäude: Basis, Reaktor, Farm
    ✓ Gebäude speichern in einer Liste

Bisher gelernt (Stunde 4 — HUD & Ressourcenanzeige):
    ✓ HUD (Heads-Up Display) am oberen Bildschirmrand zeichnen
    ✓ Ressourcen-Anzeige: Gold, Energie, Holz
    ✓ Tasten 1/2/3 für Gebäude-Auswahl (wie in Final Earth 2!)
    ✓ Ressourcen als Dictionary speichern {"gold": 100, ...}

Bisher gelernt (Stunde 5 — Ressourcen-Logik & Wirtschaft):
    ✓ Ressourcen-Produktion und Verbrauch pro Gebäude
    ✓ Baukosten: Gebäude bauen kostet jetzt Ressourcen
    ✓ Tick-System: 1× pro Sekunde produzieren/verbrauchen Gebäude
    ✓ Basis kann nur 1× gebaut werden
    ✓ Wenn Rohstoffe fehlen → Gebäude produziert nichts

Heute in Stunde 7 lernen wir NEU dazu:
    ✓ Neuer Rohstoff: Bevölkerung (fünfte Ressource)
    ✓ Neues Gebäude: Wohnhaus (produziert Bevölkerung, verbraucht Energie)
    ✓ Taste 7 für das Wohnhaus
    ✓ Bevölkerung wächst mit jedem Wohnhaus

Heute in Stunde 9 lernen wir NEU dazu (die Verbesserungsvorschläge der Schüler!):
    ✓ Gebäude abreißen können mit Rechtsklick — 50 % der Baukosten zurück
    ✓ Bei der Gebäude-Auswahl: Produktion + Verbrauch werden angezeigt
    ✓ Baumenü mit der Taste TAB (zeigt ALLE Gebäudetypen)
    ✓ Tooltip beim Hovern über ein Ressourcen-Icon
    ✓ Rote Meldung im Spiel, wenn zu wenig Rohstoffe zum Bauen da sind
    ✓ Stufenweise Freischaltung: Marktplatz ab 5 Bevölkerung, Wohnhaus ab 20 Holz

=============================================================================
"""

import pygame
import sys
import random       # Für zufällige Planeten-Generation
import gebaeude     # Gebäude-Modul aus Stunde 3 (+ Stunde 6)
import hud          # HUD-Modul aus Stunde 4 (+ Stunde 6)
import ressourcen   # Ressourcen-Modul aus Stunde 5 (+ Stunde 6)
import menu         # Baumenü-Modul — NEU in Stunde 9
import forschung    # Forschungs-Modul — NEU in Stunde 10


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: EINSTELLUNGEN (KONSTANTEN)
# ═════════════════════════════════════════════════════════════════════════════
# Konstanten sind Werte die sich während des Spiels NICHT ändern.
# Wir schreiben sie GROSS damit wir sofort sehen dass sie Konstanten sind.
# In Final Earth 2 gibt es viele verschiedene Einstellungen für die Welt.
# ═════════════════════════════════════════════════════════════════════════════

# ── Fenster-Einstellungen ──────────────────────────────────────────────────
# Das Fenster ist 1000 Pixel breit und 700 Pixel hoch.
# In Final Earth 2 ist das Fenster ähnlich groß, damit man viel sieht.
BILD_BREITE         = 1000
BILD_HOEHE          = 700
BILD_TITEL          = "Weltraum-Koloniespiel — wie Final Earth 2"
BILDER_PRO_SEKUNDE  = 60     # FPS — wie flüssig das Spiel läuft

# ── Karten-Einstellungen ────────────────────────────────────────────────────
# Die Karte ist 60×40 Kacheln groß — wie in Final Earth 2 eine schöne
# große Welt zum Erkunden.
KACHEL_GROESSE  = 48         # Jede Kachel ist 48×48 Pixel groß
KARTE_BREITE    = 60         # 60 Kacheln breit
KARTE_HOEHE     = 40         # 40 Kacheln hoch
KAMERA_SPEED    = 8          # Wie schnell die Kamera scrollt (in Pixeln)

# ── Farben — Weltraum (Hintergrund) ───────────────────────────────────────
# Der schwarze Weltraum-Hintergrund aus Stunde 1.
# In Final Earth 2 siehst du das Weltall rund um den Planeten.
FARBE_SCHWARZ       = (0,   0,   0  )    # Reines Schwarz — der Weltraum
FARBE_WEISS         = (255, 255, 255)    # Für Texte und helle Sterne
FARBE_GELB_STERN    = (255, 240, 200)    # Warme Sterne
FARBE_BLAU_STERN    = (200, 220, 255)    # Blaue Sterne

# ── Farben — Planeten-Oberfläche (wie Final Earth 2) ──────────────────────
# Auf einem fremden Planeten gibt es verschiedene Bodenarten.
# Jede Bodenart hat eine eigene Farbe — wie in Final Earth 2!
# Hellbraun — normaler Erdboden (der häufigste Untergrund)
FARBE_ERDE_HELL     = (160, 140, 110)
# Dunkelbraun — fruchtbare Erde (gut für Pflanzen)
FARBE_ERDE_DUNKEL   = (130, 110, 80)
# Grün — Grasfläche (kommt später für Gebäude)
FARBE_GRAS          = (100, 160, 80)
# Dunkelgrau — Gestein / Felsen (schwer zu bearbeiten)
FARBE_GESTEIN       = (90,  90,  95)
# Sandfarbe — Wüstenfläche (wie in Final Earth 2)
FARBE_SAND          = (195, 185, 150)

# ── Farben — Gitterlinien ───────────────────────────────────────────────────
# Die Gitternetz-Linien zwischen den Kacheln.
# In Final Earth 2 siehst du ein feines Gitter auf der Oberfläche.
FARBE_GITTER       = (60, 55, 50)       # Dunkle Gitterlinien

# ── Farben — Text und HUD ──────────────────────────────────────────────────
# In Final Earth 2 gibt es eine Anzeige mit Informationen.
FARBE_TEXT_HELL     = (220, 220, 220)   # Helles Grau für Text
FARBE_TEXT_DUNKEL   = (150, 150, 160)   # Dunkleres Grau für Hinweise


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: PYGAME INITIALISIERUNG
# ═════════════════════════════════════════════════════════════════════════════
# pygame.init() startet alle Pygame-Module.
# Das passiert nur EINMAL ganz am Anfang — bevor alles andere kommt.
# Ohne diesen Schritt können wir keine Grafiken, Töne oder Eingaben nutzen.
# ═════════════════════════════════════════════════════════════════════════════

pygame.init()

# Das Spiel-Fenster erstellen — hier wird alles gezeichnet
fenster = pygame.display.set_mode((BILD_BREITE, BILD_HOEHE))

# Titel in der Fenster-Leiste (oben am Rand)
pygame.display.set_caption(BILD_TITEL)

# Ein Taktgeber (Clock) sorgt dafür dass das Spiel auf jedem Computer
# gleich schnell läuft — egal wie stark der Prozessor ist.
uhr = pygame.time.Clock()


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: SPIELZUSTAND (Globale Variablen)
# ═════════════════════════════════════════════════════════════════════════════
# Hier speichern wir den aktuellen Zustand des Spiels.
# In Final Earth 2 gibt es viele Werte: Kameraposition, Ressourcen, Gebäude...
# ═════════════════════════════════════════════════════════════════════════════

# ── Kamera-Position ─────────────────────────────────────────────────────────
# Die Kamera bestimmt welchen Ausschnitt der Karte wir sehen.
# 0, 0 = wir schauen auf die obere linke Ecke.
kamera_x = 0
kamera_y = 0

# ── Karten-Daten (wie in Final Earth 2) ────────────────────────────────────
# Die Karte ist ein 2D-Array (Liste von Listen).
# Jede Kachel hat einen Typ: 0 = Erde, 1 = Gras, 2 = Gestein, 3 = Sand
# In Final Earth 2 bestimmt der Bodentyp was du dort bauen kannst.
#
# karten_daten[zeile][spalte] gibt den Typ der Kachel an Position (spalte, zeile)
# Beispiel: karten_daten[5][3] = 0 → Kachel in Zeile 5, Spalte 3 ist Erde
karten_daten = []      # Wird in karte_generieren() befüllt

# ── Sterne für den Hintergrund ─────────────────────────────────────────────
# Wie in Final Earth 2 funkeln Sterne im Weltraum-Hintergrund.
# Jeder Stern hat eine x/y-Position und eine Helligkeit.
sterne_liste = []

# ── Ressourcen (ab Stunde 4) ────────────────────────────────────────────────
# In Final Earth 2 verwaltest du Ressourcen wie Gold, Energie und Nahrung.
# Diese Ressourcen werden ab Stunde 5 automatisch produziert und verbraucht.
# Das Dictionary speichert jede Ressource mit ihrem Namen und aktuellen Wert.
#
# Neu in Stunde 6: Der Rohstoff "stein" kommt dazu!
# Startwert = 20, damit der Steinmetz direkt nach dem Bau loslegen kann.
#
# Neu in Stunde 7: Der Rohstoff "bevoelkerung" kommt dazu!
# Startwert = 10 — damit der Spieler direkt ein paar Bewohner hat
# für die ersten Produktionsgebäude.
#
# Neu in Stunde 8: Der Rohstoff "nahrung" kommt dazu!
# Startwert = 50 — damit die ersten Wohnhäuser versorgt werden können.
# Neu in Stunde 10: Der Rohstoff "forschung" kommt dazu!
# Startwert = 0 — Forschungspunkte werden im Labor produziert.
ressourcen_dict = {"gold": 100, "energie": 50, "holz": 30, "stein": 20, "bevoelkerung": 10, "nahrung": 50, "forschung": 0, "kohle": 0, "eisen": 0}

# ├────────────────────────────────────────────────────────────────────────────
# │ STUNDE 3 — NEUE VARIABLEN                                                 │
# │                                                                           │
# │ In dieser Stunde kommen neue Variablen dazu:                              │
# │ Wir brauchen eine Liste für alle Gebäude, die auf der Karte stehen.       │
# │ Wir brauchen eine Variable, welches Gebäude gerade ausgewählt ist.        │
# │ Wir brauchen die Maus-Position und wo der Spieler geklickt hat.           │
# │                                                                           │
# │ Diese Variablen werden hier definiert (global):                          │
# └────────────────────────────────────────────────────────────────────────────┘

liste_gebaeude = []       # Alle Gebäude auf der Karte
# Neu in Stunde 7: 0=Basis, 1=Reaktor, 2=Farm, 3=Holzfaeller,
#                   4=Steinmetz, 5=Marktplatz, 6=Wohnhaus, 7=Labor
gebaeude_auswahl = 0      # Welches Gebäude ist ausgewählt? (0-7)
maus_x = 0                # Maus-X-Position auf dem Bildschirm
maus_y = 0                # Maus-Y-Position auf dem Bildschirm
klick_x = -1              # Zuletzt angeklickte Kachel (Spalte)
klick_y = -1              # Zuletzt angeklickte Kachel (Zeile)

# ── Tick-System (aus Stunde 5) ─────────────────────────────────────────────
# Der tick_zaehler zählt die Frames (Bilder pro Sekunde).
# Bei 60 FPS ist 1 Sekunde = 60 Frames.
# Wenn tick_zaehler 60 erreicht, rufen wir ressourcen_produzieren() auf
# und setzen den Zähler zurück auf 0.
# So läuft die Wirtschaft 1× pro Sekunde — nicht jeden Frame!
#
# Neu in Stunde 8: spiel_geschwindigkeit für Pause/Start/Beschleunigen
#   1 = normal (1× pro Sekunde)
#   0 = pausiert
#   2 = doppelt so schnell (alle 30 Frames)
tick_zaehler = 0
spiel_geschwindigkeit = 1   # Normal-Geschwindigkeit
_hilfe_offen = False         # NEU St. 10: Hilfe-Overlay ein/aus


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: PLANETEN-GENERIERUNG
# ═════════════════════════════════════════════════════════════════════════════
# In Final Earth 2 wird jeder Planet zufällig generiert.
# Das bedeutet: Jedes Spiel sieht anders aus!
# Hier erstellen wir unsere eigene zufällige Planeten-Oberfläche.
# ═════════════════════════════════════════════════════════════════════════════

def karte_generieren():
    """
    Generiert eine zufällige Planeten-Oberfläche.
    
    Wie in Final Earth 2 gibt es verschiedene Bodentypen:
    - Erde (0):   Der normale Boden — überall zu finden
    - Gras (1):   Fruchtbare Flächen — gut für Farmen
    - Gestein (2): Felsen — schwer zu bearbeiten aber wertvoll
    - Sand (3):   Wüstenfläche
    
    Die Karte wird zufällig erstellt, aber mit "Bereichen":
    - Große Flächen mit demselben Bodentyp (wie richtige Landschaften)
    - Kein wildes Durcheinander!
    """
    global karten_daten
    
    # Leere Karte erstellen (erstmal alles Erde)
    karten_daten = []
    for zeile in range(KARTE_HOEHE):
        neue_zeile = []
        for spalte in range(KARTE_BREITE):
            neue_zeile.append(0)  # 0 = Erde (Standard)
        karten_daten.append(neue_zeile)
    
    # ── Schritt 1: Große Gras-Flächen erzeugen ────────────────────────────
    anzahl_gras_flaechen = 8
    for _ in range(anzahl_gras_flaechen):
        mitte_x = random.randint(5, KARTE_BREITE - 5)
        mitte_y = random.randint(5, KARTE_HOEHE - 5)
        radius = random.randint(4, 10)
        for zeile in range(KARTE_HOEHE):
            for spalte in range(KARTE_BREITE):
                abstand = ((spalte - mitte_x) ** 2 + (zeile - mitte_y) ** 2) ** 0.5
                if abstand < radius:
                    karten_daten[zeile][spalte] = 1  # 1 = Gras
    
    # ── Schritt 2: Gesteins-Flächen erzeugen ──────────────────────────────
    anzahl_gestein_flaechen = 5
    for _ in range(anzahl_gestein_flaechen):
        mitte_x = random.randint(5, KARTE_BREITE - 5)
        mitte_y = random.randint(5, KARTE_HOEHE - 5)
        radius = random.randint(3, 7)
        for zeile in range(KARTE_HOEHE):
            for spalte in range(KARTE_BREITE):
                abstand = ((spalte - mitte_x) ** 2 + (zeile - mitte_y) ** 2) ** 0.5
                if abstand < radius:
                    karten_daten[zeile][spalte] = 2  # 2 = Gestein
    
    # ── Schritt 3: Sand-Flächen erzeugen ──────────────────────────────────
    anzahl_sand_flaechen = 6
    for _ in range(anzahl_sand_flaechen):
        mitte_x = random.randint(5, KARTE_BREITE - 5)
        mitte_y = random.randint(5, KARTE_HOEHE - 5)
        radius = random.randint(3, 8)
        for zeile in range(KARTE_HOEHE):
            for spalte in range(KARTE_BREITE):
                abstand = ((spalte - mitte_x) ** 2 + (zeile - mitte_y) ** 2) ** 0.5
                if abstand < radius:
                    karten_daten[zeile][spalte] = 3  # 3 = Sand


def sterne_generieren():
    """
    Erzeugt zufällige Sterne für den Weltraum-Hintergrund.
    Jeder Stern hat eine zufällige Position und Helligkeit.
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
# BLOCK: KARTE ZEICHNEN
# ═════════════════════════════════════════════════════════════════════════════

def karte_zeichnen():
    """
    Zeichnet alle Kacheln der Planeten-Oberfläche auf den Bildschirm.
    """
    farben = {
        0: FARBE_ERDE_HELL,
        1: FARBE_GRAS,
        2: FARBE_GESTEIN,
        3: FARBE_SAND
    }
    
    for zeile in range(KARTE_HOEHE):
        for spalte in range(KARTE_BREITE):
            pixel_x = spalte * KACHEL_GROESSE - kamera_x
            pixel_y = zeile  * KACHEL_GROESSE - kamera_y
            
            if pixel_x + KACHEL_GROESSE < 0:   continue
            if pixel_y + KACHEL_GROESSE < 0:   continue
            if pixel_x > BILD_BREITE:          continue
            if pixel_y > BILD_HOEHE:           continue
            
            boden_typ = karten_daten[zeile][spalte]
            kachel_farbe = farben[boden_typ]
            kachel_rect = pygame.Rect(pixel_x, pixel_y, KACHEL_GROESSE, KACHEL_GROESSE)
            pygame.draw.rect(fenster, kachel_farbe, kachel_rect)
            pygame.draw.rect(fenster, FARBE_GITTER, kachel_rect, 1)


# ── Gebäude zeichnen ────────────────────────────────────────────────────────
# Die Funktion gebaeude_zeichnen() wurde in Stunde 3 in das Modul
# gebaeude.py ausgelagert. Sie wird in der Spielschleife aufgerufen:
#   gebaeude.gebaeude_zeichnen(liste_gebaeude, kamera_x, kamera_y)
# Neu in Stunde 6: Die Funktion funktioniert automatisch für alle
# 5 Gebäudetypen, weil sie Farbe+Kürzel aus GEBAEUDE_TYPEN holt.


def kamera_begrenzen():
    """
    Verhindert dass die Kamera über den Rand der Karte scrollt.
    """
    global kamera_x, kamera_y
    karte_pixel_breite = KARTE_BREITE * KACHEL_GROESSE
    karte_pixel_hoehe  = KARTE_HOEHE  * KACHEL_GROESSE
    max_kamera_x = karte_pixel_breite - BILD_BREITE
    max_kamera_y = karte_pixel_hoehe  - BILD_HOEHE
    kamera_x = max(0, min(max_kamera_x, kamera_x))
    kamera_y = max(0, min(max_kamera_y, kamera_y))


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: WELTRAUM-HINTERGRUND
# ═════════════════════════════════════════════════════════════════════════════

def hintergrund_zeichnen():
    """
    Zeichnet den Weltraum-Hintergrund mit Sternen.
    1. Zuerst alles schwarz färben (der Weltraum)
    2. Dann Sterne darauf malen
    """
    fenster.fill(FARBE_SCHWARZ)
    for stern in sterne_liste:
        h = stern["helligkeit"]
        if random.randint(0, 10) < 2:
            stern_farbe = (h - 55, h - 35, h)
        elif random.randint(0, 10) < 2:
            stern_farbe = (h, h - 15, h - 55)
        else:
            stern_farbe = (h, h, h)
        pygame.draw.circle(fenster, stern_farbe, (stern["x"], stern["y"]), stern["groesse"])


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: HUD / ANZEIGE
# ═════════════════════════════════════════════════════════════════════════════
# Hinweis: Die alte Funktion info_text_zeichnen() wurde in Stunde 4 durch
# das HUD-Modul (hud.py) ersetzt. Alle Anzeigen laufen jetzt über:
#   hud.hud_zeichnen(ressourcen, gebaeude_auswahl, gebaeude.GEBAEUDE_TYPEN,
#                    kamera_x, kamera_y)
# ═════════════════════════════════════════════════════════════════════════════


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: EREIGNISSE VERARBEITEN
# ═════════════════════════════════════════════════════════════════════════════

def ereignisse_verarbeiten():
    """
    Geht alle Ereignisse durch die seit dem letzten Frame passiert sind.
    Gibt True zurück wenn das Spiel weiterlaufen soll, False zum Beenden.
    """
    global kamera_x, kamera_y, gebaeude_auswahl
    
    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            return False
        
        if ereignis.type == pygame.KEYDOWN:
            if ereignis.key == pygame.K_ESCAPE:
                return False
            
            # STUNDE 4 + STUNDE 6 + STUNDE 7 — GEBAEUDE-AUSWAHL MIT
            # TASTEN 1/2/3/4/5/6/7
            # Wie in Final Earth 2 wechselt der Spieler mit Tasten
            # zwischen den Gebäude-Typen.
            #   Taste 1 → Basis       (Index 0)
            #   Taste 2 → Reaktor     (Index 1)
            #   Taste 3 → Farm        (Index 2)
            #   Taste 4 → Holzfäller  (Index 3) — NEU in Stunde 6!
            #   Taste 5 → Steinmetz   (Index 4) — NEU in Stunde 6!
            #   Taste 6 → Marktplatz  (Index 5)
            #   Taste 7 → Wohnhaus    (Index 6) — NEU in Stunde 7!
            
            if ereignis.key == pygame.K_1:
                gebaeude_auswahl = 0
                print("Gebäude-Auswahl: Basis (Taste 1)")
            if ereignis.key == pygame.K_2:
                gebaeude_auswahl = 1
                print("Gebäude-Auswahl: Reaktor (Taste 2)")
            if ereignis.key == pygame.K_3:
                gebaeude_auswahl = 2
                print("Gebäude-Auswahl: Farm (Taste 3)")
            if ereignis.key == pygame.K_4:
                gebaeude_auswahl = 3
                print("Gebäude-Auswahl: Holzfaeller (Taste 4)")
            if ereignis.key == pygame.K_5:
                gebaeude_auswahl = 4
                print("Gebäude-Auswahl: Steinmetz (Taste 5)")
            if ereignis.key == pygame.K_6:
                gebaeude_auswahl = 5
                print("Gebäude-Auswahl: Marktplatz (Taste 6)")
            if ereignis.key == pygame.K_7:
                gebaeude_auswahl = 6
                print("Gebäude-Auswahl: Wohnhaus (Taste 7)")
            if ereignis.key == pygame.K_8:
                gebaeude_auswahl = 7
                print("Gebäude-Auswahl: Universitaet (Taste 8)")
            if ereignis.key == pygame.K_9:
                gebaeude_auswahl = 8
                print("Gebäude-Auswahl: Mine (Taste 9)")
            if ereignis.key == pygame.K_0:
                gebaeude_auswahl = 9
                print("Gebäude-Auswahl: Strasse (Taste 0)")

            # ── STUNDE 9 — NEU: TAB öffnet/schließt das Baumenü ────────────
            # Verbesserungsvorschlag 3: Mit TAB sieht man ALLE Gebäudetypen
            # gleichzeitig (mit Baukosten und Freischaltung) im Overlay.
            # menu.menu_umschalten() togglet den Zustand (_menu_offen).
            if ereignis.key == pygame.K_TAB:
                menu.menu_umschalten()

            # ── STUNDE 10 — NEU: F öffnet/schließt das Forschungsmenü ───────
            # Mit der Taste F kann man neue Technologien erforschen.
            if ereignis.key == pygame.K_f:
                forschung.forschung_menu_umschalten()

            # ── STUNDE 10 — NEU: F1/F2/F3 erforscht eine Technologie ───────
            # Nur wirksam, wenn das Forschungsmenü offen ist.
            if forschung.forschung_menu_ist_offen():
                if ereignis.key == pygame.K_F1:
                    forschung.technologie_erforschen("wohnbau", ressourcen_dict)
                elif ereignis.key == pygame.K_F2:
                    forschung.technologie_erforschen("produktion", ressourcen_dict)
                elif ereignis.key == pygame.K_F3:
                    forschung.technologie_erforschen("stein_effizienz", ressourcen_dict)
                elif ereignis.key == pygame.K_F4:
                    forschung.technologie_erforschen("minenbau", ressourcen_dict)
                elif ereignis.key == pygame.K_F5:
                    forschung.technologie_erforschen("reaktor_upgrade", ressourcen_dict)

            # ── STUNDE 10 — NEU: H öffnet/schließt die Hilfe ────────────────
            if ereignis.key == pygame.K_h:
                global _hilfe_offen
                _hilfe_offen = not _hilfe_offen
            
            # ── STUNDE 8 — NEU: Pause/Start/Beschleunigung ─────────────────
            # Mit der Leertaste kann pausiert werden
            # Mit Taste 1 und 2 wird die Geschwindigkeit angepasst
            if ereignis.key == pygame.K_SPACE:
                global spiel_geschwindigkeit
                spiel_geschwindigkeit = 1 if spiel_geschwindigkeit == 0 else 0
                status = "pausiert" if spiel_geschwindigkeit == 0 else "gestartet"
                print(f"Spiel {status}!")
            if ereignis.key == pygame.K_1:
                spiel_geschwindigkeit = 1
                print("Normale Geschwindigkeit (1×)")
            if ereignis.key == pygame.K_2:
                spiel_geschwindigkeit = 2
                print("Doppelte Geschwindigkeit (2×)")
            
            # ── STUNDE 7 — NEU: Taste B springt zur Basis ──────────────────
            # Die Basis ist das erste Gebäude (Index 0).
            # Wenn der Spieler "B" drückt, suchen wir die Basis in der Liste
            # und setzen die Kamera direkt darauf — ohne Animation.
            # Das ist hilfreich bei großen Karten, um schnell zurückzufinden.
            # Achtung: Die Schleifen-Variable heißt "ein_gebaeude" und NICHT
            # "gebaeude" — sonst würden wir das importierte Modul überschreiben!
            if ereignis.key == pygame.K_b:
                for ein_gebaeude in liste_gebaeude:
                    if ein_gebaeude["typ"] == 0:  # 0 = Basis
                        # Mitte der Basis-Kachel berechnen
                        ziel_x = ein_gebaeude["kachel_x"] * KACHEL_GROESSE
                        ziel_y = ein_gebaeude["kachel_y"] * KACHEL_GROESSE
                        # Kamera zentrieren (Fenster-Mitte minus halbe Kachel)
                        kamera_x = ziel_x - BILD_BREITE // 2 + KACHEL_GROESSE // 2
                        kamera_y = ziel_y - BILD_HOEHE // 2 + KACHEL_GROESSE // 2
                        kamera_begrenzen()  # Nicht über den Rand scrollen!
                        print(f"Kamera zur Basis gesprungen! ({ziel_x}, {ziel_y})")
                        break  # Nur die erste Basis suchen

        # STUNDE 3 — MAUSKLICK ERKENNEN
        # pygame.MOUSEBUTTONDOWN wird ausgelöst, wenn der Spieler klickt.
        # Wir fragen die Mausposition ab und berechnen die Kachel.
        # Dann speichern wir ein neues Gebäude in liste_gebaeude.
        #
        # STUNDE 5 — BAUEN KOSTET JETZT RESSOURCEN!
        # Bevor wir bauen, prüfen wir:
        #   1. Kann das Gebäude überhaupt gebaut werden?
        #      (Basis nur 1×, genug Ressourcen?)
        #   2. Wenn ja: Baukosten abziehen + Gebäude platzieren
        #   3. Wenn nein: Konsolenausgabe, kein Bau
        #
        # STUNDE 9 — NEU: Abreißen mit der RECHTEN Maustaste (button 3)
        # Verbesserungsvorschlag 1. Man bekommt 50 % der Baukosten zurück.

        # Mausklick erkennen (linke Maustaste) - platziert ein Gebäude
        if ereignis.type == pygame.MOUSEBUTTONDOWN:
            if ereignis.button == 1:  # 1 = linke Maustaste
                maus_x, maus_y = ereignis.pos
                # Bildschirm-Position -> Kachel-Position umrechnen
                # (Kamera-Versatz addieren, dann durch Kachelgröße teilen)
                kachel_x = (maus_x + kamera_x) // KACHEL_GROESSE
                kachel_y = (maus_y + kamera_y) // KACHEL_GROESSE
                
                # ── STUNDE 8: Boden-Typ der Kachel prüfen ──────────────────
                # Hole den Bodentyp der angeklickten Kachel
                if 0 <= kachel_y < KARTE_HOEHE and 0 <= kachel_x < KARTE_BREITE:
                    boden_typ = karten_daten[kachel_y][kachel_x]
                else:
                    boden_typ = None  # Außerhalb der Karte
                
                # ── STUNDE 5: Baukosten prüfen vor dem Bauen ──────────────
                # kann_bauen() prüft:
                #   - Darf die Basis nur 1× gebaut werden?
                #   - Sind genug Ressourcen für die Baukosten da?
                #   - Ist das Gebäude schon freigeschaltet? (NEU in Stunde 9)
                # Neu in Stunde 6: Funktioniert automatisch für alle 5 Typen!
                # Neu in Stunde 8: Prüft auch ob der Bodentyp passt!
                if ressourcen.kann_bauen(ressourcen_dict, liste_gebaeude,
                                          gebaeude_auswahl, boden_typ):
                    # Baukosten von den Ressourcen abziehen
                    ressourcen.baukosten_abziehen(ressourcen_dict,
                                                   gebaeude_auswahl)
                    # Gebäude platzieren (wie in Stunde 3)
                    gebaeude.gebaeude_platzieren(liste_gebaeude,
                                                  gebaeude_auswahl,
                                                  kachel_x, kachel_y)
                else:
                    # kann_bauen() hat False zurückgegeben
                    # Der Grund steht schon in der Konsolenausgabe
                    # (z.B. "Nicht genug Ressourcen fuer Holzfaeller!"
                    #  oder "Farm kann nur auf Gras gebaut werden!")
                    #
                    # NEU in Stunde 9: Damit der Spieler es AUCH IM SPIEL
                    # sieht (nicht nur in der Konsole!), zeigen wir eine
                    # rote Meldung oben an (Verbesserungsvorschlag 5).
                    # Den Gebäudenamen holen wir aus GEBAEUDE_TYPEN.
                    gebaeude_name = gebaeude.GEBAEUDE_TYPEN[gebaeude_auswahl]["name"]
                    hud.meldung_anzeigen(
                        f"Nicht genug Rohstoffe fuer {gebaeude_name}!")

            # ── STUNDE 9 — NEU: Rechtsklick reißt ein Gebäude ab ──────────
            # ereignis.button == 3 ist die RECHTE Maustaste.
            elif ereignis.button == 3:
                maus_x, maus_y = ereignis.pos
                kachel_x = (maus_x + kamera_x) // KACHEL_GROESSE
                kachel_y = (maus_y + kamera_y) // KACHEL_GROESSE

                # 1. Gebäude von der Kachel entfernen.
                #    gebaeude_abreissen() gibt den typ_index zurück oder None.
                #    Die Basis (Index 0) kann NICHT abgerissen werden!
                typ_index = gebaeude.gebaeude_abreissen(
                    liste_gebaeude, kachel_x, kachel_y)

                # 2. Nur wenn wirklich ein Gebäude abgerissen wurde:
                if typ_index is not None:
                    # 3. 50 % der Baukosten zurückbekommen.
                    #    Die Funktion fügt die Werte zu ressourcen_dict hinzu
                    #    und liefert ein Dictionary mit den Beträgen zurück.
                    rueckerstattung = ressourcen.ressourcen_zurueckerstatten(
                        ressourcen_dict, typ_index)

                    # 4. Konsolenausgabe wie beim Bauen:
                    #    z.B. "Reaktor abgerissen! +10 gold zurueckerstattet"
                    name = gebaeude.GEBAEUDE_TYPEN[typ_index]["name"]
                    for ress_name, betrag in rueckerstattung.items():
                        print(f"{name} abgerissen! "
                              f"+{betrag} {ress_name} zurueckerstattet")
        
        # WICHTIG (Stunde 9): Das Baumenü blockiert die Mausklicks NICHT.
        # Solange es offen ist, kann man trotzdem weiterbauen. Das ist
        # bewusst so einfach gehalten — mehr dazu steht in menu.py.
        
    # ── Schritt 2: Gehaltene Tasten prüfen (Pfeiltasten UND WASD) ─────
    # WASD ist in vielen Spielen Standard (linke Hand bleibt auf der
    # Tastatur, rechte Hand kann die Maus bedienen).
    #   W = hoch, A = links, S = runter, D = rechts
    gedrueckte_tasten = pygame.key.get_pressed()
    if gedrueckte_tasten[pygame.K_LEFT] or gedrueckte_tasten[pygame.K_a]:
        kamera_x -= KAMERA_SPEED
    if gedrueckte_tasten[pygame.K_RIGHT] or gedrueckte_tasten[pygame.K_d]:
        kamera_x += KAMERA_SPEED
    if gedrueckte_tasten[pygame.K_UP] or gedrueckte_tasten[pygame.K_w]:
        kamera_y -= KAMERA_SPEED
    if gedrueckte_tasten[pygame.K_DOWN] or gedrueckte_tasten[pygame.K_s]:
        kamera_y += KAMERA_SPEED
    
    # ── Schritt 3: Rand-Scrolling mit der Maus ────────────────────────
    # Wie in Final Earth 2 (und vielen Strategiespielen): Wenn der
    # Mauszeiger nah an den Bildschirmrand kommt, scrollt die Kamera
    # automatisch in diese Richtung — ohne dass eine Taste gedrückt wird.
    RAND_ABSTAND = 25
    maus_pos_x, maus_pos_y = pygame.mouse.get_pos()
    
    if maus_pos_x < RAND_ABSTAND:
        kamera_x -= KAMERA_SPEED
    if maus_pos_x > BILD_BREITE - RAND_ABSTAND:
        kamera_x += KAMERA_SPEED
    if maus_pos_y < RAND_ABSTAND:
        kamera_y -= KAMERA_SPEED
    if maus_pos_y > BILD_HOEHE - RAND_ABSTAND:
        kamera_y += KAMERA_SPEED
    
    kamera_begrenzen()
    return True


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: SPIELSCHLEIFE (GAME LOOP)
# ═════════════════════════════════════════════════════════════════════════════

def spiel_starten():
    """
    Startet die Hauptspielschleife.
    Reihenfolge wie in Final Earth 2:
    1. Weltraum-Hintergrund
    2. Planeten-Oberfläche
    3. HUD / Anzeigetexte
    """
    global tick_zaehler
    
    print("Generiere Planeten-Oberfläche...")
    karte_generieren()
    print("Erzeuge Sternenhimmel...")
    sterne_generieren()
    
    # Gebäude-Modul initialisieren (Stunde 3) — WICHTIG!
    # Ohne diesen Aufruf bleibt _fenster in gebaeude.py auf None
    # und gebaeude_zeichnen() zeichnet dann nichts.
    gebaeude.gebaeude_initialisieren(fenster, KACHEL_GROESSE)
    
    # HUD-Modul initialisieren (Stunde 4)
    hud.hud_initialisieren(fenster)

    # Baumenü-Modul initialisieren (NEU in Stunde 9)
    # Ohne diesen Aufruf bleibt _fenster in menu.py auf None und das
    # Baumenü würde beim Öffnen (Taste TAB) nichts zeichnen.
    menu.menu_initialisieren(fenster)

    # Forschungs-Modul initialisieren (NEU in Stunde 10)
    forschung.forschung_initialisieren(fenster)
    
    print("Spiel gestartet! Drücke ESC zum Beenden.")
    print(f"Karte: {KARTE_BREITE} x {KARTE_HOEHE} Kacheln = "
          f"{KARTE_BREITE * KACHEL_GROESSE} x {KARTE_HOEHE * KACHEL_GROESSE} Pixel")
    
    laeuft = True
    
    while laeuft:
        laeuft = ereignisse_verarbeiten()
        
        # ── TICK-SYSTEM — 1× pro Sekunde (abhängig von Geschwindigkeit) ─────
        # tick_zaehler zählt die Frames (Bilder pro Sekunde).
        # Bei 60 FPS: 60 Frames = 1 Sekunde.
        # Wenn tick_zaehler 60 erreicht → produzieren → zurücksetzen.
        # Neu in Stunde 6: Auch Holzfäller und Steinmetz produzieren jetzt!
        # Neu in Stunde 8: Die Geschwindigkeit ist einstellbar:
        #   spiel_geschwindigkeit = 1 → 60 Frames (normal)
        #   spiel_geschwindigkeit = 2 → 30 Frames (doppelt)
        #   spiel_geschwindigkeit = 0 → pausiert
        global tick_zaehler, spiel_geschwindigkeit
        if spiel_geschwindigkeit > 0:
            tick_zaehler = tick_zaehler + 1
            if tick_zaehler >= 60 // spiel_geschwindigkeit:
                tick_zaehler = 0
                # Alle Gebäude produzieren/verbrauchen jetzt Ressourcen
                ressourcen.ressourcen_produzieren(ressourcen_dict,
                                                   liste_gebaeude)
        
        # ZEICHNEN (RENDERING)
        hintergrund_zeichnen()
        karte_zeichnen()
        
        # GEBÄUDE ZEICHNEN
        # Zeichnet alle platzierten Gebäude auf der Karte
        # Neu in Stunde 6: Auch Holzfäller (H) und Steinmetz (S)!
        gebaeude.gebaeude_zeichnen(liste_gebaeude, kamera_x, kamera_y)
        
        # Das HUD — immer zuletzt (liegt ganz oben)
        # Mit Baukosten-Anzeige (gebaeude_wirtschaft)
        # NEU in Stunde 9: Mausposition mitgeben → Tooltip beim Ressourcen-Icon
        hud.hud_zeichnen(ressourcen_dict, gebaeude_auswahl,
                          gebaeude.GEBAEUDE_TYPEN,
                          kamera_x, kamera_y,
                          ressourcen.GEBAEUDE_WIRTSCHAFT,
                          pygame.mouse.get_pos())

        # Das Baumenü — GANZ ZULETZT (NEU in Stunde 9)
        # Es liegt über allem anderen (halbtransparenter Hintergrund).
        # menu_zeichnen() zeichnet nur etwas, wenn das Menü offen ist.
        menu.menu_zeichnen(gebaeude.GEBAEUDE_TYPEN,
                           ressourcen.GEBAEUDE_WIRTSCHAFT,
                           ressourcen_dict)

        # Das Forschungsmenü — GANZ ZULETZT (NEU in Stunde 10)
        # Liegt über dem Baumenü, wenn es offen ist.
        forschung.forschung_menu_zeichnen(ressourcen_dict,
                                           gebaeude.GEBAEUDE_TYPEN)

        # Die Hilfe — GANZ ZULETZT (NEU in Stunde 10)
        # Wird bei Taste H ein-/ausgeblendet.
        if _hilfe_offen:
            hilfe_zeichnen()

        pygame.display.flip()
        uhr.tick(BILDER_PRO_SEKUNDE)


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: HILFE ANZEIGE
# ═════════════════════════════════════════════════════════════════════════════

def hilfe_zeichnen():
    """
    Zeichnet ein halbtransparentes Hilfe-Overlay mit allen Tasten und
    ihrer Funktion — wie ein Spickzettel für neue Spieler.

    Wird bei Taste H ein-/ausgeblendet.
    """
    overlay = pygame.Surface(fenster.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    fenster.blit(overlay, (0, 0))

    schrift_gross  = pygame.font.Font(None, 36)
    schrift_normal = pygame.font.Font(None, 24)

    titel = schrift_gross.render("HILFE — Steuerung", True, (255, 255, 100))
    fenster.blit(titel, (30, 25))

    zeilen = [
        "Tasten 1-8  — Gebäude auswählen (1=Basis, 2=Reaktor, ..., 8=Labor)",
        "TAB         — Baumenü öffnen/schließen",
        "F           — Forschungsmenü öffnen/schließen",
        "F1 / F2 / F3 — Technologie erforschen (wenn Forschungsmenü offen)",
        "H           — Diese Hilfe ein-/ausblenden",
        "ESC         — Spiel beenden",
        "",
        "Maus        — Linksklick = Gebäude bauen",
        "             Rechtsklick = Gebäude abreißen (50% zurück)",
        "Pfeiltasten / WASD — Kamera scrollen",
        "Mausrand    — Automatisch scrollen am Bildschirmrand",
        "B           — Springe zur Basis",
        "Leertaste   — Pause / Start",
        "1 / 2       — Geschwindigkeit 1x / 2x",
    ]

    y = 80
    for zeile in zeilen:
        text = schrift_normal.render(zeile, True, (220, 220, 220))
        fenster.blit(text, (50, y))
        y += 28

    hinweis = schrift_normal.render("(H drücken zum Schließen)", True, (150, 150, 150))
    fenster.blit(hinweis, (50, y + 10))


# ═════════════════════════════════════════════════════════════════════════════
# PROGRAMMSTART
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    spiel_starten()
    pygame.quit()
    sys.exit()


# =============================================================================
# ENDE STUNDE 9
# =============================================================================
# Wiederholung: Was wir heute gelernt haben
#
# Stunde 1 (Wiederholung):
#   ✓ pygame.init() startet Pygame
#   ✓ display.set_mode() erstellt das Fenster
#   ✓ Die Spielschleife: Eingaben → Logik → Zeichnen
#   ✓ Farben als (R, G, B) Tupel
#   ✓ Konstanten in GROSSBUCHSTABEN
#   ✓ Funktionen mit def
#   ✓ Kein Umlaut in Variablennamen! (laeuft statt läuft)
#
# Stunde 2 (Wiederholung):
#   ✓ Verschachtelte Schleifen (for zeile ... for spalte ...)
#   ✓ Kamera-Prinzip: pixel_x = spalte × KACHEL_GROESSE − kamera_x
#   ✓ continue = Schleifenrunde überspringen
#   ✓ pygame.key.get_pressed() für gehaltene Tasten
#   ✓ global Keyword zum Ändern globaler Variablen
#   ✓ 2D-Arrays (karten_daten[zeile][spalte])
#   ✓ Zufällige Kartengenerierung mit random
#   ✓ Sternenhimmel im Hintergrund
#
# Stunde 3 (Wiederholung):
#   ✓ pygame.MOUSEBUTTONDOWN — Mausklicks erkennen
#   ✓ ereignis.pos — Mausposition abfragen
#   ✓ Kachel aus Mausposition berechnen: kachel = (maus + kamera) // kachel_groesse
#   ✓ Gebäude speichern als Wörterbuch: {"typ": 0, "x": ..., "y": ...}
#   ✓ Gebäude zeichnen — farbige Rechtecke auf der Karte
#   ✓ Doppelbelegung prüfen — Ist die Kachel schon belegt?
#   ✓ gebaeude_zeichnen() in der richtigen Reihenfolge aufrufen
#
# Stunde 4 (Wiederholung):
#   ✓ HUD (Heads-Up Display) am oberen Bildschirmrand zeichnen
#   ✓ Ressourcen-Anzeige: Gold, Energie, Holz
#   ✓ Tasten 1/2/3 für Gebäude-Auswahl (wie in Final Earth 2!)
#   ✓ Ressourcen als Dictionary speichern {"gold": 100, ...}
#
# Stunde 5 (Wiederholung):
#   ✓ Tick-System: tick_zaehler zählt Frames, bei 60 = 1 Sekunde
#   ✓ ressourcen.ressourcen_produzieren() — 1× pro Sekunde
#   ✓ Gebäude produzieren und verbrauchen automatisch
#   ✓ Baukosten: Gebäude bauen kostet jetzt Ressourcen
#   ✓ kann_bauen() prüft vor dem Bauen (Ressourcen + Basis-Limit)
#   ✓ baukosten_abziehen() zieht Baukosten ab
#   ✓ Wenn Rohstoffe fehlen → Gebäude produziert nichts
#   ✓ Basis kann nur 1× gebaut werden
#   ✓ Baukosten-Anzeige im HUD
#
# Stunde 6 (Wiederholung):
#   ✓ Neuer Rohstoff: Stein (vierte Ressource, Startwert 20)
#   ✓ Neues Gebäude: Holzfäller (Index 3, produziert +6 Holz, kostet 1480 Gold + 5 Energie)
#   ✓ Neues Gebäude: Steinmetz (Index 4, produziert +5 Stein, kostet 15 Gold + 10 Energie)
#   ✓ Tasten 4 und 5 für Holzfäller / Steinmetz
#   ✓ GEBAEUDE_TYPEN und GEBAEUDE_WIRTSCHAFT auf 5 Einträge erweitert
#   ✓ ressourcen_produzieren() funktioniert automatisch für alle Indizes
#   ✓ gebaeude_zeichnen() funktioniert automatisch — holt Farbe aus GEBAEUDE_TYPEN
#   ✓ HUD zeigt jetzt 4 Ressourcen: Gold, Energie, Holz, Stein
#
# Stunde 7 (Wiederholung):
#   ✓ Neuer Rohstoff: Bevölkerung (fünfte Ressource, Startwert 0)
#   ✓ Neues Gebäude: Wohnhaus (Index 6, produziert +2 Bevölkerung, kostet 20 Gold + 15 Holz + 10 Stein)
#   ✓ Wohnhaus verbraucht −3 Energie pro Sekunde
#   ✓ Taste 7 für das Wohnhaus
#   ✓ GEBAEUDE_TYPEN und GEBAEUDE_WIRTSCHAFT auf 7 Einträge erweitert
#   ✓ HUD zeigt jetzt 5 Ressourcen: Gold, Energie, Holz, Stein, Bevölkerung
#   ✓ Je mehr Wohnhäuser, desto mehr Bevölkerung!
#
# Stunde 9 (HEUTE NEU):
#   ✓ Gebäude abreißen mit Rechtsklick (ereignis.button == 3)
#   ✓ 50 % der Baukosten zurück: gebaeude_abreissen() + ressourcen_zurueckerstatten()
#   ✓ Die Basis (Index 0) kann NICHT abgerissen werden
#   ✓ Baumenü mit Taste TAB (menu.py) — zeigt ALLE Gebäudetypen
#   ✓ Tooltip beim Hovern über ein Ressourcen-Icon
#   ✓ Rote Meldung im Spiel bei zu wenig Rohstoffen (hud.meldung_anzeigen)
#   ✓ Stufenweise Freischaltung: Marktplatz ab 5 Bevölkerung, Wohnhaus ab 20 Holz
#
# HÄUFIGE FEHLER zum Merken (alle Stunden):
#   ✗ spiel_laeuft ≠ spiel_laeuft  → Python sieht das als 2 verschiedene Variablen!
#   ✗ Einrückung vergessen        → IndentationError
#   ✗ Klammern nicht geschlossen  → SyntaxError
#   ✗ karte_zeichnen() vergessen  → nur schwarzer Bildschirm!
#   ✗ global kamera_x vergessen   → UnboundLocalError
#   ✗ hintergrund NACH karte      → Karte wird übermalt!
#   ✗ karten_daten[zeile][spalte] → zeile zuerst, dann spalte!
#   ✗ Kachel-Berechnung: (maus_x + kamera_x) // GROESSE vergessen
#   ✗ gebaeude_zeichnen() in falscher Reihenfolge aufgerufen
#   ✗ Kameraposition nicht in die Berechnung einbezogen
#   ✗ tick_zaehler nicht global deklariert → UnboundLocalError!
#   ✗ kann_bauen() vergessen → Gebäude gebaut ohne Ressourcen zu bezahlen
#   ✗ baukosten_abziehen() ohne vorherige kann_bauen()-Prüfung → Schulden!
#   ✗ GEBAEUDE_TYPEN und GEBAEUDE_WIRTSCHAFT müssen gleiche Länge haben!
#   ✗ Beim Hinzufügen neuer Gebäude beide Listen gleichzeitig erweitern!
#   ✗ Rückerstattung ohne vorherige Abriss-Prüfung → Gold geschenkt!
#     (Erst gebaeude_abreissen() aufrufen und typ_index auf None prüfen.)
#   ✗ TAB-Menü blockiert nicht den Mausklick — daran denken!
#     (Solange es offen ist, kann man trotzdem bauen.)
#   ✗ Freischaltung vergessen bei neuen Gebäuden nachzutragen!
#     (Sonst Index- bzw. KeyError zwischen den beiden Listen.)
#   ✗ Mausposition nicht an hud_zeichnen() übergeben → kein Tooltip.
#
# Nächste Stunde (Stunde 10):
#   → Volles Forschungssystem als eigenes Modul (forschung.py)
#   → Feinschliff, Balancing & mehr Gebäude
# =============================================================================
