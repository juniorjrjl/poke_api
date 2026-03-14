import pokebase
from src.models.item_machine import ItemMachine
from src.repository.item_repository import ItemRepository
from src.repository.move_repository import MoveRepository
from src.repository.version_group_repository import VersionGroupRepository
from src.repository.item_machine_repository import ItemMachineRepository

class ItemMachinePopulationService:

    def __init__(
        self,
        repository: ItemMachineRepository,
        item_repository: ItemRepository,
        move_repository: MoveRepository,
        version_group_repository: VersionGroupRepository,
        batch_size: int = 50
    ):
        self.__repository = repository
        self.__item_repository = item_repository
        self.__move_repository = move_repository
        self.__version_group_repository = version_group_repository
        self.__batch_size = batch_size

    def populate(self):
        machines = pokebase.APIResourceList("machine")

        machines_entities = []
        for machine_ref in machines:
            machine = pokebase.machine(int(machine_ref['url'].rstrip("/").split("/")[-1]))

            with self.__repository.get_session() as session:
                item = self.__item_repository.find_by_name(session, machine.item.name)
                move = self.__move_repository.find_by_name(session, machine.move.name)
                version_group = self.__version_group_repository.find_by_name(session, machine.version_group.name)

                if not item or not move or not version_group:
                    continue

                if self.__repository.exists_by_primary_key(session, item.id, move.id, version_group.id):
                    continue

                machines_entities.append(
                    ItemMachine(
                        item_id=item.id,
                        move_id=move.id,
                        version_group_id=version_group.id,
                    )
                )
                if len(machines_entities) >= self.__batch_size:
                    with self.__repository.get_session() as session:
                        self.__repository.batch_save(session, machines_entities)
                        session.commit()
                    machines_entities.clear()

        if machines_entities:
            with self.__repository.get_session() as session:
                self.__repository.batch_save(session, machines_entities)
                session.commit()
