# Debugging-Hinweise für Stunde 7

Diese Datei hilft dir, die 10 Fehler im Projekt zu finden.
Die Hinweise verraten **nicht** die Lösung — sie zeigen dir nur,
**wo** du suchen solltest.

---

## Allgemeine Tipps

* Vergleiche den Code mit der README.md — stimmen alle Zahlen überein?
* Teste jedes Gebäude **einzeln** — baue nur ein Wohnhaus und beobachte.
* Achte auf Konsolenausgaben — sie zeigen oft schon den Fehler an.
* Prüfe die Koordinaten im HUD — sitzen alle Icons und Texte korrekt?

---

## Hinweis 1 — Gebäude-Definitionen

Schau dir die Definition des Wohnhauses in `gebaeude.py` genau an.
Vergleiche Farbe und Kürzel mit den anderen Gebäuden.
Passt das Kürzel zur Taste 7 und zum HUD?

---

## Hinweis 2 — Ressourcen-Produktion

Baue ein Wohnhaus und warte einige Sekunden.
Wächst die Bevölkerung wirklich so schnell wie erwartet?
Vergleiche den Produktionswert in `ressourcen.py` mit der README.md.

---

## Hinweis 3 — Startbedingungen

Starte das Spiel neu. Steht die Bevölkerung wirklich auf 0?
Was sagt der Kommentar in `main.py` zum Startwert?

---

## Hinweis 4 — HUD-Layout

Schaue dir das HUD oben im Spiel an.
Sitzen alle 5 Icons sauber nebeneinander?
Oder überlappen sie? Vergleiche die x-Positionen der Icons.

---

## Hinweis 5 — Dictionary-Schlüssel

Achte auf die `schluessel`-Einträge im HUD.
Kannst du einen unsichtbaren Unterschied zwischen den Schlüsseln entdecken?
`"bevoelkerung"` und `"bevoelkerung "` sehen gleich aus — sind sie es?

---

## Hinweis 6 — Namenslisten

Baue ein Wohnhaus und schau in die Konsole.
Welchen Namen zeigt die Ausgabe an?
Vergleiche die Namensliste in `ressourcen.py` mit den tatsächlichen Gebäude-Typen.

---

## Hinweis 7 — Konsistenz zwischen README und Code

Lies die Gebäude-Tabelle in der README.md.
Steht dort dieselbe Produktionsmenge wie im Code?
Suche nach Widersprüchen zwischen Dokumentation und Implementierung.

---

## Hinweis 8 — Index-Bereiche

Zähle die Tasten von 1 bis 7.
Wie viele Gebäude-Typen gibt es wirklich?
Steht die höchste Nummer auch im Kommentar bei `gebaeude_auswahl`?