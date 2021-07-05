from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import OPTIMAL, FEASIBLE

import ORM
from BeispielDaten import neuePrüfung
from Raum import Raum
def main():
    A = {'0', '0', '1', '2'}
    B = {'0'}

    print(A - B)

    print(B - A)
    Raum1 = Raum(name="AM2", groesse="60")
    Raum2 = Raum(name="AM1", groesse="80")
    Raeume = [Raum1,Raum2]
    Pruefung1 = neuePrüfung("Ma1", "SB112", 30)
    Pruefung2 = neuePrüfung("Inf1", "SB122", 40)
    Pruefung3 = neuePrüfung("Inf2", "SB122", 40)
    Prüfungen = [Pruefung1,Pruefung2, Pruefung3]
    orm = ORM
    model = cp_model.CpModel()
    for pruefung in Prüfungen:
        pruefung.raumVar = model.NewIntVar(1,len(Raeume),"RaumVar")
        pruefung.zeitVar = model.NewIntVar(1,2,"ZeitVar")
        pruefung.aufsichtVar = model.NewIntVar(1, 2, "aufsichtVar")
    #Raum Constraint
    for i in range(len(Prüfungen)):
        for j in range(i + 1, len(Prüfungen)):
            pruef_i, pruef_j = Prüfungen[i], Prüfungen[j]
            ungleicheZeit = model.NewBoolVar("")
            model.Add(pruef_i.zeitVar == pruef_j.zeitVar).OnlyEnforceIf(ungleicheZeit)
            model.Add(pruef_i.zeitVar != pruef_j.zeitVar).OnlyEnforceIf(ungleicheZeit.Not())
            model.Add(pruef_i.raumVar != pruef_j.raumVar).OnlyEnforceIf(ungleicheZeit)

    #AufsichtRaum Constraint


    for r in range(len(Prüfungen)):
        for s in range(r + 1, len(Prüfungen)):
            pruef_r, pruef_s = Prüfungen[r], Prüfungen[s]
            # Wenn Sie gleichzeitig stattfinden
            gleicheZeit = model.NewBoolVar("")
            model.Add(pruef_r.zeitVar == pruef_s.zeitVar).OnlyEnforceIf(gleicheZeit)
            model.Add(pruef_r.zeitVar != pruef_s.zeitVar).OnlyEnforceIf(gleicheZeit.Not())
            # Boolean ob die Klausuren im gleichen Raum sind
            gleicheAufsicht = model.NewBoolVar("")
            model.Add(pruef_r.aufsichtVar == pruef_s.aufsichtVar).OnlyEnforceIf(gleicheAufsicht)
            model.Add(pruef_r.aufsichtVar != pruef_s.aufsichtVar).OnlyEnforceIf(gleicheAufsicht.Not())
            # Wenn Aufsicht gleich, dann muss raum auch gleich sein
            gleicheZeitGleicheAufsicht = model.NewBoolVar("")
            model.Add(gleicheZeit == gleicheAufsicht == True).OnlyEnforceIf(gleicheZeitGleicheAufsicht)

            model.Add(pruef_r.raumVar == pruef_s.raumVar).OnlyEnforceIf(gleicheZeitGleicheAufsicht)

    solver = cp_model.CpSolver()
    solver.Solve(model)
    status = solver.Solve(model)
    if (status == OPTIMAL or status == FEASIBLE):
        x = 0
        for pruefung in Prüfungen:
                x += 1
                print("\n Prüfung %i" % (x))
                print("Zeit " + str(solver.Value(pruefung.zeitVar)))
                print("Raum "+ str(solver.Value(pruefung.raumVar)))
                print("Aufsicht " + str(solver.Value(pruefung.aufsichtVar)))

if __name__ == '__main__':

    ORM.init()
    main()