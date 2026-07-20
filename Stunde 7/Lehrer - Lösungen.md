# Lehrer — Lösungen zu den 10 Fehlern (Stunde 7)

Diese Datei ist **nur für die Lehrkraft** gedacht.
Sie enthält alle 10 Fehler mit genauer Beschreibung und der korrekten Lösung.

---

## Fehler 1 — `gebaeude.py` — Wohnhaus-Farbe

**Datei:** `gebaeude.py`  
**Funktion/Stelle:** `GEBAEUDE_TYPEN` — Eintrag Index 6 (Wohnhaus)  
**Zeile (ca.):** Zeile mit `"farbe":`

**Fehler:**
```python
"farbe":   (180, 180, 200),   # Fast Violett — Wohnungen für die Leute
```

**Richtig:**
```python
"farbe":   (180, 120, 200),   # Violett — Wohnungen für die Leute
```

**Warum ist das didaktisch sinnvoll?**  
Schüler müssen die Farbe im Code mit der Beschreibung abgleichen. Der Kommentar sagt "Violett", der Code enthält aber einen geänderten RGB-Wert. Das fördert die Aufmerksamkeit für konsistente Dokumentation.

---

## Fehler 2 — `gebaeude.py` — Wohnhaus-Kürzel

**Datei:** `gebaeude.py`  
**Funktion/Stelle:** `GEBAEUDE_TYPEN` — Eintrag Index 6 (Wohnhaus)  
**Zeile (ca.):** Zeile mit `"kuerzel":`

**Fehler:**
```python
"kuerzel": "V",
```

**Richtig:**
```python
"kuerzel": "W",
```

**Warum ist das didaktisch sinnvoll?**  
Das Kürzel "W" für Wohnhaus ist naheliegend, steht aber nicht im Code. Schüler müssen das HUD und die Tastenbelegung prüfen, um zu sehen, dass Taste 7 ein "W" anzeigen sollte.

---

## Fehler 3 — `ressourcen.py` — Wohnhaus-Produktionsmenge

**Datei:** `ressourcen.py`  
**Funktion/Stelle:** `GEBAEUDE_WIRTSCHAFT` — Eintrag Index 6 (Wohnhaus)  
**Zeile (ca.):** Zeile mit `"produktion":`

**Fehler:**
```python
"produktion": {"bevoelkerung": 1},   # Produziert Bevölkerung
```

**Richtig:**
```python
"produktion": {"bevoelkerung": 2},   # Produziert Bevölkerung
```

**Warum ist das didaktisch sinnvoll?**  
Schüler sehen, dass ein Wohnhaus nur +1 Bevölkerung gibt statt +2. Sie müssen den Wert mit der Dokumentation in README.md und main.py abgleichen und verstehen, dass Produktionswerte in der Wirtschafts-Tabelle gespeichert sind.

---

## Fehler 4 — `main.py` — Bevölkerungs-Startwert

**Datei:** `main.py`  
**Funktion/Stelle:** Initialisierung von `ressourcen_dict`  
**Zeile (ca.):** Die Zeile mit `"bevoelkerung":`

**Fehler:**
```python
ressourcen_dict = {"gold": 100, "energie": 50, "holz": 30, "stein": 20, "bevoelkerung": 5}
```

**Richtig:**
```python
ressourcen_dict = {"gold": 100, "energie": 50, "holz": 30, "stein": 20, "bevoelkerung": 0}
```

**Warum ist das didaktisch sinnvoll?**  
Der Startwert 5 ist inkonsistent zur Kommentierung ("Startwert = 0"). Schüler müssen prüfen, woher der erste Wert im Spiel kommt und ob er mit der Dokumentation übereinstimmt.

---

## Fehler 5 — `hud.py` — Bevölkerung-Icon-Position

**Datei:** `hud.py`  
**Funktion/Stelle:** `_ressourcen_leiste_zeichnen()` — Ressourcen-Typen  
**Zeile (ca.):** `"icon_pos"` bei Bevölkerung

**Fehler:**
```python
"icon_pos": (500, 15),
```

**Richtig:**
```python
"icon_pos": (480, 15),
```

**Warum ist das didaktisch sinnvoll?**  
Das Icon ist um 20 Pixel zu weit rechts. Schüler sehen visuell, dass das Bevölkerungs-Icon überlappt oder zu weit außen liegt. Sie müssen die Position im Code anpassen, bis die Anzeige sauber aussieht.

---

## Fehler 6 — `hud.py` — Bevölkerung-Text-Position

