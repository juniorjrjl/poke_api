import pokebase
from src.exceptions.entity_not_found_exception import EntityNotFoundException
from src.models.move import Move
from src.repository.move_repository import MoveRepository
from src.repository.type_repository import TypeRepository

class MovePopulationService:

    def __init__(self, repository: MoveRepository, type_repository: TypeRepository, batch_size: int = 100):
        self.__repository = repository
        self.__type_repository = type_repository
        self.batch_size = batch_size

    def populate(self, move_limit: int = None):
        moves_list = pokebase.APIResourceList('move')
        all_moves = list(moves_list)
        if move_limit:
            all_moves = all_moves[:move_limit]

        names = [m['name'] for m in moves_list]

        with self.__repository.get_session() as session:
            existing = self.__repository.get_names_already_stored(session, names)
        existing_names = {name for (name,) in existing}

        for move_item in moves_list:
            move_name = move_item['name']
            if move_name in existing_names:
                continue

            try:
                move_data = pokebase.move(move_name)
            except Exception as e:
                print(f"[WARN] Não foi possível buscar o Move '{move_name}': {e}")
                continue

            self.__insert(move_data)


    def __insert(self, move_data) -> None:
        with self.__type_repository.get_session() as session:
            type_entity = self.__type_repository.find_by_name(session, move_data.type.name)
            if type_entity is None:
                raise EntityNotFoundException(f'O tipo #{move_data.type.name} não foi encontrado')

            meta = getattr(move_data, "meta", None)

            move = Move(
                name = getattr(move_data, "name", None),
                power = getattr(move_data, "power", None),
                pp = getattr(move_data, "pp", None),
                accuracy = getattr(move_data, "accuracy", None),
                type_id = type_entity.id if type_entity else None,
                category = meta.category.name if meta and getattr(meta, "category", None) else None,
                critical_rate = getattr(meta, "crit_rate", None) if meta else None,
                status = meta.ailment.name if meta and getattr(meta, "ailment", None) else None,
                status_chance = getattr(meta, "stat_chance", None) if meta else None,
                effect_text = next(
                    (e.effect for e in getattr(move_data, "effect_entries", []) if e.language.name == "en"),
                    None
                ),
                contact = getattr(meta, "contact", False) if meta else False,
            )
            self.__repository.save(session, move)
            session.commit()
