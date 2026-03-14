import pokebase

from src.models.item_flavor_text import ItemFlavorText
from src.repository.item_flavor_text_repository import ItemFlavorTextRepository
from src.repository.item_repository import ItemRepository
from src.repository.version_group_repository import VersionGroupRepository


class ItemFlavorTextPopulationService:

    def __init__(self, 
                repository: ItemFlavorTextRepository,
                version_group_repository: VersionGroupRepository,
                item_repository: ItemRepository,
                batch_size: int = 50):
        self.__repository = repository
        self.__version_group_repository = version_group_repository
        self.__item_repository = item_repository
        self.__batch_size = batch_size

    def populate(self):
        with self.__repository.get_session() as session:
            items = self.__item_repository.find_items_without_flavor_text(session)

        if not items:
            print("Nenhum item para processar.")
            return

        new_flavor_texts = []

        for item in items:
            try:
                item_data = pokebase.item(item.name)
            except Exception as e:
                print(f"[WARN] Não foi possível buscar dados de '{item.name}': {e}")
                continue

            flavor_texts = getattr(item_data, "flavor_text_entries", [])
            for ft in flavor_texts:

                text_is_not_english = ft.language.name != "en"
                with self.__repository.get_session() as session:
                    version_group = self.__version_group_repository.find_by_name(session, ft.version_group.name)
                    flavor_text_stored = self.__repository.exists_by_primary_key(session, item.id, version_group.id)
                if text_is_not_english or version_group is None or flavor_text_stored:
                    continue

                new_flavor_texts.append(
                    ItemFlavorText(
                        item_id = item.id,
                        version_group_id = version_group.id,
                        text = ft.text,
                    )
                )

                if len(new_flavor_texts) >= self.__batch_size:
                    with self.__repository.get_session() as session:
                        self.__repository.batch_save(session, new_flavor_texts)
                        session.commit()
                    new_flavor_texts.clear()

        if new_flavor_texts:
            with self.__repository.get_session() as session:
                self.__repository.batch_save(session, new_flavor_texts)
                session.commit()
