from sqlalchemy import exists, and_
from sqlalchemy.orm import Session
from src.models.evolution import Evolution
from src.repository.abstract_repository import AbstractRepository


class EvolutionRepository(AbstractRepository):

    def save(self, session: Session, entity: Evolution)-> None:
        session.add(entity)

    def exists_by_primary_key(self, session: Session, from_form_id: int, to_form_id: int)-> bool:
        return session.query(
            exists()
            .where(
                and_(Evolution.from_form_id == from_form_id, Evolution.to_form_id == to_form_id)
                )).scalar()