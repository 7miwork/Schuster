"""
=============================================================================
MODUL: ressourcen.py  —  Weltraum-Koloniespiel  (Stunde 6)
=============================================================================

Was ist ein Ressourcen-Modul?
    In Final Earth 2 produzieren Gebäude automatisch Ressourcen und
    verbrauchen andere. Ein Reaktor braucht zum Beispiel Holz, um
    Energie zu erzeugen. Dieses Modul verwaltet die Wirtschaft:
    - Baukosten: Was kostet es, ein Gebäude zu bauen?
    - Produktion: Was produziert jedes Gebäude?
    - Verbrauch: Was verbraucht jedes Gebäude?
    - Tick-System: 1× pro Sekunde werden alle Gebäude abgerechnet

Aufgabe dieses Moduls:
    Alles rund um die Wirtschaft des Spiels:
    - GEBAEUDE_WIRTSCHAFT — Wirtschaftsdaten für jeden Gebäudetyp
    - kann_bauen() — Prüft ob genug Ressourcen für ein Gebäude da sind
    - baukosten_abziehen() — Zieht die Baukosten von den Ressourcen ab
    - ressourcen_produzieren() — Lässt alle Gebäude produzieren (1×/Sekunde)

Konzepte in dieser Datei:
    ✓ Dictionary — Wirtschaftsdaten als Schlüssel-Wert-Paare
    ✓ Parallele Listen — GEBAEUDE_WIRTSCHAFT hat denselben Index
      wie GEBAEUDE_TYPEN in gebaeude.py (0=Basis, 1=Reaktor, ...)
    ✓ Funktionen mit Parametern und Return-Werten
    ✓ Werte dürfen nie negativ werden — Sicherheitsprüfung!
    ✓ Tick-System: Nur 1× pro Sekunde rechnen, nicht jeden Frame

Stunde 5 — Was der Spieler gelernt hat:
    ✓ Wirtschaftsdaten pro Gebäude (Baukosten, Produktion, Verbrauch)
    ✓ Prüfen ob Bauen möglich ist (Ressourcen-Voraussetzungen)
    ✓ Baukosten automatisch abziehen
    ✓ Produktion/Verbrauch läuft automatisch (Tick-System)
    ✓ Gebäude produziert nichts, wenn der Rohstoff fehlt
    ✓ Basis kann nur 1× gebaut werden

Stunde 6 — NEU dazu:
    ✓ Zwei neue Gebäude: Holzfäller und Steinmetz
    ✓ Neuer Rohstoff: Stein (vierter Rohstoff im Spiel)
    ✓ Wirtschaftsdaten auf 5 Gebäude erweitert (Indizes 0–4)
=============================================================================
"""

# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: WIRTSCHAFTSDATEN
# ═════════════════════════════════════════════════════════════════════════════
# GEBAEUDE_WIRTSCHAFT ist eine Liste von Dictionaries — GENAU wie
# GEBAEUDE_TYPEN in gebaeude.py. Beide Listen haben denselben Index:
#   Index 0 = Basis       (GEBAEUDE_TYPEN[0])
#   Index 1 = Reaktor     (GEBAEUDE_TYPEN[1])
#   Index 2 = Farm        (GEBAEUDE_TYPEN[2])
#   Index 3 = Holzfäller  (GEBAEUDE_TYPEN[3]) — NEU in Stunde 6
#   Index 4 = Steinmetz   (GEBAEUDE_TYPEN[4]) — NEU in Stunde 6
#
# Das ist wichtig: Wenn wir später neue Gebäude hinzufügen, müssen
# beide Listen erweitert werden — und die Indizes müssen zusammenpassen!
#
# Jedes Dictionary enthält:
#   "baukosten"      — Dictionary: was kostet der Bau?
#                      z.B. {"gold": 20} bedeutet: kostet 20 Gold
#   "produktion"     — Dictionary: was wird pro Sekunde produziert?
#                      z.B. {"energie": 5} bedeutet: +5 Energie/Sekunde
#   "verbrauch"      — Dictionary: was wird pro Sekunde verbraucht?
#                      z.B. {"holz": 2} bedeutet: −2 Holz/Sekunde
#   "max_anzahl"     — Wie oft kann man dieses Gebäude bauen?
#                      1 = nur einmal (Basis), None = unbegrenzt
# ═════════════════════════════════════════════════════════════════════════════

