"""
=============================================================================
PROJEKT: Weltraum-Koloniespiel  —  wie FINAL EARTH 2
STUNDE 3 — Gebäude bauen und Kolonie aufbauen
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

Heute in Stunde 3 lernen wir NEU dazu:
    ✓ Mausklick erkennen mit pygame.MOUSEBUTTONDOWN
    ✓ Kachel unter dem Mauszeiger berechnen
    ✓ Gebäude auf der Karte platzieren (wie in Final Earth 2!)
    ✓ Gebäude zeichnen (farbige Rechtecke auf der Karte)
    ✓ Erste Kolonie-Gebäude: Basis, Reaktor, Farm
    ✓ Gebäude speichern in einer Liste

=============================================================================
"""

import pygame
import sys
import random       # Für zufällige Planeten-Generation


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
# Für Stunde 2 haben wir erstmal die Kamera und die Karten-Daten.
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

# ├────────────────────────────────────────────────────────────────────────────
# ┌────────────────────────────────────────────────────────────────────────────┐
# │ STUNDE 3 — NEUE VARIABLEN                                                 │
# │                                                                           │
# │ In dieser Stunde kommen neue Variablen dazu:                              │
# │ Wir brauchen eine Liste für alle Gebäude, die auf der Karte stehen.       │
# │ Wir brauchen eine Variable, welches Gebäude gerade ausgewählt ist.        │
# │ Wir brauchen die Maus-Position und wo der Spieler geklickt hat.           │
# │                                                                           │
# │ TODO: Diese Variablen werden in Stunde 3 aktiviert.                       │
# │ FÜGE SIE EIN unter den bestehenden Variablen (nach sterne_liste):         │
# │                                                                           │
# │   liste_gebaeude = []       # Alle Gebäude auf der Karte                  │
# │   gebaeude_auswahl = 0      # 0 = Basis, 1 = Reaktor, 2 = Farm           │
# │   maus_x = 0                # Maus-X-Position auf dem Bildschirm          │
# │   maus_y = 0                # Maus-Y-Position auf dem Bildschirm          │
# │   klick_x = -1              # Zuletzt angeklickte Kachel (Spalte)         │
# │   klick_y = -1              # Zuletzt angeklickte Kachel (Zeile)          │
# │                                                                           │
# └────────────────────────────────────────────────────────────────────────────┘


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
    # [ [0, 0, 0, ...], [0, 0, 0, ...], ... ]
    karten_daten = []
    for zeile in range(KARTE_HOEHE):
        neue_zeile = []
        for spalte in range(KARTE_BREITE):
            neue_zeile.append(0)  # 0 = Erde (Standard)
        karten_daten.append(neue_zeile)
    
    # ── Schritt 1: Große Gras-Flächen erzeugen ────────────────────────────
    # Wir wählen zufällig 8 Stellen auf der Karte aus.
    # Um jede Stelle entsteht eine große Gras-Fläche.
    anzahl_gras_flaechen = 8
    
    for _ in range(anzahl_gras_flaechen):
        # Zufällige Mittelpunkt-Position
        mitte_x = random.randint(5, KARTE_BREITE - 5)
        mitte_y = random.randint(5, KARTE_HOEHE - 5)
        
        # Die Grasfläche ist 4-10 Kacheln groß (zufällig)
        radius = random.randint(4, 10)
        
        # Alle Kacheln im Umkreis werden zu Gras
        for zeile in range(KARTE_HOEHE):
            for spalte in range(KARTE_BREITE):
                # Abstand zum Mittelpunkt berechnen
                abstand = ((spalte - mitte_x) ** 2 + (zeile - mitte_y) ** 2) ** 0.5
                # Wenn der Abstand kleiner als der Radius ist → Gras
                if abstand < radius:
                    karten_daten[zeile][spalte] = 1  # 1 = Gras
    
    # ── Schritt 2: Gesteins-Flächen erzeugen ──────────────────────────────
    # Felsen sind seltener als Gras — nur 5 Vorkommen.
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
    # Sand gibt es an 6 Stellen.
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
    
    Wie in Final Earth 2 funkeln im Hintergrund Sterne.
    Jeder Stern hat eine zufällige Position und Helligkeit.
    Die Sterne sind über das ganze Fenster verteilt — auch hinter der Karte.
    """
    global sterne_liste
    
    sterne_liste = []
    
    # 150 Sterne erzeugen — genug für einen schönen Sternenhimmel
    for _ in range(150):
        stern = {
            "x": random.randint(0, BILD_BREITE),           # Zufällige x-Position
            "y": random.randint(0, BILD_HOEHE),            # Zufällige y-Position
            "groesse": random.randint(1, 3),               # 1, 2 oder 3 Pixel groß
            "helligkeit": random.randint(100, 255)          # 100 = dunkel, 255 = hell
        }
        sterne_liste.append(stern)


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: KARTE ZEICHNEN
# ═════════════════════════════════════════════════════════════════════════════
# Der wichtigste Block dieser Stunde!
# Hier zeichnen wir die Planeten-Oberfläche auf den Bildschirm.
# Wie in Final Earth 2 siehst du ein Gitter aus Kacheln.
# ═════════════════════════════════════════════════════════════════════════════

def karte_zeichnen():
    """
    Zeichnet alle Kacheln der Planeten-Oberfläche auf den Bildschirm.
    
    So wie in Final Earth 2:
    - Die Karte besteht aus vielen kleinen Kacheln
    - Jede Kachel hat eine Farbe je nach Bodentyp
    - Durch Kamerascrollen können wir die ganze Karte erkunden
    
    KAMERA-PRINZIP (wichtig!):
        pixel_x = spalte * KACHEL_GROESSE - kamera_x
        pixel_y = zeile  * KACHEL_GROESSE - kamera_y
        
        Wenn kamera_x = 100 → alle Kacheln 100 Pixel nach links
        → Es sieht aus als ob wir 100 Pixel nach rechts geschaut haben!
    """
    # Die Farben für jeden Bodentyp (0, 1, 2, 3)
    farben = {
        0: FARBE_ERDE_HELL,     # Erde (häufigster Boden)
        1: FARBE_GRAS,          # Gras (fruchtbar)
        2: FARBE_GESTEIN,       # Gestein (Felsen)
        3: FARBE_SAND           # Sand (Wüste)
    }
    
    # Durch alle Zeilen der Karte gehen (von oben nach unten)
    for zeile in range(KARTE_HOEHE):
        
        # Durch alle Spalten der Karte gehen (von links nach rechts)
        for spalte in range(KARTE_BREITE):
            
            # --- SCHRITT 1: Bildschirm-Position berechnen ---
            # pixel_x / pixel_y = wo die Kachel auf dem Bildschirm erscheint
            # Formel: Gitterposition × Kachelgröße − Kamera-Versatz
            pixel_x = spalte * KACHEL_GROESSE - kamera_x
            pixel_y = zeile  * KACHEL_GROESSE - kamera_y
            
            # --- SCHRITT 2: Unsichtbare Kacheln überspringen ---
            # Wenn eine Kachel nicht auf dem Bildschirm zu sehen ist,
            # müssen wir sie nicht zeichnen. Das spart Rechenzeit!
            # 
            # Bedingungen für "nicht sichtbar":
            #   - Komplett links vom Fenster (pixel_x + groesse < 0)
            #   - Komplett über dem Fenster (pixel_y + groesse < 0)
            #   - Komplett rechts vom Fenster (pixel_x > BILD_BREITE)
            #   - Komplett unter dem Fenster (pixel_y > BILD_HOEHE)
            #
            # continue = "diese Schleifenrunde überspringen, nächste starten"
            if pixel_x + KACHEL_GROESSE < 0:   continue    # zu weit links
            if pixel_y + KACHEL_GROESSE < 0:   continue    # zu weit oben
            if pixel_x > BILD_BREITE:          continue    # zu weit rechts
            if pixel_y > BILD_HOEHE:           continue    # zu weit unten
            
            # --- SCHRITT 3: Boden-Typ aus der Karte lesen ---
            boden_typ = karten_daten[zeile][spalte]
            
            # --- SCHRITT 4: Farbe für diesen Bodentyp holen ---
            kachel_farbe = farben[boden_typ]
            
            # --- SCHRITT 5: Kachel zeichnen ---
            # Ein Rechteck (Rect) beschreibt eine Position und Größe.
            # pygame.Rect(x, y, breite, hoehe)
            kachel_rect = pygame.Rect(pixel_x, pixel_y, KACHEL_GROESSE, KACHEL_GROESSE)
            
            # Die Kachel mit der Bodenfarbe ausfüllen
            pygame.draw.rect(fenster, kachel_farbe, kachel_rect)
            
            # Gitterlinie als Rahmen zeichnen (1 Pixel dick)
            # So sieht es aus wie in Final Earth 2!
            pygame.draw.rect(fenster, FARBE_GITTER, kachel_rect, 1)


# ├────────────────────────────────────────────────────────────────────────────
# ┌────────────────────────────────────────────────────────────────────────────┐
# │ STUNDE 3 — NEUE FUNKTION: gebaeude_zeichnen()                            │
# │                                                                           │
# │ Nachdem alle Kacheln gezeichnet sind, müssen wir die Gebäude zeichnen.    │
# │ Die Gebäude sind farbige Rechtecke auf der Karte — wie in Final Earth 2! │
# │                                                                           │
# │ Jedes Gebäude in liste_gebaeude hat:                                      │
# │   - "typ": 0 = Basis, 1 = Reaktor, 2 = Farm                              │
# │   - "x": Kachel-Spalte                                                    │
# │   - "y": Kachel-Zeile                                                     │
# │                                                                           │
# │ TODO: Diese Funktion in Stunde 3 AUSSERHALB von karte_zeichnen()          │
# │ als eigene Funktion definieren:                                           │
# │                                                                           │
# │   def gebaeude_zeichnen(fenster, kamera_x, kamera_y):                     │
# │       for gebaeude in liste_gebaeude:                                     │
# │           pixel_x = gebaeude["x"] * KACHEL_GROESSE - kamera_x             │
# │           pixel_y = gebaeude["y"] * KACHEL_GROESSE - kamera_y             │
# │           # Gebäude als farbiges Rechteck zeichnen                        │
# │           pygame.draw.rect(fenster, farbe, (pixel_x, pixel_y, ...))       │
# │                                                                           │
# │ Die Funktion wird dann in der Spielschleife aufgerufen!                   │
# └────────────────────────────────────────────────────────────────────────────┘


def kamera_begrenzen():
    """
    Verhindert dass die Kamera über den Rand der Karte scrollt.
    
    Stell dir vor: Du hast eine große Zeitung auf dem Tisch.
    Mit einer Lupe schaust du darauf. Du kannst die Lupe nur so weit
    bewegen bis du am Rand der Zeitung angekommen bist.
    
    Genauso ist es mit der Kamera:
    - Maximaler Ausschnitt = Kartengröße in Pixeln minus Fenstergröße
    - Kamera kann nicht negativ werden (linker/oberer Rand)
    - Kamera kann nicht größer als Maximum werden (rechter/unterer Rand)
    """
    global kamera_x, kamera_y  # global = wir dürfen die Werte ändern
    
    # Kartengröße in Pixeln berechnen
    karte_pixel_breite = KARTE_BREITE * KACHEL_GROESSE
    karte_pixel_hoehe  = KARTE_HOEHE  * KACHEL_GROESSE
    
    # Wie weit können wir maximal scrollen?
    # Antwort: Kartengröße − Fenstergröße
    # (Wenn die Karte genau so groß wie das Fenster ist → gar nicht scrollen)
    max_kamera_x = karte_pixel_breite - BILD_BREITE
    max_kamera_y = karte_pixel_hoehe  - BILD_HOEHE
    
    # max(0, wert) = Wert kann nicht kleiner als 0 werden
    # min(max, wert) = Wert kann nicht größer als max werden
    kamera_x = max(0, min(max_kamera_x, kamera_x))
    kamera_y = max(0, min(max_kamera_y, kamera_y))


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: WELTRAUM-HINTERGRUND
# ═════════════════════════════════════════════════════════════════════════════
# Der Weltraum-Hintergrund aus Stunde 1 — aber jetzt mit Sternen!
# Wie in Final Earth 2 siehst du das Weltall mit funkelnden Sternen.
# ═════════════════════════════════════════════════════════════════════════════

def hintergrund_zeichnen():
    """
    Zeichnet den Weltraum-Hintergrund mit Sternen.
    
    Wie in Final Earth 2:
    1. Zuerst alles schwarz färben (der Weltraum)
    2. Dann Sterne darauf malen (als kleine weiße Punkte)
    
    Das machen wir JEDEN Frame als erstes — damit wird der letzte
    Frame komplett übermalt. Sonst verschmiert alles!
    """
    # 1. Schwarzer Weltraum-Hintergrund
    fenster.fill(FARBE_SCHWARZ)
    
    # 2. Sterne zeichnen
    for stern in sterne_liste:
        # Die Helligkeit bestimmt die Farbe
        # dunkle Sterne = grau, helle Sterne = weiß/gelb/blau
        h = stern["helligkeit"]
        
        # Verschiedene Sternfarben für Abwechslung
        if random.randint(0, 10) < 2:  # 20% Chance für blauen Stern
            stern_farbe = (h - 55, h - 35, h)
        elif random.randint(0, 10) < 2:  # 20% Chance für gelben Stern
            stern_farbe = (h, h - 15, h - 55)
        else:  # 60% normale weiße Sterne
            stern_farbe = (h, h, h)
        
        # Den Stern als kleinen Kreis oder Rechteck zeichnen
        pygame.draw.circle(
            fenster,
            stern_farbe,
            (stern["x"], stern["y"]),
            stern["groesse"]
        )


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: HUD / ANZEIGE (Kameraposition und Steuerung)
# ═════════════════════════════════════════════════════════════════════════════
# Das HUD (Heads-Up-Display) zeigt Informationen auf dem Bildschirm an.
# Wie in Final Earth 2 siehst du hier die wichtigsten Daten.
# # TIPP: In Stunde 4 kommt hier die Ressourcen-Anzeige dazu!
# ═════════════════════════════════════════════════════════════════════════════

def info_text_zeichnen():
    """
    Zeigt Kameraposition und Steuerungshinweise an.
    
    Wie in Final Earth 2 siehst du oben links Informationen:
    - Wo bist du gerade auf der Karte? (Kameraposition)
    - Wie bedienst du das Spiel? (Steuerung)
    
    TIPP für später:
    In Stunde 4 wird diese Funktion durch hud_zeichnen() ersetzt.
    Dann siehst du hier:
    - Ressourcen (Gold, Energie, Holz)
    - Gebäude-Auswahl
    - Missions-Ziele
    """
    # Eine Schrift erstellen: None = Standardschrift, Größe in Pixeln
    schrift = pygame.font.Font(None, 24)
    schrift_klein = pygame.font.Font(None, 18)
    
    # ── Kameraposition anzeigen ──────────────────────────────────────────
    # Welche Kachel sehen wir gerade in der oberen linken Ecke?
    kachel_x = max(0, kamera_x // KACHEL_GROESSE)
    kachel_y = max(0, kamera_y // KACHEL_GROESSE)
    
    kamera_info = schrift.render(
        f"Position: Kachel ({kachel_x}, {kachel_y})  |  Kamera: x={kamera_x}  y={kamera_y}",
        True, FARBE_TEXT_HELL
    )
    fenster.blit(kamera_info, (15, 15))
    
    # ── Karten-Größe anzeigen ────────────────────────────────────────────
    karten_info = schrift_klein.render(
        f"Karte: {KARTE_BREITE} x {KARTE_HOEHE} Kacheln  |  "
        f"Pfeiltasten zum Scrollen  |  ESC = Beenden",
        True, FARBE_TEXT_DUNKEL
    )
    fenster.blit(karten_info, (15, 45))
    
    # ── Legende der Bodentypen ────────────────────────────────────────────
    # Wie in Final Earth 2 — eine kleine Legende der Umgebung
    legende_text = schrift_klein.render(
        "Legende:  █ Erde  █ Gras  █ Gestein  █ Sand",
        True, FARBE_TEXT_DUNKEL
    )
    fenster.blit(legende_text, (15, 70))
    
    # Kleine farbige Kästchen für die Legende zeichnen
    legende_start = 330  # x-Position für die Farbkästchen
    farben_legende = [FARBE_ERDE_HELL, FARBE_GRAS, FARBE_GESTEIN, FARBE_SAND]
    for i, farbe in enumerate(farben_legende):
        kasten_x = legende_start + i * 55
        kasten_rect = pygame.Rect(kasten_x, 70, 14, 14)
        pygame.draw.rect(fenster, farbe, kasten_rect)
        pygame.draw.rect(fenster, FARBE_GITTER, kasten_rect, 1)


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: EREIGNISSE VERARBEITEN
# ═════════════════════════════════════════════════════════════════════════════
# Diese Funktion prüft was der Spieler gerade tut.
# Wie in Final Earth 2 kannst du:
# - Mit Pfeiltasten die Karte erkunden
# - Mit ESC das Spiel beenden
# - Auf das X klicken um das Fenster zu schließen
# ═════════════════════════════════════════════════════════════════════════════

def ereignisse_verarbeiten():
    """
    Geht alle Ereignisse durch die seit dem letzten Frame passiert sind.
    Gibt True zurück wenn das Spiel weiterlaufen soll, False zum Beenden.
    
    In Final Earth 2 gibt es viele Eingabe-Möglichkeiten:
    - Tastatur (Pfeiltasten, Zahlen, ESC)
    - Maus (Klicken, Ziehen)
    - Fenster-Ereignisse (Schließen, Minimieren)
    
    TIPP: Hier kommen in späteren Stunden mehr Eingaben dazu!
    - Stunde 3: Mausklick → Gebäude platzieren
    - Stunde 4: Tasten 1/2/3 → Gebäude-Typ wechseln
    
    So würde Mausklick in Stunde 3 funktionieren:
    1. pygame.MOUSEBUTTONDOWN erkennen (Maus wurde geklickt)
    2. Maus-Position abfragen: ereignis.pos
    3. Kachel berechnen: 
       kachel_x = (maus_x + kamera_x) // KACHEL_GROESSE
       kachel_y = (maus_y + kamera_y) // KACHEL_GROESSE
    4. Gebäude in liste_gebaeude speichern
    """
    global kamera_x, kamera_y
    
    # ── Schritt 1: Einmal-Ereignisse prüfen ────────────────────────────
    # pygame.event.get() gibt eine Liste aller neuen Ereignisse zurück
    for ereignis in pygame.event.get():
        
        # QUIT = Spieler hat auf das X-Symbol geklickt
        if ereignis.type == pygame.QUIT:
            return False
        
        # KEYDOWN = eine Taste wurde gedrückt (nur einmal!)
        if ereignis.type == pygame.KEYDOWN:
            # K_ESCAPE = die ESC-Taste
            if ereignis.key == pygame.K_ESCAPE:
                return False

        # ├────────────────────────────────────────────────────────────────────
        # ┌────────────────────────────────────────────────────────────────────┐
        # │ STUNDE 3 — MAUSKLICK ERKENNEN                                     │
        # │                                                                   │
        # │ pygame.MOUSEBUTTONDOWN wird ausgelöst, wenn der Spieler klickt.    │
        # │ Wir fragen die Mausposition ab und berechnen die Kachel.          │
        # │ Dann speichern wir ein neues Gebäude in liste_gebaeude.           │
        # │                                                                   │
        # │ TODO: Diesen Code in Stunde 3 EINFÜGEN an dieser Stelle:          │
        # │                                                                   │
        # │   # Mausklick erkennen (linke Maustaste)                          │
        # │   if ereignis.type == pygame.MOUSEBUTTONDOWN:                     │
        # │       if ereignis.button == 1:  # Linke Maustaste                 │
        # │           maus_x, maus_y = ereignis.pos                           │
        # │           # Kachel-Position berechnen:                            │
        # │           kachel_x = (maus_x + kamera_x) // KACHEL_GROESSE        │
        # │           kachel_y = (maus_y + kamera_y) // KACHEL_GROESSE        │
        # │           # Gebäude zur Liste hinzufügen                          │
        # │           neues_gebaeude = {                                      │
        # │               "typ": gebaeude_auswahl,                            │
        # │               "x": kachel_x,                                      │
        # │               "y": kachel_y                                       │
        # │           }                                                       │
        # │           liste_gebaeude.append(neues_gebaeude)                   │
        # │                                                                   │
        # └────────────────────────────────────────────────────────────────────┘
    
    # ── Schritt 2: Gehaltene Tasten prüfen ────────────────────────────
    # get_pressed() = reagiert SOLANGE die Taste gedrückt ist
    # So können wir mit Pfeiltasten flüssig scrollen wie in Final Earth 2!
    gedrueckte_tasten = pygame.key.get_pressed()
    
    if gedrueckte_tasten[pygame.K_LEFT]:
        kamera_x -= KAMERA_SPEED
    if gedrueckte_tasten[pygame.K_RIGHT]:
        kamera_x += KAMERA_SPEED
    if gedrueckte_tasten[pygame.K_UP]:
        kamera_y -= KAMERA_SPEED
    if gedrueckte_tasten[pygame.K_DOWN]:
        kamera_y += KAMERA_SPEED
    
    # ── Schritt 3: Kamera begrenzen ──────────────────────────────────
    # Nach jeder Bewegung prüfen ob die Kamera noch innerhalb der Karte ist
    kamera_begrenzen()
    
    return True  # True = Spiel läuft weiter


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: SPIELSCHLEIFE (GAME LOOP)
# ═════════════════════════════════════════════════════════════════════════════
# Das ist das Herz jedes Spiels!
# Die Spielschleife läuft 60 Mal pro Sekunde und macht immer 3 Schritte:
#
#   SCHRITT 1: EINGABEN   → Was hat der Spieler getan? (Tasten, Maus)
#   SCHRITT 2: LOGIK      → Spiel-Berechnungen (Bewegung, Kollision)
#   SCHRITT 3: ZEICHNEN   → Alles auf den Bildschirm malen
#
# Wie in Final Earth 2 — ohne Spielschleife kein Spiel!
# ═════════════════════════════════════════════════════════════════════════════

def spiel_starten():
    """
    Startet die Hauptspielschleife.
    Läuft so lange bis der Spieler das Spiel beendet (ESC oder X klicken).
    
    Die Reihenfolge beim Zeichnen ist EXTREM wichtig!
    Was zuletzt gezeichnet wird, liegt OBEN drauf.
    Wie bei einem Daumenkino: Das oberste Blatt überdeckt alles darunter.
    
    Reihenfolge wie in Final Earth 2:
    1. Weltraum-Hintergrund (schwarz + Sterne)
    2. Planeten-Oberfläche (die Karte mit Kacheln)
    3. HUD / Anzeigetexte (immer oben drauf)
    """
    # Zuerst die Planeten-Oberfläche generieren
    # Jedes Spiel hat eine andere Karte!
    print("Generiere Planeten-Oberfläche...")
    karte_generieren()
    
    # Dann die Sterne für den Hintergrund erzeugen
    print("Erzeuge Sternenhimmel...")
    sterne_generieren()
    
    # Startmeldung
    print("Spiel gestartet! Drücke ESC zum Beenden.")
    print(f"Karte: {KARTE_BREITE} x {KARTE_HOEHE} Kacheln = "
          f"{KARTE_BREITE * KACHEL_GROESSE} x {KARTE_HOEHE * KACHEL_GROESSE} Pixel")
    
    # laeuft = True solange das Spiel läuft
    # WICHTIG: Kein Umlaut in Variablennamen! (laeuft statt läuft)
    # Python erlaubt Umlaute aber es macht oft Probleme — besser vermeiden!
    laeuft = True
    
    while laeuft:
        
        # --- SCHRITT 1: EINGABEN VERARBEITEN ---
        # Prüfen was der Spieler gemacht hat
        # Wenn False zurückkommt: Schleife beenden
        laeuft = ereignisse_verarbeiten()
        
        # --- SCHRITT 2: LOGIK UND BERECHNUNGEN ---
        # Hier berechnen wir was sich im Spiel verändert hat
        # TIPP: Ab Stunde 5 kommen hier Ressourcen-Updates rein
        # TIPP: Ab Stunde 6 kommen hier Gegner-Bewegungen rein
        pass    # pass = "hier kommt noch etwas, aber erst später"
        
        # --- SCHRITT 3: ZEICHNEN (RENDERING) ---
        # REIHENFOLGE BEACHTEN! Was zuletzt kommt, liegt oben!
        # In Final Earth 2 wird so gezeichnet:
        #   1. Hintergrund (Weltall + Sterne)
        #   2. Planeten-Oberfläche (Kacheln + Gitter)
        #   3. Gebäude (Basis, Reaktor, Farm — NEU in Stunde 3!)
        #   4. HUD (Informationen — wird in Stunde 4 erweitert)
        
        # 1. Zuerst Hintergrund — übermalt alles vom letzten Frame
        hintergrund_zeichnen()
        
        # 2. Dann die Planeten-Oberfläche (die Karte)
        karte_zeichnen()
        
        # ├────────────────────────────────────────────────────────────────────
        # ┌────────────────────────────────────────────────────────────────────┐
        # │ STUNDE 3 — GEBÄUDE ZEICHNEN                                       │
        # │                                                                   │
        # │ Hier rufen wir die neue Funktion gebaeude_zeichnen() auf.         │
        # │ Die Gebäude müssen zwischen Karte und HUD liegen!                 │
        # │                                                                   │
        # │ TODO: Diese Zeile in Stunde 3 HIER EINFÜGEN (zwischen Karte+HUD): │
        # │                                                                   │
        # │   gebaeude_zeichnen(fenster, kamera_x, kamera_y)                  │
        # │                                                                   │
        # └────────────────────────────────────────────────────────────────────┘
        
        # 3. Das HUD / Anzeigetexte — immer zuletzt (liegt ganz oben)
        # TIPP: Ab Stunde 4 wird info_text_zeichnen() durch hud_zeichnen() ersetzt
        info_text_zeichnen()
        
        # display.flip() zeigt alles was wir gemalt haben an
        # (vorher war es nur im Hintergrund vorbereitet — wie ein Daumenkino)
        pygame.display.flip()
        
        # Die Uhr begrenzt die Geschwindigkeit auf BILDER_PRO_SEKUNDE FPS
        # Damit läuft das Spiel auf jedem Computer gleich schnell
        uhr.tick(BILDER_PRO_SEKUNDE)


# ═════════════════════════════════════════════════════════════════════════════
# PROGRAMMSTART
# ═════════════════════════════════════════════════════════════════════════════
# Dieser Block wird nur ausgeführt wenn wir DIESE Datei direkt starten.
# Wenn die Datei importiert wird (import main), läuft dieser Block NICHT.
# Das bleibt immer ganz unten — das ändert sich nie!
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    spiel_starten()     # Das Spiel starten
    pygame.quit()       # Pygame sauber beenden wenn die Schleife endet
    sys.exit()          # Das Programm komplett beenden


# =============================================================================
# ENDE STUNDE 3
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
# Stunde 3 (HEUTE NEU):
#   ✓ pygame.MOUSEBUTTONDOWN — Mausklicks erkennen
#   ✓ ereignis.pos — Mausposition abfragen
#   ✓ Kachel aus Mausposition berechnen: kachel = (maus + kamera) // kachel_groesse
#   ✓ Gebäude speichern als Wörterbuch: {"typ": 0, "x": ..., "y": ...}
#   ✓ Gebäude zeichnen — farbige Rechtecke auf der Karte
#   ✓ Doppelbelegung prüfen — Ist die Kachel schon belegt?
#   ✓ gebaeude_zeichnen() in der richtigen Reihenfolge aufrufen
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
#
# Nächste Stunde (Stunde 4):
#   → Ressourcen-Anzeige (HUD erweitern)
#   → Gebäude-Auswahl mit Tasten 1/2/3
#   → hud_zeichnen() statt info_text_zeichnen()
#   → Ressourcen sammeln: Gold, Energie, Holz
# =============================================================================