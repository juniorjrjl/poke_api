import pokebase as pb
from src.models.egg_group import EggGroup
from src.repository.egg_group_repository import EggGroupRepository

class EggGroupPopulationService:
    def __init__(self, repository: EggGroupRepository, egg_group_amount: int):
        self.__repository = repository
        self.__egg_group_amount = egg_group_amount

    def populate(self):
        for group_id in range(1, self.__egg_group_amount):
            data = pb.egg_group(group_id)
            name = data.name

            with self.__repository.get_session() as session:
                if not self.__repository.existis_by_name(session, name):
                    self.__repository.save(session, EggGroup(id=group_id, name=name))
                    session.commit()
