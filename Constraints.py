import ORM
from ortools.sat.python.cp_model import CpModel
from ORM import ZEITSLOTS_PRO_TAG, PRUEFUNGSTAGE

RAUMSTRAFE = 10
WUNSCHSTRAFE = 3
"""
Klasse zur Erstellung der benötigten Variablen und Constraints für das CpModel.
Jede Methode bekommt das CpModel und eine Referenz ORM

"""


def erzeugeZeitRaumAufsichtVar(model: CpModel, orm: ORM):
    """
    Methode zur Generierung benötigten Raum- und ZeitVars.
    :param model: Model zum Lösen mittels Google OR Tools
    :param orm: ORM für das Handling der Datenbankeinträgen
    :return:
    """

    # für alle Prüfungen die verteilt werden sollen
    for pruefung in orm.getPruefungen():
        # Erzeugung raumvar für jede Prüfung
        pruefung.raumAnzahl = model.NewIntVar(1, 6, "Prüfung_raumAnzahl")
        pruefung.raumVars = []
        pruefung.raumAuslastungVars = []
        pruefung.aufsichtVars = []
        for i in range(6):
            pruefung.raumVars.append(model.NewIntVar(0, len(orm.getRaeume()), "raumVar"))
            pruefung.aufsichtVars.append(model.NewIntVar(0, len(orm.getAufsichten()), "aufsichtVar"))
            pruefung.raumAuslastungVars.append(model.NewIntVar(0, 200, "AuslastungsVar"))
        pruefung.zeitVar = model.NewIntVar(1, (PRUEFUNGSTAGE * ZEITSLOTS_PRO_TAG), "ZeitVar")


def raumAnzahlVerwaltung(model: CpModel, orm: ORM):
    """
    maximale RaumAnzahl im Zusammenhang mit der Teilnehmerzahl
    :param model: CpModel
    :param orm: ORM
    :return:
    """
    for p in orm.getPruefungen():
        bools = []
        bools.append(True)
        bool1 = model.NewBoolVar("größer")
        model.Add(p.teilnehmerzahl <= 40).OnlyEnforceIf(bool1.Not())
        model.Add(p.teilnehmerzahl > 40).OnlyEnforceIf(bool1)
        bools.append(bool1)
        bool1 = model.NewBoolVar("größer")
        model.Add(p.teilnehmerzahl <= 100).OnlyEnforceIf(bool1.Not())
        model.Add(p.teilnehmerzahl > 100).OnlyEnforceIf(bool1)
        bools.append(bool1)
        bools.append(bool1)
        bool1 = model.NewBoolVar("größer")
        model.Add(p.teilnehmerzahl <= 200).OnlyEnforceIf(bool1.Not())
        model.Add(p.teilnehmerzahl > 200).OnlyEnforceIf(bool1)
        bools.append(bool1)
        bools.append(bool1)
        model.Add(p.raumAnzahl <= sum(bools))


def definiereRaumAnzahlVar(model: CpModel, orm: ORM):
    """
    Methode zur Belegung der Raumanzahl. Zählt alle raumVars einer Prüfung ungleich 0
    :param model:  Model
    :param orm: ORM
    :return:
    """

    for p in orm.getPruefungen():
        bools = []
        for i in range(len(p.raumVars)):
            boole = model.NewBoolVar("nicht0")
            model.Add(p.raumVars[i] != 0).OnlyEnforceIf(boole)
            model.Add(p.raumVars[i] == 0).OnlyEnforceIf(boole.Not())
            bools.append(boole)
        model.Add(p.raumAnzahl == sum(bools))

