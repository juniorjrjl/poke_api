from typing import Optional
from src.models.ability import Ability
from src.repository.abstract_repository import AbstractRepository
from sqlalchemy.orm import Session

class AbilityRepository(AbstractRepository):

    def batch_save(self, session: Session, entities: list[Ability])-> None:
        session.bulk_save_objects(entities)

    def get_names_already_stored(self, session: Session, names: list[str])-> list[str]:
        return session.query(Ability.name).filter(Ability.name.in_(names)).all()
    
    def find_by_name(self, session: Session, name: str )-> Optional[Ability]:
        return session.query(Ability).filter_by(name=name).first()
