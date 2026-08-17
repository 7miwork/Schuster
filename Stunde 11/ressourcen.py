"""Wirtschaft, Personal, Speicher und Produktionsboni für Stunde 11."""

import math
import forschung


_wirtschafts_tick = 0

RESSOURCEN_NAMEN = {
    "gold": "Gold", "energie": "Energie", "holz": "Holz", "stein": "Stein",
    "bevoelkerung": "Bevoelkerung", "nahrung": "Nahrung", "forschung": "Forschung",
    "kohle": "Kohle", "eisen": "Eisen", "roboter": "Roboter",
}

# Alle Ressourcen haben eine Obergrenze. Das verhindert, dass die Kolonie durch
# wenige Gebäude sofort unendlich reich wird.
SPEICHER_BASIS = {
    "gold": 500.0, "energie": 100.0, "holz": 250.0, "stein": 250.0,
    "bevoelkerung": 100.0, "nahrung": 250.0, "forschung": 500.0,
    "kohle": 200.0, "eisen": 200.0, "roboter": 100.0,
}


GEBAEUDE_WIRTSCHAFT = [
    {"baukosten": {}, "produktion": {}, "verbrauch": {}, "personalbedarf": 0,
     "max_anzahl": 1, "freischaltung": None, "grosse_anlage": False},
    {"baukosten": {"gold": 20}, "produktion": {"energie": 5}, "verbrauch": {"holz": 2},
     "personalbedarf": 1, "max_anzahl": None, "freischaltung": None, "grosse_anlage": False},
    {"baukosten": {"gold": 15, "energie": 10}, "produktion": {"nahrung": 5},
     "verbrauch": {"energie": 2}, "personalbedarf": 2, "max_anzahl": None,
     "freischaltung": None, "grosse_anlage": False},
    {"baukosten": {"gold": 10, "energie": 5}, "produktion": {"holz": 6},
     "verbrauch": {"energie": 2}, "personalbedarf": 1, "max_anzahl": None,
     "freischaltung": None, "grosse_anlage": False},
    {"baukosten": {"gold": 15, "energie": 10}, "produktion": {"stein": 5},
     "verbrauch": {"energie": 3}, "personalbedarf": 2, "max_anzahl": None,
     "freischaltung": None, "grosse_anlage": False},
    {"baukosten": {"gold": 30, "energie": 15}, "produktion": {"gold": 12},
     "verbrauch": {"stein": 5}, "personalbedarf": 1, "max_anzahl": None,
     "freischaltung": {"typ": "ressource", "ressource": "bevoelkerung", "menge": 5},
     "grosse_anlage": False},
    {"baukosten": {"gold": 20, "holz": 15, "stein": 10}, "produktion": {"bevoelkerung": 1},
     "verbrauch": {"energie": 3}, "personalbedarf": 0, "max_anzahl": 10,
     "freischaltung": {"typ": "ressource", "ressource": "bevoelkerung", "menge": 5},
     "grosse_anlage": True},
    {"baukosten": {"gold": 40, "energie": 20}, "produktion": {"forschung": 5},
     "verbrauch": {"gold": 2, "energie": 3}, "personalbedarf": 2, "max_anzahl": None,
     "freischaltung": [{"typ": "ressource", "ressource": "bevoelkerung", "menge": 5},
                        {"typ": "ressource", "ressource": "gold", "menge": 40}],
     "grosse_anlage": True},
    {"baukosten": {"gold": 35, "energie": 10, "stein": 15}, "produktion": {"kohle": 2},
     "verbrauch": {"energie": 2}, "personalbedarf": 3, "max_anzahl": None,
     "freischaltung": {"typ": "forschung", "technologie": "minenbau"}, "grosse_anlage": True},
    {"baukosten": {"stein": 2}, "produktion": {}, "verbrauch": {}, "personalbedarf": 0,
     "max_anzahl": None, "freischaltung": None, "grosse_anlage": False},
    {"baukosten": {"gold": 100, "energie": 20, "stein": 40, "eisen": 20},
     "produktion": {"energie": 25}, "verbrauch": {"kohle": 5}, "personalbedarf": 4,
     "max_anzahl": None, "freischaltung": {"typ": "forschung", "technologie": "fusionsreaktor"},
     "grosse_anlage": True},
    {"baukosten": {"gold": 60, "energie": 20, "eisen": 10}, "produktion": {"roboter": 1},
     "verbrauch": {"energie": 2, "kohle": 1}, "personalbedarf": 2, "max_anzahl": None,
     "freischaltung": {"typ": "forschung", "technologie": "einfache_robotik"},
     "grosse_anlage": True},
]


