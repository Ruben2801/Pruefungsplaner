

from Base import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class SemesterGruppe(Base):
    """
           Klasse zur Darstellung eines Semestergruppe
           Zu jedem Studiengang gehören mehrere Semestergruppe
           Bsp. Informatik/Softwaretechnik -> Inf1 - Inf6
    """
    __tablename__ = 'semestergruppe'

    # Primär Schlüssel ID der Semestergruppen.
    id = Column(Integer, primary_key=True)

    # Name einer Semestergruppe
    name = Column(String)

    # Name des Studiengang
    studiengang = Column(Integer, ForeignKey('studiengang.id'))

    pruefungen = None

    def getPruefungen(self):
        """
        getter für alle Prüfungen einer Semestergruppe
        Returns: Liste aller Prüfungen einer SemesterGruppe
        """
        return self.pruefungen

    def __repr__(self):
        """
        String Repräsentation einer StudienGruppe
        "SemesterGroup(id= 1 , name= inf1 )"
        """
        return "SemesterGroup(id= %s , name= %s )" % \
               (self.id, self.name)
