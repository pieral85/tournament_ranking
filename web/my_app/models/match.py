import enum
from datetime import datetime as dt

from sqlalchemy import and_, Column, Boolean, DateTime, func, Integer, not_, or_  # , String  #  , Enum
from sqlalchemy import event, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.orm import aliased, reconstructor, relationship
from sqlalchemy.orm.exc import NoResultFound  # , MultipleResultsFound
from sqlalchemy.orm.session import Session

from .. import Base  # TODO import points_dict  # from . import Base, points_dict
# from .. import points_matrix  # working if "from ..tools import points_matrix" has been written in web/my_app/__init__.py
# from ... import tools  # working
from ...tools import points_matrix
# import tools.points_matrix as matrix

# 2020-01-28 from . import entry #from .entry import Entry
from .draw import Draw, DrawType
from .link import Link
# from .player import Player

points_dict = points_matrix.get_points_dict()
week_days = ('Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim')


class Winner(enum.Enum):
    none = 0
    team1 = 1
    team2 = 2


class ScoreStatus(enum.Enum):
    none = None
    walkover = 1
    retired = 2
    dist = 3
    no_match = 4
    promoted = 5


class Match(Base):
    __tablename__ = 'PlayerMatch'

    @reconstructor
    def init_on_load(self):
         # TODO regarder s'il ne serait pas possible de mettre TOUS ces paramètres à None par défaut
        self._previous_team_id = False  # False by default as it could become None as a query result
        self._previous_match_ids = None
        self._next_match_id = False  # False by default as it could become None as a query result
        self._index_team_init = None
        self._index_team_final = None
        self._gained_index = False
        self._index_match = None
        self._team1_id = False
        self._team2_id = False
        self._winning_entry_id = False
        self._losing_entry_id = False
        self._round_robin_match_ids = None

    id = Column(Integer, primary_key=True)
    # event  # useful? could be reached through draw_id.event isn't it?
    draw = Column(Integer, ForeignKey('Draw.id'))
    draw_id = relationship('Draw', back_populates='match_ids')
    draw_type = association_proxy('draw_id', 'drawtype')
    event = Column(Integer, ForeignKey('Event.id'))
    event_id = relationship('Event', back_populates='match_ids')
    entry = Column(Integer, ForeignKey('Entry.id'))
    entry_id = relationship('Entry', back_populates='match_ids')
    link = Column(Integer, ForeignKey('Link.id'))
    link_id = relationship('Link', back_populates='match_ids')

    winner = Column(Integer, default=0)  # Column(Enum(Winner))
    scorestatus = Column(Integer)
    # link
    # court
    court = Column(Integer, ForeignKey('Court.id'))
    court_id = relationship('Court', back_populates='match_ids')
    # # court.py: match_ids = relationship('Match', back_populates='court_id')
    # plandate Date/Heure
    # locatioh  # useful? could be reached through court.location isn't it?
    planning = Column(Integer)
    van1 = Column(Integer, default=0)
    van2 = Column(Integer, default=0)
    wn = Column(Integer, default=0)
    roundnr = Column(Integer)
    team1set1 = Column(Integer, default=0)
    team2set1 = Column(Integer, default=0)
    team1set2 = Column(Integer, default=0)
    team2set2 = Column(Integer, default=0)
    team1set3 = Column(Integer, default=0)
    team2set3 = Column(Integer, default=0)
    plandate = Column(DateTime)
    starttime = Column(DateTime)
    reversehomeaway = Column(Boolean)
    # name = Column(String(50))
    # player_ids = relationship('Player', back_populates='club_id')

    # @property
    # def session(self):
    #     return Session.object_session(self)

    @hybrid_property
    def gained_index(self):
        if self._gained_index == False:
            if self.draw_type == DrawType.ELIMINATION.value:
                self._gained_index = 1 if self.is_played else 0
            elif self.draw_type == DrawType.ROUND_ROBIN.value:
                if self.entry:
                    self._gained_index = len([m for m in self.round_robin_match_ids if m.is_played])
                else:
                    # import ipdb; ipdb.set_trace()  # Check truthyness of self.entry
                    # For "real" round robin matches, we don't consider gained index
                    self._gained_index = None
        return self._gained_index

    @hybrid_property
    def index_team_init(self):
        if self._index_team_init is None:
            print(f'  COMPUTING index_team_init for {self}')
            # if self.id in (392, 409):
            #     import ipdb; ipdb.set_trace()
            # WORKING for type==elimination
            # if self.draw_type == DrawType.ELIMINATION.value:
            #     # if self.previous_team_id is None:  # was not working when a team was "bye" at 1st round
            #     if not self.is_played:
            #         self._index_team_init = 0
            #     else:
            #         self._index_team_init = self.previous_team_id.index_team_init + 1
            # elif self.draw_type == DrawType.ROUND_ROBIN.value:
            #     self._index_team_init = -1  # TODO
            # else:
            #     raise NotImplementedError(f'{self}: unknown drawtype value ({self.draw_type})')

