"""Gebäudetypen, Mehrkachel-Platzierung und Darstellung für Stunde 11."""

import os
import pygame
import forschung


GEBAEUDE_TYPEN = [
    {"name": "Basis", "bild": "basis.png", "farbe": (100, 180, 255), "kuerzel": "B", "taste": "1", "breite": 1, "hoehe": 1},
    {"name": "Reaktor", "bild": "reaktor.png", "farbe": (255, 200, 50), "kuerzel": "R", "taste": "2", "breite": 1, "hoehe": 1},
    {"name": "Farm", "bild": "farm.png", "farbe": (80, 200, 100), "kuerzel": "F", "taste": "3", "breite": 1, "hoehe": 1},
    {"name": "Holzfaeller", "bild": "holzfaeller.png", "farbe": (160, 120, 60), "kuerzel": "H", "taste": "4", "breite": 1, "hoehe": 1},
    {"name": "Steinmetz", "bild": "steinmetz.png", "farbe": (140, 140, 150), "kuerzel": "S", "taste": "5", "breite": 1, "hoehe": 1},
    {"name": "Marktplatz", "bild": "marktplatz.png", "farbe": (220, 180, 80), "kuerzel": "M", "taste": "6", "breite": 1, "hoehe": 1},
    {"name": "Wohnhaus", "bild": "wohnhaus.png", "farbe": (180, 120, 200), "kuerzel": "W", "taste": "7", "breite": 1, "hoehe": 1},
    # Die Universität ist das erste echte Mehrkachel-Gebäude: 2 breit x 3 hoch.
    {"name": "Universitaet", "bild": "schule_2x3_kacheln_64x96.png", "farbe": (150, 200, 255), "kuerzel": "L", "taste": "8", "breite": 2, "hoehe": 3},
    {"name": "Mine", "bild": None, "farbe": (110, 110, 120), "kuerzel": "M", "taste": "9", "breite": 1, "hoehe": 1},
    {"name": "Strasse", "bild": None, "farbe": (90, 90, 95), "kuerzel": "S", "taste": "0", "breite": 1, "hoehe": 1},
    {"name": "Fusionsreaktor", "bild": None, "farbe": (255, 110, 210), "kuerzel": "F", "taste": "G", "breite": 1, "hoehe": 1},
    {"name": "Roboterfabrik", "bild": None, "farbe": (100, 210, 210), "kuerzel": "R", "taste": "T", "breite": 1, "hoehe": 1},
]

_fenster = None
_kachel_groesse = 48
_bilder = {}


def gebaeude_initialisieren(fenster_obj, kachel_groesse):
    global _fenster, _kachel_groesse, _bilder
    _fenster = fenster_obj
    _kachel_groesse = kachel_groesse
    bilder_ordner = os.path.join(os.path.dirname(__file__), "bilder")
    _bilder = {}
    for typ_daten in GEBAEUDE_TYPEN:
        dateiname = typ_daten.get("bild")
        if not dateiname:
            continue
        bild_pfad = os.path.join(bilder_ordner, dateiname)
        if os.path.exists(bild_pfad):
            _bilder[typ_daten["name"]] = pygame.image.load(bild_pfad).convert_alpha()


def _masse_fuer_typ(typ_index):
    typ_daten = GEBAEUDE_TYPEN[typ_index]
    return typ_daten.get("breite", 1), typ_daten.get("hoehe", 1)


def gebaeude_flaeche(typ_index, kachel_x, kachel_y):
    """Gibt alle Kacheln zurück, die ein Gebäude beansprucht."""
    breite, hoehe = _masse_fuer_typ(typ_index)
    return [(kachel_x + dx, kachel_y + dy)
            for dy in range(hoehe) for dx in range(breite)]


def _gebaeude_flaeche(gebaeude):
    return gebaeude_flaeche(gebaeude["typ"], gebaeude["kachel_x"], gebaeude["kachel_y"])


def _kompakt_erlaubt(typ_index):
    breite, hoehe = _masse_fuer_typ(typ_index)
    return (breite == 1 and hoehe == 1 and
            forschung.ist_technologie_erforscht("kompakte_maschinen") and
            typ_index not in (0, 9))


def kann_platzieren(liste_gebaeude, typ_index, kachel_x, kachel_y,
                    karten_breite=None, karten_hoehe=None):
    """Prüft Kachelgrenzen, Mehrkachelfläche und Kompaktbelegung."""
    neue_flaeche = set(gebaeude_flaeche(typ_index, kachel_x, kachel_y))
    if karten_breite is not None and karten_hoehe is not None:
        if any(x < 0 or y < 0 or x >= karten_breite or y >= karten_hoehe
               for x, y in neue_flaeche):
            return False

    ueberlappungen = []
    for vorhandenes in liste_gebaeude:
        alte_flaeche = set(_gebaeude_flaeche(vorhandenes))
        schnitt = neue_flaeche.intersection(alte_flaeche)
        if schnitt:
            ueberlappungen.append(vorhandenes)

    if not ueberlappungen:
        return True

    # Ein Mehrkachel-Gebäude darf niemals mit einem anderen Gebäude überlappen.
    if len(neue_flaeche) != 1 or any(len(_gebaeude_flaeche(g)) != 1 for g in ueberlappungen):
        return False

    # Kompakte Maschinen erlaubt höchstens zwei kleine Produktionsgebäude auf
    # genau einer Kachel. Ein 2x3-Gebäude bleibt davon ausgeschlossen.
    if len(ueberlappungen) >= 2 or not _kompakt_erlaubt(typ_index):
        return False
    return _kompakt_erlaubt(ueberlappungen[0]["typ"])


