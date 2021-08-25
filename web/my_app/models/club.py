from sqlalchemy import Column, Integer, String
from sqlalchemy import event
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import reconstructor, relationship
from sqlalchemy.orm.session import Session

# from . import Base  # 2021-02-02
from .entry import Entry
from .player import Player

from .. import Base  # from my_app import Base  # this one also works
# =============================2021-02-02
# taken from https://www.digitalocean.com/community/tutorials/how-to-structure-large-flask-applications:
# from app import db

# Define a base model for other database tables to inherit
# class Club(db.Model):
#     pass
# =============================

class Club(Base):
    __tablename__ = 'Club'

    @reconstructor
    def init_on_load(self):
        self._points = None

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    player_ids = relationship('Player', back_populates='club_id')

    @hybrid_property
    def entry_ids(self):
        return (self.session.query(Club, Player, Entry).filter_by(id=self.id)
                .join(Player, Club.player_ids)
                .join(Entry, Player.entry_ids)
                .from_self(Entry).all())

    @hybrid_property
    def real_match_ids(self):
        matches = []
        for entry in self.entry_ids:
            matches += entry.real_match_ids
        return matches

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
    if not target:
        return
    target._points = None
