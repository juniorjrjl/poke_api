from typing import Optional
from sqlalchemy.orm import Session
from src.models.item import Item
from src.models.item_flavor_text import ItemFlavorText
from src.repository.abstract_repository import AbstractRepository

class ItemRepository(AbstractRepository):

    def batch_save(self, session: Session, entities: list[Item])-> None:
        session.bulk_save_objects(entities)

    def find_by_names(self, session: Session, names: list[str]) -> list[Item]:
        return session.query(Item.name).filter(Item.name.in_(names)).all()
    
    def find_by_name(self, session: Session, name: str)-> Optional[Item]:
        return session.query(Item).filter_by(name=name).first()
    
    def find_items_without_flavor_text(self, session: Session) -> list[Item]:
        return session.query(Item).outerjoin(ItemFlavorText, Item.id == ItemFlavorText.item_id).filter(ItemFlavorText.item_id == None).all()
    
    def find_all(self, session: Session) -> list[Item]:
        return session.query(Item).all()
