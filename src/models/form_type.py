from sqlalchemy import Column, Integer, ForeignKey

from src.models.config.db import Base

class FormType(Base):
    __tablename__ = "form_types"

    form_id = Column(Integer, ForeignKey('pokemon_forms.id'), primary_key=True)
    type_id = Column(Integer, ForeignKey('types.id'), primary_key=True)
