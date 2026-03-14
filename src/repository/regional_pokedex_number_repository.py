from sqlalchemy import exists, and_
from sqlalchemy.orm import Session
from src.models.regional_pokedex_number import RegionalPokedexNumber
from src.repository.abstract_repository import AbstractRepository


class RegionalPokedexNumberRepository(AbstractRepository):

    def exists_by_specie_id_and_pokedex_name(self, session: Session, specie_id: int, pokedex_name: str)-> bool:
        return session.query(
            exists()
            .where(
                and_(RegionalPokedexNumber.specie_id == specie_id, RegionalPokedexNumber.pokedex_name == pokedex_name)
                )).scalar()
    
    def save(self, session: Session, entity: RegionalPokedexNumber)-> RegionalPokedexNumber:
        session.add(entity)
        return entity
