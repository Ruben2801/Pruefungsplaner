from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

import ORM
from Pruefung import Pruefung
from Raum import Raum
from SemesterGruppe import SemesterGruppe
from Studiengang import Studiengang
from Aufsicht import Aufsicht
from ZeitSlot import ZeitSlot
from Base import Base


def neuePrüfung(Name, kurz, PruefNummer, Teilnehmerzahl,wunsch):
    """
    Erzeugen einer Prüfung
    :param Name: Name der Prüfung
    :param PruefNummer: Prüfungsnummer für das QIS
    :param Teilnehmerzahl: Anzahl der Teilnehmer an einer Prüfung
    :return: Objekt vom Typ Prüfung
    """

    Pruef = Pruefung(name=Name, kurzform=kurz, pruefungsnummer=PruefNummer, teilnehmerzahl=Teilnehmerzahl,wunschtermin = wunsch)

    return Pruef


def zeitslotByID(session, ID) -> ZeitSlot:
    return session.query(ZeitSlot).get(ID)


def genTestDatenKlein(session: Session):
    s = session

    i = 1

    while i <= ORM.PRUEFUNGSTAGE:
        zeit1 = ZeitSlot(pruefungstag_nummer=i, slotTag_nummer=1)
        zeit2 = ZeitSlot(pruefungstag_nummer=i, slotTag_nummer=2)
        zeit3 = ZeitSlot(pruefungstag_nummer=i, slotTag_nummer=3)
        zeit4 = ZeitSlot(pruefungstag_nummer=i, slotTag_nummer=4)
        session.add_all([zeit1, zeit2, zeit3, zeit4])
        i += 1

    Aufsicht1 = Aufsicht(name="Max Müller", kurzform="mül")
    Aufsicht2 = Aufsicht(name="Klaus Kleber", kurzform="kle")
    Aufsicht3 = Aufsicht(name="Werner Weiß", kurzform="wei")
    Aufsicht4 = Aufsicht(name="Anna Angst", kurzform="ang")

    Aufsicht1.nicht_verfuegbare_aufsicht_zeitslots.extend([zeitslotByID(session, 1), zeitslotByID(session, 2)])
    # Aufsicht3.nicht_verfuegbare_aufsicht_zeitslots.extend([ZeitSlot(pruefungstag_nummer=0, slotTag_nummer=3)])
    # Aufsicht4.nicht_verfuegbare_aufsicht_zeitslots.extend([ZeitSlot(pruefungstag_nummer=1, slotTag_nummer=1)])

    session.add_all([Aufsicht1, Aufsicht2, Aufsicht3, Aufsicht4])

    Raum1 = Raum(name="AM2", groesse="60")
    Raum2 = Raum(name="AM1", groesse="80")
    Raum3 = Raum(name="18.1.01", groesse="30")
    Raum4 = Raum(name="18.1.03", groesse="35")
    Raum1.nicht_verfuegbare_zeitslots.extend([zeitslotByID(session, 1), zeitslotByID(session, 2)])
    # Raum2.nicht_verfuegbare_zeitslots.extend([ZeitSlot(pruefungstag_nummer=0, slotTag_nummer=2)])
    # Raum3.nicht_verfuegbare_zeitslots.extend([ZeitSlot(pruefungstag_nummer=0, slotTag_nummer=3)])
    # Raum4.nicht_verfuegbare_zeitslots.extend([ZeitSlot(pruefungstag_nummer=0, slotTag_nummer=1)])

    session.add_all([Raum1, Raum2, Raum3, Raum4])

    SemesterGruppe1 = SemesterGruppe(name="inf1", studiengang=1)
    SemesterGruppe2 = SemesterGruppe(name="inf3", studiengang=1)
    SemesterGruppe3 = SemesterGruppe(name="inf5", studiengang=1)
    SemesterGruppe4 = SemesterGruppe(name="eks1", studiengang=2)
    SemesterGruppe5 = SemesterGruppe(name="eks3", studiengang=2)

    Studiengang1 = Studiengang(name="Informatik/Softwaretechnik", kurzform="Inf/Swt")
    Studiengang2 = Studiengang(name="Elektrotechnik- Kommunikationssysteme", kurzform="EKS")

    Pruefung1 = neuePrüfung("Mathematik 1", "Ma1", "SB112", 30,2)
    Pruefung2 = neuePrüfung("Informatik 1", "Inf1", "SB122", 40,0)
    Pruefung3 = neuePrüfung("Physik 1", "Phy1", "SB132", 100,0)
    Pruefung4 = neuePrüfung("Elektronik 1", "Elt1", "SB152", 5,0)
    Pruefung5 = neuePrüfung("Elektronik 2", "Elt2", "SB152", 5,0)

    Pruefung1.pruefung_SemesterGruppe_table.append(SemesterGruppe1)
    Pruefung2.pruefung_SemesterGruppe_table.append(SemesterGruppe1)
    Pruefung3.pruefung_SemesterGruppe_table.append(SemesterGruppe4)
    Pruefung4.pruefung_SemesterGruppe_table.append(SemesterGruppe4)
    Pruefung5.pruefung_SemesterGruppe_table.append(SemesterGruppe2)
    Pruefung1.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung2.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung3.pruefung_Studiengang_table.append(Studiengang2)
    Pruefung4.pruefung_Studiengang_table.append(Studiengang2)
    Pruefung5.pruefung_Studiengang_table.append(Studiengang1)

    session.add_all([Pruefung1, Pruefung2, Pruefung3, Pruefung4, Pruefung5])
    session.add_all([Studiengang1, Studiengang2])
    session.add_all([SemesterGruppe1, SemesterGruppe2, SemesterGruppe3, SemesterGruppe4, SemesterGruppe5])

    session.commit()


