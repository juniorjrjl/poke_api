from sqlalchemy import exists, and_
from sqlalchemy.orm import Session
from src.models.pokemon_sprite import PokemonSprite
from src.repository.abstract_repository import AbstractRepository


class PokemonSpriteRepository(AbstractRepository):

    def save(self, session: Session, entity: PokemonSprite)-> None:
        session.add(entity)

    def exists_by_specie_id_and_gender_id(self, session: Session, form_id: int, gender_id: int, is_shiny: bool)-> bool:
        return session.query(
            exists()
            .where(
                and_(PokemonSprite.form_id == form_id, PokemonSprite.gender_id == gender_id, PokemonSprite.is_shiny == is_shiny)
                )).scalar()