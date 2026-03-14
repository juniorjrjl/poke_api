from src.models.item_machine import ItemMachine
from src.repository.abstract_repository import AbstractRepository
from sqlalchemy import exists, and_
from sqlalchemy.orm import Session

class ItemMachineRepository(AbstractRepository):

    def batch_save(self, session: Session, entities: list[ItemMachine])-> None:
        session.bulk_save_objects(entities)

    def exists_by_primary_key(self, session: Session, item_id: int, move_id: int, version_group_id: int)-> bool:
        return session.query(
            exists()
            .where(
                and_(ItemMachine.item_id == item_id, ItemMachine.move_id == move_id, ItemMachine.version_group_id == version_group_id)
                )).scalar() 