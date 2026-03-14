from typing import Optional
from sqlalchemy import exists
from sqlalchemy.orm import Session
from src.models.gender import Gender
from src.repository.abstract_repository import AbstractRepository


class GenderRepository(AbstractRepository):

    def save(self, session: Session, entity: Gender)-> None:
        session.add(entity)

    def exists_by_name(self, session: Session, name: str)-> bool:
        return session.query(exists().where(Gender.name == name)).scalar()
    
    def find_by_name(self, session: Session, name: str) -> Optional[Gender]:
        return session.query(Gender).filter_by(name=name).first()

    def find_all(self, session: Session) -> list[Gender]:
        return session.query(Gender).all()

