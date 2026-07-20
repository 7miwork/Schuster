# Weltraum-Koloniespiel 🚀
### Ein Pygame-Lernprojekt — inspiriert von Final Earth 2

---

## Projektstruktur

| Datei           | Inhalt                                          |
|-----------------|-------------------------------------------------|
| `main.py`       | Hauptdatei: Spielschleife, Karte, Kamera, HUD   |
| `gebaeude.py`   | Modul: Gebäude-Typen, platzieren, zeichnen      |
| `hud.py`        | Modul: Ressourcenanzeige, Gebäude-Auswahl im HUD |
| `ressourcen.py` | Modul: Wirtschaft, Baukosten, Produktion        |
| `README.md`     | Diese Datei — Projektübersicht                  |

---

## Stunden-Übersicht

| Stunde | Thema                             | Datei(en)                              | Status      |
|--------|-----------------------------------|----------------------------------------|-------------|
| 1      | Pygame-Grundlagen, Spielschleife  | `main.py`                              | ✅ fertig   |
| 2      | Karte, Kamera, Sterne             | `main.py`                              | ✅ fertig   |
| 3      | Gebäude platzieren (Maus)         | `main.py`, `gebaeude.py`               | ✅ fertig   |
| 4      | HUD, Ressourcenanzeige            | `main.py`, `hud.py`                    | ✅ fertig   |
| 5      | Ressourcen-Logik                  | `main.py`, `ressourcen.py`             | ✅ fertig   |
| 6      | Neue Rohstoffe & Gebäude (Stein, Holzfäller, Steinmetz) | `main.py`, `gebaeude.py`, `ressourcen.py`, `hud.py` | ✅ fertig |
| 7      | Bevölkerung & Wohnungen           | `main.py`, `gebaeude.py`, `bevoelkerung.py` | 🔜 geplant |
| 8      | Gegner, Verteidigung & Wellen                   | `main.py`, `gegner.py`                 | 🔜 geplant |
| 9      | Forschung & Technologien          | `main.py`, `forschung.py`              | 🔜 geplant |
| 10     | Baumenü per Maus, Start-/Pause-Bildschirm | `main.py`, `hud.py`, `menu.py`   | 🔜 geplant |
| 11     | Sieg-/Niederlage-Bedingungen, Speichern & Laden | `main.py`, `speicherstand.py` | 🔜 geplant |
| 12     | Feinschliff, Balancing, Bugfixing — fertiges Spiel | alle Dateien              | 🔜 geplant |

Weitere Ideen: 
1. Gebaeude: Handelszentrum/Marktplatz -> NPC Trade
2. Weitere Rohstoffe: Nahrung, Moral, [Eisenerz, Kohle, Kupfer,  (Weiterverarbeitung)]

🎯 **Ziel:** Am Ende von Stunde 12 haben wir ein vollständig spielbares Koloniespiel!

---

## Starten

```bash
python main.py
```

Benötigt: Python 3 und Pygame (`pip install pygame`)

---

## Steuerung (Stand Stunde 6)

| Taste / Aktion   | Funktion                      |
|------------------|-------------------------------|
| Pfeiltasten      | Karte scrollen                |
| WASD             | Karte scrollen (Alternative)  |
| Maus an den Rand | Karte automatisch scrollen    |
| Linke Maustaste  | Gebäude platzieren (kostet Ressourcen!) |
| `1`              | Gebäude-Typ: Basis (blau)     |
| `2`              | Gebäude-Typ: Reaktor (gelb)   |
| `3`              | Gebäude-Typ: Farm (grün)      |
| `4`              | Gebäude-Typ: Holzfäller (braun) — NEU! |
| `5`              | Gebäude-Typ: Steinmetz (grau) — NEU! |
| `ESC`            | Spiel beenden                 |

> **Neu in Stunde 6:** Die Tasten 4 und 5 wählen die neuen Gebäude Holzfäller und Steinmetz aus. Bauen kostet weiterhin Ressourcen — vor dem Platzieren wird geprüft, ob genug Gold/Energie/Holz/Stein vorhanden ist.

---

## Gebäude-Typen

