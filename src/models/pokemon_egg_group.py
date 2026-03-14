from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.models.config.db import Base

class PokemonEggGroup(Base):
    __tablename__ = "pokemon_egg_groups"

    specie_id = Column(Integer, ForeignKey("pokemon_species.id"), primary_key=True)
    egg_group_id = Column(Integer, ForeignKey("egg_groups.id"), primary_key=True)


    egg_group = relationship("EggGroup", back_populates="species")
    species = relationship("PokemonSpecie", back_populates="egg_groups")
