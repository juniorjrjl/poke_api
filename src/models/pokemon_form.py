from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.models.config.db import Base
from src.models.form_ability import FormAbility
from src.models.form_type import FormType

class PokemonForm(Base):
    __tablename__ = "pokemon_forms"

    id = Column(Integer, primary_key=True)
    specie_id = Column(Integer, ForeignKey('pokemon_species.id'), nullable=False)
    generation_id = Column(Integer, ForeignKey('generations.id'), nullable=False)
    form_name = Column(String(100))
    height = Column(Integer)
    weight = Column(Integer)
    base_experience = Column(Integer)
    is_default = Column(Boolean, default=False)

    types = relationship('Type', secondary=FormType.__table__, back_populates="forms")
    abilities = relationship('Ability', secondary=FormAbility.__table__, back_populates="forms")
    form_moves = relationship("FormMove", back_populates="form")
    sprites = relationship("PokemonSprite", back_populates="form", cascade="all, delete-orphan")