from typing import Optional
from sqlalchemy import exists
from sqlalchemy.orm import Session
from src.models.version_group import VersionGroup
from src.repository.abstract_repository import AbstractRepository

class VersionGroupRepository(AbstractRepository):

    def save(self, session: Session, entity: VersionGroup)-> None:
        session.add(entity)

    def exists_by_name(self, session: Session, name: str)-> bool:
        return session.query(exists().where(VersionGroup.name == name)).scalar()
    
    def find_by_name(self, session: Session, name: str)-> Optional[VersionGroup]:
        return session.query(VersionGroup).filter_by(name=name).first()