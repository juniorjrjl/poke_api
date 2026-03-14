from typing import Optional
from sqlalchemy.orm import Session
from src.models.generation import Generation
from src.repository.abstract_repository import AbstractRepository


class GenerationRepository(AbstractRepository):

    def save(self, session: Session, entity: Generation)-> None:
        session.add(entity)

    def find_by_region(self, session: Session, region: str)-> Optional[Generation]:
        return session.query(Generation).filter_by(region=region).first()
    
    def find_by_name(self, session: Session, name: str)-> Optional[Generation]:
        return session.query(Generation).filter_by(name=name).first()
    
    def find_all(self, session: Session) -> list[Generation]:
        return session.query(Generation).order_by(Generation.id).all()
