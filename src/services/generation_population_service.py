import pokebase

from src.models.generation import Generation
from src.repository.generation_repository import GenerationRepository

class GenerationPopulationService():

    def __init__(self, repository: GenerationRepository, generations, generation_amount: int):
        self.__repository = repository
        self.__generations = generations
        self.__generation_amount = generation_amount

    def populate(self):
        for i in range(1, self.__generation_amount + 1):
            gen_data = pokebase.generation(i)
            release_year = self.__generations.get(gen_data.name)

            with self.__repository.get_session() as session:
                generation = self.__repository.find_by_region(session, gen_data.main_region.name)
                if generation is not None:
                    continue

            generation = Generation(
                name = gen_data.name,
                region = gen_data.main_region.name,
                generation_number = i,
                release_year = release_year
            )
            self.__repository.save(session, generation)
            session.commit()
