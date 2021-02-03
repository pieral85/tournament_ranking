from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import and_, event, or_
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property, reconstructor, relationship
from sqlalchemy.orm.session import Session

from .. import Base  # from . import Base
from .entry import Entry
from .match import Match

# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()


class Player(Base):
    __tablename__ = 'Player'

    @reconstructor
    def init_on_load(self):
        self._points = None

    id = Column(Integer, primary_key=True)
    name = Column(String(50))  # String(50)
    firstname = Column(String(25))  # String(25)
    fullname = column_property(firstname + ' ' + name)  # TODO Choose fullname2 (hybrid_property) instead?
    # <table FK column name> = Column(Integer, ForeignKey('ClubTN.id'))
    club = Column(Integer, ForeignKey('Club.id'))
    # club_id = relationship('<Club class name>', back_populates='player_ids')
    club_id = relationship('Club', back_populates='player_ids')

    # entries1BP = relationship('Entry', back_populates='player1_id')
    # entries2BP = relationship('Entry', back_populates='player2_id')
    entry_ids = relationship('Entry',
                             primaryjoin="or_(Player.id==Entry.player1, Player.id==Entry.player2)")

    # @hybrid_property
    # def shortname(self):
    #     return f'{self.firstname[0]}. {self.name.upper()}'

    # TODO Delete if not used (real_match_ids could be more relevant)
    @hybrid_property
    def match_ids(self):
        return (
            self.session.query(Match)
            .join(Entry, Match.entry_id)
            .join(Player, or_(Entry.player1_id,
                              Entry.player2_id,))
            .filter(Player.id == self.id)
            # .filter(and_(Player.id == self.id, Match.is_played))  # TODO reactivate me once le reste est ok
            # .filter(and_(Player.id == self.id, Match.team1_id))  # TEST
            .all()
        )

    @hybrid_property
    def real_match_ids(self):
        matches = []
        for entry in self.entry_ids:
            matches += entry.real_match_ids
        return matches



    # @hybrid_property
    # def real_match_ids2(self):
    #     return (
    #         self.session.query(Match)
    #         .select_from(Player)
    #         # .filter_by(id=self.id)
    #         .join(Entry, Player.entry_ids)
    #         .join(Match, Entry.real_match_ids)  # 'real_match_ids' is not working (check Entry.real_match_ids for help)
    #         .all()
    #     )

    @hybrid_property
    def points(self):
        if self._points is None:
            self._points = sum(entry.points for entry in self.entry_ids)
        return self._points

    @property
    def session(self):
        return Session.object_session(self)

    def __repr__(self):
        return f'<Player#{self.id}({self.fullname})>'

    def __str__(self):
        # return f'{self.firstname} {self.name[:1]}.'
        return f'{self.firstname[0]}.{self.name}'

@event.listens_for(Player, 'expire')
def receive_expire(target, attrs):
    # help: https://docs.sqlalchemy.org/en/14/orm/events.html#sqlalchemy.orm.InstanceEvents.expire
    target._points = None