#Methode zur maximalen Auslastungen von Räumen, gegebenenfalls wichtig für die Zusammenlegung
#def maxAuslastungOptimierung(model: CpModel, orm: ORM):
#
#    bool = []
#    variable = model.NewIntVar(0, 1000, "")
#    for p in orm.getPruefungen():
#        for r in orm.getRaeume():
#            for i in range(len(p.raumVars)):
#                verbucht = model.NewBoolVar("verbucht")
#                nichtvoll = model.NewBoolVar("voll")
#                model.Add(p.raumVars[i] == r.id).OnlyEnforceIf(verbucht)
#                model.Add(p.raumVars[i] != r.id).OnlyEnforceIf(verbucht.Not())
#                model.Add(p.raumAuslastungVars[i] < r.groesse).OnlyEnforceIf(nichtvoll)
#                model.Add(p.raumAuslastungVars[i] == r.groesse).OnlyEnforceIf(nichtvoll.Not())
#                model.Add(nichtvoll == False).OnlyEnforceIf(verbucht.Not())
#                bool.append(nichtvoll)
#
#    model.Add(variable == sum(bool))
#    return variable


def raumAuslastungenConstraint(model: CpModel, orm: ORM):
    """
    Methode zur Belegung der Raumauslastunge. Diese ist kleiner als Faktor * Raumgröße
    :param model:  Model
    :param orm: ORM
    :param faktor: Zwischen 0 und 1 wie viel Prozent der Raumgröße genutzt werden kann
    :return:
    """
    for p in orm.getPruefungen():
        for r in orm.getRaeume():
            for i in range(len(p.raumVars)):
                verbucht = model.NewBoolVar("verbucht")
                model.Add(p.raumVars[i] == r.id).OnlyEnforceIf(verbucht)
                model.Add(p.raumVars[i] != r.id).OnlyEnforceIf(verbucht.Not())
                model.Add(p.raumAuslastungVars[i] <= r.groesse).OnlyEnforceIf(verbucht)


def raumAuslastungenDummyConstraint(model: CpModel, orm: ORM):
    """
    Auslastung bei Dummyräumen == 0
    :param model: CpModel
    :param orm: ORM
    :return:
    """
    for p in orm.getPruefungen():
        for i in range(len(p.raumVars)):
            verbucht = model.NewBoolVar("verbucht")
            model.Add(p.raumVars[i] == 0).OnlyEnforceIf(verbucht)
            model.Add(p.raumVars[i] != 0).OnlyEnforceIf(verbucht.Not())
            model.Add(p.raumAuslastungVars[i] == 0).OnlyEnforceIf(verbucht)
            model.Add(p.raumAuslastungVars[i] != 0).OnlyEnforceIf(verbucht.Not())


def unterschiedlicheRaumVars(model: CpModel, orm: ORM):
    """
    Alle RaumVars ungleich 0 einer Prüfung müssen verschieden sein
    :param model: CpModel
    :param orm: ORM
    :return:
    """
    for p in orm.getPruefungen():
        for i in range(len(p.raumVars)):
            for j in range(i + 1, len(p.raumVars)):
                bool = model.NewBoolVar("nicht0")
                model.Add(p.raumVars[i] != 0).OnlyEnforceIf(bool)
                model.Add(p.raumVars[i] == 0).OnlyEnforceIf(bool.Not())
                model.Add(p.raumVars[i] != p.raumVars[j]).OnlyEnforceIf(bool)


def unterschiedlicheAufsichtVars(model: CpModel, orm: ORM):
    """
    Alle AufsichtVars ungleich 0 einer Prüfung müssen verschieden sein
    :param model: CpModel
    :param orm: ORM
    :return:
    """
    for p in orm.getPruefungen():
        for i in range(len(p.aufsichtVars)):
            for j in range(i + 1, len(p.aufsichtVars)):
                bool = model.NewBoolVar("nicht0")
                model.Add(p.aufsichtVars[i] != 0).OnlyEnforceIf(bool)
                model.Add(p.aufsichtVars[i] == 0).OnlyEnforceIf(bool.Not())
                model.Add(p.aufsichtVars[i] != p.aufsichtVars[j]).OnlyEnforceIf(bool)


