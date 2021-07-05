from Base import Base
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

# Zeitslots zu denen ein Raum nicht verplant werden kann.
nicht_verfuegbar_raum_table = Table('nicht_verfuegbare_zeitslots', Base.metadata,
                                    Column('raum_id', Integer, ForeignKey('raum.id')),
                                    Column('zeitslot_id', Integer, ForeignKey('zeitslot.id'))
                                    )


class Raum(Base):
    """
           Klasse zur Darstellung eines Raumes im Prüfungsplan
           Räume werden mittels derer ID Prüfungen zugeordnet.
    """

    # Tabellenname
    __tablename__ = 'raum'

    # Primär Schlüssel ID der Räume.
    id = Column(Integer, primary_key=True)

    # Name eines Raums
    name = Column(String)

    # Raumgröße zum Vergleich mit späteren Teilnehmerzahlen
    groesse = Column(Integer)

    # Liste von nicht verfügbaren ZeitSlots
    nicht_verfuegbare_zeitslots = relationship("ZeitSlot",
                                               secondary=nicht_verfuegbar_raum_table,
                                               cascade="all,delete")

    def __repr__(self):
        """
        String Ausgabe eines Raums
        Bsp: "Raum(ID= 2 , Name= 18.1.01 )"

        """
        return "Raum(ID= %s , Name= %s )" % (self.id, self.name)
