from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.models.config.db import Base


class VersionGroup(Base):
    __tablename__ = "version_groups"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    generation_id = Column(Integer, ForeignKey("generations.id"), nullable=False)
    
    generation = relationship("Generation", back_populates="version_groups")
    form_moves = relationship("FormMove", back_populates="version_group")
    item_flavor_texts = relationship("ItemFlavorText", back_populates="version_group")
    item_machines = relationship("ItemMachine", back_populates="version_group")