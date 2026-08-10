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
| `menu.py`       | Modul: Baumenü (TAB)                            |
| `forschung.py`  | Modul: Forschungsmenü (F)                       |
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
| 7      | Bevölkerung & Wohnungen           | `main.py`, `gebaeude.py`, `ressourcen.py`, `hud.py` | ✅ fertig   |
| 8      | Ideen, Fehlerbehebung                   | `main.py`, `hud.py,`, `ressourcen.py`                 | ✅ fertig |
| 9      | Gebäude abreißen, Baumenü, Freischaltung, Feedback-Meldungen | `main.py`, `gebaeude.py`, `ressourcen.py`, `hud.py`, `menu.py` | ✅ fertig |
| 10     | Forschung & Technologien             | `main.py`, `forschung.py`, `ressourcen.py`, `menu.py`, `hud.py` | ✅ fertig |
| 11     | Baumenü verfeinern, Start-/Pause-Bildschirm | `main.py`, `hud.py`, `menu.py`   | 🔜 geplant |
| 12     | Sieg-/Niederlage-Bedingungen, Speichern & Laden | `main.py`, `speicherstand.py` | 🔜 geplant |
| 13     | Feinschliff, Balancing, Bugfixing — fertiges Spiel | alle Dateien              | 🔜 geplant |

| XX     | Gegner, Verteidigung & Wellen                   | `main.py`, `gegner.py`                 | 🔜 geplant |


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

## Steuerung (Stand Stunde 10)

| Taste / Aktion   | Funktion                      |
|------------------|-------------------------------|
| Pfeiltasten      | Karte scrollen                |
| WASD             | Karte scrollen (Alternative)  |
| Maus an den Rand | Karte automatisch scrollen    |
| Linke Maustaste  | Gebäude platzieren (kostet Ressourcen!) |
| **Rechte Maustaste** | **Gebäude abreißen (50 % der Baukosten zurück!)** |
| **`TAB`**        | **Baumenü öffnen/schließen (zeigt alle Gebäudetypen)** |
| **`F`**          | **Forschungsmenü öffnen/schließen — NEU!** |
| **`F1` / `F2` / `F3`** | **Technologie erforschen (wenn Forschungsmenü offen) — NEU!** |
| **`H`**          | **Hilfe ein-/ausblenden (Spickzettel) — NEU!** |
| `1`              | Gebäude-Typ: Basis (blau)     |
| `2`              | Gebäude-Typ: Reaktor (gelb)   |
| `3`              | Gebäude-Typ: Farm (grün)      |
| `4`              | Gebäude-Typ: Holzfäller (braun) |
| `5`              | Gebäude-Typ: Steinmetz (grau) |
| `6`              | Gebäude-Typ: Marktplatz (sandgold) |
| `7`              | Gebäude-Typ: Wohnhaus (violett) |
| `8`              | Gebäude-Typ: Labor (hellblau-cyan) — NEU! |
| `B`              | Kamera sofort zur Basis zentrieren |
| `Leertaste`      | Pause / Start                 |
| `1` / `2`        | Geschwindigkeit 1× / 2×       |
| `ESC`            | Spiel beenden                 |

> **Neu in Stunde 9:** Rechtsklick reißt ein Gebäude ab (die Basis kann nicht abgerissen werden!). `TAB` öffnet das Baumenü, in dem alle Gebäudetypen mit Baukosten und Freischaltung zu sehen sind.

> **Neu in Stunde 7:** Taste 7 wählt das Wohnhaus aus. Bauen kostet Gold, Holz und Stein. Wohnhäuser produzieren Bevölkerung — die neue fünfte Ressource! Mit Tasten 1–7 wählst du zwischen 7 Gebäude-Typen.

---

## Gebäude-Typen

