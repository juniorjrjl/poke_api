import pokebase

from src.models.item import Item
from src.repository.item_repository import ItemRepository


class ItemPopulationService:

    def __init__(self, repository: ItemRepository, batch_size: int = 50):
        self.__repository = repository
        self.__batch_size = batch_size

    def populate(self):
        items_list = pokebase.APIResourceList("item")
        all_items = list(items_list)

        names = [i["name"] for i in all_items]
        with self.__repository.get_session() as session:
            existing = self.__repository.find_by_names(session, names)

        existing_names = {name for (name,) in existing}

        new_items = []
        seen_names = set()

        item_data_cache = {}

        for item_entry in all_items:
            item_name = item_entry["name"]
            if item_name in existing_names or item_name in seen_names:
                continue

            try:
                item_data = pokebase.item(item_name)
            except Exception as e:
                print(f"[WARN] Não foi possível buscar o item '{item_name}': {e}")
                continue

            item = Item(
                name=item_data.name,
                price=getattr(item_data, "cost", None),
                category=getattr(item_data.category, "name", None),
                fling_power=getattr(item_data, "fling_power", None),
                fling_effect=getattr(item_data.fling_effect, "name", None)
                if getattr(item_data, "fling_effect", None)
                else None,
            )
            new_items.append(item)
            seen_names.add(item_name)
            item_data_cache[item_name] = item_data

        for i in range(0, len(new_items), self.__batch_size):
            with self.__repository.get_session() as session:
                batch = new_items[i:i+self.__batch_size]
                self.__repository.batch_save(session, batch)
                session.commit()
