from sqlalchemy import Column, ForeignKey, Integer, String
# from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
# from sqlalchemy.orm.session import Session

from .. import Base  # from . import Base


class Link(Base):
    __tablename__ = 'Link'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    src_draw = Column(Integer, ForeignKey('Draw.id'), default=0)
    src_draw_id = relationship('Draw', back_populates='link_ids')
    match_ids = relationship('Match', back_populates='link_id')

    def __repr__(self):
        return f"<Link#{self.id}({self.name})>"
