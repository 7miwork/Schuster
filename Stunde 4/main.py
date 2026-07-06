"""
=============================================================================
PROJEKT: Weltraum-Koloniespiel  —  wie FINAL EARTH 2
STUNDE 4 — HUD & Ressourcenanzeige
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

Heute in Stunde 4 lernen wir NEU dazu:
    ✓ HUD (Heads-Up Display) am oberen Bildschirmrand zeichnen
    ✓ Ressourcen-Anzeige: Gold, Energie, Holz
    ✓ Tasten 1/2/3 für Gebäude-Auswahl (wie in Final Earth 2!)
    ✓ Ressourcen als Dictionary speichern {"gold": 100, ...}

=============================================================================
"""

import pygame
import sys
import random       # Für zufällige Planeten-Generation
import gebaeude     # Gebäude-Modul aus Stunde 3
import hud          # HUD-Modul aus Stunde 4


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
# Für Stunde 4 zeigen wir sie erstmal nur im HUD an.
# Das Dictionary speichert jede Ressource mit ihrem Namen und aktuellen Wert.
ressourcen = {"gold": 100, "energie": 50, "holz": 30}

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
gebaeude_auswahl = 0      # 0 = Basis, 1 = Reaktor, 2 = Farm
maus_x = 0                # Maus-X-Position auf dem Bildschirm
maus_y = 0                # Maus-Y-Position auf dem Bildschirm
klick_x = -1              # Zuletzt angeklickte Kachel (Spalte)
klick_y = -1              # Zuletzt angeklickte Kachel (Zeile)

# Für Stunde 4 fügen wir ausserdem die Ressourcen-Anzeige hinzu.


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


# ├────────────────────────────────────────────────────────────────────────────
# │ STUNDE 3 — GEBÄUDE ZEICHNEN
# │ Jedes Gebäude in liste_gebaeude hat: "typ", "kachel_x", "kachel_y"
# │ TODO: Diese Funktion in Stunde 3 als eigene Funktion definieren:
# │   def gebaeude_zeichnen(fenster, kamera_x, kamera_y):
# │       for gebaeude in liste_gebaeude:
# │           pixel_x = gebaeude["kachel_x"] * KACHEL_GROESSE - kamera_x
# │           pixel_y = gebaeude["kachel_y"] * KACHEL_GROESSE - kamera_y
# │           # Gebäude als farbiges Rechteck zeichnen
# │ Die Funktion wird dann in der Spielschleife aufgerufen!
# └────────────────────────────────────────────────────────────────────────────┘


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

