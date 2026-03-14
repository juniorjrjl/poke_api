from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from src.models.config.db import Base

class FormMove(Base):
    __tablename__ = "form_moves"

    form_id = Column(Integer, ForeignKey('pokemon_forms.id'), primary_key=True)
    move_id = Column(Integer, ForeignKey('moves.id'), primary_key=True)
    version_group_id = Column(Integer, ForeignKey("version_groups.id"), primary_key=True)
    move_learn_method = Column(String(50), nullable=False)
    level_learned_at = Column(Integer, nullable=True)
    form = relationship("PokemonForm", back_populates="form_moves")
    move = relationship("Move", back_populates="form_moves")
    version_group = relationship("VersionGroup", back_populates="form_moves")
