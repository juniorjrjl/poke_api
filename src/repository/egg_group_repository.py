from typing import Optional
from sqlalchemy import exists
from sqlalchemy.orm import Session
from src.models.egg_group import EggGroup
from src.repository.abstract_repository import AbstractRepository


class EggGroupRepository(AbstractRepository):

    def save(self, session: Session, entity: EggGroup)-> None:
        session.add(entity)

    def existis_by_name(self, session: Session, name: str)-> bool:
        return session.query(exists().where(EggGroup.name == name)).scalar()
    
    def find_by_name(self, session: Session, name: str ) -> Optional[EggGroup]:
        return session.query(EggGroup).filter_by(name=name).first()