GEBAEUDE_WIRTSCHAFT = [
    # ── Index 0: Basis (das Hauptquartier) ────────────────────────────────
    # Die Basis ist kostenlos, produziert/verbraucht nichts.
    # Sie kann nur 1× pro Spiel gebaut werden (max_anzahl = 1).
    {
        "baukosten":  {},                      # Kostenlos!
        "produktion": {},                      # Produziert nichts
        "verbrauch":  {},                      # Verbraucht nichts
        "max_anzahl": 1,                       # Nur 1× baubar
    },
    # ── Index 1: Reaktor (Energieproduktion) ──────────────────────────────
    # Kostet 20 Gold, produziert +5 Energie, verbraucht −2 Holz.
    # Kann beliebig oft gebaut werden (max_anzahl = None).
    {
        "baukosten":  {"gold": 20},            # Baukosten
        "produktion": {"energie": 5},          # Produziert Energie
        "verbrauch":  {"holz": 2},             # Verbraucht Holz
        "max_anzahl": None,                    # Beliebig oft baubar
    },
    # ── Index 2: Farm (Geldproduktion) ────────────────────────────────────
    # Kostet 15 Gold + 10 Energie, produziert +8 Gold, verbraucht −3 Energie.
    # Kann beliebig oft gebaut werden (max_anzahl = None).
    {
        "baukosten":  {"gold": 15, "energie": 10},   # Baukosten
        "produktion": {"gold": 8},                    # Produziert Gold
        "verbrauch":  {"energie": 3},                 # Verbraucht Energie
        "max_anzahl": None,                           # Beliebig oft baubar
    },
    # ── Index 3: Holzfäller (Holzproduktion) — NEU in Stunde 6 ────────────
    # Kostet 10 Gold + 5 Energie, produziert +6 Holz, verbraucht −2 Energie.
    # Der Holzfäller liefert Holz — das brauchen wir für Reaktoren!
    {
        "baukosten":  {"gold": 10, "energie": 5},    # Baukosten
        "produktion": {"holz": 6},                    # Produziert Holz
        "verbrauch":  {"energie": 2},                 # Verbraucht Energie
        "max_anzahl": None,                           # Beliebig oft baubar
    },
    # ── Index 4: Steinmetz (Steinproduktion) — NEU in Stunde 6 ────────────
    # Kostet 15 Gold + 10 Energie, produziert +5 Stein, verbraucht −3 Energie.
    # Stein ist ein neuer Rohstoff — wird für spätere Gebäude wichtig!
    {
        "baukosten":  {"gold": 15, "energie": 10},   # Baukosten
        "produktion": {"stein": 5},                   # Produziert Stein
        "verbrauch":  {"energie": 3},                 # Verbraucht Energie
        "max_anzahl": None,                           # Beliebig oft baubar
    },
]


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: HILFSFUNKTION — Ressourcen prüfen
# ═════════════════════════════════════════════════════════════════════════════
# Diese kleine Hilfsfunktion prüft, ob in einem Dictionary (z.B. ressourcen)
# genug von einer bestimmten Ressource vorhanden ist.
#
# Beispiel: Hat der Spieler genug Gold?
#   hat_genug(ressourcen, "gold", 20) → True wenn ressourcen["gold"] >= 20
#
# Wichtig: Wenn eine Ressource im Dictionary nicht existiert, ist der Wert 0.
# Das verhindert KeyError-Abstürze!
# ═════════════════════════════════════════════════════════════════════════════

def _hat_genug(ressourcen_dict, ressourcen_name, benoetigte_menge):
    """
    Prüft ob von einer Ressource genug vorhanden ist.
    
    Diese Funktion ist "privat" (beginnt mit _) — sie wird NUR innerhalb
    dieses Moduls aufgerufen. Von aussen (aus main.py) sieht man sie nicht.
    
    Parameter:
        ressourcen_dict  — das Ressourcen-Dictionary (z.B. {"gold": 100, ...})
        ressourcen_name  — Name der Ressource (z.B. "gold")
        benoetigte_menge — wie viel wird benötigt? (z.B. 20)
    
    Rückgabe:
        True  — wenn genug vorhanden ist
        False — wenn nicht genug da ist (oder Ressource fehlt)
    """
    # get() holt den Wert oder 0 wenn nicht vorhanden — sicherer als []
    vorhanden = ressourcen_dict.get(ressourcen_name, 0)
    return vorhanden >= benoetigte_menge


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: kann_bauen() — Baukosten prüfen
# ═════════════════════════════════════════════════════════════════════════════
# Bevor ein Gebäude platziert wird, müssen wir prüfen:
#   1. Ist die Basis (Index 0) schon gebaut? → Basis nur 1× erlaubt!
#   2. Sind genug Ressourcen für die Baukosten da?
#
# Diese Funktion gibt True oder False zurück — ein klares Ja/Nein.
# In main.py wird dann entschieden: bei True → bauen, bei False → nichts tun.
# ═════════════════════════════════════════════════════════════════════════════