def info_text_zeichnen():
    """
    Zeigt Kameraposition und Steuerungshinweise an.
    TIPP fuer spaeter:
    In Stunde 4 wird diese Funktion durch hud_zeichnen() ersetzt.
    """
    schrift = pygame.font.Font(None, 24)
    schrift_klein = pygame.font.Font(None, 18)
    
    kachel_x = max(0, kamera_x // KACHEL_GROESSE)
    kachel_y = max(0, kamera_y // KACHEL_GROESSE)
    
    kamera_info = schrift.render(
        f"Position: Kachel ({kachel_x}, {kachel_y})  |  Kamera: x={kamera_x}  y={kamera_y}",
        True, FARBE_TEXT_HELL
    )
    fenster.blit(kamera_info, (15, 15))
    
    karten_info = schrift_klein.render(
        f"Karte: {KARTE_BREITE} x {KARTE_HOEHE} Kacheln  |  "
        f"Pfeiltasten zum Scrollen  |  ESC = Beenden",
        True, FARBE_TEXT_DUNKEL
    )
    fenster.blit(karten_info, (15, 45))
    
    legende_text = schrift_klein.render(
        "Legende:  Erde  Gras  Gestein  Sand",
        True, FARBE_TEXT_DUNKEL
    )
    fenster.blit(legende_text, (15, 70))
    
    legende_start = 330
    farben_legende = [FARBE_ERDE_HELL, FARBE_GRAS, FARBE_GESTEIN, FARBE_SAND]
    for i, farbe in enumerate(farben_legende):
        kasten_x = legende_start + i * 55
        kasten_rect = pygame.Rect(kasten_x, 70, 14, 14)
        pygame.draw.rect(fenster, farbe, kasten_rect)
        pygame.draw.rect(fenster, FARBE_GITTER, kasten_rect, 1)


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
            
            # STUNDE 4 — GEBAEUDE-AUSWAHL MIT TASTEN 1/2/3
            # Wie in Final Earth 2 wechselt der Spieler mit Tasten 1/2/3
            # zwischen den Gebäude-Typen.
            #   Taste 1 → Basis (Index 0)
            #   Taste 2 → Reaktor (Index 1)
            #   Taste 3 → Farm (Index 2)
            
            if ereignis.key == pygame.K_1:
                gebaeude_auswahl = 0
                print("Gebäude-Auswahl: Basis (Taste 1)")
            if ereignis.key == pygame.K_2:
                gebaeude_auswahl = 1
                print("Gebäude-Auswahl: Reaktor (Taste 2)")
            if ereignis.key == pygame.K_3:
                gebaeude_auswahl = 2
                print("Gebäude-Auswahl: Farm (Taste 3)")

        # STUNDE 3 — MAUSKLICK ERKENNEN
        # pygame.MOUSEBUTTONDOWN wird ausgelöst, wenn der Spieler klickt.
        # Wir fragen die Mausposition ab und berechnen die Kachel.
        # Dann speichern wir ein neues Gebäude in liste_gebaeude.
        
        # Mausklick erkennen (linke Maustaste) - platziert ein Gebäude
        if ereignis.type == pygame.MOUSEBUTTONDOWN:
            if ereignis.button == 1:  # 1 = linke Maustaste
                maus_x, maus_y = ereignis.pos
                # Bildschirm-Position -> Kachel-Position umrechnen
                # (Kamera-Versatz addieren, dann durch Kachelgröße teilen)
                kachel_x = (maus_x + kamera_x) // KACHEL_GROESSE
                kachel_y = (maus_y + kamera_y) // KACHEL_GROESSE
                # Gebäude über das Modul platzieren lassen
                # (prüft intern schon ob die Kachel frei ist)
                gebaeude.gebaeude_platzieren(liste_gebaeude, gebaeude_auswahl,
                                              kachel_x, kachel_y)
        
    # ── Schritt 2: Gehaltene Tasten prüfen ────────────────────────────
    gedrueckte_tasten = pygame.key.get_pressed()
    if gedrueckte_tasten[pygame.K_LEFT]:
        kamera_x -= KAMERA_SPEED
    if gedrueckte_tasten[pygame.K_RIGHT]:
        kamera_x += KAMERA_SPEED
    if gedrueckte_tasten[pygame.K_UP]:
        kamera_y -= KAMERA_SPEED
    if gedrueckte_tasten[pygame.K_DOWN]:
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
    print("Generiere Planeten-Oberfläche...")
    karte_generieren()
    print("Erzeuge Sternenhimmel...")
    sterne_generieren()
    
    # HUD-Modul initialisieren (Stunde 4)
    hud.hud_initialisieren(fenster)
    
    print("Spiel gestartet! Drücke ESC zum Beenden.")
    print(f"Karte: {KARTE_BREITE} x {KARTE_HOEHE} Kacheln = "
          f"{KARTE_BREITE * KACHEL_GROESSE} x {KARTE_HOEHE * KACHEL_GROESSE} Pixel")
    
    laeuft = True
    
    while laeuft:
        laeuft = ereignisse_verarbeiten()
        
        # ZEICHNEN (RENDERING)
        hintergrund_zeichnen()
        karte_zeichnen()
        
        # STUNDE 3 — GEBÄUDE ZEICHNEN
        # Zeichnet alle platzierten Gebäude auf der Karte
        gebaeude.gebaeude_zeichnen(liste_gebaeude, kamera_x, kamera_y)
        
        # 3. Das HUD — immer zuletzt (liegt ganz oben)
        hud.hud_zeichnen(ressourcen, gebaeude_auswahl, gebaeude.GEBAEUDE_TYPEN,
                          kamera_x, kamera_y)
        
        pygame.display.flip()
        uhr.tick(BILDER_PRO_SEKUNDE)


# ═════════════════════════════════════════════════════════════════════════════
# PROGRAMMSTART
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    spiel_starten()
    pygame.quit()
    sys.exit()


# =============================================================================
# ENDE STUNDE 4
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
# Stunde 4 (HEUTE NEU):
#   ✓ HUD (Heads-Up Display) am oberen Bildschirmrand zeichnen
#   ✓ Ressourcen-Anzeige: Gold, Energie, Holz
#   ✓ Tasten 1/2/3 für Gebäude-Auswahl (wie in Final Earth 2!)
#   ✓ Ressourcen als Dictionary speichern {"gold": 100, ...}
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
# Nächste Stunde (Stunde 5):
#   → Ressourcen-Produktion und Verbrauch
#   → Automatisches Einkommen pro Gebäude
#   → Baukosten von Gebäuden
#   → Ressourcen-Logik in der Spielschleife
# =============================================================================