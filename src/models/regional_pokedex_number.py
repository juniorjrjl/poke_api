from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.models.config.db import Base

class RegionalPokedexNumber(Base):
    __tablename__ = "regional_pokedex_numbers"

    id = Column(Integer, primary_key=True)
    specie_id = Column(Integer, ForeignKey("pokemon_species.id"), nullable=False)
    pokedex_name = Column(String(50), nullable=False)
    entry_number = Column(Integer, nullable=False)

    species = relationship("PokemonSpecie", back_populates="regional_numbers")