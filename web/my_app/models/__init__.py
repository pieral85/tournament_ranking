# from sqlalchemy.ext.declarative import declarative_base

# import tools.points_matrix as matrix

# # import ipdb
# # ipdb.set_trace()

# Base = declarative_base()
# points_dict = matrix.get_points_dict()
# test = 5

from .club import Club  # Solution #1
from .draw import Draw
from .entry import Entry
from .event import Event
from .link import Link
# from . import player  # Solution #2
from .player import Player  # Solution #1
from .match import Match
