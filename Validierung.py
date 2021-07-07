from Constraints import *
from Plan import PRUEFUNG, RAUM,AUFSICHT, Plan
from ZeitSlot import ZeitSlot
def validierePlan(plan) -> bool:

    valide = True

    valide = validiereRaumVerfuegbarkeit(plan, plan.orm) and validiereAufsichtVerfuegbarkeit(plan,plan.orm) and validiereStudiengangConstraint(plan, plan.orm) and validiereSemestergruppenConstraint(plan, plan.orm) and validiereUnterschiedlicheRaeume(plan, plan.orm) and validiereUnterschiedlicheAufsichten(plan, plan.orm) and validiereRaumGroesse(plan, plan.orm) and validiereRaumAnzahl(plan, plan.orm) and validiereAufsichtRaumZeitConstraint(plan, plan.orm)

    return valide

# Beachten der Raum Verfügbarkeit
def validiereRaumVerfuegbarkeit(plan: Plan, orm: ORM) -> bool:
    valide = True
    for raum in orm.getRaeume():
        for zeitslot in raum.nicht_verfuegbare_zeitslots:
            valide = valide and raum not in map(lambda tu: tu[RAUM], plan.getZeitMap()[zeitslot])
    return valide

# Beachten der Aufsicht Verfügbarkeit
def validiereAufsichtVerfuegbarkeit(plan: Plan, orm: ORM) -> bool:
    valide = True
    for aufsicht in orm.getAufsichten():
        for zeitslot in aufsicht.nicht_verfuegbare_aufsicht_zeitslots:
            valide = valide and aufsicht not in map(lambda tu: tu[AUFSICHT], plan.getZeitMap()[zeitslot])
    return valide

#Beachten des StudiengangConstraint
def validiereStudiengangConstraint(plan: Plan, orm: ORM) -> bool:
    summe = 0
    for studiengang in orm.getStudiengaenge():
        slots = []
        for pruefung in studiengang.pruefungen:
            slots.append(plan.getZeitSlotPruefung(pruefung))
        for i in range(len(slots)):
            for j in range(i + 1,len(slots)):
                if slots[i] == slots[j]:
                    summe +=1
    return summe == 0
#Beachten des SemestergruppenConstraint
def validiereSemestergruppenConstraint(plan: Plan, orm: ORM) -> bool:
    summe = 0
    for sg in orm.getSemesterGruppen():
        slots = []
        for pruefung in sg.pruefungen:
            slots.append(plan.getZeitSlotPruefung(pruefung).pruefungstag_nummer)
            for i in range(len(slots)):
                for j in range(i + 1, len(slots)):
                    if slots[i] == slots[j]:
                        summe += 1

    return summe == 0
def validiereAufsichtRaumZeitConstraint(plan: Plan, orm: ORM) -> bool:
    summe = 0
    for i in range(len(orm.getPruefungen())):
        raeume = [ ]
        aufsichten = []
        raeume.append(list(set(plan.getRaumVonPrüfung(orm.getPruefungen()[i]))))
        aufsichten.append(list(set(plan.getAufsichtVonPrüfung(orm.getPruefungen()[i]))))
        slot = plan.getZeitSlotPruefung(orm.getPruefungen()[i])
        #Suche Prüfungen im gleichen Slot
        for j in range(i + 1, len(orm.getPruefungen())):
            if(plan.getZeitSlotPruefung(orm.getPruefungen()[j]) == slot):
                raeume.append(list(set(plan.getRaumVonPrüfung(orm.getPruefungen()[j]))))
                aufsichten.append(list(set(plan.getAufsichtVonPrüfung(orm.getPruefungen()[j]))))
        #Geht denn Anzahl der Aufsichten == Anzahl der Räume
        for r in range(len(raeume)):
            for s in range(r + 1,len(raeume)):
                if(raeume[r] == raeume[s]):
                    summe += 1
                if (aufsichten[r] == aufsichten[s]):
                    summe += 1
    return summe == 0
def validiereUnterschiedlicheRaeume(plan: Plan, orm: ORM) -> bool:
    summe = 0
    for p in orm.getPruefungen():
        # Da Räume pro Prüfung doppelt in der Map vorhanden aufgrund des Befüllens der Map in Planung.py
        raeume = list(set(plan.getRaumVonPrüfung(p)))
        for i in range(len(raeume)):
            for j in range(i + 1, len(raeume)):
                #Räume gleich
                if raeume[i] == raeume[j]:
                    summe += 1
    return summe == 0
def validiereUnterschiedlicheAufsichten(plan: Plan, orm: ORM) -> bool:
    summe = 0
    for p in orm.getPruefungen():
        # Da Aufsichten pro Prüfung doppelt in der Map vorhanden aufgrund des Befüllens der Map in Planung.py
        a = list(set(plan.getAufsichtVonPrüfung(p)))
        for i in range(len(a)):
            for j in range(i + 1, len(a)):
                #Gleiche Aufsicht
                if a[i] == a[j]:
                    summe += 1
    return summe == 0
def validiereRaumGroesse(plan: Plan, orm: ORM) -> bool:
    summe = 0
    for p in orm.getPruefungen():
        kapazität = 0
        #Siehe OBEN
        raeume = list(set(plan.getRaumVonPrüfung(p)))
        for r in raeume:
            kapazität += r.groesse

        #Räume zu klein
        if(p.teilnehmerzahl > kapazität):
            summe += 1
    return summe == 0
def validiereRaumAnzahl(plan: Plan, orm: ORM) -> bool:
    summe = 0
    for p in orm.getPruefungen():
        l = len(list(set(plan.getRaumVonPrüfung(p))))
        #mehr als ein Raum für < 40 Teilnehmer
        if(p.teilnehmerzahl < 40 and l > 1):
            summe += 1
        # mehr als 2 Räume für <= 100 Teilnehmer
        if (p.teilnehmerzahl <= 100 and l > 2):
            summe += 1
        # mehr als 4 Räume für <= 200 Teilnehmer
        if (p.teilnehmerzahl <= 200 and l > 4):
            summe += 1
        # mehr als 6 Räume für eine Prüfung
        if (l > 6):
            summe += 1
    return summe == 0