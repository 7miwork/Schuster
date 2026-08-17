# Weltraum-Koloniespiel — Stunde 11/12

Dieses Projekt ist ein kleines Weltraum-Koloniespiel in Python und Pygame. Die aktuelle Fassung verbindet die Forschungsideen der Schülerinnen und Schüler mit einer sichtbaren Wirtschaftssimulation: Gebäude produzieren und verbrauchen Ressourcen, Bewohner und Roboter arbeiten in Betrieben, große Gebäude belegen mehrere Kacheln, Forschungen benötigen Zeit und neue Gebäude werden durch Technologien freigeschaltet.

## Projektstruktur

| Datei oder Ordner | Aufgabe |
|---|---|
| `main.py` | Spielschleife, Karte, Eingaben, Kamera, Bauen, Abriss und Overlays |
| `gebaeude.py` | Gebäudedaten, Kategorien, Bildzuordnung, Rechteckflächen und Kollision |
| `ressourcen.py` | Baukosten, Produktion, Verbrauch, Personal, Speicher und Terraforming |
| `forschung.py` | Forschungsbaum, Voraussetzungen, Forschungspunkte und Forschungszeiten |
| `handel.py` | 2:1-Ressourcentausch, Marktplatz, Handelsposten und NPC-Angebote |
| `hud.py` | Ressourcenleiste, Gebäudestatus, Baukosten, Bildvorschau und Personalstatus |
| `menu.py` | Kategorisiertes, scrollbares Baumenü mit Bildvorschauen |
| `bilder/` | Alle verwendeten PNG-Gebäude-Assets |
| `test_stunde11.py` | Portabler Selbsttest für zentrale Spielregeln |
| `STUNDE11_SCHUELERHANDBUCH.md` | Schritt-für-Schritt-Erklärung für eigene Änderungen |
| `BILDER_ANLEITUNG.md` | Anleitung zum Erstellen und Einbinden eigener Bilder |
| `STUNDE11_DESIGN.md` | Verbindliche Spielregeln und Datenmodell |

## Starten und testen

Installiert Pygame, falls es noch fehlt:

```bash
python3 -m pip install pygame
```

Startet das Spiel aus diesem Ordner:

```bash
python3 main.py
```

Der Selbsttest wird so ausgeführt:

```bash
python3 test_stunde11.py
```

Bei erfolgreichem Test erscheint `STUNDE11_TESTS_OK`.

## Aktuelle Steuerung

| Taste oder Aktion | Wirkung |
|---|---|
| `1` bis `9` | Kategorie auswählen |
| `Pfeil links/rechts` | Innerhalb der gewählten Kategorie zum nächsten oder vorherigen Gebäude wechseln |
| Mausrad | In geöffneten Forschungs- oder Baumenüs scrollen |
| `0` | Das zuletzt erfolgreich gebaute Gebäude erneut auswählen |
| `G` | Schnellzugriff auf den Fusionsreaktor |
| `T` | Schnellzugriff auf die Roboterfabrik, sofern kein Handelsmenü geöffnet ist |
| Linksklick | Ausgewähltes Gebäude bauen oder im Terraforming-Modus eine Kachel umwandeln |
| Rechtsklick | Gebäude vollständig abreißen und 50 Prozent der aktuellen Baukosten zurückerhalten |
| `TAB` | Baumenü öffnen oder schließen |
| `F` | Forschungsmenü öffnen oder schließen |
| `F1` bis `F12` | Sichtbare Forschungszeile starten |
| `Bild auf/Bild ab` | Forschungsmenü seitenweise scrollen |
| `E` | Handelsmenü öffnen oder schließen |
| `Q/W/R/T/Y/U` | Im Handelsmenü einen angezeigten 2:1-Tausch ausführen |
| `J/K` | NPC-Handelsangebot annehmen oder ablehnen |
| `Z` | Terraforming-Modus ein- oder ausschalten, wenn erforscht |
| `Leertaste` | Pause oder Spielstart |
| `+` und `-` | Spielgeschwindigkeit zwischen 1× und 4× ändern |
| `WASD` oder Pfeiltasten | Kamera bewegen, sofern die Taste nicht gerade ein Gebäude innerhalb der Kategorie wechselt |
| `B` | Kamera zur Basis bewegen |
| `H` | Hilfe-Overlay öffnen oder schließen |
| `ESC` | Spiel beenden |