def kann_bauen(ressourcen_dict, liste_gebaeude, typ_index):
    """
    Prüft ob ein Gebäude gebaut werden kann.
    
    Zwei Prüfungen:
    1. Basis-Check (Index 0): Darf nur 1× gebaut werden!
    2. Ressourcen-Check: Sind genug Ressourcen für die Baukosten da?
    
    Parameter:
        ressourcen_dict  — das Ressourcen-Dictionary (z.B. {"gold": 100, ...})
        liste_gebaeude   — Liste aller bereits gebauten Gebäude
        typ_index        — welcher Gebäude-Typ soll gebaut werden?
                           (0=Basis, 1=Reaktor, 2=Farm, 3=Holzfaeller, 4=Steinmetz)
    
    Rückgabe:
        True  — Bauen ist möglich
        False — Bauen nicht möglich (Grund wird in der Konsole ausgegeben)
    """
    # ── Prüfung 1: Darf dieses Gebäude nur 1× gebaut werden? ────────────
    # Hol die Wirtschaftsdaten für diesen Gebäude-Typ
    wirtschaft = GEBAEUDE_WIRTSCHAFT[typ_index]
    max_anzahl = wirtschaft["max_anzahl"]
    
    # max_anzahl = 1 bedeutet: Dieses Gebäude darf nur 1× existieren
    if max_anzahl is not None:
        # Zählen wie viele Gebäude dieses Typs schon gebaut wurden
        anzahl_vorhanden = 0
        for gebaeude in liste_gebaeude:
            if gebaeude["typ"] == typ_index:
                anzahl_vorhanden = anzahl_vorhanden + 1
        
        # Wenn schon genug da sind → nicht bauen
        if anzahl_vorhanden >= max_anzahl:
            gebaeude_name = "Basis" if typ_index == 0 else "dieses Gebaeude"
            print(f"Kann {gebaeude_name} nur 1× bauen — bereits vorhanden!")
            return False
    
    # ── Prüfung 2: Sind genug Ressourcen für die Baukosten da? ──────────
    # Baukosten ist selbst ein Dictionary: z.B. {"gold": 20}
    baukosten = wirtschaft["baukosten"]
    
    # Gehe durch alle benötigten Ressourcen in den Baukosten
    for ress_name, benoetigt in baukosten.items():
        if not _hat_genug(ressourcen_dict, ress_name, benoetigt):
            # Gebaeude-Namen aus den Indizes ableiten (ohne Import aus gebaeude.py,
            # um Import-Zirkel zu vermeiden)
            gebaeude_namen = ["Basis", "Reaktor", "Farm", "Holzfaeller", "Steinmetz"]
            name = gebaeude_namen[typ_index] if typ_index < len(gebaeude_namen) else "Unbekannt"
            print(f"Nicht genug Ressourcen fuer {name}!"
                  f" Brauche {benoetigt} {ress_name}")
            return False
    
    # ── Beide Prüfungen bestanden → Bauen ist möglich ────────────────────
    return True


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: baukosten_abziehen() — Ressourcen verbrauchen
# ═════════════════════════════════════════════════════════════════════════════
# Nachdem kann_bauen() True zurückgegeben hat, rufen wir diese Funktion auf.
# Sie zieht die Baukosten von den Ressourcen ab.
#
# Wichtig: Diese Funktion darf NUR aufgerufen werden wenn vorher
# kann_bauen() True war! Sonst könnte der Spieler Schulden machen.
# ═════════════════════════════════════════════════════════════════════════════

