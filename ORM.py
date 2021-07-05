from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Pruefung import Pruefung
from Aufsicht import Aufsicht
from Raum import Raum
from SemesterGruppe import SemesterGruppe
from Studiengang import Studiengang
from ZeitSlot import ZeitSlot
from Base import Base
from Helferfunktionen import *

# Anzahl der Prüfungstage die zu Verplanung stehen
PRUEFUNGSTAGE = 7

ZEITSLOTS_PRO_TAG = 4
#Starttag für die Prüfungstag
START = datetime(2021, 7, 19)
PT2 = datetime(2021, 7, 20)
PT3 = datetime(2021, 7, 21)
PT4 = datetime(2021, 7, 22)
PT5 = datetime(2021, 7, 23)
PT6 = datetime(2021, 7, 26)
PT7 = datetime(2021, 7, 27)
ZEITEN = ["8:15 - 9:45","10:00 - 11:30","12:00 - 13:30", "14:00 - 15:30"]

TAGE = []
TAGE.extend([START,PT2,PT3,PT4,PT5,PT6,PT7])




NAME = "PruefungsPlaner.db"


def init():
    global session
    global aufsicht
    global pruefungen
    global raeume
    global semesterGruppe
    global studiengang
    global zeitSlots

    engine = create_engine("sqlite:///" + NAME + "?check_same_thread=False", echo=True)

    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)

    aufsicht = list(session.query(Aufsicht).all())
    pruefungen = list(session.query(Pruefung).all())
    raeume = list(session.query(Raum).all())
    zeitSlots = list(session.query(ZeitSlot).all())
    semesterGruppe = list(session.query(SemesterGruppe).all())
    studiengang = list(session.query(Studiengang).all())


def getSession():
    """
    :return: Das Session Objekt
    """
    return session


def getRaeume():
    """
    :return: Alle Raum Objekte
    """
    return raeume
def getRaumByID(id):
    """

    :param id: raum ID
    :return: raum mit der ID id
    """
    return getRaeume()[id]


def getAufsichten():
    """
    :return: Alle Aufsicht Objekte
    """
    return aufsicht


def getPruefungen():
    """

    :return: Alle Prüfungen
    """
    return pruefungen
def getZeitSlots():

    return zeitSlots

def getZeitSlotProTag():
    """

    :return: Liste an Listen
    """
    tage = []

    for i in range(1,PRUEFUNGSTAGE):
        tag =list(filter(lambda z: z.pruefungstag_nummer == i,getZeitSlots()))
        tage.append(tag)


def getStudiengaenge():
    """

    :return: Alle Studiengang Objekte
    """
    return studiengang


def getSemesterGruppen():
    """

    :return: Alle SemesterGruppen Objekte
    """
    return semesterGruppe

