from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.models.config.db import Base

class ItemMachine(Base):
    __tablename__ = "item_machines"

    item_id = Column(Integer, ForeignKey("items.id"), primary_key=True)
    move_id = Column(Integer, ForeignKey("moves.id"), primary_key=True)
    version_group_id = Column(Integer, ForeignKey("version_groups.id"), primary_key=True, nullable=True)

    item = relationship("Item", back_populates="machines")
    move = relationship("Move")
    version_group = relationship("VersionGroup", back_populates="item_machines")
