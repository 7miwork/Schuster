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