_GEBAEUDE_NAMEN = ["Basis", "Reaktor", "Farm", "Holzfaeller", "Steinmetz", "Marktplatz",
                   "Wohnhaus", "Universitaet", "Mine", "Strasse", "Fusionsreaktor", "Roboterfabrik"]


def _hat_genug(ressourcen_dict, ressourcen_name, benoetigte_menge):
    return ressourcen_dict.get(ressourcen_name, 0) >= benoetigte_menge


def _gebaeude_name_fuer_index(typ_index):
    return _GEBAEUDE_NAMEN[typ_index] if 0 <= typ_index < len(_GEBAEUDE_NAMEN) else "Unbekannt"


def _ressourcen_name(ress_name):
    return RESSOURCEN_NAMEN.get(ress_name, ress_name)


def maximaler_speicher(ressourcen_name):
    limit = SPEICHER_BASIS.get(ressourcen_name, 9999.0)
    if ressourcen_name == "energie" and forschung.ist_technologie_erforscht("energiespeicher"):
        limit *= 1.25
    return limit


def ressourcen_begrenzen(ressourcen_dict):
    for name, limit in SPEICHER_BASIS.items():
        wert = ressourcen_dict.get(name, 0)
        ressourcen_dict[name] = max(0.0, min(float(wert), maximaler_speicher(name)))


def baukosten_berechnen(typ_index):
    rohkosten = GEBAEUDE_WIRTSCHAFT[typ_index].get("baukosten", {})
    kosten = dict(rohkosten)
    for ress_name, wert in list(kosten.items()):
        faktor = 1.0
        if forschung.ist_technologie_erforscht("effiziente_bautechnik"):
            faktor *= 0.95
        if ress_name == "holz" and forschung.ist_technologie_erforscht("effizientere_holzverwendung"):
            faktor *= 0.95
        kosten[ress_name] = max(1, int(math.ceil(wert * faktor)))
    return kosten


def ist_freigeschaltet(ressourcen_dict, typ_index):
    freischaltung = GEBAEUDE_WIRTSCHAFT[typ_index].get("freischaltung")
    if freischaltung is None:
        return True

    def pruefen(bedingung):
        if bedingung.get("typ", "ressource") == "forschung":
            return forschung.ist_technologie_erforscht(bedingung["technologie"])
        return _hat_genug(ressourcen_dict, bedingung["ressource"], bedingung["menge"])

    if isinstance(freischaltung, list):
        return all(pruefen(bedingung) for bedingung in freischaltung)
    return pruefen(freischaltung)


def freischaltung_hinweis(ressourcen_dict, typ_index):
    freischaltung = GEBAEUDE_WIRTSCHAFT[typ_index].get("freischaltung")
    if freischaltung is None or ist_freigeschaltet(ressourcen_dict, typ_index):
        return ""
    bedingungen = freischaltung if isinstance(freischaltung, list) else [freischaltung]
    texte = []
    for bedingung in bedingungen:
        if bedingung.get("typ", "ressource") == "forschung":
            texte.append("Technologie: " + forschung.technologie_name(bedingung["technologie"]))
        else:
            texte.append(f"{bedingung['menge']} {_ressourcen_name(bedingung['ressource'])}")
    return "Benötigt " + " und ".join(texte)


def kann_bauen(ressourcen_dict, liste_gebaeude, typ_index, boden_typ=None):
    if typ_index < 0 or typ_index >= len(GEBAEUDE_WIRTSCHAFT):
        return False
    if not ist_freigeschaltet(ressourcen_dict, typ_index):
        print(f"{_gebaeude_name_fuer_index(typ_index)} gesperrt: {freischaltung_hinweis(ressourcen_dict, typ_index)}")
        return False
    wirtschaft = GEBAEUDE_WIRTSCHAFT[typ_index]
    max_anzahl = wirtschaft.get("max_anzahl")
    if max_anzahl is not None and sum(g["typ"] == typ_index for g in liste_gebaeude) >= max_anzahl:
        print(f"{_gebaeude_name_fuer_index(typ_index)}: maximales Limit erreicht")
        return False
    if boden_typ is not None:
        boden_anforderung = {2: 1, 3: 1, 4: 2}
        if typ_index in boden_anforderung and boden_typ != boden_anforderung[typ_index]:
            return False
    for ress_name, benoetigt in baukosten_berechnen(typ_index).items():
        if not _hat_genug(ressourcen_dict, ress_name, benoetigt):
            print(f"Nicht genug {_ressourcen_name(ress_name)} für {_gebaeude_name_fuer_index(typ_index)}")
            return False
    return True


