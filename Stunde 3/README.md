# Weltraum-Koloniespiel 🚀
### Ein Pygame-Lernprojekt — inspiriert von Final Earth 2

---

## Projektstruktur

| Datei         | Inhalt                                          |
|---------------|-------------------------------------------------|
| `main.py`     | Hauptdatei: Spielschleife, Karte, Kamera, HUD   |
| `gebaeude.py` | Modul: Gebäude-Typen, platzieren, zeichnen      |
| `README.md`   | Diese Datei — Projektübersicht                  |

---

## Stunden-Übersicht

| Stunde | Thema                             | Datei(en)                    | Status      |
|--------|-----------------------------------|------------------------------|-------------|
| 1      | Pygame-Grundlagen, Spielschleife  | `main.py`                    | ✅ fertig   |
| 2      | Karte, Kamera, Sterne             | `main.py`                    | ✅ fertig   |
| 3      | Gebäude platzieren (Maus)         | `main.py`, `gebaeude.py`     | 🔨 aktuell  |
| 4      | HUD, Ressourcenanzeige            | `main.py`, `hud.py`          | 🔜 geplant  |
| 5      | Ressourcen-Logik                  | `main.py`, `ressourcen.py`   | 🔜 geplant  |
| 6      | Gegner / Wellen                   | `main.py`, `gegner.py`       | 🔜 geplant  |

---

## Starten

```bash
python main.py
```

Benötigt: Python 3 und Pygame (`pip install pygame`)

---

## Steuerung (Stand Stunde 3)

| Taste / Aktion   | Funktion                      |
|------------------|-------------------------------|
| Pfeiltasten      | Karte scrollen                |
| Linke Maustaste  | Gebäude platzieren            |
| `1`              | Gebäude-Typ: Basis (blau)     |
| `2`              | Gebäude-Typ: Reaktor (gelb)   |
| `3`              | Gebäude-Typ: Farm (grün)      |
| `ESC`            | Spiel beenden                 |

---

## Gebäude-Typen

| Kürzel | Name    | Farbe       | Zweck (ab Stunde 5)       |
|--------|---------|-------------|---------------------------|
| B      | Basis   | Hellblau    | Hauptquartier der Kolonie |
| R      | Reaktor | Gelb-Orange | Energieversorgung         |
| F      | Farm    | Grün        | Nahrungsproduktion        |

---

## Was wir bisher gelernt haben

**Stunde 1:** `pygame.init()`, Spielschleife (Eingaben → Logik → Zeichnen), Farben als `(R, G, B)`, Konstanten in GROSSBUCHSTABEN

**Stunde 2:** Verschachtelte Schleifen, Kamera-Prinzip (`pixel_x = spalte × KACHEL_GROESSE − kamera_x`), `get_pressed()` für gehaltene Tasten, 2D-Arrays, zufällige Kartengenerierung

**Stunde 3:** Module (`import from`), Dictionary (`{ "key": wert }`), `MOUSEBUTTONDOWN` für Mausklick, Bildschirmposition → Kachelposition, Liste von Dictionaries