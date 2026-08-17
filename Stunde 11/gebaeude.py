"""Gebäudetypen, Platzierung und Darstellung für Stunde 11."""

import os
import pygame
import forschung


GEBAEUDE_TYPEN = [
    {"name": "Basis", "bild": "basis.png", "farbe": (100, 180, 255), "kuerzel": "B", "taste": "1"},
    {"name": "Reaktor", "bild": "reaktor.png", "farbe": (255, 200, 50), "kuerzel": "R", "taste": "2"},
    {"name": "Farm", "bild": "farm.png", "farbe": (80, 200, 100), "kuerzel": "F", "taste": "3"},
    {"name": "Holzfaeller", "bild": "holzfaeller.png", "farbe": (160, 120, 60), "kuerzel": "H", "taste": "4"},
    {"name": "Steinmetz", "bild": "steinmetz.png", "farbe": (140, 140, 150), "kuerzel": "S", "taste": "5"},
    {"name": "Marktplatz", "bild": "marktplatz.png", "farbe": (220, 180, 80), "kuerzel": "M", "taste": "6"},
    {"name": "Wohnhaus", "bild": "wohnhaus.png", "farbe": (180, 120, 200), "kuerzel": "W", "taste": "7"},
    {"name": "Universitaet", "bild": "labor.png", "farbe": (150, 200, 255), "kuerzel": "L", "taste": "8"},
    {"name": "Mine", "bild": None, "farbe": (110, 110, 120), "kuerzel": "M", "taste": "9"},
    {"name": "Strasse", "bild": None, "farbe": (90, 90, 95), "kuerzel": "S", "taste": "0"},
    {"name": "Fusionsreaktor", "bild": None, "farbe": (255, 110, 210), "kuerzel": "F", "taste": "G"},
    {"name": "Roboterfabrik", "bild": None, "farbe": (100, 210, 210), "kuerzel": "R", "taste": "T"},
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


def _kompakt_erlaubt(typ_index):
    return forschung.ist_technologie_erforscht("kompakte_maschinen") and typ_index not in (0, 9)


def kann_platzieren(liste_gebaeude, typ_index, kachel_x, kachel_y):
    gleiche_kachel = [g for g in liste_gebaeude
                      if g["kachel_x"] == kachel_x and g["kachel_y"] == kachel_y]
    if not gleiche_kachel:
        return True
    if len(gleiche_kachel) >= 2 or not _kompakt_erlaubt(typ_index):
        return False
    return all(_kompakt_erlaubt(g["typ"]) for g in gleiche_kachel)


def gebaeude_platzieren(liste_gebaeude, typ_index, kachel_x, kachel_y):
    if not kann_platzieren(liste_gebaeude, typ_index, kachel_x, kachel_y):
        print(f"Kachel ({kachel_x}, {kachel_y}) ist bereits vollständig belegt.")
        return False
    neues_gebaeude = {
        "typ": typ_index, "kachel_x": kachel_x, "kachel_y": kachel_y,
        "arbeitet": False,
    }
    if typ_index == 3 and forschung.ist_technologie_erforscht("forstwirtschaft"):
        neues_gebaeude["wald_vorrat"] = 30
        neues_gebaeude["wald_nachwuchs"] = 0
    liste_gebaeude.append(neues_gebaeude)
    print(f"{GEBAEUDE_TYPEN[typ_index]['name']} auf ({kachel_x}, {kachel_y}) platziert.")
    return True


def gebaeude_abreissen(liste_gebaeude, kachel_x, kachel_y):
    for gebaeude in list(liste_gebaeude):
        if gebaeude["kachel_x"] == kachel_x and gebaeude["kachel_y"] == kachel_y:
            if gebaeude["typ"] == 0:
                print("Die Basis kann nicht abgerissen werden.")
                return None
            typ_index = gebaeude["typ"]
            liste_gebaeude.remove(gebaeude)
            return typ_index
    return None


def _position_fuer_stapel(liste_gebaeude, gebaeude):
    gleiche = [g for g in liste_gebaeude
               if g["kachel_x"] == gebaeude["kachel_x"] and g["kachel_y"] == gebaeude["kachel_y"]]
    return gleiche.index(gebaeude) if gebaeude in gleiche else 0


def gebaeude_zeichnen(liste_gebaeude, kamera_x, kamera_y):
    if _fenster is None:
        return
    schrift = pygame.font.Font(None, 23)
    for gebaeude in liste_gebaeude:
        pixel_x = gebaeude["kachel_x"] * _kachel_groesse - kamera_x
        pixel_y = gebaeude["kachel_y"] * _kachel_groesse - kamera_y
        if pixel_x + _kachel_groesse < 0 or pixel_y + _kachel_groesse < 0:
            continue
        if pixel_x > _fenster.get_width() or pixel_y > _fenster.get_height():
            continue
        typ_daten = GEBAEUDE_TYPEN[gebaeude["typ"]]
        stapel_index = _position_fuer_stapel(liste_gebaeude, gebaeude)
        if stapel_index:
            x_offset, y_offset = _kachel_groesse // 2, _kachel_groesse // 2
            groesse = _kachel_groesse // 2
        else:
            x_offset = y_offset = 4
            groesse = _kachel_groesse - 8
        rect = pygame.Rect(pixel_x + x_offset, pixel_y + y_offset, groesse, groesse)
        bild = _bilder.get(typ_daten["name"])
        if bild is not None:
            _fenster.blit(pygame.transform.smoothscale(bild, rect.size), rect)
        else:
            pygame.draw.rect(_fenster, typ_daten["farbe"], rect)
        pygame.draw.rect(_fenster, (255, 255, 255), rect, 2)
        text = schrift.render(typ_daten["kuerzel"], True, (20, 20, 20))
        _fenster.blit(text, text.get_rect(center=rect.center))
        if gebaeude.get("arbeitet") is False and gebaeude["typ"] not in (0, 9):
            pygame.draw.circle(_fenster, (220, 70, 70), (rect.right - 5, rect.top + 5), 4)