def baukosten_abziehen(ressourcen_dict, typ_index):
    for ress_name, kosten in baukosten_berechnen(typ_index).items():
        ressourcen_dict[ress_name] = max(0.0, ressourcen_dict.get(ress_name, 0) - kosten)


def ressourcen_zurueckerstatten(ressourcen_dict, typ_index):
    rueckerstattung = {}
    for ress_name, kosten in baukosten_berechnen(typ_index).items():
        betrag = kosten // 2
        if betrag:
            ressourcen_dict[ress_name] = ressourcen_dict.get(ress_name, 0) + betrag
            rueckerstattung[ress_name] = betrag
    ressourcen_begrenzen(ressourcen_dict)
    return rueckerstattung


def personalbedarf(typ_index):
    bedarf = GEBAEUDE_WIRTSCHAFT[typ_index].get("personalbedarf", 0)
    if forschung.ist_technologie_erforscht("autonome_fabriken") and bedarf:
        return max(1, int(round(bedarf * 0.70)))
    return bedarf


def personal_info(ressourcen_dict, liste_gebaeude):
    verfuegbar = int(ressourcen_dict.get("bevoelkerung", 0) + ressourcen_dict.get("roboter", 0))
    bedarf = sum(personalbedarf(g["typ"]) for g in liste_gebaeude)
    return verfuegbar, bedarf


def _produktion_multiplikator(typ_index, ress_name):
    faktor = 1.0
    if forschung.ist_technologie_erforscht("produktion"):
        faktor *= 1.25
    if ress_name == "energie" and forschung.ist_technologie_erforscht("verbesserte_generatoren"):
        faktor *= 1.10
    if typ_index == 2 and forschung.ist_technologie_erforscht("verbesserte_landwirtschaft"):
        faktor *= 1.10
    if typ_index == 3 and forschung.ist_technologie_erforscht("verbesserte_aexte"):
        faktor *= 1.10
    if typ_index == 4 and forschung.ist_technologie_erforscht("effizienter_aufbau"):
        faktor *= 1.10
    if typ_index == 5 and forschung.ist_technologie_erforscht("verbesserte_marktstaende"):
        faktor *= 1.10
    if typ_index == 7 and ress_name == "forschung" and forschung.ist_technologie_erforscht("neue_instrumente"):
        faktor *= 1.05
    if typ_index == 8 and forschung.ist_technologie_erforscht("tiefenbohrung"):
        faktor *= 1.50
    return faktor


def _waldbetrieb_moeglich(gebaeude):
    if not forschung.ist_technologie_erforscht("forstwirtschaft"):
        return True
    if "wald_vorrat" not in gebaeude:
        gebaeude["wald_vorrat"] = 30
        gebaeude["wald_nachwuchs"] = 0
    if gebaeude["wald_vorrat"] > 0:
        return True
    gebaeude["wald_nachwuchs"] += 1.5 if forschung.ist_technologie_erforscht("forstwirtschaft") else 1.0
    if gebaeude["wald_nachwuchs"] >= 6:
        gebaeude["wald_vorrat"] = 30
        gebaeude["wald_nachwuchs"] = 0
        return True
    return False


