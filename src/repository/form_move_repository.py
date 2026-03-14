from sqlalchemy import exists, and_
from sqlalchemy.orm import Session
from src.models.form_move import FormMove
from src.repository.abstract_repository import AbstractRepository

class FormMoveRepository(AbstractRepository):

    def save(self, session: Session, entity: FormMove)-> None:
        session.add(entity)

    def exists_by_primary_key(self, session: Session, form_id: int, move_id: int, version_group_id: int) -> bool:
        return session.query(
            exists()
            .where(
                and_(FormMove.form_id == form_id, FormMove.move_id == move_id, FormMove.version_group_id == version_group_id)
                )).scalar()