Die Zifferntasten sind jetzt **Kategorien** und keine festen Gebäudenummern mehr. So können weitere Gebäude ergänzt werden, ohne die gesamte Tastaturbelegung neu zu erfinden. Die Unterauswahl erfolgt mit links/rechts und wird unten im HUD zusammen mit einer Bildvorschau angezeigt. `1` bleibt damit die Kategorie für die Basis; die Geschwindigkeit wird nicht mehr mit `1` und `2`, sondern mit `+` und `-` geändert.

## Gebäudekategorien

| Ziffer | Kategorie | Enthaltene Gebäude |
|---:|---|---|
| `1` | Basis / Kolonie-Zentrum | Basis |
| `2` | Erzeuger / Rohstoffe | Reaktor, Farm, Holzfäller, Steinmetz, Mine, Gewächshaus |
| `3` | Wohngebäude | Wohnhaus, Wohnblock |
| `4` | Veredelung / Fabriken | Marktplatz, Roboterfabrik, Stahlwerk |
| `5` | Forschung / Bildung | Universität |
| `6` | Energie | Reaktor, Fusionsreaktor |
| `7` | Infrastruktur | Straße, Lagerhaus |
| `8` | Handel | Marktplatz, Handelsposten |
| `9` | Spezial / Prestige | Koloniezentrum |

Ein Gebäude darf in mehreren Kategorien auftauchen. Das ist ein Schnellzugriff und kein doppeltes Gebäude.

## Gebäude-Typen und Spielwerte

| Index | Gebäude | Größe | Grundfunktion | Personal |
|---:|---|---:|---|---:|
| 0 | Basis | 1×1 | +1 Gold, +1 Energie, +1 Holz und +1 Stein pro Tick; nur einmal | 0 |
| 1 | Reaktor | 1×1 | +5 Energie, verbraucht 2 Holz | 1 |
| 2 | Farm | 1×1 | +5 Nahrung, verbraucht 2 Energie | 2 |
| 3 | Holzfäller | 1×1 | +6 Holz, verbraucht 2 Energie; Forstwirtschaft ermöglicht Nachwuchs | 1 |
| 4 | Steinmetz | 1×1 | +5 Stein, verbraucht 3 Energie | 2 |
| 5 | Marktplatz | 1×1 | +12 Gold, verbraucht 5 Stein; aktiviert Tausch und Angebote | 1 |
| 6 | Wohnhaus | 1×1 | +1 Bevölkerung, verbraucht 3 Energie | 0 |
| 7 | Universität | **2×3** | +5 Forschung, verbraucht 2 Gold und 3 Energie | 2 |
| 8 | Mine | 1×1 | +2 Kohle; regelmäßig zusätzlich Eisen | 3 |
| 9 | Straße | 1×1 | Infrastruktur ohne Produktion | 0 |
| 10 | Fusionsreaktor | 1×1 | +25 Energie, verbraucht 5 Kohle | 4 |
| 11 | Roboterfabrik | 1×1 | +1 Roboter, verbraucht Energie und Kohle | 2 |
| 12 | Stahlwerk | 1×1 | Verarbeitet Eisen und Kohle zu Stahl | 3 |
| 13 | Gewächshaus | 1×1 | Zusätzliche Nahrungsproduktion | 2 |
| 14 | Lagerhaus | 1×1 | Erhöht mit Forschung die Speichergrenzen | 0 |
| 15 | Wohnblock | 1×1 | +3 Bevölkerung, verbraucht Energie und Nahrung | 0 |
| 16 | Handelsposten | 1×1 | +4 Gold und interkoloniale Handelsfunktion | 2 |
| 17 | Koloniezentrum | 1×1 | Prestigegebäude; stärkt bei vorhandener Anlage die gesamte Produktion um 5 Prozent | 0 |

### Die Universität als großes Gebäude

Das Schulbild `bilder/schule_2x3_kacheln_64x96.png` ist 64×96 Pixel groß. Das Seitenverhältnis 2:3 entspricht exakt zwei Kacheln Breite und drei Kacheln Höhe. Beim Bau ist die angeklickte Kachel die linke obere Ecke. Das Spiel prüft alle sechs Kacheln gegen Kartenrand und vorhandene Gebäude.

Beim Abriss genügt ein Rechtsklick auf eine beliebige der sechs Universitätskacheln. Die Liste enthält nur ein Universitätsobjekt; deshalb werden Gebäude und Rückerstattung nicht sechsmal bearbeitet.

## Ressourcen und Personal

