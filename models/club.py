from sqlalchemy import Column, Integer, String
from sqlalchemy import event
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import reconstructor, relationship
from sqlalchemy.orm.session import Session

from . import Base
from .entry import Entry
from .player import Player


class Club(Base):
    __tablename__ = 'Club'

    @reconstructor
    def init_on_load(self):
        self._points = None

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    player_ids = relationship('Player', back_populates='club_id')

    @hybrid_property
    def entriesTEST(self):  # TODO Rename w/ `entry_ids`?
        return (self.session.query(Club, Player, Entry).filter_by(id=self.id)
                .join(Player, Club.player_ids)
                .join(Entry, Player.entry_ids)
                .from_self(Entry).all())

    @hybrid_property
    def points(self):
        if self._points is None:
            self._points = sum(player.points for player in self.player_ids)
        return self._points

    @property
    def session(self):
        return Session.object_session(self)

    def __repr__(self):
        return f'<Club#{self.id}({self.name})>'

    def __str__(self):
        return f'{self.name}'

@event.listens_for(Player, 'expire')
def receive_expire(target, attrs):
    # help: https://docs.sqlalchemy.org/en/14/orm/events.html#sqlalchemy.orm.InstanceEvents.expire
    target._points = None
