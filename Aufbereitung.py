from datetime import datetime

import xlsxwriter
import xlsxwriter.worksheet

from ORM import TAGE, ZEITEN
from Plan import *

formatierung = dict()


# ZeitSlotHeader für die Tage und SLots
def erzeugeZeitSlotHeader(worksheet, semester, reihe):
    worksheet.merge_range(reihe, 0, reihe + 2, 2, semester, formatierung["semesterNameFormat"])
    column = 4
    worksheet.set_row(reihe, 35)

    for i in range(3, PRUEFUNGSTAGE * ZEITSLOTS_PRO_TAG + 14):
        worksheet.set_column(0, i, 25)
    for tag in range(PRUEFUNGSTAGE):
        # Datum des Tages

        worksheet.merge_range(reihe, column, reihe, column - 2 + ZEITSLOTS_PRO_TAG, TAGE[tag],
                              formatierung["datumForTag"])
        for slot in range(1, ZEITSLOTS_PRO_TAG + 1):
            # Slot Nummer

            worksheet.write_string(reihe + 2, column, "%s" % ZEITEN[slot - 1], formatierung["kleinFormat3"])
            if (slot == 4):
                # Leerzeichen
                worksheet.write_string(reihe + 2, column + 1, " ", formatierung["simpleBoldFormat"])
                column += 1

            column += 1
    return reihe + 3


# Header für die Studentensicht (Nur Prüfungstage)
def erzeugeZeitSlotStudHeader(worksheet, reihe):
    column = 3
    worksheet.set_row(reihe, 26)
    worksheet.set_column(column, 50)
    for tag in range(PRUEFUNGSTAGE):
        # Datum des Tages
        worksheet.merge_range(reihe, column, reihe, column + 1, TAGE[tag],
                              formatierung["datumForTag"])
        column += 2
    return reihe + 1


# header
def erzeugeHeader(worksheet, fachbereich, semester, sicht, orm, reihe) -> int:
    laenge = len(orm.getZeitSlots()) + 5
    tag = datetime.today().date()
    worksheet.write(reihe, 0, "Stand:", formatierung["simpleBoldFormat"])
    worksheet.write(reihe, 1, tag, formatierung["datumFor"])

    reihe += 1
    worksheet.set_column(0, 0, 30)
    worksheet.set_column(1, 1, 20)
    worksheet.set_column(2, 2, 20)
    worksheet.set_column(3, 8, 7)

    for column in range(0, laenge + 3):
        worksheet.write(reihe, column, None, formatierung["mainHeaderFormat"])
    worksheet.write(reihe, 0, "Prüfungsplanung", formatierung["mainHeaderFormat"])
    worksheet.write(reihe, 3, fachbereich, formatierung["mainHeaderFormat"])
    worksheet.write(reihe, 7, sicht, formatierung["mainHeaderFormat"])

    # größe
    worksheet.set_row(reihe, 27.75)
    reihe += 1
    if (sicht == "Aufsichten"):
        reihe = erzeugeZeitSlotHeader(worksheet, semester, reihe)
    else:
        reihe = erzeugeZeitSlotStudHeader(worksheet, reihe)

    return reihe


# AufsichtView für Aufsichten
def erzeugeAufsichtView(plan, workbook, fachbereich, semester, orm):
    worksheet = workbook.add_worksheet("Aufsichten")
    reihe = 0
    reihe = erzeugeHeader(worksheet, fachbereich, semester, "Aufsichten", orm, reihe)
    worksheet.freeze_panes(reihe, (PRUEFUNGSTAGE * ZEITSLOTS_PRO_TAG + 5))
    aufsichten = orm.getAufsichten()
    aufsichten.sort(key=lambda a: a.name)

    for aufsicht in aufsichten:
        worksheet.merge_range(reihe, 0, reihe, 0 + 1, "%s" % aufsicht.name, formatierung["simpleBoldFormat"])
        worksheet.set_row(reihe, 20)  # Row height.

        pruefungen = []
        for p in orm.getPruefungen():
            list = plan.getAufsichtVonPrüfung(p)
            for a in list:
                if (a.id == aufsicht.id):
                    if p not in pruefungen:
                        pruefungen.append(p)
        for pr in pruefungen:
            raeume = plan.getRaumVonPrüfung(pr)
            slot = plan.getZeitSlotPruefung(pr)
            raumName = ""
            # konkreter zu beaufsichtigender Raum
            for i in range(len(raeume)):
                if raumName.find(raeume[i].name) == -1:
                    raumName += raeume[i].name + ","
            raumName = raumName[:-1]
            string = pr.kurzform + " , " + raumName
            if (raumName == ""):
                string = pr.kurzform + " , " + raeume[0].name

            worksheet.write_string(reihe, 3 + slot.slotTag_nummer + (5 * (slot.pruefungstag_nummer - 1)), string,
                                   formatierung["kleinFormat2"])
        reihe += 1

    reihe += 1
    worksheet.set_row(reihe, 2)


