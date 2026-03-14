from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.models.config.db import Base

class Gender(Base):
    __tablename__ = "genders"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)

    pokemon_ratios = relationship("PokemonGenderRatio", back_populates="gender")
    sprites = relationship("PokemonSprite", back_populates="gender")
