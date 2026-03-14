from sqlalchemy.orm import Session
from typing import Optional
from src.models.pokemon_form import PokemonForm
from src.repository.abstract_repository import AbstractRepository


class PokemonFormRepository(AbstractRepository):

    def save(self, session: Session, entity: PokemonForm)-> PokemonForm:
        session.add(entity)
        return entity

    def find_by_specie_id_and_generation_id_and_form_name(self, session: Session, specie_id: int, generation_id: int, form_name: str) -> Optional[PokemonForm]:
        return session.query(PokemonForm).filter_by(specie_id = specie_id, generation_id = generation_id, form_name = form_name).first()
    
    def find_by_specie_id_and_generation_id(self, session: Session, specie_id: int, generation_id: int) -> list[PokemonForm]:
        return session.query(PokemonForm).filter_by(specie_id = specie_id, generation_id = generation_id).all()