import argparse

import time
from datetime import datetime

from ortools.sat.python.cp_model import UNKNOWN, MODEL_INVALID, INFEASIBLE, OPTIMAL, FEASIBLE
from ortools.sat.python import cp_model

import Aufbereitung
from Maps import *
from Constraints import *
from Plan import Plan
from Validierung import *

# Strafen für die Optimierungsfunktion
VIERTER_SLOT_STRAFE = 10
DRITTER_SLOT_STRAFE = 1
# Maximale Suchzeit
MAX_ZEIT = 5.0
# Bezeichnungen für den Plan
uniName = "TH-Lübeck"
fachbereichName = "Elektrotechnik_Informatik"
semesterName = "SoSe-2021"


def main():
    orm = ORM
    model = cp_model.CpModel()

    # Hard Constraints
    erzeugeZeitRaumAufsichtVar(model, orm)
    erzeugeZeitVars(model, orm)
    unterschiedlicheRaumVars(model, orm)
    unterschiedlicheAufsichtVars(model, orm)
    definiereRaumAnzahlVar(model, orm)
    raumAufsichtVarConstraint(model, orm)
    aufsichtZeitConstraint(model, orm)
    raumZeitConstraint(model, orm)
    raumAuslastungenConstraint(model, orm)
    raumAnzahlVerwaltung(model, orm)
    raumAuslastungenDummyConstraint(model, orm)
    raumGroesseConstraint(model, orm)
    prüfungenEinerSemesterGruppeConstraint(model, orm)
    pruefungenStudiengangsConstraint(model, orm)
    einePrüfungProTagSemesterGruppeConstraint(model, orm)
    aufsichtNichtVerfuegbarConstraint(model, orm)
    raumNichtVerfuegbarConstraint(model, orm)

    # Constraints für die Einführung von zusammengelegten Klausuren
    # raumGroeßeZsmPruefungConstraint(model, orm)
    # raumZeitConstraintnew(model, orm)
    # aufsichtZeitConstraintnew(model, orm)
    # raumGroeßeZsmPruefungConstraint(model, orm)

    # Möglichst wenig Räume verteilt = viele Dummyräume

    # Möglichst wenig Räume vergeben,späteZeitSlots 3 und 4 vermeiden, Wunschtermine
    summanden = raumOptimierung(model, ORM), spaeteZeitSlots(model, ORM, 4, VIERTER_SLOT_STRAFE), \
                spaeteZeitSlots(model, ORM, 3,DRITTER_SLOT_STRAFE), beachteWunschTermine(model, ORM)

    # Minimierung der Summe der Ausdrücke
    model.Minimize(sum(summanden))

    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 4
    solver.parameters.max_time_in_seconds = MAX_ZEIT
    print("Suche Läuft...")
    status = solver.Solve(model)

    if (status == OPTIMAL or status == FEASIBLE):
        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        print("STOP =", current_time)
        for raum in orm.getRaeume():
            print("Raum ID %i Größe %i" % (raum.id, raum.groesse))

        for pruefung in orm.getPruefungen():
            print(pruefung)
            print("ZeitSlot Nummer %s" % (solver.Value(pruefung.zeitVar)))
            print("belegte Räume %s" % (solver.Value(pruefung.raumAnzahl)))
            for r in range(len(pruefung.raumVars)):
                if (solver.Value(pruefung.raumVars[r]) != 0):
                    print("Raum Nummer %s" % solver.Value(pruefung.raumVars[r]))
                    print("Raum Auslastung %s" % solver.Value(pruefung.raumAuslastungVars[r]))
            for a in range(len(pruefung.aufsichtVars)):
                if (solver.Value(pruefung.aufsichtVars[a]) != 0):
                    print("Aufsicht Nummer %s" % solver.Value(pruefung.aufsichtVars[a]))

        # Export

        # Maps zum Speichern von IntVars
        zeitSlotMap = createZeitSlotMap(orm.getZeitSlots())
        aufsichtMap = createAufsichtMap(orm.getAufsichten())

        raumMap = createRaumMap(orm.getRaeume())
        plan = Plan(orm)
        time.sleep(0.5)
        for pruefung in orm.getPruefungen():
            for rVar in pruefung.raumVars:
                for aVar in pruefung.aufsichtVars:
                    if (solver.Value(rVar) != 0 and solver.Value(aVar) != 0):
                        plan.addPruefung(pruefung, raumMap[solver.Value(rVar)],
                                         aufsichtMap[solver.Value(aVar)],
                                         zeitSlotMap[solver.Value(pruefung.zeitVar)])

        if(validierePlan(plan)):
            print("Der Plan ist gültig!")
        Aufbereitung.writeTimeTableExcelFile(plan, uniName, fachbereichName, semesterName, orm)

    if status == INFEASIBLE:
        print("\nkeine Lösung möglich!")
    elif status == UNKNOWN:
        print("\nBisher keine Lösung gefunden.")
    elif status == MODEL_INVALID:
        print("\nError. Daten führten zu einem ungültigen CpModel.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-u', '--uni', metavar='NAME', type=str, default=uniName,
                        help='Setzt Namen für den zu exportierenden Plan.')

    parser.add_argument('-f', '--fachbereich', metavar='NAME', type=str, default=fachbereichName,
                        help='Name des Fachbereichs für den Plan.')

    parser.add_argument('-s', '--semester', metavar='NAME', type=str, default=semesterName,
                        help='Senester für die Erstellung des Plans.')
    args = parser.parse_args()
    params = vars(args)
    semesterName = params['semester']
    departmentName = params['fachbereich']
    uniName = params['uni']

    ORM.init()
    main()
