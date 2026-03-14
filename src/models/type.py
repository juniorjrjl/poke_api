from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.models.config.db import Base
from src.models.form_type import FormType

class Type(Base):
    __tablename__ = "types"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

Type.forms = relationship(
    'PokemonForm',
    secondary=FormType.__table__,
    back_populates="types"
)