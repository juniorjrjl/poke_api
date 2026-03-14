from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.models.config.db import Base

class EggGroup(Base):
    __tablename__ = "egg_groups"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    species = relationship("PokemonEggGroup", back_populates="egg_group")