def ressourcen_produzieren(ressourcen_dict, liste_gebaeude, karten_daten=None):
    global _wirtschafts_tick
    _wirtschafts_tick += 1

    # Die Bewohner essen pro Tick. Ein leerer Nahrungsspeicher blockiert nicht
    # die ganze Wirtschaft, erzeugt aber eine sichtbare Defizitmeldung im Status.
    nahrungsverbrauch = ressourcen_dict.get("bevoelkerung", 0) * 0.05
    if forschung.ist_technologie_erforscht("hoeher_saettigende_nahrung"):
        nahrungsverbrauch *= 0.95
    ressourcen_dict["nahrung"] = max(0.0, ressourcen_dict.get("nahrung", 0) - nahrungsverbrauch)

    verfuegbares_personal = int(ressourcen_dict.get("bevoelkerung", 0) + ressourcen_dict.get("roboter", 0))
    aktive_labore = 0
    for gebaeude in liste_gebaeude:
        typ_index = gebaeude["typ"]
        wirtschaft = GEBAEUDE_WIRTSCHAFT[typ_index]
        personal = personalbedarf(typ_index)
        if personal > verfuegbares_personal:
            gebaeude["arbeitet"] = False
            continue
        if typ_index == 3 and not _waldbetrieb_moeglich(gebaeude):
            gebaeude["arbeitet"] = False
            continue

        verbrauch = dict(wirtschaft.get("verbrauch", {}))
        produktion = dict(wirtschaft.get("produktion", {}))
        if forschung.ist_technologie_erforscht("energieoptimierung") and "energie" in verbrauch:
            verbrauch["energie"] *= 0.95
        if typ_index == 1 and forschung.ist_technologie_erforscht("reaktor_upgrade"):
            verbrauch["kohle"] = verbrauch.get("kohle", 0) + 1
            produktion["energie"] = produktion.get("energie", 0) + 3
        if typ_index == 8 and _wirtschafts_tick % (5 if forschung.ist_technologie_erforscht("tiefenbohrung") else 10) == 0:
            produktion["eisen"] = 1
        if forschung.ist_technologie_erforscht("stein_effizienz") and typ_index == 4:
            verbrauch["energie"] = max(0, verbrauch.get("energie", 0) - 1)
        if forschung.ist_technologie_erforscht("mini_reaktor") and wirtschaft.get("grosse_anlage") and typ_index != 1:
            produktion["energie"] = produktion.get("energie", 0) + 1

        if any(not _hat_genug(ressourcen_dict, name, menge) for name, menge in verbrauch.items()):
            gebaeude["arbeitet"] = False
            continue

        for ress_name, menge in verbrauch.items():
            ressourcen_dict[ress_name] = max(0.0, ressourcen_dict.get(ress_name, 0) - menge)
        verfuegbares_personal -= personal
        gebaeude["arbeitet"] = True
        if typ_index == 7:
            aktive_labore += 1

        effizient_bonus = 1.0
        if forschung.ist_technologie_erforscht("anpassende_architektur"):
            effizient_bonus += 0.15
        for ress_name, menge in produktion.items():
            faktor = effizient_bonus * _produktion_multiplikator(typ_index, ress_name)
            hinzu = menge * faktor
            ressourcen_dict[ress_name] = ressourcen_dict.get(ress_name, 0) + hinzu
        if typ_index == 3 and forschung.ist_technologie_erforscht("forstwirtschaft"):
            gebaeude["wald_vorrat"] = max(0, gebaeude.get("wald_vorrat", 30) - 1)

    # Labor-Forschung und alle Speicherobergrenzen werden nach dem Tick aktualisiert.
    forschung.forschung_tick(ressourcen_dict, aktive_labore)
    ressourcen_begrenzen(ressourcen_dict)
    ressourcen_dict["personal_verfuegbar"] = int(ressourcen_dict.get("bevoelkerung", 0) + ressourcen_dict.get("roboter", 0))
    ressourcen_dict["personal_bedarf"] = sum(personalbedarf(g["typ"]) for g in liste_gebaeude)
    ressourcen_dict["wirtschafts_tick"] = _wirtschafts_tick


def energie_status(ressourcen_dict):
    return f"Energie {ressourcen_dict.get('energie', 0):.0f}/{maximaler_speicher('energie'):.0f}"


def ressourcen_limit_text(ressourcen_dict, name):
    return f"{ressourcen_dict.get(name, 0):.1f}/{maximaler_speicher(name):.0f}"


def terraformieren(ressourcen_dict, karten_daten, kachel_x, kachel_y):
    if not forschung.ist_technologie_erforscht("terraforming"):
        return False, "Terraforming ist noch nicht erforscht."
    if not (0 <= kachel_y < len(karten_daten) and 0 <= kachel_x < len(karten_daten[0])):
        return False, "Diese Kachel liegt außerhalb der Karte."
    if karten_daten[kachel_y][kachel_x] == 1:
        return False, "Diese Kachel ist bereits fruchtbarer Boden."
    kosten = {"energie": 5, "stein": 3}
    if any(ressourcen_dict.get(name, 0) < wert for name, wert in kosten.items()):
        return False, "Terraforming benötigt 5 Energie und 3 Stein."
    for name, wert in kosten.items():
        ressourcen_dict[name] -= wert
    karten_daten[kachel_y][kachel_x] = 1
    return True, "Kachel wurde in fruchtbaren Boden umgewandelt."
