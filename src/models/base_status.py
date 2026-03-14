from sqlalchemy import Column, ForeignKey, Integer

from src.models.config.db import Base

class BaseStatus(Base):
    __tablename__ = "base_status"

    form_id = Column(Integer, ForeignKey('pokemon_forms.id'), nullable=False, primary_key=True)
    hp = Column(Integer, nullable=False)
    attack = Column(Integer, nullable=False)
    defense = Column(Integer, nullable=False)
    special_attack = Column(Integer, nullable=False)
    special_defense = Column(Integer, nullable=False)
    speed = Column(Integer, nullable=False)
