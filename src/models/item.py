from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.models.config.db import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    price = Column(Integer, nullable=True)
    category = Column(String(50), nullable=True)
    fling_power = Column(Integer, nullable=True)
    fling_effect = Column(String(100), nullable=True)

    flavor_texts = relationship("ItemFlavorText", back_populates="item", cascade="all, delete-orphan")
    machines = relationship("ItemMachine", back_populates="item", cascade="all, delete-orphan")
