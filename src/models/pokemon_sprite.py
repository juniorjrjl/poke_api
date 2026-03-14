from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from src.models.config.db import Base

class PokemonSprite(Base):
    __tablename__ = "pokemon_sprites"

    form_id = Column(Integer, ForeignKey("pokemon_forms.id"), primary_key=True)
    gender_id = Column(Integer, ForeignKey("genders.id"), primary_key=True)
    is_shiny = Column(Boolean, nullable=False, default=False, primary_key=True)
    front_sprite = Column(String(255), nullable=True)
    back_sprite = Column(String(255), nullable=True)

    __table_args__ = (
        UniqueConstraint("form_id", "gender_id", "is_shiny", name="uq_form_gender_shiny"),
    )

    form = relationship("PokemonForm", back_populates="sprites")
    gender = relationship("Gender", back_populates="sprites")
