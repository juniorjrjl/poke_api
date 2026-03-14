from sqlalchemy import exists, and_
from sqlalchemy.orm import Session
from src.models.pokemon_egg_group import PokemonEggGroup
from src.repository.abstract_repository import AbstractRepository

class PokemonEggGroupRepository(AbstractRepository):

    def save(self, session: Session, entity: PokemonEggGroup)-> None:
        session.add(entity)

    def exists_by_specie_id_and_egg_group_id(self, session: Session, specie_id: int, egg_group_id: int) -> bool:
        return session.query(
            exists()
            .where(
                and_(PokemonEggGroup.specie_id == specie_id, PokemonEggGroup.egg_group_id == egg_group_id)
                )).scalar()