# ----- 2 -----
            # if self.draw_type == DrawType.ELIMINATION.value:
            if self.previous_team_id is None:
                self._index_team_init = 0
            elif self.draw_type == DrawType.ROUND_ROBIN.value and not self.entry:
                # For "real" round robin matches, we don't consider index team
                # import ipdb; ipdb.set_trace()  #TODO Check self.entry truthyness
                self._index_team_init = False
            else:
                # print('index_team_init', self)
                self._index_team_init = self.previous_team_id.index_team_final
                # if self.is_played:
                #     self._index_team_init += 1

            # if self.draw_type == DrawType.ROUND_ROBIN.value:
            #     if self.entry: # signifie que c'est l'en-tête de colonne dans les poules (en gros le type=RR et self.entry est Truthy)  # dans ce cas, _index_team_init représente l'index de l'équipe AVANT avoir fait les matchs de poule
            #         self._index_team_init += len(m for m in self.round_robin_match_ids if m.is_played)  # TODO existe-il une fct comme "filtered"?
            #     else:# signifie que c'est un match de poules: dans ce cas, index_team_init doit etre la somme des 2 index à la fin du tour précédent (très rare; la plupart du temps ces 2 index vaudront 0)
            #         _index = 0
            #         if self.my_team_id.previous_team_id is not None:  # INFO: my_team_id n'existe que pour des poules, lorsque self est réellement un match
            #             _index += self.my_team_id.previous_team_id.index_team_init
            #         if self.your_team_id.previous_team_id is not None:
            #             _index += self.your_team_id.previous_team_id.index_team_init
            #         self._index_team_init = _index
# -------------
        return self._index_team_init

    @hybrid_property
    def index_team_final(self):
        """ ... AFTER match(es) has been done """
        if self._index_team_final is None:
            print(f'  COMPUTING index_team_final for {self}')
            # if self.id in (392, 409):
            #     import ipdb; ipdb.set_trace()
            if self.draw_type == DrawType.ROUND_ROBIN.value and not self.entry:
                # import ipdb; ipdb.set_trace()  # Check truthyness of self.entry
                # For "real" round robin matches, we don't consider index team
                self._index_team_final = False
            else:
                # if self.id == 409:
                #     import ipdb; ipdb.set_trace()
                #     self._index_team_init = 0
                # else:
                #     self._index_team_final = self.index_team_init + self.gained_index
                self._index_team_final = self.index_team_init + self.gained_index
        return self._index_team_final

    @hybrid_property
    def index_match(self):
        if self._index_match is None:
            # print(f'  COMPUTING index_match for {self}')
            if self.draw_type == DrawType.ELIMINATION.value:
                # TODO Reactivate me and test me
                # if not self.is_played:
                #     self._index_match = False
                # else:
                self._index_match = sum(m.index_team_final for m in self.previous_match_ids)
            elif self.draw_type == DrawType.ROUND_ROBIN.value:
