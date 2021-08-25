from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .. import Base


class Court(Base):
    __tablename__ = 'Court'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    match_ids = relationship('Match', back_populates='court_id')

    def __repr__(self):
        return f"<Court#{self.id}({self.name})>"

    def __str__(self):
        return self.name