def baukosten_abziehen(ressourcen_dict, typ_index):
    """
    Zieht die Baukosten eines Gebäudes von den Ressourcen ab.
    
    Diese Funktion verändert das ressourcen_dict direkt (global).
    
    Wichtig: Nur aufrufen NACHDEM kann_bauen() True war!
    
    Parameter:
        ressourcen_dict  — das Ressourcen-Dictionary (wird verändert!)
        typ_index        — welcher Gebäude-Typ wird gebaut?
                          (0=Basis, 1=Reaktor, 2=Farm, 3=Holzfaeller, 4=Steinmetz)
    """
    wirtschaft = GEBAEUDE_WIRTSCHAFT[typ_index]
    baukosten = wirtschaft["baukosten"]
    
    # Gebaeude-Namen aus den Indizes ableiten (ohne Import aus gebaeude.py)
    gebaeude_namen = ["Basis", "Reaktor", "Farm", "Holzfaeller", "Steinmetz"]
    name = gebaeude_namen[typ_index] if typ_index < len(gebaeude_namen) else "Unbekannt"
    
    # Gehe durch alle benötigten Ressourcen und ziehe sie ab
    for ress_name, kosten in baukosten.items():
        aktueller_wert = ressourcen_dict.get(ress_name, 0)
        neuer_wert = aktueller_wert - kosten
        ressourcen_dict[ress_name] = neuer_wert
        
        # Kurze Konsolenausgabe zum Testen — zeigt was abgezogen wurde
        print(f"Baue {name}: -{kosten} {ress_name} (neu: {neuer_wert})")


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: ressourcen_produzieren() — Tick-System
# ═════════════════════════════════════════════════════════════════════════════
# Diese Funktion wird 1× pro Sekunde aufgerufen (nicht jeden Frame!).
# Sie geht durch alle Gebäude und wendet Produktion/Verbrauch an.
#
# Wichtige Regel: Ressourcen dürfen NIEMALS unter 0 fallen!
# Wenn der nötige Rohstoff fehlt (z.B. kein Holz für den Reaktor),
# produziert das Gebäude in DIESEM Tick einfach nichts.
# Das Gebäude "schläft" dann — es arbeitet erst wieder wenn
# genug Rohstoffe da sind.
#
# Neu in Stunde 6: Die Funktion arbeitet automatisch mit allen 5 Gebäudetypen,
# weil sie einfach durch alle Gebäude in liste_gebaeude iteriert.
# Man muss nichts umbauen — neue Indizes funktionieren sofort!
# ═════════════════════════════════════════════════════════════════════════════

def ressourcen_produzieren(ressourcen_dict, liste_gebaeude):
    """
    Wendet Produktion und Verbrauch für ALLE Gebäude an.
    
    Diese Funktion wird 1× pro Sekunde (alle 60 Frames) aufgerufen.
    
    So funktioniert ein Tick:
    1. Für jedes Gebäude in liste_gebaeude:
       a. Prüfen: Reichen die Ressourcen für den Verbrauch?
       b. Wenn ja: Verbrauch abziehen + Produktion hinzufügen
       c. Wenn nein: Gebäude produziert NICHTS in diesem Tick
    
    Wichtig: Ressourcenwerte dürfen nie negativ werden!
    
    Parameter:
        ressourcen_dict  — das Ressourcen-Dictionary (wird verändert!)
        liste_gebaeude   — Liste aller Gebäude auf der Karte
    """
    for gebaeude in liste_gebaeude:
        typ_index = gebaeude["typ"]
        wirtschaft = GEBAEUDE_WIRTSCHAFT[typ_index]
        
        # ── Schritt 1: Kann das Gebäude produzieren? ─────────────────────
        # Prüfe ob genug Ressourcen für den Verbrauch da sind.
        # Wenn z.B. der Reaktor 2 Holz braucht, aber nur 1 da ist →
        # dann kann er nicht produzieren.
        
        verbrauch = wirtschaft["verbrauch"]
        kann_produzieren = True
        
        for ress_name, menge in verbrauch.items():
            if not _hat_genug(ressourcen_dict, ress_name, menge):
                kann_produzieren = False
                break   # Sobald eine Ressource fehlt → abbrechen
        
        # ── Schritt 2: Wenn genug Ressourcen → produzieren ──────────────
        if kann_produzieren:
            # Zuerst: Verbrauchte Ressourcen abziehen
            for ress_name, menge in verbrauch.items():
                aktuell = ressourcen_dict.get(ress_name, 0)
                ressourcen_dict[ress_name] = aktuell - menge
                # Sicherheitscheck: Niemals unter 0!
                if ressourcen_dict[ress_name] < 0:
                    ressourcen_dict[ress_name] = 0
            
            # Dann: Produzierte Ressourcen hinzufügen
            produktion = wirtschaft["produktion"]
            for ress_name, menge in produktion.items():
                aktuell = ressourcen_dict.get(ress_name, 0)
                ressourcen_dict[ress_name] = aktuell + menge
        
        else:
            # Gebäude kann nicht produzieren — Grund ausgeben
            # Wir brauchen den Namen aus gebaeude.py... aber wir importieren
            # gebaeude.py hier NICHT (sonst gäbe es einen Import-Zirkel).
            # Stattdessen geben wir nur den Index aus — das reicht zum Testen.
            gebaeude_namen = ["Basis", "Reaktor", "Farm", "Holzfaeller", "Steinmetz"]
            name = gebaeude_namen[typ_index] if typ_index < len(gebaeude_namen) else "Unbekannt"
            print(f"{name} (Typ {typ_index}): Nicht genug Rohstoffe "
                  f"→ produziert nichts in diesem Tick")