# ----- 3 -----
                if self.entry:
                    self._index_match = False
                else:
                    self._index_match = self.team1_id.index_team_init + self.team2_id.index_team_init
# -------------
            else:
                raise NotImplementedError(f'{self}: unknown drawtype value ({self.draw_type})')  # TODO we should not call this every time (add a setter on this field instead?)
        return self._index_match

    @hybrid_property
    def previous_team_id(self):
        # if self.id == 15:#pdb 30:
        #     import ipdb; i.set_trace()
        if self._previous_team_id == False:
            print(f'  COMPUTING previous_team_id for {self}')
            # if self.id in (392, 409):
            #     import ipdb; ipdb.set_trace()
            if self.draw_type == DrawType.ELIMINATION.value:
                print(f'   elimination')
                match_ = aliased(Match)
                try:
                    self._previous_team_id = (
                        self.session.query(match_)
                        .select_from(Match)
                        .filter_by(id=self.id)
                        .join(match_, and_(Match.entry == match_.entry,
                                           Match.planning == match_.wn))
                        .one_or_none()
                    )
                except:  # TODO Delete me once tests are ok
                    print('\nprevious_team_id ERROR!!!', self)# import ipdb; ipdb.set_trace()
                    test = (
                        self.session.query(match_)
                        .select_from(Match)
                        .filter_by(id=self.id)
                        .join(match_, and_(Match.draw == match_.draw,
                                           Match.planning == match_.wn))
                        .all()
                    )
            # elif self.draw_type == DrawType.ROUND_ROBIN.value:
            #     self._previous_team_id = None  # TODO
# ----- 1 -----
            if self.draw_type == DrawType.ROUND_ROBIN.value or self._previous_team_id is None:  # if RR or elimination with no previous_team found (could be from an existing previous round)
                print(f'   poules')
                if self.link and self.entry:
                    match_ = aliased(Match)
                    self._previous_team_id = (
                        self.session.query(match_)
                        .select_from(Match)
                        .filter_by(id=self.id)
                        .join(Link, Match.link_id)
                        # .join(match_, and_(match_.draw == Link.src_draw, match_.entry == self.entry))
                        .join(match_, match_.draw == Link.src_draw)
                        # .filter(and_(Match.draw == Link.src_draw, Match.entry == self.entry))
                        .filter(match_.entry == self.entry)
                        .order_by(Match.roundnr.desc())
                        .one_or_none()
                    )
                else:  # For "real" round robin matches, we consider there is no previous team
                    self._previous_team_id = None
# -------------
            # if self.id in (392, 409):
            # # if self.id == 392 and self._previous_team_id.id == 409:
            #     import ipdb; ipdb.set_trace()  # THIS NEEDS TO BE INVESTIGATED
            # Ensure there is no cyclic redundancy between current team (or draw) and "previous previous" team (or draw)
            # Otherwise, an infinite loop could happen while computing the `previous_team_id` of a match
            if self._previous_team_id and self._previous_team_id._previous_team_id:
                prev_team = self._previous_team_id._previous_team_id
                if self == prev_team:
                    # TODO Create custom error and manage it
                    raise ValueError(f'ERROR in event {self.event_id}: links {self.link_id} and {prev_team.link_id} \
                        are have circular entries. You must probably modify one of these links.')
                elif self.draw_id == prev_team.draw_id:
                    raise ValueError(f'Warning in event {self.event_id}: links {self.link_id} and {prev_team.link_id} \
                        are have circular draws. You should probably modify one of these links.')
        return self._previous_team_id

    @hybrid_property
    def previous_match_ids(self):
        if self._previous_match_ids is None:
            # print(f'  COMPUTING previous_match_ids for {self}')
            if self.draw_type == DrawType.ELIMINATION.value:
                match_ = aliased(Match)
                self._previous_match_ids = (
                    self.session.query(match_)
                    .select_from(Match)
                    .filter(and_(Match.id == self.id, Match.is_played))
                    .join(match_, and_(Match.draw == match_.draw,
                        or_(Match.van1 == match_.planning,
                            Match.van2 == match_.planning)))
                    .all()
                )
            elif self.draw_type == DrawType.ROUND_ROBIN.value:
