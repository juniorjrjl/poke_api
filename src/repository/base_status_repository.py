from sqlalchemy.orm import Session
from src.models.base_status import BaseStatus
from src.repository.abstract_repository import AbstractRepository

class BaseStatusRepository(AbstractRepository):

    def save(self, session: Session, entity: BaseStatus)-> None:
        session.add(entity)