Die Ressourcen sind `gold`, `energie`, `holz`, `stein`, `bevoelkerung`, `nahrung`, `forschung`, `kohle`, `eisen`, `roboter` und `stahl`. Jede Ressource besitzt eine Speichergrenze. Ein Lagerhaus wirkt erst dann als Speicherbonus, wenn ein Lagerhaus gebaut wurde und `lagerhaus_ausbau` erforscht ist. `energiespeicher` erhöht zusätzlich die Energiegrenze um 25 Prozent.

Jedes Produktionsgebäude mit Personalbedarf versucht pro Tick freie Bewohner oder Roboter zu bekommen. Reicht das Personal nicht für alle Gebäude, arbeiten die Gebäude in Listenreihenfolge, bis keine Arbeitskräfte mehr frei sind. Ein roter Punkt am Gebäude und `arbeitet: False` zeigen den Stillstand an. Roboter zählen als Arbeitskräfte, werden aber nicht als Bewohner gezählt.

Die Universität ist eine echte Arbeitsstätte: Ohne mindestens ein arbeitendes Universitätsgebäude gibt es keinen Forschungsfortschritt. `Verbesserte Laborausrüstung` und `Quantencomputer` erhöhen danach das Forschungstempo.

## Forschung

Forschungspunkte entstehen in arbeitenden Universitäten. Eine Technologie wird nicht sofort abgeschlossen: Beim Start werden Punkte bezahlt, danach läuft die Forschung über mehrere Wirtschaftsticks. Voraussetzungen werden in `forschung.py` als Technologie-ID eingetragen.

| Forschungsbereich | Integrierte Wirkungen |
|---|---|
| Gebäude | Effiziente Bautechnik senkt Baukosten um 5 Prozent, Kompakte Maschinen erlauben zwei kleine Gebäude pro Kachel, Anpassende Architektur gibt einen Effizienzbonus. |
| Energie | Energieoptimierung senkt Verbrauch um 5 Prozent, Verbesserte Generatoren erhöhen Energieproduktion um 10 Prozent, Energiespeicher erweitert das Energie-Limit um 25 Prozent, Fusionsreaktor und Mini-Reaktor sind neue Energieoptionen. |
| Forschung | Verbesserte Laborausrüstung beschleunigt Forschung um 10 Prozent, Neue Geräte erhöhen Laborwissen um 5 Prozent, Quantencomputer beschleunigen Forschung im Endgame um weitere 40 Prozent. |
| Automatisierung | Einfache Robotik schaltet Roboterfabriken frei. Roboter zählen als Personal. Autonome Fabriken benötigen 30 Prozent weniger Personal. |
| Steinmetz und Mine | Effizienter Aufbau erhöht Steinproduktion, Tiefenbohrung verbessert Minen und lässt Eisen häufiger entstehen. |
| Holzfäller | Verbesserte Äxte erhöhen Holzproduktion, Forstwirtschaft führt erschöpfte Wälder und Nachwachsen ein, effizientere Holzverwendung senkt Holzbaukosten. |
| Marktplatz und Handel | Verbesserte Marktstände erhöhen Goldproduktion, Ressourcenhandel ermöglicht 2:1-Tausch, Handel mit anderen Kolonien erzeugt NPC-Angebote, Handelsrouten beschleunigen sie. |
| Farm und Nahrung | Verbesserte Landwirtschaft erhöht Nahrung, höher sättigende Nahrung senkt Bewohnerverbrauch, Terraforming wandelt Kacheln in fruchtbaren Boden um. |
| Metallurgie | Stahlverarbeitung schaltet das Stahlwerk frei, Hochöfen erhöhen seine Stahlproduktion. |
| Nahrung | Gewächshausbau schaltet Gewächshäuser frei, Hydroponik erhöht ihre Produktion. |
| Logistik | Logistik-Grundlagen schaltet Lagerhäuser frei, Großlager erhöht mit gebautem Lagerhaus alle Speichergrenzen um 50 Prozent. |
| Kolonie | Wohnblockbau schaltet größere Wohnkapazität frei. |
| Prestige | Koloniezentrum schaltet das Prestigegebäude frei und stärkt mit einer vorhandenen Anlage die Produktion. |

## Bilder

Jedes Gebäude besitzt jetzt einen konkreten Bildnamen in `gebaeude.py`. Im Ordner `bilder/` liegen 64×64-Pixel-PNGs für alle 1×1-Gebäude und das 64×96-Pixel-Schulbild für die Universität. `labor.png` wird nicht mehr verwendet und wurde entfernt, weil die Universität das Labor ersetzt.

