from sqlalchemy import Boolean, Column, Integer, String, Text
from sqlalchemy.orm import relationship

from src.models.config.db import Base
from src.models.form_ability import FormAbility

class Ability(Base):
    __tablename__ = "abilities"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    effect_text = Column(Text, nullable=True)
    flavor_text = Column(Text, nullable=True) 

Ability.forms = relationship(
    'PokemonForm',
    secondary=FormAbility.__table__,
    back_populates="abilities"
)