from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.models.config.db import Base

class PokemonSpecie(Base):
    __tablename__ = "pokemon_species"

    id = Column(Integer, primary_key=True)
    pokedex_number = Column(Integer, nullable=False)
    name = Column(String(100), nullable=False)

    regional_numbers = relationship("RegionalPokedexNumber", back_populates="species", cascade="all, delete-orphan")
    gender_ratios = relationship("PokemonGenderRatio", back_populates="species")
    egg_groups = relationship("PokemonEggGroup", back_populates="species")