def gebaeude_platzieren(liste_gebaeude, typ_index, kachel_x, kachel_y,
                        karten_breite=None, karten_hoehe=None):
    if not kann_platzieren(liste_gebaeude, typ_index, kachel_x, kachel_y,
                           karten_breite, karten_hoehe):
        print(f"Die Fläche ab ({kachel_x}, {kachel_y}) ist bereits belegt oder liegt außerhalb der Karte.")
        return False
    neues_gebaeude = {
        "typ": typ_index, "kachel_x": kachel_x, "kachel_y": kachel_y,
        "arbeitet": False,
    }
    if typ_index == 3 and forschung.ist_technologie_erforscht("forstwirtschaft"):
        neues_gebaeude["wald_vorrat"] = 30
        neues_gebaeude["wald_nachwuchs"] = 0
    liste_gebaeude.append(neues_gebaeude)
    breite, hoehe = _masse_fuer_typ(typ_index)
    print(f"{GEBAEUDE_TYPEN[typ_index]['name']} auf ({kachel_x}, {kachel_y}) platziert ({breite}x{hoehe} Kacheln).")
    return True


def gebaeude_abreissen(liste_gebaeude, kachel_x, kachel_y):
    """Reißt das Gebäude ab, dessen Fläche die angeklickte Kachel enthält."""
    for gebaeude in list(liste_gebaeude):
        if (kachel_x, kachel_y) in _gebaeude_flaeche(gebaeude):
            if gebaeude["typ"] == 0:
                print("Die Basis kann nicht abgerissen werden.")
                return None
            typ_index = gebaeude["typ"]
            liste_gebaeude.remove(gebaeude)
            return typ_index
    return None


def _position_fuer_stapel(liste_gebaeude, gebaeude):
    gleiche = [g for g in liste_gebaeude
               if len(_gebaeude_flaeche(g)) == 1
               and g["kachel_x"] == gebaeude["kachel_x"]
               and g["kachel_y"] == gebaeude["kachel_y"]]
    return gleiche.index(gebaeude) if gebaeude in gleiche else 0


def gebaeude_zeichnen(liste_gebaeude, kamera_x, kamera_y):
    if _fenster is None:
        return
    schrift = pygame.font.Font(None, 23)
    for gebaeude in liste_gebaeude:
        typ_index = gebaeude["typ"]
        typ_daten = GEBAEUDE_TYPEN[typ_index]
        breite, hoehe = _masse_fuer_typ(typ_index)
        pixel_x = gebaeude["kachel_x"] * _kachel_groesse - kamera_x
        pixel_y = gebaeude["kachel_y"] * _kachel_groesse - kamera_y
        voll_breite = breite * _kachel_groesse
        voll_hoehe = hoehe * _kachel_groesse
        if pixel_x + voll_breite < 0 or pixel_y + voll_hoehe < 0:
            continue
        if pixel_x > _fenster.get_width() or pixel_y > _fenster.get_height():
            continue

        if breite > 1 or hoehe > 1:
            # Mehrkachel-Gebäude werden als ein zusammenhängendes Bild gezeichnet.
            rect = pygame.Rect(pixel_x + 4, pixel_y + 4,
                               voll_breite - 8, voll_hoehe - 8)
            stapel_index = 0
        else:
            stapel_index = _position_fuer_stapel(liste_gebaeude, gebaeude)
            if stapel_index:
                x_offset, y_offset = _kachel_groesse // 2, _kachel_groesse // 2
                groesse = _kachel_groesse // 2
            else:
                x_offset = y_offset = 4
                groesse = _kachel_groesse - 8
            rect = pygame.Rect(pixel_x + x_offset, pixel_y + y_offset,
                               groesse, groesse)

        bild = _bilder.get(typ_daten["name"])
        if bild is not None:
            _fenster.blit(pygame.transform.smoothscale(bild, rect.size), rect)
        else:
            pygame.draw.rect(_fenster, typ_daten["farbe"], rect)
        pygame.draw.rect(_fenster, (255, 255, 255), rect, 2)

        # Bei großen Gebäuden reicht ein kleines Kürzel oben links; das Bild
        # selbst bleibt vollständig sichtbar.
        if breite == 1 and hoehe == 1:
            text = schrift.render(typ_daten["kuerzel"], True, (20, 20, 20))
            _fenster.blit(text, text.get_rect(center=rect.center))
        else:
            text = schrift.render(typ_daten["kuerzel"], True, (20, 20, 20))
            _fenster.blit(text, (rect.left + 6, rect.top + 4))

        if gebaeude.get("arbeitet") is False and typ_index not in (0, 9):
            pygame.draw.circle(_fenster, (220, 70, 70), (rect.right - 7, rect.top + 7), 4)
