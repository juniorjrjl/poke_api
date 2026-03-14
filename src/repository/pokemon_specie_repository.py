from typing import Optional
from sqlalchemy.orm import Session
from src.models.pokemon_specie import PokemonSpecie
from src.repository.abstract_repository import AbstractRepository

class PokemonSpecieRepository(AbstractRepository):

    def save(self, session: Session, entity: PokemonSpecie) -> PokemonSpecie:
        session.add(entity)
        return entity

    def find_by_name(self, session: Session, name: str ) -> Optional[PokemonSpecie]:
        return session.query(PokemonSpecie).filter_by(name=name).first()