from Base import Base
from sqlalchemy import Column, Integer


class ZeitSlot(Base):
    """
       Klasse zur Darstellung eines Zeitslots im Prüfungsplan
       Jeder Zeitslot hat die gleiche Länge. Während der Zeitslots finden Prüfungen statt
    """
    # Name der Tabelle in der Datenbank
    __tablename__ = 'zeitslot'

    # ID eines Zeitslots Primär Schlüssel, Verwendung in der Zuordnung
    id = Column(Integer, primary_key=True)

    # Zu welchem Prüfungstag der Zeitslot gehört
    pruefungstag_nummer = Column(Integer)

    # wievielter Slot eines Prüfungstages
    slotTag_nummer = Column(Integer)

    def __repr__(self):
        """
        String Repräsentation eines Zeitslots
        Bsp: ZeitSlot(id= 1, tag= 1, tagSlot = 2)
        """
        return "ZeitSlot(id= %s, tag= %s, tagSlot = %s)" % \
               (self.id, self.pruefungstag_nummer, self.slotTag_nummer,)
