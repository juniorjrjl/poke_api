from sqlalchemy import exists, and_
from sqlalchemy.orm import Session
from src.models.type_effectiveness import TypeEffectiveness
from src.repository.abstract_repository import AbstractRepository


class TypeEffectivenessRepository(AbstractRepository):

    def exists_by_primary_key(self, session: Session, attack_type_id: int, defense_type_id: int)-> bool:
        return session.query(
            exists()
            .where(
                and_(TypeEffectiveness.attack_type_id == attack_type_id, TypeEffectiveness.defense_type_id == defense_type_id)
                )).scalar()
    
    def find_by_defense_type(self, session: Session, defense_type_id: int) -> list[TypeEffectiveness]:
        return session.query(TypeEffectiveness.attack_type_id).filter_by(defense_type_id=defense_type_id).all()
    
    def save(self, session: Session, entity: TypeEffectiveness)-> None:
        session.add(entity)