from typing import Optional
from sqlalchemy.orm import Session
from src.models.move import Move
from src.repository.abstract_repository import AbstractRepository


class MoveRepository(AbstractRepository):

    def save(self, session: Session, entity: Move)-> None:
        session.add(entity)

    def get_names_already_stored(self, session: Session, names: list[str])-> list[str]:
        return session.query(Move.name).filter(Move.name.in_(names)).all()
    
    def find_by_name(self, session: Session, name: str)-> Optional[Move]:
        return session.query(Move).filter_by(name=name).first()