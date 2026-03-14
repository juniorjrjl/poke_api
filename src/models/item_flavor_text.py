from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from src.models.config.db import Base

class ItemFlavorText(Base):
    __tablename__ = "item_flavor_texts"

    item_id = Column(Integer, ForeignKey("items.id"), primary_key=True)
    version_group_id = Column(Integer, ForeignKey("version_groups.id"), primary_key=True)
    text = Column(String(255), nullable=False)

    item = relationship("Item", back_populates="flavor_texts")
    version_group = relationship("VersionGroup", back_populates="item_flavor_texts")
