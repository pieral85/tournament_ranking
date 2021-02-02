from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy import and_, event, or_
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import aliased, reconstructor, relationship
from sqlalchemy.orm.session import Session

from . import Base#, points_dict
from .match import Match
# from . import match


class Entry(Base):
    __tablename__ = 'Entry'

    @reconstructor
    def init_on_load(self):
        self._points = None

    id = Column(Integer, primary_key=True)
    # event = Column(Integer, ForeignKey('Event.id'))
    # eventBP = relationship('eventCls', back_populates='EntrysBP')
    player1 = Column(Integer, ForeignKey('Player.id'), nullable=False)  # TODO Implement , nullable=False in all required Column objects
    player2 = Column(Integer, ForeignKey('Player.id'), default=0)
    player1_id = relationship('Player', foreign_keys=[player1])  # back_populates='entries1BP', #foreign_keys='Entry.player1')
    player2_id = relationship('Player', foreign_keys=[player2])  # back_populates='entries2BP',  #foreign_keys='Entry.player2')
    # # <table FK column name> = Column(Integer, ForeignKey('ClubTN.id'))
    # club = Column(Integer, ForeignKey('Club.id'))
    # # club_id = relationship('<Club class name>', back_populates='EntrysBP')
    # club_id = relationship('Club', back_populates='EntrysBP')
    event = Column(Integer, ForeignKey('Event.id'), nullable=False)
    event_id = relationship('Event', back_populates='entry_ids')
    match_ids = relationship('Match', back_populates='entry_id')

    @hybrid_property
    def real_match_ids(self):
#         Good but it should return sth more "flat" instead
# [(<Match#829(MX C1 (Poule  2))>, <Match#836(MX C1 (Poule  2): F.Laporte + ...)>),
#  (<Match#829(MX C1 (Poule  2))>, <Match#834(MX C1 (Poule  2): F.Laporte +...)>),
#  (<Match#847(MX C1: A.Maquet + ...)>, None),
#  (<Match#849(MX C1: Q.Sold + ...)>, None)]
        # match_ = aliased(Match)
        # temp = (
        #     self.session.query(Match, match_)
        #     .select_from(Match)
        #     .join(match_, and_(Match.draw == match_.draw,
        #                        Match.planning == match_.van1), isouter=True)
        #     # .join(Entry, Match.entry_id)
        #     .filter(and_(Match.entry==self.id,
        #                  or_(Match.is_played, match_.is_played)))
        #     # .filter(Entry.id==self.id)
        #     # .all()# TODO Add filter: is_played
        # )
        # print(temp)
        # return temp.all()

        # Look at https://dokk.org/documentation/sqlalchemy/rel_1_0_18/orm/mapped_sql_expr/#using-column-property
        # The purpose is to let this attribute being called within a seach/join query
        match_ = aliased(Match)
        return (
            self.session.query(match_)
            .select_from(Match)
            .join(match_, and_(Match.draw == match_.draw,
                               Match.planning == match_.van1))
            .filter(and_(Match.entry==self.id,
                         match_.is_played))
        ).union(
            self.session.query(Match)
            .filter(and_(Match.entry==self.id,
                         Match.is_played))
        ).all()

    @hybrid_property
    def points(self):
        if self._points is None:
            self._points = 0
            # import ipdb; ipdb.set_trace()
            self._points = sum(match.get_points(self) for match in self.real_match_ids)
            # for match in real_match_ids:
            #     match_points = points_dict[match.index_match]
            #     if match.winning_entry_id == self:
            #         self._points += match_points.win
            #     elif match.losing_entry_id == self:
            #         self._points += match_points.loss
        return self._points

    @hybrid_property
    def player_ids(self):
        players = [self.player1_id]
        if self.player2_id:
            players.append(self.player2_id)
        return players

    @property
    def session(self):
        return Session.object_session(self)

    def __repr__(self):
        p2 = f' + {self.player2_id.fullname}' if self.player2_id else ''
        return f"<Entry#{self.id}({self.event_id}: {self.player1_id.fullname}{p2})>"

    def __str__(self):
        p2 = f' + {self.player2_id}' if self.player2_id else ''
        return f'{self.player1_id}{p2}'

@event.listens_for(Entry, 'expire')
def receive_expire(target, attrs):
    # help: https://docs.sqlalchemy.org/en/14/orm/events.html#sqlalchemy.orm.InstanceEvents.expire
    target._points = None
