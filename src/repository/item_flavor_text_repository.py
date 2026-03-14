from sqlalchemy import exists, and_
from sqlalchemy.orm import Session
from src.models.item_flavor_text import ItemFlavorText
from src.repository.abstract_repository import AbstractRepository


class ItemFlavorTextRepository(AbstractRepository):

    def batch_save(self, session: Session, entities: list[ItemFlavorText])-> None:
        session.bulk_save_objects(entities)

    def exists_by_primary_key(self, session: Session, item_id: int, version_group_id: int)-> bool:
        return session.query(
            exists()
            .where(
                and_(ItemFlavorText.item_id == item_id, ItemFlavorText.version_group_id == version_group_id)
                )).scalar()