# ----- 4 -----
                self._previous_match_ids = []  # pas de previous matchs dans les poules car l'ordre n'a pas de sens
# -------------
            else:
                raise NotImplementedError(f'{self}: unknown drawtype value ({self.draw_type})')
        return self._previous_match_ids

    @hybrid_property
    def round_robin_match_ids(self):
        # TODO Delete if not used
        if self._round_robin_match_ids is None:
            match_ = aliased(Match)
            self._round_robin_match_ids = (
                self.session.query(match_)
                .select_from(Match)
                .filter_by(id=self.id)
                .join(match_, and_(Match.draw == match_.draw,
                                   Match.planning == match_.van1))
                .all()
            )
        return self._round_robin_match_ids

    @hybrid_property
    def team1_id(self):
        if self._team1_id == False:
            match_ = aliased(Match)
            self._team1_id = (
                self.session.query(match_)
                .select_from(Match)
                .filter_by(id=self.id)
                .join(match_, and_(Match.draw == match_.draw,
                                   Match.van1 == match_.planning))
                .one_or_none()
            )
        return self._team1_id

    @hybrid_property
    def team2_id(self):
        if self._team2_id == False:
            match_ = aliased(Match)
            self._team2_id = (
                self.session.query(match_)
                .select_from(Match)
                .filter_by(id=self.id)
                .join(match_, and_(Match.draw == match_.draw,
                                   Match.van2 == match_.planning))
                .one_or_none()
            )
        return self._team2_id

    @hybrid_property
    def next_match_id(self):
        # TODO Delete if not used
        if self._next_match_id == False:
            # print(f'  COMPUTING next_match_id for {self}')
            if self.draw_type == DrawType.ELIMINATION.value:
                match_ = aliased(Match)
                self._next_match_id = (
                    self.session.query(match_)
                    .select_from(Match)
                    .filter_by(id=self.id)
                    .join(match_, and_(Match.draw == match_.draw,
                                       Match.wn == match_.planning))
                    .one_or_none()
                )
            elif self.draw_type == DrawType.ROUND_ROBIN.value:
                self._next_match_id = []  # TODO
            else:
                raise NotImplementedError(f'{self}: unknown drawtype value ({self.draw_type})')
        return self._next_match_id

    @hybrid_property
    def is_played(self):
        return bool(self.team1set1 or self.team2set1 or self.scorestatus != ScoreStatus.none.value)
    @is_played.expression
    def is_played(cls):
        return or_(cls.team1set1 > 0, cls.team2set1 > 0, cls.scorestatus != ScoreStatus.none.value)

    @hybrid_property
    def playing(self):
        return bool(self.court and self.team1set1 == 0 and self.team2set1 == 0 and self.scorestatus == ScoreStatus.none.value)
    @playing.expression
    def playing(cls):
        return and_(cls.court.isnot(None), cls.team1set1 == 0, cls.team2set1 == 0, cls.scorestatus == ScoreStatus.none.value)

    @hybrid_property
    def will_play(self):
        return bool(not self.court and self.is_planned and not self.reversehomeaway and self.team1set1 == 0 and self.team2set1 == 0 and self.scorestatus == ScoreStatus.none.value)
    @will_play.expression
    def will_play(cls):
        return and_(cls.court.is_(None), cls.is_planned, not_(cls.reversehomeaway), cls.team1set1 == 0, cls.team2set1 == 0, cls.scorestatus == ScoreStatus.none.value)

    @hybrid_property
    def id_internal(self):
        """

        :return: Custom identifier so that:
         - "fake" matches are 0 (matches which are not real ones)
         - "mirror" matches have the same value (round robin matches which oppose the same teams)
        """
        if self.van1 == 0 and self.van2 == 0:
            return ''
        return f'{self.draw}_{min(self.van1, self.van2)}_{max(self.van1, self.van2)}'

    # @hybrid_property
    # def winner_name(self):
    #     # TODO Hum, pas top d'utiliser `Winner.none.value`. Y aurait pas mieux?
    #     return None if self.winner == Winner.none.value else Winner(self.winner).name
    @hybrid_property
    def winning_entry_id(self):
        if self._winning_entry_id == False:
            if self.is_played and self.winner == Winner.none.value:
                self._winning_entry_id = None  # raise ValueError(f'{self}: `is_played` and `winner` attributes do not match.')
            if self.winner == Winner.none.value:
                self._winning_entry_id = None
            elif self.winner == Winner.team1.value:
                self._winning_entry_id = self.team1_id.entry_id
            elif self.winner == Winner.team2.value:
                self._winning_entry_id = self.team2_id.entry_id
        return self._winning_entry_id


    @hybrid_property
    def losing_entry_id(self):
        if self._losing_entry_id == False:
            if self.is_played and self.winner == Winner.none.value or \
               not self.is_played and self.winner != Winner.none.value:
                self._losing_entry_id = None # raise ValueError(f'{self}: `is_played` and `winner` attributes do not match.')
            if self.winner == Winner.none.value:
                self._losing_entry_id = None
            elif self.winner == Winner.team1.value:
                self._losing_entry_id = self.team2_id.entry_id
            elif self.winner == Winner.team2.value:
                self._losing_entry_id = self.team1_id.entry_id
        return self._losing_entry_id

    @hybrid_method
    def get_points(self, entry):
        structure = points_dict[self.index_match]
        if not entry or not self.is_played:
            return 0
        if entry == self.winning_entry_id:
            return structure.win
        elif entry == self.losing_entry_id:
            return structure.loss
        # elif self.is_played:
        return structure.win #raise ValueError(f'{self}: Cannot compute points for {entry}.')

    @hybrid_property
    def result(self):
        if self.winner == Winner.none.value:
            return None
        set3 = f' {self.team1set3}/{self.team2set3}' if self.team1set3 or self.team2set3 else ''
        return f'{self.team1set1}/{self.team2set1} {self.team1set2}/{self.team2set2}{set3}'

    @hybrid_property
    def is_planned(self):
        return self.plandate.year >= 1900  #TODO Better way to catch "empty" datetimes?
    @is_planned.expression
    def is_planned(cls):
        # print(cls, cls.plandate)
        return cls.plandate >= 1

    # TODO Test this property with records having false and true values
    @hybrid_property
    def is_started(self):
        return bool(self.starttime)
    @is_started.expression
    def is_started(cls):
        return cls.starttime != None

    @hybrid_property
    def plandate_str(self):
        if not self.is_planned:
            return ''
        day = week_days[dt.weekday(self.plandate)]
        return f'{day} {self.plandate:%H:%M}'

    @property
    def session(self):
        return Session.object_session(self)

    def __repr__(self):
        teams = f': {self.team1_id.entry_id}' if self.team1_id else ''
        teams += f' VS {self.team2_id.entry_id}' if self.team2_id else ''
        return f'<Match#{self.id}({self.draw_id.fullname}{teams})>'

@event.listens_for(Match, 'expire')
def receive_expire(target, attrs):
    if not target:
        return
    # help: https://docs.sqlalchemy.org/en/14/orm/events.html#sqlalchemy.orm.InstanceEvents.expire
    target._previous_team_id = False
    target._previous_match_ids = None
    target._next_match_id = False
    target._index_team_init = None
    target._index_team_final = None
    target._gained_index = False
    target._index_match = None
    target._team1_id = False
    target._team2_id = False
    target._winning_entry_id = False
    target._losing_entry_id = False
    target._round_robin_match_ids = None
