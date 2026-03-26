from src.models.type import Type
from src.repository.type_repository import TypeRepository

class TypePopulationService:

    def __init__(self, repository: TypeRepository, allowed_types: list[str], batch_size: int = 10):
        self.__repository = repository
        self.__batch_size = batch_size
        self.__allowed_types = [t.lower().strip() for t in allowed_types]

    def populate(self):
        names = self.__allowed_types
        with self.__repository.get_session() as session:
            existing = self.__repository.get_names_already_stored(session, names)
            new_names = [name for name in names if name not in existing]
            new_types = [Type(name=name) for name in new_names]
            if not new_types:
                print("All types already existing in the database. Skipping population.")
                return

            print(f"Saving {len(new_types)} new types...")

            for i in range(0, len(new_types), self.__batch_size):
                batch = new_types[i:i+self.__batch_size]
                self.__repository.batch_save(session, batch)
                session.commit()

        print("Type population completed!")