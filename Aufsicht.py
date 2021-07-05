from Base import Base
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

# Zeitslots zu denen eine Aufsicht nicht verplant werden kann.
nicht_verfuegbar_table = Table('nicht_verfuegbare_aufsicht_zeitslots', Base.metadata,
                               Column('aufsicht_id', Integer, ForeignKey('aufsicht.id')),
                               Column('zeitslot_id', Integer, ForeignKey('zeitslot.id'))
                               )


class Aufsicht(Base):
    """
           Klasse zur Darstellung einer Aufsicht im Prüfungsplan
           Aufsichten werden mittels ID zugeordnet
    """

    # Tabellenname
    __tablename__ = 'aufsicht'

    # Primär Schlüssel ID der Aufsicht.
    id = Column(Integer, primary_key=True)

    # Name der Person
    name = Column(String)

    # Kurzform für den Namen im Prüfungsplan
    kurzform = Column(String)

    # Liste von nicht verfügbaren ZeitSlots
    nicht_verfuegbare_aufsicht_zeitslots = relationship("ZeitSlot",
                                                    secondary=nicht_verfuegbar_table,
                                                    cascade="all,delete")

    def __repr__(self):
        """
        String Ausgabe einer Aufischt
        Bsp: "Aufsicht(ID= 2 , Name= Max Mustermann , Kurz = Mus)"

        """
        return "Aufsicht(ID= %s , Name= %s , Kurz = %s)" % (self.id, self.name, self.kurzform)


