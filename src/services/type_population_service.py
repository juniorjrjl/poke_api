import pokebase
from src.models.type import Type
from src.repository.type_repository import TypeRepository

class TypePopulationService:

    def __init__(self, repository: TypeRepository, batch_size: int = 10):
        self.__repository = repository
        self.__batch_size = batch_size

    def populate(self):
        types_list = pokebase.APIResourceList('type')
        names = [t['name']for t in types_list]

        with self.__repository.get_session() as session:
            existing = self.__repository.get_names_already_stored(session, names)
            session.commit()
        new_names = {name for name in names if name not in existing}

        new_types = [Type(name=name) for name in names if name in new_names]

        with self.__repository.get_session() as session:
            for i in range(0, len(new_types), self.__batch_size):
                batch = new_types[i:i+self.__batch_size]
                self.__repository.batch_save(session, batch)
                session.commit()