def raumAufsichtVarConstraint(model: CpModel, orm: ORM):
    """
    Raum/AufsichtVar Beziehung  Dummy Raum 0 -> Dummy Aufsicht 0
    Echter Raum -> Echte Aufsicht vergeben
    :param model:
    :param orm:
    :return:
    """
    for p in orm.getPruefungen():
        for i in range(len(p.raumVars)):
            bool = model.NewBoolVar("nicht0")
            model.Add(p.raumVars[i] != 0).OnlyEnforceIf(bool)
            model.Add(p.raumVars[i] == 0).OnlyEnforceIf(bool.Not())
            model.Add(p.aufsichtVars[i] != 0).OnlyEnforceIf(bool)
            model.Add(p.aufsichtVars[i] == 0).OnlyEnforceIf(bool.Not())


def raumOptimierung(model: CpModel, orm: ORM):
    """
    Optimierung der Raumanzahl, Durch Summe aller belegten Räume pro Prüfung
    :param model:
    :param orm:
    :return: Ausdruck zur Optimierung durch das Model/Solver
    """
    belegteRaeume = model.NewConstant(0)

    for pruefung in orm.getPruefungen():
        belegteRaeume += pruefung.raumAnzahl

    return belegteRaeume * RAUMSTRAFE


def erzeugeZeitVars(model: CpModel, orm: ORM):
    """
    Methode zur Generierung benötigten Raum- und ZeitVars.
    :param model: Model zum Lösen mittels Google OR Tools
    :param orm: ORM für das Handling der Datenbankeinträgen
    :return:
    """
    for pruefung in orm.getPruefungen():
        if not (hasattr(pruefung, "tagVar")
                and hasattr(pruefung, "slotVar")
        ):
            # Tag an dem eine Prüfung stattfindet
            pruefung.tagVar = model.NewIntVar(1, PRUEFUNGSTAGE, "")
            # SlotNummer des Slots am Prüfungstag
            pruefung.slotVar = model.NewIntVar(1, ZEITSLOTS_PRO_TAG, "")
            # Beziehung zwischen tagVar, slotVar und zeitVar  übernommen aus TimeTabling Projekt von Jonas Huber
            model.Add(pruefung.zeitVar ==
                      (pruefung.tagVar - 1) * ZEITSLOTS_PRO_TAG + pruefung.slotVar)


def raumGroesseConstraint(model: CpModel, orm: ORM):
    """
    Sichert zu das Prüfungen nur in Räumen stattfinden die groß genug sind
    :param model: Model zum Lösen mittels Google OR Tools
    :param orm: ORM für das Handling der Datenbankeinträgen
    :return:
    """
    for pruefung in orm.getPruefungen():
        sum = model.NewConstant(0)

        for r in range(len(pruefung.raumAuslastungVars)):
            intVar = model.NewIntVar(0, 400, "")
            model.Add(intVar == pruefung.raumAuslastungVars[r])
            sum += intVar

        model.Add(sum == pruefung.teilnehmerzahl)


#def raumGroeßeZsmPruefungConstraint(model: CpModel, orm: ORM):
#     for i in range(len(orm.getPruefungen())):
#        pImSelbenRaum = []
#       for j in range(i + 1, len(orm.getPruefungen())):
#           bools = []
#           pruef_i, pruef_j = orm.getPruefungen()[i], orm.getPruefungen()[j]
#           # Wenn Sie gleichzeitig stattfinden
#            gleicheZeit = model.NewBoolVar("")
#            model.Add(pruef_i.zeitVar == pruef_j.zeitVar).OnlyEnforceIf(gleicheZeit)
#            model.Add(pruef_i.zeitVar != pruef_j.zeitVar).OnlyEnforceIf(gleicheZeit.Not())
#            bools.append(gleicheZeit)
#            for raum in orm.getRaeume():
#                for r1 in range(len(pruef_i.raumVars)):
#                    for r2 in range(len(pruef_j.raumVars)):
#                        gleicherRaum = model.NewBoolVar("")
#                        model.Add(pruef_i.raumVars[r1] == pruef_j.raumVars[r2]).OnlyEnforceIf(gleicherRaum)
#                        model.Add(pruef_i.raumVars[r1] != pruef_j.raumVars[r2]).OnlyEnforceIf(gleicherRaum.Not())
#                        bools.append(gleicherRaum)
#                        konkreterRaum = model.NewBoolVar("")
#                       model.Add(pruef_i.raumVars[r1] == raum.id).OnlyEnforceIf(konkreterRaum)
#                        model.Add(pruef_i.raumVars[r1] != raum.id).OnlyEnforceIf(konkreterRaum.Not())
#                        bools.append(konkreterRaum)