def genTestDatenMittel(session: Session):
    s = session

    i = 1

    while i <= ORM.PRUEFUNGSTAGE:
        zeit1 = ZeitSlot(pruefungstag_nummer=i, slotTag_nummer=1)
        zeit2 = ZeitSlot(pruefungstag_nummer=i, slotTag_nummer=2)
        zeit3 = ZeitSlot(pruefungstag_nummer=i, slotTag_nummer=3)
        zeit4 = ZeitSlot(pruefungstag_nummer=i, slotTag_nummer=4)
        session.add_all([zeit1, zeit2, zeit3, zeit4])
        i += 1

    Aufsicht1 = Aufsicht(name="Max Müller", kurzform="mül")
    Aufsicht2 = Aufsicht(name="Klaus Kleber", kurzform="kle")
    Aufsicht3 = Aufsicht(name="Werner Weiß", kurzform="wei")
    Aufsicht4 = Aufsicht(name="Anna Angst", kurzform="ang")
    Aufsicht5 = Aufsicht(name="Ben Bus", kurzform="ang")
    Aufsicht6 = Aufsicht(name="Walter Weiß", kurzform="wei")
    Aufsicht7 = Aufsicht(name="Adam Angst", kurzform="ang")
    Aufsicht8 = Aufsicht(name="Lukas Neu", kurzform="ang")
    Aufsicht9 = Aufsicht(name="Jonas Pohn", kurzform="axg")
    Aufsicht10 = Aufsicht(name="Willi Mein", kurzform="wdi")
    Aufsicht11 = Aufsicht(name="Jochen Angst", kurzform="atg")
    Aufsicht12 = Aufsicht(name="Manuela Grün", kurzform="ayg")
    Aufsicht13 = Aufsicht(name="Lara Neun", kurzform="azg")
    Aufsicht14 = Aufsicht(name="Johannes Pohn", kurzform="aug")
    Aufsicht15 = Aufsicht(name="Klaus Mein", kurzform="wii")
    Aufsicht16 = Aufsicht(name="Detlef Angst", kurzform="arg")
    Aufsicht17 = Aufsicht(name="Prof. Dr. Max Mustermann", kurzform="aig")
    Aufsicht18 = Aufsicht(name="Georg Grün", kurzform="aog")
    Aufsicht19 = Aufsicht(name="Lisa Grün", kurzform="apg")
    Aufsicht20 = Aufsicht(name="Olga Grün", kurzform="alg")

    Aufsicht1.nicht_verfuegbare_aufsicht_zeitslots.extend([zeitslotByID(session, 1), zeitslotByID(session, 2)])
    Aufsicht3.nicht_verfuegbare_aufsicht_zeitslots.extend([ZeitSlot(pruefungstag_nummer=0, slotTag_nummer=3)])
    Aufsicht4.nicht_verfuegbare_aufsicht_zeitslots.extend([ZeitSlot(pruefungstag_nummer=1, slotTag_nummer=1)])

    session.add_all(
        [Aufsicht1, Aufsicht2, Aufsicht3, Aufsicht4, Aufsicht5, Aufsicht6, Aufsicht7, Aufsicht8, Aufsicht9, Aufsicht10,
         Aufsicht11, Aufsicht12, Aufsicht13, Aufsicht14, Aufsicht15, Aufsicht16, Aufsicht17, Aufsicht18, Aufsicht19,
         Aufsicht20])

    Raum1 = Raum(name="AM2", groesse="60")
    Raum2 = Raum(name="AM1", groesse="80")
    Raum3 = Raum(name="18.1.01", groesse="30")
    Raum4 = Raum(name="18.1.03", groesse="35")
    Raum5 = Raum(name="AM3", groesse="60")
    Raum6 = Raum(name="18.1.04", groesse="30")
    Raum7 = Raum(name="17.1.01", groesse="30")
    Raum8 = Raum(name="17.1.02", groesse="35")
    Raum9 = Raum(name="17.1.03", groesse="40")
    Raum10 = Raum(name="19.1.01", groesse="35")
    Raum11 = Raum(name="19.1.02", groesse="30")
    Raum12 = Raum(name="19.1.03", groesse="40")
    Raum13 = Raum(name="19.1.04", groesse="50")
    Raum14 = Raum(name="19.1.05", groesse="60")
    Raum15 = Raum(name="19.1.06", groesse="25")
    Raum16 = Raum(name="19.1.07", groesse="30")

    Raum1.nicht_verfuegbare_zeitslots.extend([zeitslotByID(session, 1), zeitslotByID(session, 2)])
    Raum2.nicht_verfuegbare_zeitslots.extend([ZeitSlot(pruefungstag_nummer=0, slotTag_nummer=2)])
    Raum3.nicht_verfuegbare_zeitslots.extend([ZeitSlot(pruefungstag_nummer=0, slotTag_nummer=3)])
    Raum4.nicht_verfuegbare_zeitslots.extend([ZeitSlot(pruefungstag_nummer=0, slotTag_nummer=1)])

    session.add_all(
        [Raum1, Raum2, Raum3, Raum4, Raum5, Raum6, Raum7, Raum8, Raum9, Raum10, Raum11, Raum12, Raum13, Raum14, Raum15,
         Raum16])

    SemesterGruppe1 = SemesterGruppe(name="inf1", studiengang=1)
    SemesterGruppe2 = SemesterGruppe(name="inf3", studiengang=1)
    SemesterGruppe3 = SemesterGruppe(name="inf5", studiengang=1)
    SemesterGruppe4 = SemesterGruppe(name="inf2", studiengang=1)
    SemesterGruppe5 = SemesterGruppe(name="inf4", studiengang=1)
    SemesterGruppe6 = SemesterGruppe(name="AET1", studiengang=2)
    SemesterGruppe7 = SemesterGruppe(name="AET2", studiengang=2)
    SemesterGruppe8 = SemesterGruppe(name="ITB6", studiengang=3)
    SemesterGruppe9 = SemesterGruppe(name="ITB7", studiengang=3)

    Studiengang1 = Studiengang(name="Informatik/Softwaretechnik", kurzform="Inf/Swt")
    Studiengang2 = Studiengang(name="Allgemeine Elektrotechnik", kurzform="AET")
    Studiengang3 = Studiengang(name="Information Technology", kurzform="ITECH")
    # Inf 1 Semester
    Pruefung1 = neuePrüfung("Mathematik 1", "Ma1", "SB112", 100,0)
    Pruefung2 = neuePrüfung("Informatik 1", "Inf1", "SB122", 60,0)
    Pruefung3 = neuePrüfung("Datenbanken", "Db", "SB1142", 55,0)
    Pruefung4 = neuePrüfung("Programmieren 1", "Prog1", "SB1152", 50,0)
    # Inf 3 Semester
    Pruefung5 = neuePrüfung("Softwaretechnik 1", "SWT1", "SB1162", 30,0)
    Pruefung6 = neuePrüfung("Rechnernetze", "RN", "SB1182", 35,0)
    Pruefung7 = neuePrüfung("Betriebssysteme", "BS", "SB1192", 40,0)
    Pruefung8 = neuePrüfung("Verteilte Systeme", "VSys", "SB1183", 45,0)
    # Inf 5 Semester
    Pruefung9 = neuePrüfung("Formale Sprachen", "Übs", "SB1163", 30,0)
    Pruefung10 = neuePrüfung("Rechnernetze2", "RN2", "SB1186", 35,0)
    Pruefung11 = neuePrüfung("Betriebssysteme2", "BS2", "SB1197", 40,0)
    Pruefung12 = neuePrüfung("Verteilte Systeme2", "VSys2", "SB1189", 45,0)

    # Inf 2
    Pruefung13 = neuePrüfung("Programmieren 2", "Prog 2", "SB1176", 50,0)
    Pruefung14 = neuePrüfung("Informatik 2", "Inf 2", "SB1276", 45,0)
    Pruefung15 = neuePrüfung("Mathematik II für Informatiker*innen", "Ma II Inf", "SB213", 45,0)
    Pruefung16 = neuePrüfung("Theoretische Informatik", "TI", "1203", 40,0)
    # inf 4
    Pruefung21 = neuePrüfung("Betriebswirtschaftslehre", "BWL", "25423", 60,0)
    Pruefung22 = neuePrüfung("Datenmanagement", "BWL", "26423", 30,0)

    # AET 1
    Pruefung17 = neuePrüfung("Physik", "Phy", "SB2176", 40,0)
    Pruefung18 = neuePrüfung("Grundlagen der Gleichstromtechnik", "GE 1", "SB2276", 45,0)
    Pruefung19 = neuePrüfung("Prozedurale Programmierung", "Prog 1", "12342", 40,0)
    Pruefung20 = neuePrüfung("Projekt- und Selbstmanagement", "PM_SM", "23423", 40,0)

    Pruefung17.pruefung_SemesterGruppe_table.append(SemesterGruppe6)
    Pruefung18.pruefung_SemesterGruppe_table.append(SemesterGruppe6)
    Pruefung19.pruefung_SemesterGruppe_table.append(SemesterGruppe6)
    Pruefung20.pruefung_SemesterGruppe_table.append(SemesterGruppe6)

    # AET2
    Pruefung23 = neuePrüfung("Grundlagen der Wechselstromtechnik", "GEW 1", "1171", 35,0)
    Pruefung24 = neuePrüfung("Mathematik für Elektrotechniker", "MAE", "1160", 40,0)
    Pruefung25 = neuePrüfung("Digitaltechnik", "DT", "1191", 40,0)

    Pruefung23.pruefung_SemesterGruppe_table.append(SemesterGruppe7)
    Pruefung24.pruefung_SemesterGruppe_table.append(SemesterGruppe7)
    Pruefung25.pruefung_SemesterGruppe_table.append(SemesterGruppe7)
    Pruefung23.pruefung_Studiengang_table.append(Studiengang2)
    Pruefung24.pruefung_Studiengang_table.append(Studiengang2)
    Pruefung25.pruefung_Studiengang_table.append(Studiengang2)

    # inf 1
    Pruefung1.pruefung_SemesterGruppe_table.append(SemesterGruppe1)
    Pruefung1.pruefung_SemesterGruppe_table.append(SemesterGruppe6)
    Pruefung2.pruefung_SemesterGruppe_table.append(SemesterGruppe1)
    Pruefung3.pruefung_SemesterGruppe_table.append(SemesterGruppe1)
    Pruefung4.pruefung_SemesterGruppe_table.append(SemesterGruppe1)
    # inf2
    Pruefung5.pruefung_SemesterGruppe_table.append(SemesterGruppe2)
    Pruefung6.pruefung_SemesterGruppe_table.append(SemesterGruppe2)
    Pruefung7.pruefung_SemesterGruppe_table.append(SemesterGruppe2)
    Pruefung8.pruefung_SemesterGruppe_table.append(SemesterGruppe2)
    # inf3
    Pruefung9.pruefung_SemesterGruppe_table.append(SemesterGruppe3)
    Pruefung10.pruefung_SemesterGruppe_table.append(SemesterGruppe3)
    Pruefung11.pruefung_SemesterGruppe_table.append(SemesterGruppe3)
    Pruefung12.pruefung_SemesterGruppe_table.append(SemesterGruppe3)
    # inf2
    Pruefung13.pruefung_SemesterGruppe_table.append(SemesterGruppe4)
    Pruefung14.pruefung_SemesterGruppe_table.append(SemesterGruppe4)
    Pruefung15.pruefung_SemesterGruppe_table.append(SemesterGruppe4)
    Pruefung16.pruefung_SemesterGruppe_table.append(SemesterGruppe4)
    # inf4
    Pruefung21.pruefung_SemesterGruppe_table.append(SemesterGruppe5)
    Pruefung22.pruefung_SemesterGruppe_table.append(SemesterGruppe5)

    Pruefung1.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung1.pruefung_Studiengang_table.append(Studiengang2)
    Pruefung2.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung3.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung4.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung5.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung6.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung7.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung8.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung9.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung10.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung11.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung12.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung13.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung14.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung15.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung16.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung17.pruefung_Studiengang_table.append(Studiengang2)
    Pruefung18.pruefung_Studiengang_table.append(Studiengang2)
    Pruefung19.pruefung_Studiengang_table.append(Studiengang2)
    Pruefung20.pruefung_Studiengang_table.append(Studiengang2)
    Pruefung21.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung22.pruefung_Studiengang_table.append(Studiengang1)

    session.add_all(
        [Pruefung1, Pruefung2, Pruefung3, Pruefung4, Pruefung5, Pruefung6, Pruefung7, Pruefung8, Pruefung9, Pruefung10,
         Pruefung11, Pruefung12, Pruefung13, Pruefung14, Pruefung15, Pruefung16, Pruefung17, Pruefung18, Pruefung19,
         Pruefung20, Pruefung21, Pruefung22, Pruefung23, Pruefung24, Pruefung25])
    session.add_all([Studiengang1, Studiengang2, Studiengang3])
    session.add_all(
        [SemesterGruppe1, SemesterGruppe2, SemesterGruppe3, SemesterGruppe4, SemesterGruppe5, SemesterGruppe6,
         SemesterGruppe7, SemesterGruppe8, SemesterGruppe9])

    session.commit()