**Datei:** `hud.py`  
**Funktion/Stelle:** `_ressourcen_leiste_zeichnen()` — Ressourcen-Typen  
**Zeile (ca.):** `"text_pos"` bei Bevölkerung

**Fehler:**
```python
"text_pos": (515, 12),
```

**Richtig:**
```python
"text_pos": (495, 12),
```

**Warum ist das didaktisch sinnvoll?**  
Der Text beginnt zu weit rechts — neben dem Icon soll nicht der Text stehen. Schüler müssen bemerken, dass Icon-Position und Text-Position zusammengehören und beim Anpassen des Icons auch den Text anpassen müssen.

---

## Fehler 7 — `hud.py` — Dictionary-Key mit Leerzeichen

**Datei:** `hud.py`  
**Funktion/Stelle:** `_ressourcen_leiste_zeichnen()` — Ressourcen-Typen  
**Zeile (ca.):** `"schluessel"` bei Bevölkerung

**Fehler:**
```python
"schluessel": "bevoelkerung ",
```

**Richtig:**
```python
"schluessel": "bevoelkerung",
```

**Warum ist das didaktisch sinnvoll?**  
Das Leerzeichen am Ende führt dazu, dass `ressourcen.get("bevoelkerung ", 0)` immer 0 zurückgibt — im echten Ressourcen-Dictionary steht der Key aber ohne Leerzeichen. Schüler müssen den Tippfehler finden und verstehen, dass Dictionary-Keys **exakt** stimmen müssen.

---

## Fehler 8 — `main.py` — Falscher Index-Bereich im Kommentar

**Datei:** `main.py`  
**Funktion/Stelle:** Definition von `gebaeude_auswahl`  
**Zeile (ca.):** Die Zeile mit `gebaeude_auswahl = 0`

**Fehler:**
```python
gebaeude_auswahl = 0      # Welches Gebäude ist ausgewählt? (0-5)
```

**Richtig:**
```python
gebaeude_auswahl = 0      # Welches Gebäude ist ausgewählt? (0-6)
```

**Warum ist das didaktisch sinnvoll?**  
Der Kommentar sagt 0-5, also 6 Gebäude. Tatsächlich gibt es 7 (0-6). Schüler prüfen die Tastenbelegung: Taste 7 wählt Index 6 aus. Der Widerspruch führt sie zum Fehler.

---

## Fehler 9 — `main.py` — Falscher Wert in der Stunde-7-Zusammenfassung

**Datei:** `main.py`  
**Funktion/Stelle:** Footer-Block — Wiederholung Stunde 7  
**Zeile (ca.):** Zeile mit "produziert +1 Bevölkerung"

**Fehler:**
```python
#   ✓ Neues Gebäude: Wohnhaus (Index 6, produziert +1 Bevölkerung, kostet 20 Gold + 15 Holz + 10 Stein)
```

**Richtig:**
```python
#   ✓ Neues Gebäude: Wohnhaus (Index 6, produziert +2 Bevölkerung, kostet 20 Gold + 15 Holz + 10 Stein)
```

**Warum ist das didaktisch sinnvoll?**  
Der Kommentar im Footer widerspricht der README und der Wirtschafts-Tabelle in ressourcen.py. Schüler müssen die Konsistenz zwischen Hauptcode, Modulen und Dokumentation prüfen.

---

## Fehler 10 — `ressourcen.py` — Fehlender Eintrag in Namensliste

**Datei:** `ressourcen.py`  
**Funktion/Stelle:** `baukosten_abziehen()` — Liste `gebaeude_namen`  
**Zeile (ca.):** Die Liste mit den 6 Gebäude-Namen

**Fehler:**
```python
gebaeude_namen = ["Basis", "Reaktor", "Farm", "Holzfaeller",
                  "Steinmetz", "Wohnhaus"]
```
(6 Einträge: Index 0–5; Index 6 = Wohnhaus fehlt)

**Richtig:**
```python
gebaeude_namen = ["Basis", "Reaktor", "Farm", "Holzfaeller",
                  "Steinmetz", "Marktplatz", "Wohnhaus"]
```
(7 Einträge: Index 0–6)

**Warum ist das didaktisch sinnvoll?**  
Wenn ein Schüler das Wohnhaus baut, wird der Name als "Unbekannt" ausgegeben — weil Index 6 nicht in der Liste steht. Das zeigt, was passiert, wenn parallele Listen nicht synchronisiert werden.

---