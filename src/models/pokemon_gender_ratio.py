from sqlalchemy import DECIMAL, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.models.config.db import Base

class PokemonGenderRatio(Base):
    __tablename__ = "pokemon_gender_ratio"

    specie_id = Column(Integer, ForeignKey("pokemon_species.id"), primary_key=True)
    gender_id = Column(Integer, ForeignKey("genders.id"), primary_key=True)
    probability = Column(DECIMAL(5,2), nullable=False)

    gender = relationship("Gender", back_populates="pokemon_ratios")
    species = relationship("PokemonSpecie", back_populates="gender_ratios")
