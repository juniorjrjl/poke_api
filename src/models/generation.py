from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.models.config.db import Base

class Generation(Base):
    __tablename__ = "generations"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    region = Column(String(100))
    generation_number = Column(Integer, nullable=True)
    release_year = Column(Integer, nullable=True)

    version_groups = relationship("VersionGroup", back_populates="generation")

