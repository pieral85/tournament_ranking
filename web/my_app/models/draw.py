import enum

from sqlalchemy import Column, Integer, String  # , Enum
from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
# from sqlalchemy.orm.session import Session

from .. import Base  # from . import Base
# from .entry import Entry
# from .player import Player


class DrawType(enum.Enum):
    ELIMINATION = 1
    ROUND_ROBIN = 2


class Draw(Base):
    __tablename__ = 'Draw'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    event = Column(Integer, ForeignKey('Event.id'))
    event_id = relationship('Event', back_populates='draw_ids')
    drawtype = Column(Integer, nullable=False, default=0)  # Column(Enum(DrawType))
    drawsize = Column(Integer, nullable=False)
    match_ids = relationship('Match', back_populates='draw_id')
    link_ids = relationship('Link', back_populates='src_draw_id')

    @hybrid_property
    def drawtype_name(self):
        return DrawType(self.drawtype).name

    @hybrid_property
    def fullname(self):
        name = f'{self.event_id}'
        draw_name = f'{self}'
        if draw_name not in name:
            # name = f'{name} ({draw_name})'
            name += f' ({draw_name})'
        return name

    # @property
    # def session(self):
    #     return Session.object_session(self)

    # @hybrid_property
    # def entriesTEST(self):
    #     return (self.session.query(Club, Player, Entry).filter_by(id=self.id)
    #             .join(Player, Club.player_ids)
    #             .join(Entry, Player.entry_ids)
    #             .from_self(Entry).all())

    def __repr__(self):
        return f"<Draw#{self.id}({self.name})>"

    def __str__(self):
        return self.name