| Kürzel | Name        | Farbe       | Baukosten              | Produziert/Sek. | Verbraucht/Sek. | Max. Anzahl | Freigeschaltet ab (St. 9) |
|--------|-------------|-------------|------------------------|-----------------|-----------------|-------------|---------------------------|
| B      | Basis       | Hellblau    | Kostenlos              | –               | –               | 1× pro Spiel | Sofort |
| R      | Reaktor     | Gelb-Orange | 20 Gold                | +5 Energie      | −2 Holz         | unbegrenzt  | Sofort |
| F      | Farm        | Grün        | 15 Gold + 10 Energie   | +8 Gold         | −3 Energie      | unbegrenzt  | Sofort |
| H      | Holzfäller  | Braun       | 10 Gold + 5 Energie    | +6 Holz         | −2 Energie      | unbegrenzt  | Sofort |
| S      | Steinmetz   | Grau        | 15 Gold + 10 Energie   | +5 Stein        | −3 Energie      | unbegrenzt  | Sofort |
| M      | Marktplatz  | Sandgold    | 30 Gold + 15 Energie   | +12 Gold        | −5 Stein        | unbegrenzt  | ab **5 Bevölkerung** |
| W      | Wohnhaus    | Violett     | 20 Gold + 15 Holz + 10 Stein | +2 Bevölkerung | −3 Energie | unbegrenzt  | ab **20 Holz** |

> **Wichtig:** Wenn der nötige Rohstoff zum Verbrauchen fehlt (z.B. keine Energie für den Holzfäller), produziert das Gebäude in diesem Tick NICHTS. Ressourcenwerte fallen nie unter 0!

---

## Rohstoffe

Das Spiel hat jetzt **6 Rohstoffe**, die miteinander verbunden sind:

| Rohstoff     | Farbe       | Wofür?                                                |
|--------------|-------------|-------------------------------------------------------|
| Gold         | Gold-Gelb   | Universelle Währung — wird für fast alle Gebäude benötigt |
| Energie      | Gelb-Orange | Wird von Reaktoren produziert — viele Gebäude brauchen Energie |
| Holz         | Braun       | Wird von Holzfällern produziert — Reaktoren brauchen Holz |
| Stein        | Grau        | Wird von Steinmetzen produziert — wird in späteren Stunden wichtig |
| Bevölkerung  | Rosa        | Wird von Wohnhäusern produziert — die Kolonie wächst! |
| Forschung    | Hellblau    | Wird im Labor produziert — für neue Technologien im Forschungsmenü (Taste F) |

**Zusammenhang:** Farmen → Gold → Reaktoren + Holzfäller + Steinmetze + Marktplatz → Energie + Holz + Stein + Gold → Wohnhäuser → Bevölkerung + Forschung → Kreislauf schließt sich!

---

## Was wir bisher gelernt haben

**Stunde 1:** `pygame.init()`, Spielschleife (Eingaben → Logik → Zeichnen), Farben als `(R, G, B)`, Konstanten in GROSSBUCHSTABEN

**Stunde 2:** Verschachtelte Schleifen, Kamera-Prinzip (`pixel_x = spalte × KACHEL_GROESSE − kamera_x`), `get_pressed()` für gehaltene Tasten, 2D-Arrays, zufällige Kartengenerierung

**Stunde 3:** Module (`import from`), Dictionary (`{ "key": wert }`), `MOUSEBUTTONDOWN` für Mausklick, Bildschirmposition → Kachelposition, Liste von Dictionaries

**Stunde 4:** HUD (Heads-Up Display), Ressourcen als Dictionary, `hud_zeichnen()` statt `info_text_zeichnen()`, Tasten 1/2/3 für Gebäude-Auswahl

**Stunde 5:** Tick-System (Frame-Zähler, 1× pro Sekunde produzieren), Ressourcenproduktion und -verbrauch pro Gebäude, Baukosten prüfen vor dem Bauen (`kann_bauen()`), Baukosten automatisch abziehen (`baukosten_abziehen()`), Modul-Kopplung zwischen `gebaeude.py` und `ressourcen.py` über gemeinsame Indizes, Basis kann nur 1× gebaut werden, Gebäude produziert nichts bei fehlenden Rohstoffen, Baukosten-Anzeige im HUD

**Stunde 6:** Neue Rohstoffe und Gebäude hinzufügen (Stein als vierte Ressource, Holzfäller und Steinmetz als neue Gebäude), Tabellen erweitern (sowohl `GEBAEUDE_TYPEN` in `gebaeude.py` als auch `GEBAEUDE_WIRTSCHAFT` in `ressourcen.py` müssen gleichzeitig wachsen), Tastenhandling erweitern (neue `if`-Blöcke für Taste 4 und 5), HUD erweitern (vierte Ressource in der Leiste), `ressourcen_produzieren()` funktioniert automatisch für neue Indizes — keine Änderung nötig! `gebaeude_zeichnen()` funktioniert automatisch — holt Farbe und Kürzel aus der Liste

