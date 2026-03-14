import pokebase
from src.models.ability import Ability
from src.repository.ability_repository import AbilityRepository

class AbilityPopulationService:

    def __init__(self, repository: AbilityRepository, batch_size: int = 100):
        self.__repository = repository
        self.batch_size = batch_size

    def populate(self):
        abilities_list = pokebase.APIResourceList('ability')
        names = [a['name'] for a in abilities_list]

        with self.__repository.get_session() as session:
            existing = self.__repository.get_names_already_stored(session, names)

        existing_names = {name for (name,) in existing}

        new_abilities = []

        for name in names:
            if name in existing_names:
                continue

            try:
                ability_data = pokebase.ability(name)
            except Exception as e:
                print(f"[WARN] Não foi possível buscar a ability '{name}': {e}")
                continue

            effect_entry = next(
                (e.effect for e in ability_data.effect_entries if e.language.name == "en"),
                None
            )

            flavor_entry = next(
                (f.flavor_text for f in ability_data.flavor_text_entries if f.language.name == "en"),
                None
            )

            ability = Ability(
                name = ability_data.name,
                effect_text = effect_entry,
                flavor_text = flavor_entry
            )

            new_abilities.append(ability)

        for i in range(0, len(new_abilities), self.batch_size):
            batch = new_abilities[i:i+self.batch_size]
            with self.__repository.get_session() as session:
                self.__repository.batch_save(session, batch)
                session.commit()
