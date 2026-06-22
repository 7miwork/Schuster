# =============================================================================
# PROJEKT: Weltraum-Koloniespiel
# STUNDE 01: Das Fundament
# =============================================================================
# Was wir heute bauen:
#   - Ein Pygame-Fenster öffnet sich
#   - Das Spiel läuft in einer Schleife (Spielschleife / Game Loop)
#   - Das Fenster kann sauber geschlossen werden
#
# TIPP FÜR SPÄTER — hier wird in jeder Stunde mehr eingefügt:
#   - Stunde 2: Die Karte (Gitter) kommt in den Zeichenbereich
#   - Stunde 3: Gebäude kommen dazu
#   - Stunde 6: Gegner erscheinen
# =============================================================================
 
# -----------------------------------------------------------------------------
# IMPORTS
# Hier laden wir die Werkzeuge die wir für unser Spiel brauchen.
# -----------------------------------------------------------------------------
 
import pygame   # Das Haupt-Modul für die Spieleentwicklung
import sys      # Wird benötigt um das Programm richtig zu beenden
 
 
# -----------------------------------------------------------------------------
# KONSTANTEN
# Das sind Werte die sich während des Spiels NICHT ändern.
# Wir schreiben sie GROSS damit wir sofort sehen dass sie Konstanten sind.
# TIPP: Hier kommen in späteren Stunden mehr Konstanten dazu
#       z.B. Kachelgröße, Kartenbreite, Gebäudekosten
# -----------------------------------------------------------------------------
 
BILD_BREITE         = 800               # Die Breite des Fensters in Pixeln
BILD_HOEHE          = 600               # Die Höhe des Fensters in Pixeln
BILD_TITEL          = "Weltraum-Koloniespiel"   # Text oben im Fenster
BILDER_PRO_SEKUNDE  = 60                # Wie oft das Spiel pro Sekunde aktualisiert wird (FPS)
 
 
# -----------------------------------------------------------------------------
# FARBEN
# In Pygame werden Farben als RGB (Rot, Grün, Blau) definiert.
# Jeder Wert geht von 0 bis 255.
# TIPP: Hier kommen später mehr Farben dazu z.B. für Gebäude und Gegner
# -----------------------------------------------------------------------------
 
FARBE_SCHWARZ   = (0,   0,   0  )   # Kein Licht — unser Weltraum-Hintergrund
FARBE_WEISS     = (255, 255, 255)   # Volles Licht
FARBE_BLAU      = (0,   0,   255)   # Rein Blau
FARBE_GRAU      = (100, 100, 100)   # Mittleres Grau für Hinweistexte
 
 
# -----------------------------------------------------------------------------
# INITIALISIERUNG
# Hier bereiten wir Pygame vor — das passiert nur EINMAL beim Start.
# -----------------------------------------------------------------------------
 
pygame.init()   # Startet alle Pygame-Module auf einmal
 
# Wir erstellen das Fenster mit Breite und Höhe von oben
# "fenster" ist unser Zeichenbrett — darauf malen wir alles
fenster = pygame.display.set_mode((BILD_BREITE, BILD_HOEHE))
 
# Den Titel des Fensters setzen (der Text oben in der Leiste)
pygame.display.set_caption(BILD_TITEL)
 
# Ein Taktgeber damit das Spiel auf jedem Computer gleich schnell läuft
uhr = pygame.time.Clock()
 
 
# -----------------------------------------------------------------------------
# HILFSFUNKTIONEN
# Funktionen sind Codeblöcke die wir immer wieder aufrufen können.
# TIPP: Hier kommen in jeder Stunde neue Funktionen dazu
#       z.B. karte_zeichnen(), gebaeude_zeichnen(), gegner_update()
# -----------------------------------------------------------------------------
 
def hintergrund_zeichnen():
    """
    Füllt den ganzen Bildschirm mit Schwarz (unser Weltraum).
    Das machen wir JEDEN Frame als erstes damit der letzte Frame
    vollständig übermalt wird — sonst verschmiert alles!
    """
    fenster.fill(FARBE_SCHWARZ)
 
 
def info_text_zeichnen():
    """
    Zeigt einen kleinen Hinweistext auf dem Bildschirm.
    Nur für Stunde 1 damit das Fenster nicht leer aussieht.
    TIPP: In Stunde 4 ersetzen wir das durch das richtige HUD
          mit Gold, Holz und anderen Ressourcen.
    """
    # Eine Schrift erstellen: None = Standard-Schrift, 28 = Größe in Pixeln
    schrift = pygame.font.Font(None, 28)
 
    # render() wandelt Text in ein Bild um
    # True = glatte Kanten, FARBE_WEISS = Textfarbe
    text_bild = schrift.render("Weltraum-Koloniespiel wird hier entstehen!", True, FARBE_WEISS)
 
    # Das Textbild auf das Fenster zeichnen an Position x=50, y=50
    fenster.blit(text_bild, (50, 50))
 
    # Einen zweiten Hinweistext anzeigen
    hinweis = schrift.render("ESC = Beenden", True, FARBE_GRAU)
    fenster.blit(hinweis, (50, 90))
 
 
# -----------------------------------------------------------------------------
# EREIGNISSE VERARBEITEN
# Diese Funktion prüft was der Spieler gerade tut.
# TIPP: Hier kommen später Maus-Klick-Ereignisse für Gebäude dazu (Stunde 3)
# -----------------------------------------------------------------------------
 