#                        bool = model.NewBoolVar("")
#                        model.Add(sum(bools) == 3).OnlyEnforceIf(bool)
#                        model.Add(sum(bools) != 3).OnlyEnforceIf(bool.Not())
#                        model.Add(pruef_i.teilnehmerzahl + pruef_j.teilnehmerzahl < raum.groesse).OnlyEnforceIf(bool)

#Methode zur Anpassung der Zusammenlegung
#def aufsichtZeitConstraintnew(model: CpModel, orm: ORM):
#    """
#    Aufsicht Zeit Constraint Gleiche ZeitVar && GleicherRaum -> gleicheAufsicht
#    :param model:
#    :param orm:
#    :return:
#    """
#    # Für alle Paare aus i und j aus Prüfungen
#    for i in range(len(orm.getPruefungen())):
#        pImSelbenRaum = []
#        for j in range(i + 1, len(orm.getPruefungen())):
#            bools = []
#            pruef_i, pruef_j = orm.getPruefungen()[i], orm.getPruefungen()[j]
#            # Wenn Sie gleichzeitig stattfinden
#            gleicheZeit = model.NewBoolVar("")
#            model.Add(pruef_i.zeitVar == pruef_j.zeitVar).OnlyEnforceIf(gleicheZeit)
#            model.Add(pruef_i.zeitVar != pruef_j.zeitVar).OnlyEnforceIf(gleicheZeit.Not())
#            bools.append(gleicheZeit)
#            for r1 in range(len(pruef_i.raumVars)):
#                for r2 in range(len(pruef_j.raumVars)):
#                    gleicherRaum = model.NewBoolVar("")
#                    model.Add(pruef_i.raumVars[r1] == pruef_j.raumVars[r2]).OnlyEnforceIf(gleicherRaum)
#                    model.Add(pruef_i.raumVars[r1] != pruef_j.raumVars[r2]).OnlyEnforceIf(gleicherRaum.Not())
#                    bools.append(gleicherRaum)
#                    bool = model.NewBoolVar("")
#                    model.Add(sum(bools) == 2).OnlyEnforceIf(bool)
#                    model.Add(sum(bools) != 2).OnlyEnforceIf(bool.Not())
#                    model.Add(pruef_i.aufsichtsVars[r1] == pruef_j.aufsichtsVars[r2]).OnlyEnforceIf(bool)
#                    pImSelbenRaum.append(bool)
#                    del bools[-1]
#        # Nicht mehr als 1 weitere Prüfung im selben Raum
#        model.Add(sum(pImSelbenRaum) <= 1)


