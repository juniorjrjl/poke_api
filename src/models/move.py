from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from src.models.config.db import Base
from src.models.form_move import FormMove
from src.models.type import Type

class Move(Base):
    __tablename__ = "moves"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    power = Column(Integer)
    pp = Column(Integer)
    accuracy = Column(Integer)
    category = Column(String(20))
    critical_rate = Column(Integer)
    status = Column(String(50))
    status_chance = Column(Integer)
    effect_text = Column(Text)
    contact = Column(Boolean, default=False)
    type_id = Column(Integer, ForeignKey('types.id'))

    move_type = relationship('Type')
    form_moves = relationship("FormMove", back_populates="move")
