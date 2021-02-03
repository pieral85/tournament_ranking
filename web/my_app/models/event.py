import enum

from sqlalchemy import Column, Integer, String  #  , Enum
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from .. import Base  # from . import Base


class Gender(enum.Enum):
    messieurs = 1
    dames = 2
    mixtes = 3


class Event(Base):
    __tablename__ = 'Event'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    gender = Column(Integer)  # Column(Enum(Gender))
    eventtype = Column(Integer)
    level = Column(Integer)
    entry_ids = relationship('Entry', back_populates='event_id')
    draw_ids = relationship('Draw', back_populates='event_id')
    match_ids = relationship('Match', back_populates='event_id')

    @hybrid_property
    def gender_name(self):
        return Gender(self.gender).name

    def __repr__(self):
        return f'<Event#{self.id}({self.name})>'

    def __str__(self):
        return self.name