| Kürzel | Name        | Farbe       | Baukosten              | Produziert/Sek. | Verbraucht/Sek. | Max. Anzahl |
|--------|-------------|-------------|------------------------|-----------------|-----------------|-------------|
| B      | Basis       | Hellblau    | Kostenlos              | –               | –               | 1× pro Spiel |
| R      | Reaktor     | Gelb-Orange | 20 Gold                | +5 Energie      | −2 Holz         | unbegrenzt  |
| F      | Farm        | Grün        | 15 Gold + 10 Energie   | +8 Gold         | −3 Energie      | unbegrenzt  |
| H      | Holzfäller  | Braun       | 10 Gold + 5 Energie    | +6 Holz         | −2 Energie      | unbegrenzt  |
| S      | Steinmetz   | Grau        | 15 Gold + 10 Energie   | +5 Stein        | −3 Energie      | unbegrenzt  |

> **Wichtig:** Wenn der nötige Rohstoff zum Verbrauchen fehlt (z.B. keine Energie für den Holzfäller), produziert das Gebäude in diesem Tick NICHTS. Ressourcenwerte fallen nie unter 0!

---

## Rohstoffe

Das Spiel hat jetzt **4 Rohstoffe**, die miteinander verbunden sind:

| Rohstoff  | Farbe       | Wofür?                                                |
|-----------|-------------|-------------------------------------------------------|
| Gold      | Gold-Gelb   | Universelle Währung — wird für fast alle Gebäude benötigt |
| Energie   | Gelb-Orange | Wird von Reaktoren produziert — viele Gebäude brauchen Energie |
| Holz      | Braun       | Wird von Holzfällern produziert — Reaktoren brauchen Holz |
| Stein     | Grau        | Wird von Steinmetzen produziert — wird in späteren Stunden wichtig |

**Zusammenhang:** Farmen → Gold → Reaktoren + Holzfäller + Steinmetze → Energie + Holz + Stein → Kreislauf schließt sich!

---

## Was wir bisher gelernt haben

**Stunde 1:** `pygame.init()`, Spielschleife (Eingaben → Logik → Zeichnen), Farben als `(R, G, B)`, Konstanten in GROSSBUCHSTABEN

**Stunde 2:** Verschachtelte Schleifen, Kamera-Prinzip (`pixel_x = spalte × KACHEL_GROESSE − kamera_x`), `get_pressed()` für gehaltene Tasten, 2D-Arrays, zufällige Kartengenerierung

**Stunde 3:** Module (`import from`), Dictionary (`{ "key": wert }`), `MOUSEBUTTONDOWN` für Mausklick, Bildschirmposition → Kachelposition, Liste von Dictionaries

**Stunde 4:** HUD (Heads-Up Display), Ressourcen als Dictionary, `hud_zeichnen()` statt `info_text_zeichnen()`, Tasten 1/2/3 für Gebäude-Auswahl

**Stunde 5:** Tick-System (Frame-Zähler, 1× pro Sekunde produzieren), Ressourcenproduktion und -verbrauch pro Gebäude, Baukosten prüfen vor dem Bauen (`kann_bauen()`), Baukosten automatisch abziehen (`baukosten_abziehen()`), Modul-Kopplung zwischen `gebaeude.py` und `ressourcen.py` über gemeinsame Indizes, Basis kann nur 1× gebaut werden, Gebäude produziert nichts bei fehlenden Rohstoffen, Baukosten-Anzeige im HUD

**Stunde 6:** Neue Rohstoffe und Gebäude hinzufügen (Stein als vierte Ressource, Holzfäller und Steinmetz als neue Gebäude), Tabellen erweitern (sowohl `GEBAEUDE_TYPEN` in `gebaeude.py` als auch `GEBAEUDE_WIRTSCHAFT` in `ressourcen.py` müssen gleichzeitig wachsen), Tastenhandling erweitern (neue `if`-Blöcke für Taste 4 und 5), HUD erweitern (vierte Ressource in der Leiste), `ressourcen_produzieren()` funktioniert automatisch für neue Indizes — keine Änderung nötig! `gebaeude_zeichnen()` funktioniert automatisch — holt Farbe und Kürzel aus der Liste