def aufsichtZeitConstraint(model: CpModel, orm: ORM):
    """
    Aufsicht Zeit Constraint(alt) Gleiche ZeitVar -> Aufsichten verschieden
    :param model:
    :param orm:
    :return:
    """
    # Für alle Paare aus i und j aus Prüfungen
    for i in range(len(orm.getPruefungen())):
        for j in range(i + 1, len(orm.getPruefungen())):
            pruef_i, pruef_j = orm.getPruefungen()[i], orm.getPruefungen()[j]

            bools = []
            gleicheZeit = model.NewBoolVar("")
            model.Add(pruef_i.zeitVar == pruef_j.zeitVar).OnlyEnforceIf(gleicheZeit)
            model.Add(pruef_i.zeitVar != pruef_j.zeitVar).OnlyEnforceIf(gleicheZeit.Not())
            bools.append(gleicheZeit)

            for r1 in range(len(pruef_i.aufsichtVars)):
                keinDummyRaum = model.NewBoolVar("bool")
                model.Add(pruef_i.aufsichtVars[r1] != 0).OnlyEnforceIf(keinDummyRaum)
                model.Add(pruef_i.aufsichtVars[r1] == 0).OnlyEnforceIf(keinDummyRaum.Not())
                bools.append(keinDummyRaum)
                richtigerRaum = model.NewBoolVar("")
                model.Add(sum(bools) == 2).OnlyEnforceIf(richtigerRaum)
                model.Add(sum(bools) != 2).OnlyEnforceIf(richtigerRaum.Not())
                for r2 in range(len(pruef_j.aufsichtVars)):
                    model.Add(pruef_i.aufsichtVars[r1] != pruef_j.aufsichtVars[r2]).OnlyEnforceIf(richtigerRaum)
                del bools[-1]


def raumZeitConstraint(model: CpModel, orm: ORM):
    """
    Aufsicht Zeit Constraint(alt) Gleiche ZeitVar -> RaumVars verschieden
    :param model: CpModel
    :param orm: ORM
    :return:
    """
    # Für alle Paare aus i und j aus Prüfungen
    for i in range(len(orm.getPruefungen())):
        for j in range(i + 1, len(orm.getPruefungen())):
            pruef_i, pruef_j = orm.getPruefungen()[i], orm.getPruefungen()[j]

            bools = []
            gleicheZeit = model.NewBoolVar("")
            model.Add(pruef_i.zeitVar == pruef_j.zeitVar).OnlyEnforceIf(gleicheZeit)
            model.Add(pruef_i.zeitVar != pruef_j.zeitVar).OnlyEnforceIf(gleicheZeit.Not())
            bools.append(gleicheZeit)

            for r1 in range(len(pruef_i.raumVars)):
                keinDummyRaum = model.NewBoolVar("bool")
                model.Add(pruef_i.raumVars[r1] != 0).OnlyEnforceIf(keinDummyRaum)
                model.Add(pruef_i.raumVars[r1] == 0).OnlyEnforceIf(keinDummyRaum.Not())
                bools.append(keinDummyRaum)
                richtigerRaum = model.NewBoolVar("")
                model.Add(sum(bools) == 2).OnlyEnforceIf(richtigerRaum)
                model.Add(sum(bools) != 2).OnlyEnforceIf(richtigerRaum.Not())
                for r2 in range(len(pruef_j.raumVars)):
                    model.Add(pruef_i.raumVars[r1] != pruef_j.raumVars[r2]).OnlyEnforceIf(richtigerRaum)
                del bools[-1]

