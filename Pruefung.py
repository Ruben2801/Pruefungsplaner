from Base import Base
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, backref


pruefung_SemesterGruppe_table = Table('pruefung_semestergruppe_table', Base.metadata,
                                      Column('pruefung_id', Integer, ForeignKey('pruefung.id')),
                                      Column('semestergruppe_id', Integer, ForeignKey('semestergruppe.id'))
                                      )
pruefung_Studiengang_table = Table('pruefung_studiengang_table', Base.metadata,
                                   Column('pruefung_id', Integer, ForeignKey('pruefung.id')),
                                   Column('studiengang_id', Integer, ForeignKey('studiengang.id'))
                                   )


class Pruefung(Base):
    __tablename__ = 'pruefung'

    # Primär Schlüssel ID der Prüfung.
    id = Column(Integer, primary_key=True)

    # Name einer Prüfung
    name = Column(String)

    # Name einer Prüfung
    kurzform = Column(String)

    # Prüfungsnummer der Klausur
    pruefungsnummer = Column(Integer)

    # Teilnehmerzahl der Klausur
    teilnehmerzahl = Column(Integer)
    wunschtermin = Column(Integer, ForeignKey('zeitslot.id'), nullable=True)

    # Prüfungen Zuordnung zu Semestergruppen
    pruefung_SemesterGruppe_table = relationship("SemesterGruppe", secondary=pruefung_SemesterGruppe_table,
                                                 cascade="all,delete",
                                                 backref=backref("pruefungen", cascade="all,delete"))

    # Prüfungen Zuordnung zu Studiengängen
    pruefung_Studiengang_table = relationship("Studiengang", secondary=pruefung_Studiengang_table,
                                              cascade="all,delete", backref=backref("pruefungen", cascade="all,delete"))

    def __repr__(self):
        """
        Klasse zur Repräsentation einer Prüfung

        """
        return "Prüfung(id= %i , Name= %s , Prüfungsnummer= %s , Teilnehmerzahl= %s )" % \
               (self.id, self.name, self.pruefungsnummer, self.teilnehmerzahl)
