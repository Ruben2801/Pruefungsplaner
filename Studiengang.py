from Base import Base
from sqlalchemy import Column, Integer, String


class Studiengang(Base):
    """
           Klasse zur Darstellung eines Studiengangs
           Zu jedem Studiengang gehören mehrere Semestergruppe
           Bsp. Informatik/Softwaretechnik -> Inf1 - Inf6
    """
    __tablename__ = 'studiengang'

    # Primär Schlüssel ID der Studiengänge.
    id = Column(Integer, primary_key=True)

    # Name eines Studiengangs
    name = Column(String)

    # Abkürzung eines Studiengangs, benötigt für Plan.
    kurzform = Column(String)

    pruefungen = None

    def getPruefungen(self):
        """
        getter für alle Prüfungen eines Studiengangs
        Returns: Liste aller Prüfungen eines Studiengangs
        """
        return self.pruefungen