#RaumZeitConstraint für die Zusammenlegung gedacht
#def raumZeitConstraintnew(model: CpModel, orm: ORM):
#    """
#    Raum Zeit Constraint Gleiche ZeitVar && GleicheAufsicht -> gleicherRaum
#    :param model:
#    :param orm:
#    :return:
#    """
#    # Für alle Paare aus i und j aus Prüfungen
#    for i in range(len(orm.getPruefungen())):
#        for j in range(i + 1, len(orm.getPruefungen())):
#            bools = []
#            pruef_i, pruef_j = orm.getPruefungen()[i], orm.getPruefungen()[j]
#            # Wenn Sie gleichzeitig stattfinden
#            gleicheZeit = model.NewBoolVar("")
#            model.Add(pruef_i.zeitVar == pruef_j.zeitVar).OnlyEnforceIf(gleicheZeit)
#            model.Add(pruef_i.zeitVar != pruef_j.zeitVar).OnlyEnforceIf(gleicheZeit.Not())
#            bools.append(gleicheZeit)
#            for r1 in range(len(pruef_i.aufsichtVars)):
#                for r2 in range(len(pruef_j.aufsichtVars)):
#                    gleicheAufsicht = model.NewBoolVar("")
#                    model.Add(pruef_i.aufsichtVars[r1] == pruef_j.aufsichtVars[r2]).OnlyEnforceIf(gleicheAufsicht)
#                    model.Add(pruef_i.aufsichtVars[r1] != pruef_j.aufsichtVars[r2]).OnlyEnforceIf(gleicheAufsicht.Not())
#                    bools.append(gleicheAufsicht)
#                    bool = model.NewBoolVar("")
#                    model.Add(sum(bools) == 2).OnlyEnforceIf(bool)
#                    model.Add(sum(bools) != 2).OnlyEnforceIf(bool.Not())
#                    model.Add(pruef_i.raumVars[r1] == pruef_j.raumVars[r2]).OnlyEnforceIf(bool)
#                    del bools[-1]


def raumNichtVerfuegbarConstraint(model: CpModel, orm: ORM):
    """
    Dieses Constraint sichert zu, dass ein Raum der zu einem ZeitSlot anderweitig vergeben ist,
    nicht verplant werden kann.
    :param model: Model zum Lösen mittels Google OR Tools
    :param orm: ORM für das Handling der Datenbankeinträgen
    :return:
    """
    # Für alle Räume in der Menge aller Räume
    for raum in orm.getRaeume():
        # Wenn Liste für die verplanten ZeitSlots nicht leer ist
        for ZeitSlot in raum.nicht_verfuegbare_zeitslots:
            for pruefung in orm.getPruefungen():
                for r in range(len(pruefung.raumVars)):
                    verbucht = model.NewBoolVar("")
                    model.Add(pruefung.raumVars[r] == raum.id).OnlyEnforceIf(verbucht)
                    model.Add(pruefung.raumVars[r] != raum.id).OnlyEnforceIf(verbucht.Not())
                    model.Add(pruefung.zeitVar != ZeitSlot.id).OnlyEnforceIf(verbucht)


def aufsichtNichtVerfuegbarConstraint(model: CpModel, orm: ORM):
    for aufsicht in orm.getAufsichten():
        for ZeitSlot in aufsicht.nicht_verfuegbare_aufsicht_zeitslots:
            for pruefung in orm.getPruefungen():
                for a in range(len(pruefung.aufsichtVars)):
                    verbucht = model.NewBoolVar("")
                    model.Add(pruefung.aufsichtVars[a] == aufsicht.id).OnlyEnforceIf(verbucht)
                    model.Add(pruefung.aufsichtVars[a] != aufsicht.id).OnlyEnforceIf(verbucht.Not())
                    model.Add(pruefung.zeitVar != ZeitSlot.id).OnlyEnforceIf(verbucht)


def prüfungenEinerSemesterGruppeConstraint(model: CpModel, orm: ORM):
    """
    Dieses Constraint sichert zu, dass eine SemesterGruppe nur eine Prüfung gleichzeitig ablegen kann.
    Dazu müssen die ZeitVars aller Prüfungen, die zu einer Semestergruppe gehören, unterschiedlich sein.
    :param model: Model zum Lösen mittels Google OR Tools
    :param orm: ORM für das Handling der Datenbankeinträgen
    :return:
    """

    for semestergruppe in orm.getSemesterGruppen():
        for i in range(len(semestergruppe.getPruefungen())):
            for j in range(i + 1, len(semestergruppe.getPruefungen())):
                pruef_i, pruef_j = semestergruppe.getPruefungen()[i], semestergruppe.getPruefungen()[j]
                model.AddAllDifferent([pruef_i.zeitVar, pruef_j.zeitVar])