def ereignisse_verarbeiten():
    """
    Geht alle Ereignisse durch die seit dem letzten Frame passiert sind.
    Gibt True zurück wenn das Spiel weiterlaufen soll, False zum Beenden.
    """
    # pygame.event.get() gibt eine Liste aller neuen Ereignisse zurück
    for ereignis in pygame.event.get():
 
        # QUIT = Spieler hat auf das X-Symbol geklickt
        if ereignis.type == pygame.QUIT:
            return False    # False = Spiel soll beenden
 
        # KEYDOWN = eine Taste wurde gedrückt
        if ereignis.type == pygame.KEYDOWN:
            # K_ESCAPE = die ESC-Taste
            if ereignis.key == pygame.K_ESCAPE:
                return False    # False = Spiel soll beenden
 
    # Kein Beenden-Ereignis: True zurückgeben (weiterspielen)
    return True
 
 
# -----------------------------------------------------------------------------
# SPIELSCHLEIFE (GAME LOOP)
# Das ist das Herz des Spiels! Läuft 60 Mal pro Sekunde durch 3 Schritte:
#
#   SCHRITT 1: EINGABEN   → Was hat der Spieler getan? (Tasten, Maus)
#   SCHRITT 2: LOGIK      → Spiel-Berechnungen (Bewegung, Kollision usw.)
#   SCHRITT 3: ZEICHNEN   → Alles auf den Bildschirm malen
#
# TIPP: In diesem Bereich wird in jeder Stunde mehr hinzugefügt!
# -----------------------------------------------------------------------------
 
def spiel_starten():
    """
    Startet die Hauptspielschleife.
    Läuft so lange bis der Spieler das Spiel beendet.
    """
    # laeuft = True solange das Spiel läuft
    # WICHTIG: Kein Umlaut in Variablennamen! "laeuft" nicht "läuft"
    #          Python erlaubt Umlaute aber es macht oft Probleme — besser vermeiden!
    laeuft = True
 
    while laeuft:
 
        # --- SCHRITT 1: EINGABEN VERARBEITEN ---
        # Prüfen was der Spieler gemacht hat
        # Wenn False zurückkommt: Schleife beenden
        laeuft = ereignisse_verarbeiten()
 
        # --- SCHRITT 2: LOGIK UND BERECHNUNGEN ---
        # Hier berechnen wir was sich im Spiel verändert hat
        # TIPP: Ab Stunde 3 kommen hier Gebäude-Updates rein
        # TIPP: Ab Stunde 5 kommen hier Ressourcen-Updates rein
        # TIPP: Ab Stunde 6 kommen hier Gegner-Bewegungen rein
        pass    # pass = "hier kommt noch etwas, aber erst später"
 
        # --- SCHRITT 3: ZEICHNEN (RENDERING) ---
        # Zuerst Hintergrund — übermalt alles vom letzten Frame
        hintergrund_zeichnen()
 
        # Dann unseren Info-Text anzeigen
        # TIPP: Ab Stunde 2 kommt hier die Karte (karte_zeichnen())
        # TIPP: Ab Stunde 3 kommt hier gebaeude_zeichnen()
        # TIPP: Ab Stunde 4 kommt hier hud_zeichnen()
        info_text_zeichnen()
 
        # display.flip() zeigt alles was wir gemalt haben an
        # (vorher war es nur im Hintergrund vorbereitet — wie ein Daumenkino)
        pygame.display.flip()
 
        # Die Uhr begrenzt die Geschwindigkeit auf BILDER_PRO_SEKUNDE FPS
        # Damit läuft das Spiel auf jedem Computer gleich schnell
        uhr.tick(BILDER_PRO_SEKUNDE)
 
 
# -----------------------------------------------------------------------------
# PROGRAMMSTART
# Dieser Block wird nur ausgeführt wenn wir DIESE Datei direkt starten.
# TIPP: Das bleibt immer ganz unten — das ändert sich nie!
# -----------------------------------------------------------------------------
 
if __name__ == "__main__":
    spiel_starten()     # Das Spiel starten
    pygame.quit()       # Pygame sauber beenden wenn die Schleife endet
    sys.exit()          # Das Programm komplett beenden
 
 
# =============================================================================
# ENDE STUNDE 1
# Was wir gelernt haben:
#   ✓ pygame.init() startet Pygame
#   ✓ display.set_mode() erstellt das Fenster
#   ✓ Die Spielschleife: Eingaben → Logik → Zeichnen
#   ✓ Farben als (R, G, B) Tupel
#   ✓ Konstanten in GROSSBUCHSTABEN
#   ✓ Funktionen mit def
#   ✓ Kein Umlaut in Variablennamen! (laeuft statt läuft)
#
# HÄUFIGE FEHLER zum Merken:
#   ✗ spiel_läuft ≠ spiel_laeuft  → Python sieht das als 2 verschiedene Variablen!
#   ✗ Einrückung vergessen        → IndentationError
#   ✗ Klammern nicht geschlossen  → SyntaxError
#
# Was als nächstes kommt (Stunde 2):
#   → Kamera-Variablen einführen
#   → Das Gitter (Karte) zeichnen
#   → Mit Pfeiltasten über die Karte scrollen
# =============================================================================
 
