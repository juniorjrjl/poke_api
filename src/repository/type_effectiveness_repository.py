from sqlalchemy import exists, and_
from sqlalchemy.orm import Session
from src.models.type_effectiveness import TypeEffectiveness
from src.repository.abstract_repository import AbstractRepository


class TypeEffectivenessRepository(AbstractRepository):

    def exists_by_primary_key(self, session: Session, attack_type_id: int, defense_type_id: int, generation_id: int)-> bool:
        return session.query(
            exists()
            .where(
                and_(
                    TypeEffectiveness.attack_type_id == attack_type_id, 
                    TypeEffectiveness.defense_type_id == defense_type_id
                    , TypeEffectiveness.generation_id == generation_id)
                )).scalar()
    
    def find_by_defense_type(self, session: Session, defense_type_id: int) -> list[TypeEffectiveness]:
        return session.query(TypeEffectiveness.attack_type_id).filter_by(defense_type_id=defense_type_id).all()
    
    def find_attack_ids_by_defense_and_generation(self, session: Session, defense_type_id: int, generation_id: int) -> list[int]:
        results = session.query(TypeEffectiveness.attack_type_id).filter(
            and_(
                TypeEffectiveness.defense_type_id == defense_type_id,
                TypeEffectiveness.generation_id == generation_id
            )
        ).all()
        return [row[0] for row in results]


    def save(self, session: Session, entity: TypeEffectiveness)-> None:
        session.add(entity)