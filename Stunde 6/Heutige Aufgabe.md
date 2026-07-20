# Aufgabe: Neues Gebäude — Marktplatz 🏛️

## Ausgangslage

Stein wird seit Stunde 6 vom Steinmetz produziert — aber bisher verbraucht ihn
**kein einziges Gebäude**! Der Stein-Vorrat wächst nur immer weiter, ohne
irgendeinen Nutzen im Spiel.

**Eure Aufgabe:** Baut ein neues Gebäude, den **Marktplatz**, der Stein in
Gold verwandelt. Damit schließt sich ein weiterer Kreislauf im Spiel:

```
Steinmetz → Stein → Marktplatz → Gold
```

## Was ihr lernt

- Ihr erweitert **zwei parallele Listen** (`GEBAEUDE_TYPEN` und
  `GEBAEUDE_WIRTSCHAFT`) um einen neuen Eintrag mit demselben Index
- Ihr fügt eine neue Taste (`6`) hinzu
- Ihr seht, dass HUD und Zeichnen-Funktion **automatisch** mitziehen —
  ohne dass ihr dort etwas ändern müsst!

Das ist genau das gleiche Muster wie beim Holzfäller/Steinmetz in
Stunde 6 — nur einfacher, weil kein neuer Rohstoff dazukommt.

---

## Schritt 1 — `gebaeude.py`: Neuen Gebäude-Typ eintragen

Fügt am Ende der Liste `GEBAEUDE_TYPEN` (nach Steinmetz, Index 4) einen
neuen Eintrag hinzu:

```python
    # ── Index 5: Marktplatz (NEU!) ─────────────────────────────────────────
    {
        "name":    "Marktplatz",
        "farbe":   (220, 180, 80),    # Sandgold — Handel und Gold
        "kuerzel": "M",
    },
```

## Schritt 2 — `ressourcen.py`: Wirtschaftsdaten eintragen

Fügt am Ende der Liste `GEBAEUDE_WIRTSCHAFT` (Index 5, gleicher Index wie
oben!) einen passenden Eintrag hinzu:

```python
    # ── Index 5: Marktplatz (Steinverarbeitung) — NEU! ─────────────────────
    # Kostet 30 Gold + 15 Energie, produziert +12 Gold, verbraucht −5 Stein.
    {
        "baukosten":  {"gold": 30, "energie": 15},
        "produktion": {"gold": 12},
        "verbrauch":  {"stein": 5},
        "max_anzahl": None,
    },
```

> **Denkt dran:** Der Index in `gebaeude.py` und `ressourcen.py` muss
> übereinstimmen! Beide sind hier Index 5.

## Schritt 3 — `main.py`: Neue Taste hinzufügen

Sucht die Stelle mit den Tasten 1–5 (Suche nach `K_5`) und fügt danach
einen neuen Block hinzu:

```python
            if ereignis.key == pygame.K_6:
                gebaeude_auswahl = 5
```

---

## Testen

1. Spiel starten (`python main.py`)
2. Taste `6` drücken → HUD zeigt automatisch "Ausgewählt: Marktplatz (Taste 6)"
3. Marktplatz bauen (Linksklick) → kostet 30 Gold + 15 Energie
4. Ein paar Sekunden warten → Stein sollte sinken, Gold sollte schneller steigen

**Bonus-Frage für schnelle Schüler:** Was passiert, wenn ihr mehrere
Marktplätze baut, aber der Steinmetz nicht hinterherkommt? Testet es aus!

---
