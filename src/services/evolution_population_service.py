import pokebase
from sqlalchemy.orm import Session
from src.models.evolution import Evolution
from src.models.pokemon_form import PokemonForm
from src.repository.evolution_repository import EvolutionRepository
from src.repository.generation_repository import GenerationRepository
from src.repository.item_repository import ItemRepository
from src.repository.pokemon_form_repository import PokemonFormRepository
from src.repository.pokemon_specie_repository import PokemonSpecieRepository


class EvolutionPopulationService:

    def __init__(self,
                pokemon_amount: int,
                repository: EvolutionRepository,
                generation_repository: GenerationRepository,
                item_repository: ItemRepository,
                pokemon_form_repository: PokemonFormRepository,
                pokemon_specie: PokemonSpecieRepository
                ):
        self.__pokemon_amount = pokemon_amount
        self.__repository = repository
        self.__generation_repository = generation_repository
        self.__item_repository = item_repository
        self.__pokemon_form_repository = pokemon_form_repository
        self.__pokemon_specie = pokemon_specie
        self.__specie_cache = {}
        self.__item_cache = {}

    def populate(self):
        with self.__repository.get_session() as session:
            generations = self.__generation_repository.find_all(session)
            items = self.__item_repository.find_all(session)

        self.__item_cache = {item.name: item.id for item in items}

        for i in range(1, self.__pokemon_amount + 1):
            specie_data = pokebase.pokemon_species(i)
            chain = pokebase.evolution_chain(specie_data.evolution_chain.id)

            for generation in generations:
                with self.__repository.get_session() as session:
                    self.__add_evolutions(session, chain.chain, generation.id)
                    session.commit()

    def __add_evolutions(self, session: Session, node, generation_id: int):
        for evo in node.evolves_to:
            from_forms = self.__get_forms(session, node.species.name, generation_id)
            to_forms = self.__get_forms(session, evo.species.name, generation_id)

            for from_form in from_forms:
                for to_form in to_forms:
                    if self.__repository.exists_by_primary_key(session, from_form.id, to_form.id):
                        continue

                    level = None
                    trigger = None
                    condition = None
                    item_name = None
                    item_id = None

                    if evo.evolution_details and evo.evolution_details[0]:
                        details = evo.evolution_details[0]
                        level = getattr(details, 'min_level', None)
                        trigger = getattr(details.trigger, 'name', None)
                        condition = self.__build_condition(details)

                        if condition is not None and'held_item='.casefold() in condition.casefold():
                            cond_item = condition.split('=')
                            condition = cond_item[0]
                            item_name = cond_item[1]
                            item_id = self.__item_cache.get(item_name)

                        if details.item:
                            item_name = getattr(details.item, 'name', None)
                            item_id = self.__item_cache.get(item_name)

                    evolution = Evolution(
                        from_form_id=from_form.id,
                        to_form_id=to_form.id,
                        evolution_level=level,
                        evolution_item_id=item_id,
                        evolution_trigger=trigger,
                        evolution_condition=condition
                    )
                    self.__repository.save(session, evolution)

            self.__add_evolutions(session, evo, generation_id)

    def __get_forms(self, session: Session, specie_name: str, generation_id: int) -> list[PokemonForm]:
        specie_id = self.__get_specie_id(session, specie_name)
        if specie_id is None:
            return []
        return self.__pokemon_form_repository.find_by_specie_id_and_generation_id(session, specie_id, generation_id)

    def __get_specie_id(self, session: Session, specie_name: str) -> int:
        if specie_name in self.__specie_cache:
            return self.__specie_cache[specie_name]

        
        specie = self.__pokemon_specie.find_by_name(session, specie_name)
        specie_id = specie.id if specie is not None else None
        self.__specie_cache[specie_name] = specie_id
        return specie_id

    def __build_condition(self, details) -> str:
        conditions = []
        if hasattr(details, 'gender') and details.gender is not None:
            conditions.append(f"gender={details.gender}")
        if hasattr(details, 'location') and details.location:
            conditions.append(f"location={details.location.name}")
        if hasattr(details, 'held_item') and details.held_item:
            conditions.append(f"held_item={details.held_item.name}")
        if hasattr(details, 'known_move') and details.known_move:
            conditions.append(f"known_move={details.known_move.name}")
        if hasattr(details, 'time_of_day') and details.time_of_day:
            conditions.append(f"time_of_day={details.time_of_day}")
        if hasattr(details, 'happiness') and details.happiness:
            conditions.append(f"happiness={details.happiness}")
        if hasattr(details, 'min_beauty') and details.min_beauty:
            conditions.append(f"min_beauty={details.min_beauty}")
        return ', '.join(conditions) if conditions else None
