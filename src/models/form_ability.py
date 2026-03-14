from sqlalchemy import Boolean, Column, Integer, ForeignKey

from src.models.config.db import Base

class FormAbility(Base):
    __tablename__ = "form_abilities"

    form_id = Column(Integer, ForeignKey('pokemon_forms.id'), primary_key=True)
    ability_id = Column(Integer, ForeignKey('abilities.id'), primary_key=True)
    is_hidden = Column(Boolean, default=False)
