import pokebase
from src.models.version_group import VersionGroup
from src.repository.generation_repository import GenerationRepository
from src.repository.version_group_repository import VersionGroupRepository

class VersionGroupPopulationService:

    def __init__(self, repository: VersionGroupRepository, generation_repository :GenerationRepository):
        self.__repository = repository
        self.__generation_repository = generation_repository

    def populate(self):
        version_groups = pokebase.APIResourceList("version-group")

        for vg_item in version_groups:
            version_group_response = pokebase.version_group(vg_item["name"])

            with self.__repository.get_session() as session:
                generation = self.__generation_repository.find_by_name(session, version_group_response.generation.name)
                if self.__repository.exists_by_name(session, version_group_response.name) or generation is None:
                    continue

                version_group = VersionGroup(
                    id = version_group_response.id,
                    name = version_group_response.name,
                    generation_id = generation.id
                )
                self.__repository.save(session, version_group)
                session.commit()

