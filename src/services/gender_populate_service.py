import pokebase
from src.models.gender import Gender
from src.repository.gender_repository import GenderRepository

class GenderPopulationService:
    def __init__(self, repository: GenderRepository):
        self.__repository = repository

    def populate(self):
        for gender_id in range(1, 4):
            data = pokebase.gender(gender_id)
            name = data.name

            with self.__repository.get_session() as session:
                if not self.__repository.exists_by_name(session, name):
                    self.__repository.save(session, Gender(id=gender_id, name=name))
                    session.commit()
