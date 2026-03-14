from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.models.config.db import Base

class Evolution(Base):
    __tablename__ = "evolutions"

    from_form_id = Column(Integer, ForeignKey('pokemon_forms.id'), primary_key=True)
    to_form_id = Column(Integer, ForeignKey('pokemon_forms.id'), primary_key=True)
    evolution_level = Column(Integer)
    evolution_trigger = Column(String(50), nullable=True)
    evolution_condition = Column(String(255), nullable=True)
    evolution_item_id = Column(Integer, ForeignKey("items.id"), nullable=True)

    item = relationship("Item", lazy="joined")