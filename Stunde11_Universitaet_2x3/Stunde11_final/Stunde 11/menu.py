"""Baumenü für alle Gebäudetypen der Stunde 11."""

import pygame
import ressourcen

_fenster = None
_menu_offen = False


def menu_initialisieren(fenster_obj):
    global _fenster
    _fenster = fenster_obj


def menu_umschalten():
    global _menu_offen
    _menu_offen = not _menu_offen


def menu_ist_offen():
    return _menu_offen


def _ressourcen_name(name):
    return ressourcen.RESSOURCEN_NAMEN.get(name, name)


def _format_dict(d):
    if not d:
        return "kostenlos"
    return ", ".join(f"{menge} {_ressourcen_name(name)}" for name, menge in d.items())


def menu_zeichnen(gebaeude_typen, gebaeude_wirtschaft, ressourcen_dict=None):
    if _fenster is None or not _menu_offen:
        return
    overlay = pygame.Surface(_fenster.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 205))
    _fenster.blit(overlay, (0, 0))
    gross = pygame.font.Font(None, 32)
    klein = pygame.font.Font(None, 17)
    _fenster.blit(gross.render("BAUMENÜ  (TAB schließt)", True, (255, 255, 255)), (28, 18))
    _fenster.blit(klein.render("Taste, Kosten, Produktion, Personal und Freischaltung", True, (170, 180, 195)), (28, 48))

    for i, typ in enumerate(gebaeude_typen):
        y = 76 + i * 46
        wirtschaft = gebaeude_wirtschaft[i]
        frei = ressourcen_dict is None or ressourcen.ist_freigeschaltet(ressourcen_dict, i)
        farbe = (245, 245, 245) if frei else (125, 125, 135)
        pygame.draw.rect(_fenster, (24, 28, 40), (24, y - 3, 952, 42))
        pygame.draw.rect(_fenster, typ["farbe"], (29, y + 4, 20, 20))
        kosten = _format_dict(ressourcen.baukosten_berechnen(i))
        prod = _format_dict(wirtschaft.get("produktion", {})) if wirtschaft.get("produktion") else "nichts"
        personal = ressourcen.personalbedarf(i)
        groesse = f"{typ.get('breite', 1)}x{typ.get('hoehe', 1)} Kacheln"
        status = "frei" if frei else ressourcen.freischaltung_hinweis(ressourcen_dict, i)
        text = (f"[{typ.get('taste', i + 1)}] {typ['name']} ({groesse})  |  Kosten: {kosten}  |  "
                f"Produktion: {prod}  |  Personal: {personal}  |  {status}")
        _fenster.blit(klein.render(text, True, farbe), (58, y + 5))
        verbrauch = _format_dict(wirtschaft.get("verbrauch", {})) if wirtschaft.get("verbrauch") else "nichts"
        _fenster.blit(klein.render(f"Verbrauch: {verbrauch}", True, (170, 175, 190)), (58, y + 24))