def pruefungenStudiengangsConstraint(model: CpModel, orm: ORM):
    """
    Dieses Constraint sichert zu, dass Prüfungen eines Studiengangs nicht gleichzeitig stattfinden können.
    Dazu müssen die ZeitVars aller Prüfungen, die zu einem Studiengang gehören, unterschiedlich sein.
    :param model: Model zum Lösen mittels Google OR Tools
    :param orm: ORM für das Handling der Datenbankeinträgen
    :return:
    """

    for studiengang in orm.getStudiengaenge():

        for i in range(len(studiengang.getPruefungen())):
            for j in range(i + 1, len(studiengang.getPruefungen())):
                pruef_i = studiengang.getPruefungen()[i]
                pruef_j = studiengang.getPruefungen()[j]
                model.Add(pruef_i.zeitVar != pruef_j.zeitVar)


def einePrüfungProTagSemesterGruppeConstraint(model: CpModel, orm: ORM):
    """
    Dieses Constraint sichert zu, dass eine SemesterGruppe nur eine Prüfung pro Tag haben soll.
    Dazu müssen die TagVars aller Prüfungen, die zu einer Semestergruppe gehören, unterschiedlich sein.
    :param model: Model zum Lösen mittels Google OR Tools
    :param orm: ORM für das Handling der Datenbankeinträgen
    :return:
    """

    for semestergruppe in orm.getSemesterGruppen():
        for i in range(len(semestergruppe.getPruefungen())):
            for j in range(i + 1, len(semestergruppe.getPruefungen())):
                pruef_i, pruef_j = semestergruppe.getPruefungen()[i], semestergruppe.getPruefungen()[j]
                model.Add(pruef_i.tagVar != pruef_j.tagVar)


def spaeteZeitSlots(model: CpModel, orm: ORM, slot: int, strafe: int):
    """
    Methode um tagSlots mit Strafe zu belegen
    :param model: Model
    :param orm: ORM
    :param slot: tagSlot der zu vermeiden ist
    :param strafe: Strafe für den Verstoß
    :return: Ausdruck zur Optimierung durch Model/Solver
    """
    slotBelegt = model.NewIntVar(0, len(orm.getPruefungen()), "")
    bool = []
    for pruefung in orm.getPruefungen():
        boolVar = model.NewBoolVar("")
        model.Add(pruefung.slotVar == slot).OnlyEnforceIf(boolVar)
        model.Add(pruefung.slotVar != slot).OnlyEnforceIf(boolVar.Not())
        bool.append(boolVar)

    model.Add(slotBelegt == sum(bool))
    return slotBelegt * strafe


def beachteWunschTermine(model: CpModel, orm: ORM):
    summe = model.NewConstant(0)
    nichtbeachtet = []
    for pruefung in orm.getPruefungen():
        bools = []
        nullSlot = model.NewBoolVar("")
        model.Add(pruefung.wunschtermin != 0).OnlyEnforceIf(nullSlot)
        model.Add(pruefung.wunschtermin == 0).OnlyEnforceIf(nullSlot.Not())
        bools.append(nullSlot)
        terminGesetzt = model.NewBoolVar("")
        model.Add(pruefung.zeitVar == pruefung.wunschtermin).OnlyEnforceIf(terminGesetzt)
        model.Add(pruefung.zeitVar != pruefung.wunschtermin).OnlyEnforceIf(terminGesetzt.Not())
        bools.append(terminGesetzt)
        wunschNichtBeachtet = model.NewBoolVar("")
        model.Add(sum(bools) == 1).OnlyEnforceIf(wunschNichtBeachtet)
        model.Add(sum(bools) != 1).OnlyEnforceIf(wunschNichtBeachtet.Not())
        nichtbeachtet.append(wunschNichtBeachtet)
    model.Add(summe == sum(nichtbeachtet))
    return summe * WUNSCHSTRAFE