# Studentensicht
def erzeugeStudentenView(plan, workbook, fachbereich, semester, orm):
    worksheet = workbook.add_worksheet("Studenten")
    reihe = 0
    column = 0
    reihe = erzeugeHeader(worksheet, fachbereich, semester, "Studenten", orm, reihe)
    worksheet.freeze_panes(reihe, (PRUEFUNGSTAGE * ZEITSLOTS_PRO_TAG + 5))
    semestergruppen = orm.getSemesterGruppen()
    semestergruppen.sort(key=lambda a: a.name)

    for studiengang in orm.getStudiengaenge():

        worksheet.merge_range(reihe, column, reihe, (PRUEFUNGSTAGE * ZEITSLOTS_PRO_TAG + 5), studiengang.name,
                              formatierung["StudiengangFormat"])
        for semestergruppe in semestergruppen:
            if (semestergruppe.studiengang == studiengang.id):
                reihe += 1

                worksheet.merge_range(reihe, column, reihe, (PRUEFUNGSTAGE * ZEITSLOTS_PRO_TAG + 5),
                                      semestergruppe.name,
                                      formatierung["kleinFormat2"])
                reihe += 1
                for p in semestergruppe.getPruefungen():
                    worksheet.write_string(reihe, column,
                                           p.name,
                                           formatierung["kleinFormat"])
                    raeume = plan.getRaumVonPrüfung(p)
                    string = ""
                    for r in raeume:
                        if string.find(r.name) == -1:
                            string += r.name + ","
                    string = string[:-1]
                    worksheet.merge_range(reihe, column + 1, reihe, column + 2, string, formatierung["kleinFormat"])
                    zeitpunkt = plan.getZeitSlotPruefung(p)
                    tag = zeitpunkt.pruefungstag_nummer
                    slot = zeitpunkt.slotTag_nummer
                    worksheet.merge_range(reihe, 3 + ((tag - 1) * 2), reihe, 3 + ((tag - 1) * 2) + 1,
                                          ZEITEN[slot - 1],
                                          formatierung["ZeitFormat"])
                    reihe += 1

        reihe += 1


# Gesamtes File erzeugen
def writeTimeTableExcelFile(plan: Plan, uniName, fachbereich, semester, orm):
    s = ("%s_Prüfungsplan_%s_%s.xlsx" % (uniName, fachbereich, semester))
    workbook = xlsxwriter.Workbook(s)

    global formatierung

    formatierung["simpleBoldFormat"] = workbook.add_format({'bold': True, 'font_size': '11'})
    formatierung["kleinFormat"] = workbook.add_format({'font_size': '9', })
    formatierung["kleinFormat3"] = workbook.add_format({'font_size': '9', 'align': 'center'})
    formatierung["kleinFormat2"] = workbook.add_format({'bold': True, 'font_size': '10', 'bg_color': '#C0C0C0'})
    formatierung["StudiengangFormat"] = workbook.add_format({'bold': True, 'font_size': '14', 'bg_color': '#808080'})
    formatierung["ZeitFormat"] = workbook.add_format(
        {'bold': True, 'font_size': '11', 'align': 'center', 'bg_color': 'dark'})
    formatierung["mainHeaderFormat"] = workbook.add_format(
        {'bold': True, 'font_size': '12', 'font_name': 'Arial', 'valign': 'vcenter', 'bg_color': 'blue'})
    formatierung["datumFor"] = workbook.add_format(
        {'num_format': 'dd/mm/yy'})
    formatierung["datumForTag"] = workbook.add_format(
        {'num_format': 'dd/mm/yy', 'align': 'center'})
    formatierung["semesterNameFormat"] = workbook.add_format(
        {'bold': True, 'font_size': '20', 'font_name': 'Arial', 'align': 'center', 'valign': 'vcenter'})

    erzeugeAufsichtView(plan, workbook, fachbereich, semester, orm)
    erzeugeStudentenView(plan, workbook, fachbereich, semester, orm)

    workbook.close()