def genTestDatenGroß(session: Session):
    s = session

    i = 1

    while i <= ORM.PRUEFUNGSTAGE:
        zeit1 = ZeitSlot(pruefungstag_nummer=i, slotTag_nummer=1)
        zeit2 = ZeitSlot(pruefungstag_nummer=i, slotTag_nummer=2)
        zeit3 = ZeitSlot(pruefungstag_nummer=i, slotTag_nummer=3)
        zeit4 = ZeitSlot(pruefungstag_nummer=i, slotTag_nummer=4)
        session.add_all([zeit1, zeit2, zeit3, zeit4])
        i += 1

    Aufsicht1 = Aufsicht(name="Max Müller", kurzform="mül")
    Aufsicht2 = Aufsicht(name="Klaus Kleber", kurzform="kle")
    Aufsicht3 = Aufsicht(name="Werner Weiß", kurzform="wei")
    Aufsicht4 = Aufsicht(name="Anna Angst", kurzform="ang")
    Aufsicht5 = Aufsicht(name="Ben Bus", kurzform="ang")
    Aufsicht6 = Aufsicht(name="Walter Weiß", kurzform="wei")
    Aufsicht7 = Aufsicht(name="Adam Angst", kurzform="ang")
    Aufsicht8 = Aufsicht(name="Lukas Neu", kurzform="ang")
    Aufsicht9 = Aufsicht(name="Jonas Pohn", kurzform="axg")
    Aufsicht10 = Aufsicht(name="Willi Mein", kurzform="wdi")
    Aufsicht11 = Aufsicht(name="Jochen Angst", kurzform="atg")
    Aufsicht12 = Aufsicht(name="Manuela Grün", kurzform="ayg")
    Aufsicht13 = Aufsicht(name="Lara Neun", kurzform="azg")
    Aufsicht14 = Aufsicht(name="Johannes Pohn", kurzform="aug")
    Aufsicht15 = Aufsicht(name="Klaus Mein", kurzform="wii")
    Aufsicht16 = Aufsicht(name="Detlef Angst", kurzform="arg")
    Aufsicht17 = Aufsicht(name="Prof. Dr. Max Mustermann", kurzform="aig")
    Aufsicht18 = Aufsicht(name="Georg Grün", kurzform="aog")
    Aufsicht19 = Aufsicht(name="Lisa Grün", kurzform="apg")
    Aufsicht20 = Aufsicht(name="Olga Grün", kurzform="alg")

    Aufsicht1.nicht_verfuegbare_aufsicht_zeitslots.extend([zeitslotByID(session, 1), zeitslotByID(session, 2)])
    Aufsicht3.nicht_verfuegbare_aufsicht_zeitslots.extend([ZeitSlot(pruefungstag_nummer=0, slotTag_nummer=3)])
    Aufsicht4.nicht_verfuegbare_aufsicht_zeitslots.extend([ZeitSlot(pruefungstag_nummer=1, slotTag_nummer=1)])

    session.add_all(
        [Aufsicht1, Aufsicht2, Aufsicht3, Aufsicht4, Aufsicht5, Aufsicht6, Aufsicht7, Aufsicht8, Aufsicht9, Aufsicht10,
         Aufsicht11, Aufsicht12, Aufsicht13, Aufsicht14, Aufsicht15, Aufsicht16, Aufsicht17, Aufsicht18, Aufsicht19,
         Aufsicht20])

    Raum1 = Raum(name="AM2", groesse="60")
    Raum2 = Raum(name="AM1", groesse="80")
    Raum3 = Raum(name="18.1.01", groesse="30")
    Raum4 = Raum(name="18.1.03", groesse="35")
    Raum5 = Raum(name="AM3", groesse="60")
    Raum6 = Raum(name="18.1.04", groesse="30")
    Raum7 = Raum(name="17.1.01", groesse="30")
    Raum8 = Raum(name="17.1.02", groesse="35")
    Raum9 = Raum(name="17.1.03", groesse="40")
    Raum10 = Raum(name="19.1.01", groesse="35")
    Raum11 = Raum(name="19.1.02", groesse="30")
    Raum12 = Raum(name="19.1.03", groesse="40")
    Raum13 = Raum(name="19.1.04", groesse="50")
    Raum14 = Raum(name="19.1.05", groesse="60")
    Raum15 = Raum(name="19.1.06", groesse="25")
    Raum16 = Raum(name="19.1.07", groesse="30")
    Raum17 = Raum(name="AM3", groesse="70")
    Raum18 = Raum(name="AM5", groesse="80")
    Raum19 = Raum(name="AM6", groesse="70")
    Raum20 = Raum(name="21.0.01", groesse="70")
    Raum21 = Raum(name="21.0.02", groesse="80")
    Raum22 = Raum(name="21.0.03", groesse="70")
    Raum23 = Raum(name="KM1", groesse="70")
    Raum24 = Raum(name="KM1", groesse="80")
    Raum25 = Raum(name="KM2", groesse="70")
    Raum26 = Raum(name="23.0.01", groesse="70")
    Raum27 = Raum(name="23.0.02", groesse="80")
    Raum28 = Raum(name="23.0.03", groesse="70")

    Raum1.nicht_verfuegbare_zeitslots.extend([zeitslotByID(session, 1), zeitslotByID(session, 2)])
    Raum2.nicht_verfuegbare_zeitslots.extend([ZeitSlot(pruefungstag_nummer=0, slotTag_nummer=2)])
    Raum3.nicht_verfuegbare_zeitslots.extend([ZeitSlot(pruefungstag_nummer=0, slotTag_nummer=3)])
    Raum4.nicht_verfuegbare_zeitslots.extend([ZeitSlot(pruefungstag_nummer=0, slotTag_nummer=1)])

    session.add_all(
        [Raum1, Raum2, Raum3, Raum4, Raum5, Raum6, Raum7, Raum8, Raum9, Raum10, Raum11, Raum12, Raum13, Raum14, Raum15,
         Raum16, Raum17, Raum18, Raum19, Raum20, Raum21, Raum22, Raum23, Raum24, Raum25, Raum26, Raum27, Raum28])

    SemesterGruppe1 = SemesterGruppe(name="inf1", studiengang=1)
    SemesterGruppe2 = SemesterGruppe(name="inf3", studiengang=1)
    SemesterGruppe3 = SemesterGruppe(name="inf5", studiengang=1)
    SemesterGruppe4 = SemesterGruppe(name="inf2", studiengang=1)
    SemesterGruppe5 = SemesterGruppe(name="inf4", studiengang=1)
    SemesterGruppe6 = SemesterGruppe(name="AET1", studiengang=2)
    SemesterGruppe7 = SemesterGruppe(name="AET2", studiengang=2)
    SemesterGruppe8 = SemesterGruppe(name="ITB6", studiengang=3)
    SemesterGruppe9 = SemesterGruppe(name="ITB7", studiengang=3)
    SemesterGruppe10 = SemesterGruppe(name="ITD1", studiengang=4)
    SemesterGruppe11 = SemesterGruppe(name="ITD2", studiengang=4)
    SemesterGruppe12 = SemesterGruppe(name="ITD3", studiengang=4)
    SemesterGruppe13 = SemesterGruppe(name="ITD4", studiengang=4)
    SemesterGruppe14 = SemesterGruppe(name="ITD6", studiengang=4)
    SemesterGruppe15 = SemesterGruppe(name="ITD7", studiengang=4)
    EKS1 = SemesterGruppe(name="EKS1", studiengang=5)
    EKS2 = SemesterGruppe(name="EKS2", studiengang=5)
    EKS3 = SemesterGruppe(name="EKS3", studiengang=5)
    EKS4 = SemesterGruppe(name="EKS4", studiengang=5)
    EKS5 = SemesterGruppe(name="EKS5", studiengang=5)
    EKS6 = SemesterGruppe(name="EKS6", studiengang=5)
    AI1 = SemesterGruppe(name="AI1", studiengang=6)
    AI2 = SemesterGruppe(name="AI2", studiengang=6)
    AI3 = SemesterGruppe(name="AI3", studiengang=6)
    ISE4 = SemesterGruppe(name="ISE4", studiengang=7)
    ISE5 = SemesterGruppe(name="ISE5", studiengang=7)
    ISE6 = SemesterGruppe(name="ISE6", studiengang=7)

    Studiengang1 = Studiengang(name="Informatik/Softwaretechnik", kurzform="Inf/Swt")
    Studiengang2 = Studiengang(name="Allgemeine Elektrotechnik", kurzform="AET")
    Studiengang3 = Studiengang(name="Information Technology", kurzform="ITECH")
    Studiengang4 = Studiengang(name="Informationstechnologie und Design", kurzform="ITD")
    Studiengang5 = Studiengang(name="Elektrotechnik - Kommunikationssysteme", kurzform="EKS")
    Studiengang6 = Studiengang(name="Angewandte Informationstechnik", kurzform="AI")
    Studiengang7 = Studiengang(name="Internationales Studium Elektrotechnik", kurzform="ISE")
    # Inf 1 Semester
    Pruefung1 = neuePrüfung("Mathematik 1", "Ma1", "SB112", 100,0)
    Pruefung2 = neuePrüfung("Informatik 1", "Inf1", "SB122", 60,0)
    Pruefung3 = neuePrüfung("Datenbanken", "Db", "SB1142", 55,0)
    Pruefung4 = neuePrüfung("Programmieren 1", "Prog1", "SB1152", 50,0)
    # Inf 3 Semester
    Pruefung5 = neuePrüfung("Softwaretechnik 1", "SWT1", "SB1162", 30,0)
    Pruefung6 = neuePrüfung("Rechnernetze", "RN", "SB1182", 35,0)
    Pruefung7 = neuePrüfung("Betriebssysteme", "BS", "SB1192", 40,0)
    Pruefung8 = neuePrüfung("Verteilte Systeme", "VSys", "SB1183", 45,0)
    # Inf 5 Semester
    Pruefung9 = neuePrüfung("Formale Sprachen", "Übs", "SB1163", 30,0)
    Pruefung10 = neuePrüfung("Rechnernetze2", "RN2", "SB1186", 35,0)
    Pruefung11 = neuePrüfung("Betriebssysteme2", "BS2", "SB1197", 40,0)
    Pruefung12 = neuePrüfung("Verteilte Systeme2", "VSys2", "SB1189", 45,0)

    # Inf 2
    Pruefung13 = neuePrüfung("Programmieren 2", "Prog 2", "SB1176", 50,0)
    Pruefung14 = neuePrüfung("Informatik 2", "Inf 2", "SB1276", 45,0)
    Pruefung15 = neuePrüfung("Mathematik II für Informatiker*innen", "Ma II Inf", "SB213", 45,0)
    Pruefung16 = neuePrüfung("Theoretische Informatik", "TI", "1203", 40,0)
    # inf 4
    Pruefung21 = neuePrüfung("Betriebswirtschaftslehre", "BWL", "25423", 60,0)
    Pruefung22 = neuePrüfung("Datenmanagement", "BWL", "26423", 30,0)

    # AET 1
    Pruefung17 = neuePrüfung("Physik", "Phy", "SB2176", 40,0)
    Pruefung18 = neuePrüfung("Grundlagen der Gleichstromtechnik", "GE 1", "SB2276", 45,0)
    Pruefung19 = neuePrüfung("Prozedurale Programmierung", "Prog 1", "12342", 40,0)
    Pruefung20 = neuePrüfung("Projekt- und Selbstmanagement", "PM_SM", "23423", 40,0)

    # AET 2
    Pruefung23 = neuePrüfung("Grundlagen der Wechselstromtechnik", "GEW 1", "1171", 35,0)
    Pruefung24 = neuePrüfung("Mathematik für Elektrotechniker", "MAE", "1160", 40,0)
    Pruefung25 = neuePrüfung("Digitaltechnik", "DT", "1191", 40,0)

    # ITB 1
    Pruefung26 = neuePrüfung("Computer Networks", "CN", "1111", 30,0)
    Pruefung27 = neuePrüfung("Distributed Systems", "DS", "1121", 25,0)
    Pruefung28 = neuePrüfung("Software Engineering II", "SEII", "131", 30,0)
    Pruefung29 = neuePrüfung("Digital Signal Processing", "PM_SM", "23423", 30,0)

    # ITB 2
    Pruefung30 = neuePrüfung("Network Security", "NES", "1111", 30,0)
    Pruefung31 = neuePrüfung("Internet Programming", "IP", "1121", 25,0)
    Pruefung32 = neuePrüfung("Principles of Compilers", "POC", "131", 30,0)
    Pruefung33 = neuePrüfung("Information Systems", "IT_SYS", "23423", 30,0)

    # ITD1
    Pruefung34 = neuePrüfung("Mathematik/Physik 1", "Ma/Phy", "1211", 35,0)
    Pruefung35 = neuePrüfung("Naturwissenschaftliche Grundlagen 1", "MNG 1", "1211", 30,0)
    Pruefung36 = neuePrüfung("Medientechnik", "MT", "1212", 40,0)
    Pruefung37 = neuePrüfung("Grundlagen Programmierung", "GProg", "1213", 45,0)

    # ITD2
    Pruefung38 = neuePrüfung("Mathematik/Physik 2", "Ma/Phy2", "1211", 45,0)
    Pruefung39 = neuePrüfung("Naturwissenschaftliche Grundlagen 2", "K2", "1211", 50,0)
    Pruefung40 = neuePrüfung("Digitale Systeme", "DSys", "1212", 40,0)
    Pruefung41 = neuePrüfung("Vertiefung Programmierung", "VProg", "1213", 45,0)
    # ITD3
    Pruefung42 = neuePrüfung("Konzeption interaktiver Medien", "KiM", "1211", 45,0)
    # ITD4
    Pruefung43 = neuePrüfung("Computernetze und Webtechnologien", "CuW", "1211", 45,0)
    Pruefung44 = neuePrüfung("Skriptbasierte Programmierung", "SProg", "1211", 25,0)
    # ITD6
    Pruefung45 = neuePrüfung("Betriebswirtschaftslehre", "BWL", "1211", 45,0)
    # ITD7
    Pruefung46 = neuePrüfung("Gründungsmanagement", "GM", "1211", 45,0)
    Pruefung47 = neuePrüfung("IT-Recht", "IT-R", "1211", 45,0)

    # EKS1
    Pruefung48 = neuePrüfung("Mathematik EKS 1", "Ma E 1", "1211", 45,0)
    Pruefung49 = neuePrüfung("Physik", "Phy", "1211", 25,0)
    Pruefung50 = neuePrüfung("Grundlagen der Elektrotechnik I", "GE 1", "1211", 35,0)
    Pruefung51 = neuePrüfung("Grundlagen Gleichstrom", "GG", "1211", 35,0)

    Pruefung48.pruefung_Studiengang_table.append(Studiengang5)
    Pruefung49.pruefung_Studiengang_table.append(Studiengang5)
    Pruefung50.pruefung_Studiengang_table.append(Studiengang5)
    Pruefung51.pruefung_Studiengang_table.append(Studiengang5)
    Pruefung48.pruefung_SemesterGruppe_table.append(EKS1)
    Pruefung49.pruefung_SemesterGruppe_table.append(EKS1)
    Pruefung50.pruefung_SemesterGruppe_table.append(EKS1)
    Pruefung51.pruefung_SemesterGruppe_table.append(EKS1)
    # EKS2
    Pruefung52 = neuePrüfung("Mathematik EKS 2", "Ma E 2", "1211", 55,0)
    Pruefung53 = neuePrüfung("Physik 2", "Phy 2", "1211", 25,0)
    Pruefung54 = neuePrüfung("Grundlagen der Elektrotechnik II", "GE 2", "1211", 35,0)
    Pruefung55 = neuePrüfung("Grundlagen Wechselstrom", "GW", "1211", 35,0)
    Pruefung56 = neuePrüfung("Mikroprozessortechnik I", "MiP 1", "1122", 43,0)

    Pruefung52.pruefung_SemesterGruppe_table.append(EKS2)
    Pruefung53.pruefung_SemesterGruppe_table.append(EKS2)
    Pruefung54.pruefung_SemesterGruppe_table.append(EKS2)
    Pruefung55.pruefung_SemesterGruppe_table.append(EKS2)
    Pruefung56.pruefung_SemesterGruppe_table.append(EKS2)
    Pruefung52.pruefung_Studiengang_table.append(Studiengang5)
    Pruefung53.pruefung_Studiengang_table.append(Studiengang5)
    Pruefung54.pruefung_Studiengang_table.append(Studiengang5)
    Pruefung55.pruefung_Studiengang_table.append(Studiengang5)
    Pruefung56.pruefung_Studiengang_table.append(Studiengang5)

    # EKS3
    Pruefung57 = neuePrüfung("Mathematik EKS 3", "Ma E 3", "1211", 50,0)
    Pruefung58 = neuePrüfung("Physik 3", "Phy 3", "1211", 35,0)
    Pruefung59 = neuePrüfung("Grundlagen der Elektrotechnik III", "GE 3", "1211", 35,0)
    Pruefung60 = neuePrüfung("Grundlagen Wechselstrom", "GW 2", "1211", 45,0)
    Pruefung61 = neuePrüfung("Mikroprozessortechnik 3", "MiP 3", "1122", 46,0)

    Pruefung57.pruefung_SemesterGruppe_table.append(EKS3)
    Pruefung58.pruefung_SemesterGruppe_table.append(EKS3)
    Pruefung59.pruefung_SemesterGruppe_table.append(EKS3)
    Pruefung60.pruefung_SemesterGruppe_table.append(EKS3)
    Pruefung61.pruefung_SemesterGruppe_table.append(EKS3)
    Pruefung57.pruefung_Studiengang_table.append(Studiengang5)
    Pruefung58.pruefung_Studiengang_table.append(Studiengang5)
    Pruefung59.pruefung_Studiengang_table.append(Studiengang5)
    Pruefung60.pruefung_Studiengang_table.append(Studiengang5)
    Pruefung61.pruefung_Studiengang_table.append(Studiengang5)

    # EKS4
    Pruefung62 = neuePrüfung("Regelungstechnik", "RE", "1211", 30,0)
    Pruefung63 = neuePrüfung("Digitale Signalverarbeitung", "DSV", "1211", 35,0)
    Pruefung64 = neuePrüfung("Hochfrequenztechnik", "Hft", "1211", 35,0)
    Pruefung65 = neuePrüfung("Mikrowellentechnik", "MWT", "1211", 45,0)
    Pruefung66 = neuePrüfung("Rechnergestützer Schaltungsentwurf", "RGS", "1122", 36,0)

    Pruefung62.pruefung_SemesterGruppe_table.append(EKS4)
    Pruefung63.pruefung_SemesterGruppe_table.append(EKS4)
    Pruefung64.pruefung_SemesterGruppe_table.append(EKS4)
    Pruefung65.pruefung_SemesterGruppe_table.append(EKS4)
    Pruefung66.pruefung_SemesterGruppe_table.append(EKS4)
    Pruefung62.pruefung_Studiengang_table.append(Studiengang5)
    Pruefung63.pruefung_Studiengang_table.append(Studiengang5)
    Pruefung64.pruefung_Studiengang_table.append(Studiengang5)
    Pruefung65.pruefung_Studiengang_table.append(Studiengang5)
    Pruefung66.pruefung_Studiengang_table.append(Studiengang5)

    # EKS5
    Pruefung67 = neuePrüfung("Hochintegrierte Schaltung", "HIS", "1211", 20,0)
    Pruefung68 = neuePrüfung("Digitale Übertragungstechnik", "DÜT", "1211", 15,0)
    Pruefung69 = neuePrüfung("Kommunikationsnetze", "KN", "1211", 25,0)
    Pruefung70 = neuePrüfung("Hardwareentwurf", "HWE", "1211", 25,0)
    Pruefung71 = neuePrüfung("Eingebettete Systeme", "ESys", "1122", 26,0)

    Pruefung67.pruefung_SemesterGruppe_table.append(EKS5)
    Pruefung68.pruefung_SemesterGruppe_table.append(EKS5)
    Pruefung69.pruefung_SemesterGruppe_table.append(EKS5)
    Pruefung70.pruefung_SemesterGruppe_table.append(EKS5)
    Pruefung71.pruefung_SemesterGruppe_table.append(EKS5)
    Pruefung67.pruefung_Studiengang_table.append(Studiengang5)
    Pruefung68.pruefung_Studiengang_table.append(Studiengang5)
    Pruefung69.pruefung_Studiengang_table.append(Studiengang5)
    Pruefung70.pruefung_Studiengang_table.append(Studiengang5)
    Pruefung71.pruefung_Studiengang_table.append(Studiengang5)

    # EKS6
    Pruefung72 = neuePrüfung("Drahtlose Sensorsysteme", "DSys", "1211", 20,0)
    Pruefung73 = neuePrüfung("Sensortechnologien", "ST", "1211", 15,0)
    Pruefung74 = neuePrüfung("PC-Messtechnik", "PCM", "1211", 15,0)
    Pruefung75 = neuePrüfung("Elektromagnetische Verträglichkeit", "ElekV", "1211", 10,0)

    Pruefung72.pruefung_SemesterGruppe_table.append(EKS6)
    Pruefung73.pruefung_SemesterGruppe_table.append(EKS6)
    Pruefung74.pruefung_SemesterGruppe_table.append(EKS6)
    Pruefung75.pruefung_SemesterGruppe_table.append(EKS6)
    Pruefung72.pruefung_Studiengang_table.append(Studiengang5)
    Pruefung73.pruefung_Studiengang_table.append(Studiengang5)
    Pruefung74.pruefung_Studiengang_table.append(Studiengang5)
    Pruefung75.pruefung_Studiengang_table.append(Studiengang5)

    # AI1
    Pruefung76 = neuePrüfung("Rechnungswesen und Controlling", "RuC", "1211", 50,0)
    Pruefung77 = neuePrüfung("Angewandte Mathematik", "AMA", "1311", 55,0)
    Pruefung78 = neuePrüfung("Datenbanken/Information", "DuI", "1511", 50,0)
    Pruefung79 = neuePrüfung("Kommunikationstechnik", "Kt", "1211", 10,0)

    Pruefung76.pruefung_SemesterGruppe_table.append(AI1)
    Pruefung77.pruefung_SemesterGruppe_table.append(AI1)
    Pruefung78.pruefung_SemesterGruppe_table.append(AI1)
    Pruefung79.pruefung_SemesterGruppe_table.append(AI1)
    Pruefung76.pruefung_Studiengang_table.append(Studiengang6)
    Pruefung77.pruefung_Studiengang_table.append(Studiengang6)
    Pruefung78.pruefung_Studiengang_table.append(Studiengang6)
    Pruefung79.pruefung_Studiengang_table.append(Studiengang6)
    # AI2
    Pruefung80 = neuePrüfung("Rechnungswesen und Controlling 2", "RuC 2", "1211", 50,0)
    Pruefung81 = neuePrüfung("Angewandte Mathematik 2", "AMA 2", "1311", 55,0)
    Pruefung82 = neuePrüfung("Datenbanken/Information 2", "DuI 2", "1511", 50,0)
    Pruefung83 = neuePrüfung("Kommunikationstechnik 2", "Kt 2", "1211", 10,0)

    Pruefung80.pruefung_SemesterGruppe_table.append(AI2)
    Pruefung81.pruefung_SemesterGruppe_table.append(AI2)
    Pruefung82.pruefung_SemesterGruppe_table.append(AI2)
    Pruefung83.pruefung_SemesterGruppe_table.append(AI2)
    Pruefung80.pruefung_Studiengang_table.append(Studiengang6)
    Pruefung81.pruefung_Studiengang_table.append(Studiengang6)
    Pruefung82.pruefung_Studiengang_table.append(Studiengang6)
    Pruefung83.pruefung_Studiengang_table.append(Studiengang6)

    # AI3
    Pruefung84 = neuePrüfung("Rechnungswesen und Controlling 3", "RuC 3", "1211", 30,0)
    Pruefung85 = neuePrüfung("Angewandte Mathematik 3", "AMA 3", "1311", 45,0)
    Pruefung86 = neuePrüfung("Datenbanken/Information 3", "DuI 3", "1511", 40,0)
    Pruefung87 = neuePrüfung("Kommunikationstechnik 3", "Kt 3", "1211", 20,0)

    Pruefung84.pruefung_SemesterGruppe_table.append(AI3)
    Pruefung85.pruefung_SemesterGruppe_table.append(AI3)
    Pruefung86.pruefung_SemesterGruppe_table.append(AI3)
    Pruefung87.pruefung_SemesterGruppe_table.append(AI3)
    Pruefung84.pruefung_Studiengang_table.append(Studiengang6)
    Pruefung85.pruefung_Studiengang_table.append(Studiengang6)
    Pruefung86.pruefung_Studiengang_table.append(Studiengang6)
    Pruefung87.pruefung_Studiengang_table.append(Studiengang6)

    # ISE4
    Pruefung88 = neuePrüfung("Radio Frequencies", "RF", "1211", 30,0)
    Pruefung89 = neuePrüfung("Control Systems 1", "CS I", "1311", 45,0)
    Pruefung90 = neuePrüfung("Principles Communications I", "PC 1", "1511", 60,0)
    Pruefung91 = neuePrüfung("Analog Electronics II", "AE 2", "1211", 40,0)

    Pruefung88.pruefung_SemesterGruppe_table.append(ISE4)
    Pruefung89.pruefung_SemesterGruppe_table.append(ISE4)
    Pruefung90.pruefung_SemesterGruppe_table.append(ISE4)
    Pruefung91.pruefung_SemesterGruppe_table.append(ISE4)
    Pruefung88.pruefung_Studiengang_table.append(Studiengang7)
    Pruefung89.pruefung_Studiengang_table.append(Studiengang7)
    Pruefung90.pruefung_Studiengang_table.append(Studiengang7)
    Pruefung91.pruefung_Studiengang_table.append(Studiengang7)
    # ISE5
    Pruefung92 = neuePrüfung("Radio Frequencies 2", "RF 2", "1211", 30,0)
    Pruefung93 = neuePrüfung("Control Systems 2", "CS II", "1311", 45,0)
    Pruefung94 = neuePrüfung("Principles Communications II", "PC 2", "1511", 60,0)
    Pruefung95 = neuePrüfung("Analog Electronics III", "AE 3", "1211", 40,0)

    Pruefung92.pruefung_SemesterGruppe_table.append(ISE5)
    Pruefung93.pruefung_SemesterGruppe_table.append(ISE5)
    Pruefung94.pruefung_SemesterGruppe_table.append(ISE5)
    Pruefung95.pruefung_SemesterGruppe_table.append(ISE5)
    Pruefung92.pruefung_Studiengang_table.append(Studiengang7)
    Pruefung93.pruefung_Studiengang_table.append(Studiengang7)
    Pruefung94.pruefung_Studiengang_table.append(Studiengang7)
    Pruefung95.pruefung_Studiengang_table.append(Studiengang7)

    # ISE6
    Pruefung96 = neuePrüfung("Radio Frequencies 3", "RF 3", "1211", 30,0)
    Pruefung97 = neuePrüfung("Control Systems 3", "CS III", "1311", 45,0)
    Pruefung98 = neuePrüfung("Principles Communications III", "PC 3", "1511", 60,0)
    Pruefung99 = neuePrüfung("Analog Electronics IV", "AE 4", "1211", 40,0)

    Pruefung96.pruefung_SemesterGruppe_table.append(ISE6)
    Pruefung97.pruefung_SemesterGruppe_table.append(ISE6)
    Pruefung98.pruefung_SemesterGruppe_table.append(ISE6)
    Pruefung99.pruefung_SemesterGruppe_table.append(ISE6)
    Pruefung96.pruefung_Studiengang_table.append(Studiengang7)
    Pruefung97.pruefung_Studiengang_table.append(Studiengang7)
    Pruefung98.pruefung_Studiengang_table.append(Studiengang7)
    Pruefung99.pruefung_Studiengang_table.append(Studiengang7)
    # inf 1
    Pruefung1.pruefung_SemesterGruppe_table.append(SemesterGruppe1)
    Pruefung1.pruefung_SemesterGruppe_table.append(SemesterGruppe6)
    Pruefung2.pruefung_SemesterGruppe_table.append(SemesterGruppe1)
    Pruefung3.pruefung_SemesterGruppe_table.append(SemesterGruppe1)
    Pruefung4.pruefung_SemesterGruppe_table.append(SemesterGruppe1)
    # inf2
    Pruefung5.pruefung_SemesterGruppe_table.append(SemesterGruppe2)
    Pruefung6.pruefung_SemesterGruppe_table.append(SemesterGruppe2)
    Pruefung7.pruefung_SemesterGruppe_table.append(SemesterGruppe2)
    Pruefung8.pruefung_SemesterGruppe_table.append(SemesterGruppe2)
    # inf3
    Pruefung9.pruefung_SemesterGruppe_table.append(SemesterGruppe3)
    Pruefung10.pruefung_SemesterGruppe_table.append(SemesterGruppe3)
    Pruefung11.pruefung_SemesterGruppe_table.append(SemesterGruppe3)
    Pruefung12.pruefung_SemesterGruppe_table.append(SemesterGruppe3)
    # inf2
    Pruefung13.pruefung_SemesterGruppe_table.append(SemesterGruppe4)
    Pruefung14.pruefung_SemesterGruppe_table.append(SemesterGruppe4)
    Pruefung15.pruefung_SemesterGruppe_table.append(SemesterGruppe4)
    Pruefung16.pruefung_SemesterGruppe_table.append(SemesterGruppe4)
    # inf4
    Pruefung21.pruefung_SemesterGruppe_table.append(SemesterGruppe5)
    Pruefung22.pruefung_SemesterGruppe_table.append(SemesterGruppe5)

    # AET 1
    Pruefung17.pruefung_SemesterGruppe_table.append(SemesterGruppe6)
    Pruefung18.pruefung_SemesterGruppe_table.append(SemesterGruppe6)
    Pruefung19.pruefung_SemesterGruppe_table.append(SemesterGruppe6)
    Pruefung20.pruefung_SemesterGruppe_table.append(SemesterGruppe6)
    # AET2
    Pruefung23.pruefung_SemesterGruppe_table.append(SemesterGruppe7)
    Pruefung24.pruefung_SemesterGruppe_table.append(SemesterGruppe7)
    Pruefung25.pruefung_SemesterGruppe_table.append(SemesterGruppe7)
    # ITB 1
    Pruefung26.pruefung_SemesterGruppe_table.append(SemesterGruppe8)
    Pruefung27.pruefung_SemesterGruppe_table.append(SemesterGruppe8)
    Pruefung28.pruefung_SemesterGruppe_table.append(SemesterGruppe8)
    Pruefung29.pruefung_SemesterGruppe_table.append(SemesterGruppe8)
    # ITB 2
    Pruefung30.pruefung_SemesterGruppe_table.append(SemesterGruppe9)
    Pruefung31.pruefung_SemesterGruppe_table.append(SemesterGruppe9)
    Pruefung32.pruefung_SemesterGruppe_table.append(SemesterGruppe9)
    Pruefung33.pruefung_SemesterGruppe_table.append(SemesterGruppe9)
    # ITD 1
    Pruefung34.pruefung_SemesterGruppe_table.append(SemesterGruppe10)
    Pruefung35.pruefung_SemesterGruppe_table.append(SemesterGruppe10)
    Pruefung36.pruefung_SemesterGruppe_table.append(SemesterGruppe10)
    Pruefung37.pruefung_SemesterGruppe_table.append(SemesterGruppe10)
    # ITD 2
    Pruefung38.pruefung_SemesterGruppe_table.append(SemesterGruppe11)
    Pruefung39.pruefung_SemesterGruppe_table.append(SemesterGruppe11)
    Pruefung40.pruefung_SemesterGruppe_table.append(SemesterGruppe11)
    Pruefung41.pruefung_SemesterGruppe_table.append(SemesterGruppe11)
    # ITD 3
    Pruefung42.pruefung_SemesterGruppe_table.append(SemesterGruppe12)
    # ITD 4
    Pruefung43.pruefung_SemesterGruppe_table.append(SemesterGruppe13)
    Pruefung44.pruefung_SemesterGruppe_table.append(SemesterGruppe13)
    # ITD 6
    Pruefung45.pruefung_SemesterGruppe_table.append(SemesterGruppe14)
    # ITD 7
    Pruefung46.pruefung_SemesterGruppe_table.append(SemesterGruppe15)
    Pruefung47.pruefung_SemesterGruppe_table.append(SemesterGruppe15)
    # Studiengänge
    Pruefung1.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung1.pruefung_Studiengang_table.append(Studiengang2)
    Pruefung2.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung3.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung4.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung5.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung6.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung7.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung8.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung9.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung10.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung11.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung12.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung13.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung14.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung15.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung16.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung17.pruefung_Studiengang_table.append(Studiengang2)
    Pruefung18.pruefung_Studiengang_table.append(Studiengang2)
    Pruefung19.pruefung_Studiengang_table.append(Studiengang2)
    Pruefung20.pruefung_Studiengang_table.append(Studiengang2)
    Pruefung21.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung22.pruefung_Studiengang_table.append(Studiengang1)
    Pruefung23.pruefung_Studiengang_table.append(Studiengang2)
    Pruefung24.pruefung_Studiengang_table.append(Studiengang2)
    Pruefung25.pruefung_Studiengang_table.append(Studiengang2)
    Pruefung26.pruefung_Studiengang_table.append(Studiengang3)
    Pruefung27.pruefung_Studiengang_table.append(Studiengang3)
    Pruefung28.pruefung_Studiengang_table.append(Studiengang3)
    Pruefung29.pruefung_Studiengang_table.append(Studiengang3)
    Pruefung30.pruefung_Studiengang_table.append(Studiengang3)
    Pruefung31.pruefung_Studiengang_table.append(Studiengang3)
    Pruefung32.pruefung_Studiengang_table.append(Studiengang3)
    Pruefung33.pruefung_Studiengang_table.append(Studiengang3)
    Pruefung34.pruefung_Studiengang_table.append(Studiengang4)
    Pruefung35.pruefung_Studiengang_table.append(Studiengang4)
    Pruefung36.pruefung_Studiengang_table.append(Studiengang4)
    Pruefung37.pruefung_Studiengang_table.append(Studiengang4)
    Pruefung38.pruefung_Studiengang_table.append(Studiengang4)
    Pruefung39.pruefung_Studiengang_table.append(Studiengang4)
    Pruefung40.pruefung_Studiengang_table.append(Studiengang4)
    Pruefung41.pruefung_Studiengang_table.append(Studiengang4)
    Pruefung42.pruefung_Studiengang_table.append(Studiengang4)
    Pruefung43.pruefung_Studiengang_table.append(Studiengang4)
    Pruefung44.pruefung_Studiengang_table.append(Studiengang4)
    Pruefung45.pruefung_Studiengang_table.append(Studiengang4)
    Pruefung47.pruefung_Studiengang_table.append(Studiengang4)

    session.add_all(
        [Pruefung1, Pruefung2, Pruefung3, Pruefung4, Pruefung5, Pruefung6, Pruefung7, Pruefung8, Pruefung9, Pruefung10,
         Pruefung11, Pruefung12, Pruefung13, Pruefung14, Pruefung15, Pruefung16, Pruefung17, Pruefung18, Pruefung19,
         Pruefung20, Pruefung21, Pruefung22, Pruefung23, Pruefung24, Pruefung25, Pruefung26, Pruefung27, Pruefung28,
         Pruefung29, Pruefung30, Pruefung31, Pruefung32, Pruefung33, Pruefung34, Pruefung35, Pruefung36, Pruefung37,
         Pruefung38, Pruefung39, Pruefung40, Pruefung41, Pruefung42, Pruefung43, Pruefung44, Pruefung45, Pruefung46,
         Pruefung47, Pruefung48, Pruefung49, Pruefung50, Pruefung51, Pruefung52, Pruefung53, Pruefung54, Pruefung55,
         Pruefung56, Pruefung57, Pruefung58, Pruefung59, Pruefung60, Pruefung61, Pruefung62, Pruefung63, Pruefung64,
         Pruefung65, Pruefung66, Pruefung67, Pruefung68, Pruefung70, Pruefung71, Pruefung72, Pruefung73, Pruefung74,
         Pruefung75, Pruefung76, Pruefung77, Pruefung78, Pruefung79, Pruefung80, Pruefung81, Pruefung82, Pruefung83,
         Pruefung84, Pruefung85, Pruefung86, Pruefung87, Pruefung88, Pruefung89, Pruefung90, Pruefung91, Pruefung92,
         Pruefung93, Pruefung94, Pruefung95, Pruefung96, Pruefung97, Pruefung98, Pruefung99])
    session.add_all([Studiengang1, Studiengang2, Studiengang3, Studiengang4, Studiengang5, Studiengang6, Studiengang7])
    session.add_all(
        [SemesterGruppe1, SemesterGruppe2, SemesterGruppe3, SemesterGruppe4, SemesterGruppe5, SemesterGruppe6,
         SemesterGruppe7, SemesterGruppe8, SemesterGruppe9, SemesterGruppe10, SemesterGruppe11, SemesterGruppe12,
         SemesterGruppe13, SemesterGruppe14, SemesterGruppe15, EKS1, EKS2, EKS3, EKS4, EKS5, EKS6, AI1, AI2, ISE4, ISE5,
         ISE6])

    session.commit()


if __name__ == '__main__':
    engine = create_engine("sqlite:///" + ORM.NAME + "?check_same_thread=False", echo=False)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    # drop Table
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # Funktionen zur Erzeugung von Testdaten
    #kleine Testdaten 5 Prüfungen
    genTestDatenKlein(session)
    #große Testdaten 98 Prüfungen
    #genTestDatenGroß(session)
    #Mittlere Testdaten ~25 Klausuren
    #genTestDatenMittel(session)

    # Ausgabe, Auflistung aller Aufsichten,Räume,Prüfungen und Semestergruppen
    aufsichten = session.query(Aufsicht)
    print(*aufsichten, sep="\n")

    raeume = session.query(Raum)
    print(*raeume, sep="\n")

    pruefungen = session.query(Pruefung)
    print(*pruefungen, sep="\n")

    SemesterGruppe = session.query(SemesterGruppe)
    print(*SemesterGruppe, sep="\n")
