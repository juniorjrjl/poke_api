from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.models.config.db import Base
from src.models.type import Type

class TypeEffectiveness(Base):
    __tablename__ = "type_effectiveness"

    attack_type_id = Column(Integer, ForeignKey('types.id'), primary_key=True)
    defense_type_id = Column(Integer, ForeignKey('types.id'), primary_key=True)
    generation_id = Column(Integer, ForeignKey('generations.id'), primary_key=True)
    multiplier = Column(Float, nullable=False)

    attack_type = relationship('Type', foreign_keys=[attack_type_id])
    defense_type = relationship('Type', foreign_keys=[defense_type_id])
    generation = relationship('Generation', foreign_keys=[generation_id])
