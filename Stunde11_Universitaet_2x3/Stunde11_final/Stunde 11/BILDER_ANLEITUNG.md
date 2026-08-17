# Eigene Gebäude-Bilder einfügen

## Ziel

Jedes Gebäude kann ein eigenes PNG-Bild erhalten. Das Spiel lädt die Bilder automatisch aus dem Ordner `bilder/` und skaliert sie auf die Gebäudekachel.

## Dateinamen-Tabelle

| Gebäude | Eintrag in `gebaeude.py` | Datei im Ordner `bilder/` |
|---|---|---|
| Basis | `"bild": "basis.png"` | `bilder/basis.png` |
| Reaktor | `"bild": "reaktor.png"` | `bilder/reaktor.png` |
| Farm | `"bild": "farm.png"` | `bilder/farm.png` |
| Holzfäller | `"bild": "holzfaeller.png"` | `bilder/holzfaeller.png` |
| Steinmetz | `"bild": "steinmetz.png"` | `bilder/steinmetz.png` |
| Marktplatz | `"bild": "marktplatz.png"` | `bilder/marktplatz.png` |
| Wohnhaus | `"bild": "wohnhaus.png"` | `bilder/wohnhaus.png` |
| Universität / Schulgebäude | `"bild": "schule_2x3_kacheln_64x96.png"` | `bilder/schule_2x3_kacheln_64x96.png` (64×96 Pixel, Seitenverhältnis 2:3) |
| Mine | `"bild": None` | optional eigenes Bild |
| Straße | `"bild": None` | optional eigenes Bild |
| Fusionsreaktor | `"bild": None` | optional `fusionsreaktor.png` |
| Roboterfabrik | `"bild": None` | optional `roboterfabrik.png` |

## Schritt-für-Schritt-Anleitung

### 1. Bild erstellen

Erstellt eine quadratische Grafik, zum Beispiel mit 64 × 64 Pixeln. Zeichnet das Gebäude möglichst groß, aber lasst am Rand etwas Abstand. Ein transparentes PNG sieht im Spiel am besten aus, weil die Bodenfarbe um das Gebäude sichtbar bleibt.

### 2. Bild als PNG exportieren

Verwendet beim Export das Format PNG. Wenn das Zeichenprogramm nach einem Alpha-Kanal oder Transparenz fragt, muss diese Option aktiviert werden. Ein Bild mit weißem Hintergrund wird im Spiel als weißes Rechteck erscheinen.

### 3. Datei kopieren

Kopiert die Datei in den Ordner `bilder/`, der neben `main.py` und `gebaeude.py` liegt. Der Dateiname muss genau mit dem Wert im Dictionary übereinstimmen.

Beispiel:

```python
{
    "name": "Fusionsreaktor",
    "bild": "fusionsreaktor.png",
    "farbe": (255, 110, 210),
    "kuerzel": "F",
    "taste": "G",
},
```

Dazu muss die Datei exakt hier liegen:

```text
Stunde 11/bilder/fusionsreaktor.png
```

### 4. Spiel neu starten

Die Bilder werden beim Start in `gebaeude_initialisieren()` geladen. Nach dem Kopieren muss das Spiel neu gestartet werden. Ein bloßes Zurückkehren zum Menü lädt die Datei nicht erneut.

### 5. Fallback prüfen

Wenn eine Datei nicht gefunden wird, stürzt das Spiel nicht ab. Es zeichnet stattdessen ein farbiges Rechteck mit dem Wert aus `"farbe"`. Das ist hilfreich beim Programmieren, weil ihr zuerst die Spiellogik testen könnt und das Bild später ergänzt.

## Technischer Ablauf

In `gebaeude.py` wird zunächst der Ordner gesucht:

```python
bilder_ordner = os.path.join(os.path.dirname(__file__), "bilder")
```

Danach wird für jeden Gebäudetyp der Dateiname gelesen:

```python
dateiname = typ_daten.get("bild")
if not dateiname:
    continue
```

Anschließend wird geprüft, ob die Datei existiert und mit Transparenz geladen:

```python
bild_pfad = os.path.join(bilder_ordner, dateiname)
if os.path.exists(bild_pfad):
    _bilder[typ_daten["name"]] = pygame.image.load(
        bild_pfad).convert_alpha()
```

Beim Zeichnen wird das Bild auf die Zielgröße skaliert:

```python
bild = _bilder.get(typ_daten["name"])
if bild is not None:
    bild = pygame.transform.smoothscale(bild, rect.size)
    _fenster.blit(bild, rect)
else:
    pygame.draw.rect(_fenster, typ_daten["farbe"], rect)
```

## Fehlerkontrolle

Wenn ein Bild nicht angezeigt wird, kontrolliert ihr zuerst den Ordnernamen `bilder`, danach Groß- und Kleinschreibung, Dateiendung und Schreibweise im Dictionary. Anschließend startet ihr das Spiel aus dem richtigen Projektordner neu. Der Selbsttest prüft die Bilddateien nicht, weil fehlende Bilder bewusst durch die Fallback-Farbe ersetzt werden.

## Erweiterungsaufgabe

Erstellt ein eigenes Bild für die Roboterfabrik, ergänzt in `gebaeude.py` den Wert `"bild": "roboterfabrik.png"` und überprüft im Spiel, ob das Bild auch dann korrekt angezeigt wird, wenn zwei kompakte Gebäude dieselbe Kachel teilen.

## Das Universitätsbild als 2×3-Gebäude

Das angehängte Bild `schule_2x3_kacheln_64x96.png` ist bereits passend vorbereitet: 64 Pixel breit und 96 Pixel hoch, also im Verhältnis 2:3. Bei einer Spielkachel von 48×48 Pixeln wird es automatisch auf ungefähr 96×144 Pixel skaliert. Es bedeckt deshalb zwei Kacheln nebeneinander und drei Kacheln untereinander.

In `gebaeude.py` stehen dafür die zusätzlichen Werte:

```python
{
    "name": "Universitaet",
    "bild": "schule_2x3_kacheln_64x96.png",
    "breite": 2,
    "hoehe": 3,
    "kuerzel": "L",
    "taste": "8",
}
```

Die angeklickte Kachel ist die **linke obere Ecke** des Gebäudes. Das Spiel reserviert anschließend automatisch alle sechs Kacheln in diesem Rechteck. Die Universität darf nicht gebaut werden, wenn eine dieser sechs Kacheln bereits belegt ist oder wenn das Rechteck über den Kartenrand hinausgeht.

Beim Rechtsklick genügt es, auf eine beliebige der sechs Universitätskacheln zu klicken. Das Spiel findet das zugehörige Gebäude über seine gesamte Fläche und gibt anschließend die Rückerstattung nur einmal zurück. Dadurch wird ein großes Gebäude nicht versehentlich sechsmal abgerissen.

Für eigene 2×3-Gebäude könnt ihr dieselbe Struktur wiederverwenden. Ändert nur Bilddatei, Name, Farbe und die Werte `breite` und `hoehe`. Für ein Gebäude mit drei Kacheln Breite und zwei Kacheln Höhe wären die Werte `"breite": 3` und `"hoehe": 2`.
