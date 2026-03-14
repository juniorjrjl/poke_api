from sqlalchemy import exists, and_
from sqlalchemy.orm import Session
from src.models.pokemon_gender_ratio import PokemonGenderRatio
from src.repository.abstract_repository import AbstractRepository

class PokemonGenderRatioRepository(AbstractRepository):

    def save(self, session: Session, entity: PokemonGenderRatio)-> None:
        session.add(entity)

    def exists_by_specie_id_and_gender_id(self, session: Session, specie_id: int, gender_id: int)-> bool:
        return session.query(
            exists()
            .where(
                and_(PokemonGenderRatio.specie_id == specie_id, PokemonGenderRatio.gender_id == gender_id)
                )).scalar()