Die vollständige Anleitung befindet sich in [BILDER_ANLEITUNG.md](BILDER_ANLEITUNG.md). Die allgemeine Code-Anleitung befindet sich in [STUNDE11_SCHUELERHANDBUCH.md](STUNDE11_SCHUELERHANDBUCH.md). Die verbindlichen Regeln stehen in [STUNDE11_DESIGN.md](STUNDE11_DESIGN.md).

## Erweiterungsregel für neue Gebäude

Für ein neues Gebäude müssen mindestens vier Stellen zusammenpassen:

1. In `gebaeude.py` kommt ein Eintrag mit Name, Bild, Farbe, Kürzel, Größe und Kategorie.
2. In `ressourcen.py` kommt an **derselben Listenposition** ein Wirtschaftseintrag.
3. In `bilder/` liegt die exakt gleich geschriebene PNG-Datei.
4. In `forschung.py` wird eine Freischaltung oder eine passende Forschung eingetragen.

Danach wird das Gebäude im Baumenü, im HUD, in den Kategorien und beim Zeichnen automatisch berücksichtigt. Der Selbsttest prüft, ob die Listen gleich lang sind und ob jedes Gebäude ein Bild besitzt.

## Teststatus

Der aktuelle Selbsttest prüft Forschungs-IDs, 18 parallele Gebäude-/Wirtschaftseinträge, Bilddateien, Kategorien, kompakte Maschinen, Personal, Basisproduktion, Speichergrenzen, die 2×3-Universität, Rand- und Überlappungsschutz, Abriss, Terraforming, Handel und neue Forschungsfreischaltungen.


# Aktueller Stand nach der Gebäude- und Bildaufgabe

Die folgenden Regeln ersetzen ältere Abschnitte dieser README, in denen `1` bis `0` noch feste Einzelgebäude waren oder `1` und `2` gleichzeitig die Spielgeschwindigkeit steuerten.

## Kategorien statt fester Gebäudenummern

`1` bis `9` wählen Kategorien. Mit `Pfeil links/rechts` wird innerhalb der aktiven Kategorie weitergeschaltet. `0` wählt das zuletzt erfolgreich gebaute Gebäude aus. `+` und `-` steuern die Geschwindigkeit; `Leertaste` pausiert. Im HUD stehen Kategorie, Unterauswahl, Gebäudemaß und Bildvorschau.

| Taste | Kategorie |
|---:|---|
| 1 | Basis / Kolonie-Zentrum |
| 2 | Erzeuger / Rohstoffe |
| 3 | Wohngebäude |
| 4 | Veredelung / Fabriken |
| 5 | Forschung / Bildung |
| 6 | Energie |
| 7 | Infrastruktur |
| 8 | Handel |
| 9 | Spezial / Prestige |

Die Ziffern sind bewusst Kategorien. Ein Gebäude kann in mehreren Kategorien vorkommen, zum Beispiel der Marktplatz in `4` und `8`.

## Vollständige aktuelle Gebäudeliste

Die parallelen Listen in `gebaeude.py` und `ressourcen.py` enthalten jetzt 18 Einträge: Basis, Reaktor, Farm, Holzfäller, Steinmetz, Marktplatz, Wohnhaus, Universität, Mine, Straße, Fusionsreaktor, Roboterfabrik, Stahlwerk, Gewächshaus, Lagerhaus, Wohnblock, Handelsposten und Koloniezentrum.

Die Universität bleibt ein **2×3-Gebäude** und verwendet `bilder/schule_2x3_kacheln_64x96.png`. Neue Produktionsketten sind Eisen und Kohle → Stahl im Stahlwerk sowie zusätzliche Nahrung aus dem Gewächshaus. Lagerhaus, Wohnblock, Handelsposten und Koloniezentrum besitzen jeweils eine eigene Funktion und eine eigene Bilddatei.

## Bildstatus

Der Bilderordner enthält für jedes Gebäude eine PNG-Datei. Die 1×1-Gebäude verwenden 64×64 Pixel; das Universitätsbild verwendet 64×96 Pixel. `labor.png` wird nicht mehr verwendet, weil die Universität das Labor ersetzt hat. Die aktualisierte Dateinamen- und Einfügeanleitung befindet sich in `BILDER_ANLEITUNG.md`.

## Teststatus

`test_stunde11.py` prüft zusätzlich die 18 parallelen Gebäudedaten, die Bilddateien, die Kategorien, die Basis-Grundproduktion, die neue Ressource Stahl, die Lagerhaus-Speichererweiterung und die bestehenden Universität-, Handels-, Terraforming- und Personalregeln.
