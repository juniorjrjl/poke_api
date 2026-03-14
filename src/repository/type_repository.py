from typing import Optional
from sqlalchemy.orm import Session

from src.models.type import Type
from src.repository.abstract_repository import AbstractRepository

class TypeRepository(AbstractRepository):

    def batch_save(self, session: Session, entities: list[Type])-> None:
        session.bulk_save_objects(entities)

    def get_names_already_stored(self, session: Session, names: list[str])-> list[str]:
        rows = session.query(Type.name).filter(Type.name.in_(names)).all()
        names = [r[0] for r in rows]
        return names

    def find_by_name(self, session: Session, name: str)-> Optional[Type]:
        return session.query(Type).filter_by(name=name).first()
    
    def find_all(self, session: Session)-> list[Type]:
        return session.query(Type).all()