import Raum
from Constraints import *
from Pruefung import Pruefung

PRUEFUNG = 0
RAUM = 1
AUFSICHT = 2


class Plan:

    def __init__(self, orm: ORM):

        self.orm = orm
        # map mit Prüfungen pro Zeitslot
        self.zeitSlotMap = {}

        for slot in orm.getZeitSlots():
            # Liste für jeden ZeitSlot
            self.zeitSlotMap[slot] = []

    # Prüfung der ZeitSlotMap hinzufügen
    def addPruefung(self, p: Pruefung, raum: Raum, aufsicht, slot):
        self.zeitSlotMap[slot].append((p, raum, aufsicht))

    # getter für ZeitSlotMap
    def getPlanMap(self):
        return self.zeitSlotMap

    # Räume von Prüfungen
    def getRaumVonPrüfung(self, pruefung):
        raeume = []
        for tupleList in self.zeitSlotMap.values():  # each tuple contains a lesson and the corresponding room
            for tu in tupleList:

                if tu[PRUEFUNG] == pruefung:
                    raeume.append(tu[RAUM])

        return raeume

    # Aufsichten von Prüfungen
    def getAufsichtVonPrüfung(self, pruefung):
        aufsichten = []
        for tupleList in self.zeitSlotMap.values():
            for tu in tupleList:
                if tu[PRUEFUNG] == pruefung:
                    aufsichten.append(tu[AUFSICHT])
        return aufsichten

    # ZeitSlot zu eine prüfung
    def getZeitSlotPruefung(self, pruefung):
        for i in self.zeitSlotMap.items():
            for tu in i[1]:
                if tu[PRUEFUNG] == pruefung:
                    return i[0]

    def getZeitMap(self):
            """
            Returns: zeitSlotMap für Validierung
            """
            return self.zeitSlotMap