**Stunde 7:** Fünfter Rohstoff Bevölkerung, neues Gebäude Wohnhaus, `GEBAEUDE_TYPEN` und `GEBAEUDE_WIRTSCHAFT` auf 7 Einträge erweitert, HUD zeigt 5 Ressourcen

**Stunde 8:** Neuer Rohstoff Nahrung (Startwert 50), Farmen produzieren Nahrung, Wohnhäuser verbrauchen Nahrung, HUD zeigt 6 Ressourcen, Boden-Typen und Gebäude-Anforderungen

**Stunde 9 (abgeschlossen):** Diese Stunde setzt die Verbesserungsvorschläge der Schüler um:
- **Gebäude abreißen** mit Rechtsklick (`gebaeude_abreissen()`), dabei 50 % der Baukosten zurück (`ressourcen_zurueckerstatten()`, abgerundet mit `kosten // 2`). Die Basis kann nicht abgerissen werden.
- **Baumenü mit `TAB`** (neues Modul `menu.py`): zeigt alle Gebäudetypen mit Baukosten, Taste und Freischaltung.
- **Tooltip** beim Hovern über ein Ressourcen-Icon: zeigt welche Gebäude die Ressource produzieren/verbrauchen.
- **Meldungssystem** im HUD (`hud.meldung_anzeigen()`): rote Meldung, wenn zu wenig Rohstoffe zum Bauen da sind.
- **Stufenweise Freischaltung**: jedes Gebäude hat ein Feld `freischaltung` (z.B. Marktplatz ab 5 Bevölkerung, Wohnhaus ab 20 Holz). `ist_freigeschaltet()` prüft das.

**Stunde 10 (abgeschlossen):** Forschungssystem hinzugefügt:
- **Neues Gebäude: Labor** (Taste 8): produziert die Ressource **Forschungspunkte**.
- **Neues Modul `forschung.py`**: Forschungsmenü mit Taste `F`, Technologien mit F1/F2/F3 erforschen.
- **Technologie-Baum**: Wohnbau (schaltet Wohnhaus frei), Produktions-Boost (+25%), Stein-Effizienz.
- **Freischaltung erweitert**: Gebäude können jetzt auch durch Technologien (`{"typ": "forschung", ...}`) oder durch **Listen** von Bedingungen (UND-Verknüpfung) freigeschaltet werden.
- **Hilfe-Menü** mit Taste `H`: zeigt alle Tasten und ihre Funktion.
- **Ressourcen-Bonus**: Wenn die Technologie "Produktions-Boost" erforscht ist, produzieren alle Gebäude 25 % mehr.

---

## 💡 Tipp für die erste Runde — So überlebst du!

Die ersten Minuten sind die schwersten. Hier eine bewährte Reihenfolge:

1. **Basis** ist kostenlos und schon da — du musst nichts tun.
2. **Bau-Reihenfolge:**
   - Zuerst einen **Reaktor** (20 Gold) — er produziert Energie, die du brauchst.
   - Dann einen **Holzfäller** (10 Gold + 5 Energie) — er liefert Holz für den Reaktor.
   - Dann eine **Farm** (15 Gold + 10 Energie) — sie produziert Nahrung für die Bevölkerung.
   - Dann einen **Steinmetz** (15 Gold + 10 Energie) — er liefert Stein für spätere Gebäude.
3. **Achte auf deine Energie!** Reaktoren verbrauchen Holz, Holzfäller/Farmen/Steinmetze verbrauchen Energie. Baue immer erst einen Reaktor, bevor du Verbraucher baust.
4. **Wohnhaus** freischaltet sich ab **5 Bevölkerung** — hab etwas Geduld oder baue es, sobald du genug Gold, Holz und Stein hast.
5. **Marktplatz** (ab 5 Bevölkerung) produziert passiv Gold — sehr nützlich, aber er braucht Stein.
6. **Labor** (ab 5 Bevölkerung + 40 Gold) gibt dir Forschungspunkte für neue Technologien.
7. **Drücke `H`** wenn du nicht weiterweißt — die Hilfe zeigt dir alle Tasten!

> **Merke:** Immer schön die Ressourcen oben im Auge behalten. Wenn eine Ressource rot wird oder fehlt, produziert das Gebäude in diesem Tick NICHTS.
