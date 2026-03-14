from sqlalchemy import exists, and_
from sqlalchemy.orm import Session
from src.models.form_ability import FormAbility
from src.repository.abstract_repository import AbstractRepository

class FormAbilityRepository(AbstractRepository):

    def save(self, session: Session, entity: FormAbility)-> None:
        session.add(entity)

    def exists_by_primary_key(self, session: Session, form_id: int, ability_id: int)-> bool:
        return session.query(
            exists()
            .where(
                and_(FormAbility.form_id == form_id, FormAbility.ability_id == ability_id)
                )).scalar()